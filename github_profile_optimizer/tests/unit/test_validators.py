"""Unit tests for the validators."""
import pytest
from src.github_profile_optimizer.utils.validators import InputValidator, validate_input


def test_validate_github_username_valid():
    """Test validation of valid GitHub usernames."""
    validator = InputValidator()
    
    valid_usernames = [
        "user",
        "user123",
        "user-name",
        "User_Name",
        "a" * 39  # Maximum length
    ]
    
    for username in valid_usernames:
        assert validator.validate_github_username(username) is True


def test_validate_github_username_invalid():
    """Test validation of invalid GitHub usernames."""
    validator = InputValidator()
    
    invalid_usernames = [
        "",  # Empty
        "a" * 40,  # Too long
        "-username",  # Starts with hyphen
        "username-",  # Ends with hyphen
        "user--name",  # Consecutive hyphens
        "user@name",  # Invalid character
        "123-",  # Ends with hyphen
    ]
    
    for username in invalid_usernames:
        assert validator.validate_github_username(username) is False


def test_validate_email():
    """Test email validation."""
    validator = InputValidator()
    
    valid_emails = [
        "test@example.com",
        "user.name@domain.co.uk",
        "user+tag@example.org"
    ]
    
    for email in valid_emails:
        assert validator.validate_email(email) is True
    
    invalid_emails = [
        "invalid-email",
        "@example.com",
        "test@",
        "test@.com"
    ]
    
    for email in invalid_emails:
        assert validator.validate_email(email) is False


def test_validate_url():
    """Test URL validation."""
    validator = InputValidator()
    
    valid_urls = [
        "https://example.com",
        "http://localhost:8000",
        "https://sub.domain.com/path?query=value"
    ]
    
    for url in valid_urls:
        assert validator.validate_url(url) is True
    
    invalid_urls = [
        "invalid-url",
        "ftp://example.com",
        "http://",
        "https://"
    ]
    
    for url in invalid_urls:
        assert validator.validate_url(url) is False


def test_sanitize_string():
    """Test string sanitization."""
    validator = InputValidator()
    
    # Test basic sanitization
    result = validator.sanitize_string("Hello <script>alert('xss')</script> World")
    assert "<script>" not in result
    assert "alert('xss')" not in result
    assert result == "Hello World"
    
    # Test length truncation
    long_string = "A" * 1500
    result = validator.sanitize_string(long_string, max_length=1000)
    assert len(result) == 1000
    
    # Test whitespace normalization
    result = validator.sanitize_string("  Hello    World  ")
    assert result == "Hello World"


def test_validate_input_function():
    """Test the validate_input function."""
    # Test username validation
    assert validate_input("validuser", "username") is True
    assert validate_input("invalid-user-", "username") is False
    
    # Test email validation
    assert validate_input("test@example.com", "email") is True
    assert validate_input("invalid-email", "email") is False
    
    # Test URL validation
    assert validate_input("https://example.com", "url") is True
    assert validate_input("invalid-url", "url") is False
    
    # Test unknown validator type
    assert validate_input("test", "unknown") is False