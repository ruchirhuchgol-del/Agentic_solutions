"""Unit tests for the logger."""
import json
import logging
from src.github_profile_optimizer.utils.logger import StructuredLogger, get_logger


def test_structured_logger_initialization():
    """Test structured logger initialization."""
    logger = StructuredLogger("test_logger")
    assert logger.logger.name == "test_logger"
    assert logger.logger.level == logging.INFO


def test_structured_logger_info():
    """Test info logging."""
    logger = StructuredLogger("test_info_logger")
    
    # Capture log output
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Log a message
    logger.info("Test info message", extra_field="extra_value")
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Parse the JSON output
    log_output = captured_output.getvalue().strip()
    log_data = json.loads(log_output)
    
    assert log_data["level"] == "info"
    assert log_data["message"] == "Test info message"
    assert log_data["extra_field"] == "extra_value"
    assert "timestamp" in log_data


def test_structured_logger_error():
    """Test error logging."""
    logger = StructuredLogger("test_error_logger")
    
    # Capture log output
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Log a message
    logger.error("Test error message", error_code=500)
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Parse the JSON output
    log_output = captured_output.getvalue().strip()
    log_data = json.loads(log_output)
    
    assert log_data["level"] == "error"
    assert log_data["message"] == "Test error message"
    assert log_data["error_code"] == 500
    assert "timestamp" in log_data


def test_structured_logger_warning():
    """Test warning logging."""
    logger = StructuredLogger("test_warning_logger")
    
    # Capture log output
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Log a message
    logger.warning("Test warning message", warning_type="test")
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Parse the JSON output
    log_output = captured_output.getvalue().strip()
    log_data = json.loads(log_output)
    
    assert log_data["level"] == "warning"
    assert log_data["message"] == "Test warning message"
    assert log_data["warning_type"] == "test"
    assert "timestamp" in log_data


def test_structured_logger_debug():
    """Test debug logging."""
    logger = StructuredLogger("test_debug_logger", level=logging.DEBUG)
    
    # Capture log output
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Log a message
    logger.debug("Test debug message", debug_info="debug_value")
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Parse the JSON output
    log_output = captured_output.getvalue().strip()
    log_data = json.loads(log_output)
    
    assert log_data["level"] == "debug"
    assert log_data["message"] == "Test debug message"
    assert log_data["debug_info"] == "debug_value"
    assert "timestamp" in log_data


def test_get_logger_function():
    """Test get_logger function."""
    logger = get_logger("function_test_logger")
    assert isinstance(logger, StructuredLogger)
    assert logger.logger.name == "function_test_logger"