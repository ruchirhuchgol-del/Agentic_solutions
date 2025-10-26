"""
Intelligent rate limiting for GitHub API calls.

Provides adaptive rate limiting to respect GitHub API quotas and prevent throttling.
"""

import time
import threading
from typing import Dict, Optional, List
import redis
from ..utils.logger import get_logger
from ..exceptions import GitHubProfileOptimizerError


class RateLimitExceeded(GitHubProfileOptimizerError):
    """
    Raised when rate limit is exceeded.
    
    This exception is raised when an operation would exceed
    the configured rate limits for external APIs.
    """
    pass


class TokenBucket:
    """
    Token bucket algorithm for rate limiting.
    
    Implements the token bucket algorithm for controlling
    the rate of operations with configurable capacity and refill rate.
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket.
        
        Args:
            capacity: Maximum number of tokens
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Consume tokens from the bucket.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were available, False otherwise
        """
        with self.lock:
            now = time.time()
            # Refill tokens based on time passed
            tokens_to_add = (now - self.last_refill) * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now
            
            # Try to consume tokens
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False
    
    def available_tokens(self) -> float:
        """
        Get number of available tokens.
        
        Returns:
            Number of available tokens
        """
        with self.lock:
            now = time.time()
            tokens_to_add = (now - self.last_refill) * self.refill_rate
            return min(self.capacity, self.tokens + tokens_to_add)


class DistributedTokenBucket:
    """
    Distributed token bucket using Redis for multi-instance coordination.
    
    Provides distributed rate limiting capabilities using Redis
    for coordination across multiple application instances.
    """
    
    def __init__(self, redis_client: redis.Redis, key: str, capacity: int, refill_rate: float):
        """
        Initialize distributed token bucket.
        
        Args:
            redis_client: Redis client
            key: Redis key for this bucket
            capacity: Maximum number of tokens
            refill_rate: Tokens added per second
        """
        self.redis = redis_client
        self.key = key
        self.capacity = capacity
        self.refill_rate = refill_rate
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Consume tokens from the distributed bucket.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were available, False otherwise
        """
        try:
            # Lua script for atomic token consumption
            lua_script = """
            local key = KEYS[1]
            local capacity = tonumber(ARGV[1])
            local refill_rate = tonumber(ARGV[2])
            local tokens_requested = tonumber(ARGV[3])
            local now = tonumber(ARGV[4])
            
            -- Get current state
            local current = redis.call('HMGET', key, 'tokens', 'last_refill')
            local tokens = tonumber(current[1]) or capacity
            local last_refill = tonumber(current[2]) or now
            
            -- Refill tokens
            local tokens_to_add = (now - last_refill) * refill_rate
            tokens = math.min(capacity, tokens + tokens_to_add)
            
            -- Try to consume tokens
            if tokens >= tokens_requested then
                tokens = tokens - tokens_requested
                redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
                redis.call('EXPIRE', key, 3600) -- Expire in 1 hour
                return 1
            else
                redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
                redis.call('EXPIRE', key, 3600) -- Expire in 1 hour
                return 0
            end
            """
            
            result = self.redis.eval(
                lua_script,
                1,
                self.key,
                self.capacity,
                self.refill_rate,
                tokens,
                time.time()
            )
            
            return bool(result)
        except Exception as e:
            # Fallback to local token bucket if Redis fails
            logger = get_logger(self.__class__.__name__)
            logger.warning(f"Redis error, using local fallback: {e}")
            # In a real implementation, we would have a local fallback
            return False


class GitHubRateLimiter:
    """
    Adaptive rate limiter for GitHub API with distributed token bucket.
    
    Provides intelligent rate limiting for GitHub API calls
    with support for distributed deployments and adaptive throttling.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        Initialize GitHub rate limiter.
        
        Args:
            redis_url: Redis connection URL
        """
        self.logger = get_logger(self.__class__.__name__)
        
        # GitHub API rate limits: 5000 requests per hour for authenticated requests
        self.capacity = 5000
        self.refill_rate = 5000 / 3600  # ~1.39 tokens per second
        
        # Try to connect to Redis for distributed rate limiting
        try:
            self.redis = redis.Redis.from_url(redis_url)
            self.redis.ping()
            self.logger.info("Connected to Redis for rate limiting")
            self.distributed_bucket = DistributedTokenBucket(
                self.redis, 
                "github_rate_limit_bucket", 
                self.capacity, 
                self.refill_rate
            )
        except Exception as e:
            self.logger.warning(f"Could not connect to Redis for rate limiting: {e}")
            self.redis = None
            self.distributed_bucket = None
            # Fallback to local token bucket
            self.local_bucket = TokenBucket(self.capacity, self.refill_rate)
    
    def api_call(self, endpoint: str) -> bool:
        """
        Check if API call is allowed under rate limits.
        
        Args:
            endpoint: GitHub API endpoint
            
        Returns:
            True if call is allowed, False if rate limited
            
        Raises:
            RateLimitExceeded: If rate limit is exceeded
        """
        # Use distributed bucket if available, otherwise local bucket
        if self.distributed_bucket:
            allowed = self.distributed_bucket.consume(1)
        else:
            allowed = self.local_bucket.consume(1)
            
        if not allowed:
            self.logger.warning(f"Rate limit exceeded for endpoint: {endpoint}")
            raise RateLimitExceeded("GitHub API rate limit reached")
            
        self.logger.debug(f"API call allowed for endpoint: {endpoint}")
        return True
    
    def get_remaining_calls(self) -> int:
        """
        Get estimated number of remaining API calls.
        
        Returns:
            Estimated remaining calls
        """
        if self.distributed_bucket and self.redis:
            try:
                current = self.redis.hgetall("github_rate_limit_bucket")
                tokens = float(current.get(b'tokens', self.capacity)) if current else self.capacity
                return int(tokens)
            except Exception:
                pass  # Fall through to local estimation
        
        # Local estimation
        if hasattr(self, 'local_bucket'):
            return int(self.local_bucket.available_tokens())
        
        return self.capacity
    
    def wait_if_needed(self) -> None:
        """
        Wait if rate limit is close to being exceeded.
        """
        remaining = self.get_remaining_calls()
        if remaining < 100:  # If less than 100 calls remaining
            wait_time = (100 - remaining) / self.refill_rate
            self.logger.info(f"Rate limit low, waiting {wait_time:.2f} seconds")
            time.sleep(min(wait_time, 30))  # Max 30 second wait


# Global rate limiter instance
rate_limiter = GitHubRateLimiter()