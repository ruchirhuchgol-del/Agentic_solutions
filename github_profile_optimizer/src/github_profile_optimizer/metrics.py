"""
Metrics collection for observability.

Provides functionality for collecting and reporting application metrics.
"""

import time
from typing import Dict, Any, Callable
from functools import wraps
from .utils.logger import get_logger


class MetricsCollector:
    """
    Collects and reports application metrics.
    
    This class provides methods for tracking various metrics such as
    execution times, counters, and gauges for monitoring application performance.
    """
    
    def __init__(self):
        """Initialize the metrics collector."""
        self.logger = get_logger(self.__class__.__name__)
        self.metrics = {}
    
    def increment(self, metric_name: str, value: int = 1) -> None:
        """
        Increment a counter metric.
        
        Args:
            metric_name: Name of the metric
            value: Value to increment by
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = 0
        self.metrics[metric_name] += value
        self.logger.debug(f"Metric {metric_name} incremented by {value}")
    
    def gauge(self, metric_name: str, value: float) -> None:
        """
        Set a gauge metric.
        
        Args:
            metric_name: Name of the metric
            value: Gauge value
        """
        self.metrics[metric_name] = value
        self.logger.debug(f"Metric {metric_name} set to {value}")
    
    def timer(self, metric_name: str) -> Callable:
        """
        Timer decorator for measuring function execution time.
        
        Args:
            metric_name: Name of the timer metric
            
        Returns:
            Decorator function
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    elapsed_time = time.time() - start_time
                    self.metrics[f"{metric_name}_duration"] = elapsed_time
                    self.logger.debug(f"Function {func.__name__} took {elapsed_time:.4f} seconds")
            return wrapper
        return decorator
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all collected metrics.
        
        Returns:
            Dictionary of metrics
        """
        return self.metrics.copy()
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics.clear()
        self.logger.debug("Metrics reset")


# Global metrics collector instance
metrics_collector = MetricsCollector()


def track_tool_execution(tool_name: str):
    """
    Decorator to track tool execution metrics.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            metrics_collector.increment(f"tool_executions_{tool_name}_total")
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                metrics_collector.increment(f"tool_executions_{tool_name}_success")
                return result
            except Exception as e:
                metrics_collector.increment(f"tool_executions_{tool_name}_failure")
                raise
            finally:
                elapsed_time = time.time() - start_time
                metrics_collector.gauge(f"tool_executions_{tool_name}_duration", elapsed_time)
        return wrapper
    return decorator