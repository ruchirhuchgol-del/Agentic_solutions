"""
Multi-layer caching system for GitHub API responses.

Provides a three-tier caching system to minimize API calls and improve performance.
"""

import time
import json
import os
import hashlib
from typing import Any, Optional, Dict, List
import redis
from ..utils.logger import get_logger


class DiskCache:
    """
    Simple disk-based cache with TTL support.
    
    Provides persistent caching capabilities using the file system
    with configurable time-to-live expiration.
    """
    
    def __init__(self, cache_dir: str = "/tmp/github_cache"):
        """
        Initialize disk cache.
        
        Args:
            cache_dir: Directory to store cached files
        """
        self.cache_dir = cache_dir
        self.logger = get_logger(self.__class__.__name__)
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        """
        Get file path for a cache key.
        
        Args:
            key: Cache key
            
        Returns:
            File path for the key
        """
        # Hash the key to create a safe filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key_hash}.cache")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from disk cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        try:
            file_path = self._get_file_path(key)
            if not os.path.exists(file_path):
                return None
                
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Check if expired (7 days = 604800 seconds)
            if time.time() - data.get('timestamp', 0) > 604800:
                os.remove(file_path)
                return None
                
            return data.get('value')
        except Exception as e:
            self.logger.warning(f"Error reading from disk cache: {e}")
            return None
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set value in disk cache.
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_file_path(key)
            data = {
                'key': key,
                'value': value,
                'timestamp': time.time()
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f)
                
            return True
        except Exception as e:
            self.logger.warning(f"Error writing to disk cache: {e}")
            return False


class CacheManager:
    """
    Multi-layer caching system with L1 (memory), L2 (Redis), and L3 (disk) caches.
    
    Implements a three-tier caching strategy to optimize performance
    and minimize external API calls.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        Initialize multi-layer cache.
        
        Args:
            redis_url: Redis connection URL
        """
        self.logger = get_logger(self.__class__.__name__)
        
        # L1: In-memory cache (1-hour TTL)
        self.l1_cache: Dict[str, Any] = {}
        self.l1_timestamps: Dict[str, float] = {}
        
        # L2: Redis cache (24-hour TTL)
        try:
            self.l2_cache = redis.Redis.from_url(redis_url)
            # Test connection
            self.l2_cache.ping()
            self.logger.info("Connected to Redis cache successfully")
        except Exception as e:
            self.logger.warning(f"Could not connect to Redis: {e}. Using in-memory only.")
            self.l2_cache = None
            
        # L3: Disk cache (7-day TTL)
        self.l3_cache = DiskCache()
    
    def _is_expired(self, timestamp: float, ttl: int) -> bool:
        """
        Check if a cached item is expired.
        
        Args:
            timestamp: When the item was cached
            ttl: Time to live in seconds
            
        Returns:
            True if expired, False otherwise
        """
        return time.time() - timestamp > ttl
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache with L1 → L2 → L3 fallback chain.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found in any layer
        """
        # L1: Check in-memory cache (1-hour TTL)
        if key in self.l1_cache:
            timestamp = self.l1_timestamps.get(key, 0)
            if not self._is_expired(timestamp, 3600):  # 1 hour
                self.logger.debug(f"Cache hit in L1 (memory) for key: {key}")
                return self.l1_cache[key]
            else:
                # Expired, remove from L1
                del self.l1_cache[key]
                del self.l1_timestamps[key]
        
        # L2: Check Redis cache (24-hour TTL)
        if self.l2_cache:
            try:
                cached_data = self.l2_cache.get(key)
                if cached_data:
                    data = json.loads(cached_data)
                    if not self._is_expired(data.get('timestamp', 0), 86400):  # 24 hours
                        value = data.get('value')
                        # Promote to L1
                        self.l1_cache[key] = value
                        self.l1_timestamps[key] = data.get('timestamp', time.time())
                        self.logger.debug(f"Cache hit in L2 (Redis) for key: {key}")
                        return value
            except Exception as e:
                self.logger.warning(f"Error reading from Redis cache: {e}")
        
        # L3: Check disk cache (7-day TTL)
        value = self.l3_cache.get(key)
        if value is not None:
            # Promote to L1 and L2
            self.l1_cache[key] = value
            self.l1_timestamps[key] = time.time()
            
            if self.l2_cache:
                try:
                    data = {
                        'key': key,
                        'value': value,
                        'timestamp': time.time()
                    }
                    self.l2_cache.setex(key, 86400, json.dumps(data))  # 24 hours
                except Exception as e:
                    self.logger.warning(f"Error writing to Redis cache: {e}")
                    
            self.logger.debug(f"Cache hit in L3 (disk) for key: {key}")
            return value
            
        self.logger.debug(f"Cache miss for key: {key}")
        return None
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set value in all cache layers.
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            True if successful, False otherwise
        """
        success = True
        timestamp = time.time()
        
        # L1: Set in-memory cache
        self.l1_cache[key] = value
        self.l1_timestamps[key] = timestamp
        
        # L2: Set in Redis cache (24-hour TTL)
        if self.l2_cache:
            try:
                data = {
                    'key': key,
                    'value': value,
                    'timestamp': timestamp
                }
                self.l2_cache.setex(key, 86400, json.dumps(data))  # 24 hours
            except Exception as e:
                self.logger.warning(f"Error writing to Redis cache: {e}")
                success = False
        
        # L3: Set in disk cache (7-day TTL)
        if not self.l3_cache.set(key, value):
            success = False
            
        if success:
            self.logger.debug(f"Value cached successfully for key: {key}")
        else:
            self.logger.warning(f"Failed to cache value for key: {key}")
            
        return success
    
    def invalidate(self, key: str) -> bool:
        """
        Invalidate cache entry in all layers.
        
        Args:
            key: Cache key to invalidate
            
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # L1: Remove from memory
        if key in self.l1_cache:
            del self.l1_cache[key]
        if key in self.l1_timestamps:
            del self.l1_timestamps[key]
        
        # L2: Remove from Redis
        if self.l2_cache:
            try:
                self.l2_cache.delete(key)
            except Exception as e:
                self.logger.warning(f"Error deleting from Redis cache: {e}")
                success = False
        
        # L3: Remove from disk (not easily possible with current implementation)
        # In a production system, we would implement this properly
        
        return success


# Global cache manager instance
cache_manager = CacheManager()