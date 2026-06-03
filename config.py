"""
Configuration file for browser automation settings.
Modify these settings based on your needs.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


def _get_int(key: str, default: int, min_val: int = 0, max_val: Optional[int] = None) -> int:
    """Safely get and validate integer environment variable."""
    try:
        value = int(os.getenv(key, str(default)))
        if value < min_val:
            print(f"Warning: {key}={value} is below minimum {min_val}, using {min_val}")
            return min_val
        if max_val is not None and value > max_val:
            print(f"Warning: {key}={value} exceeds maximum {max_val}, using {max_val}")
            return max_val
        return value
    except ValueError:
        print(f"Warning: Invalid {key} value, using default {default}")
        return default


def _get_float(key: str, default: float, min_val: float = 0.0, max_val: Optional[float] = None) -> float:
    """Safely get and validate float environment variable."""
    try:
        value = float(os.getenv(key, str(default)))
        if value < min_val:
            print(f"Warning: {key}={value} is below minimum {min_val}, using {min_val}")
            return min_val
        if max_val is not None and value > max_val:
            print(f"Warning: {key}={value} exceeds maximum {max_val}, using {max_val}")
            return max_val
        return value
    except ValueError:
        print(f"Warning: Invalid {key} value, using default {default}")
        return default


def _sanitize_path(path: str) -> str:
    """Sanitize file path to prevent directory traversal."""
    # Remove any parent directory references
    path = path.replace('..', '').replace('~', '')
    # Normalize the path
    path = os.path.normpath(path)
    # Ensure it's a relative path
    if os.path.isabs(path):
        path = os.path.basename(path)
    return path


class Config:
    """Configuration settings for browser automation."""
    
    # Browser Settings
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    IMPLICIT_WAIT = _get_int('IMPLICIT_WAIT', 10, min_val=1, max_val=60)
    PAGE_LOAD_TIMEOUT = _get_int('PAGE_LOAD_TIMEOUT', 30, min_val=5, max_val=120)
    
    # Screenshot Settings
    SCREENSHOT_DIR = _sanitize_path(os.getenv('SCREENSHOT_DIR', 'screenshots'))
    SAVE_SCREENSHOTS = os.getenv('SAVE_SCREENSHOTS', 'True').lower() == 'true'
    
    # Button Interaction Settings
    WAIT_AFTER_CLICK = _get_float('WAIT_AFTER_CLICK', 0.5, min_val=0.0, max_val=10.0)
    MAX_RETRIES = _get_int('MAX_RETRIES', 3, min_val=1, max_val=10)
    RETRY_DELAY = _get_float('RETRY_DELAY', 1.0, min_val=0.1, max_val=10.0)
    
    # Logging Settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    LOG_FILE = _sanitize_path(os.getenv('LOG_FILE', 'browser_automation.log'))
    
    # Validate log level
    VALID_LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if LOG_LEVEL not in VALID_LOG_LEVELS:
        print(f"Warning: Invalid LOG_LEVEL '{LOG_LEVEL}', using 'INFO'")
        LOG_LEVEL = 'INFO'
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist with secure permissions."""
        if cls.SAVE_SCREENSHOTS and not os.path.exists(cls.SCREENSHOT_DIR):
            try:
                # Create directory with restricted permissions (owner only)
                os.makedirs(cls.SCREENSHOT_DIR, mode=0o700, exist_ok=True)
            except OSError as e:
                print(f"Warning: Could not create screenshot directory: {e}")
    
    @classmethod
    def validate_url(cls, url: str) -> bool:
        """Validate URL to ensure it's safe to navigate to."""
        if not url:
            return False
        
        # Check for valid protocol
        valid_protocols = ['http://', 'https://', 'file://']
        if not any(url.startswith(proto) for proto in valid_protocols):
            return False
        
        # Warn about non-HTTPS URLs (except file://)
        if url.startswith('http://') and not url.startswith('http://localhost'):
            print(f"Warning: Using non-HTTPS URL: {url}")
        
        return True

# Made with Bob
