"""
Advanced Example: Monitor and interact with buttons with retry logic.
This example demonstrates more advanced usage patterns.
"""

import sys
import os
import time
from datetime import datetime

# Add parent directory to path to import the framework
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from browser_automation import BrowserController, ButtonChecker
from selenium.webdriver.common.by import By
from config import Config


def monitor_button_with_retry(checker, button_locator, max_attempts=3):
    """
    Monitor a button and attempt to press it with retry logic.
    
    Args:
        checker: ButtonChecker instance
        button_locator: Dictionary with button location parameters
        max_attempts: Maximum number of retry attempts
        
    Returns:
        Final result dictionary
    """
    for attempt in range(1, max_attempts + 1):
        print(f"\nAttempt {attempt}/{max_attempts}...")
        
        result = checker.check_and_press(**button_locator)
        
        if result['success']:
            print(f"✓ Success on attempt {attempt}")
            return result
        
        if attempt < max_attempts:
            print(f"✗ Failed, retrying in {Config.RETRY_DELAY} seconds...")
            time.sleep(Config.RETRY_DELAY)
    
    print("✗ All attempts failed")
    return result


def main():
    """
    Advanced example with context manager and retry logic.
    """
    Config.ensure_directories()
    
    # Using context manager for automatic cleanup
    with BrowserController(headless=Config.HEADLESS) as browser:
        print("Browser started with context manager")
        
        # Navigate to target page
        url = "https://example.com"  # Replace with your target URL
        print(f"Navigating to {url}...")
        browser.navigate_to(url)
        
        # Initialize button checker
        checker = ButtonChecker(browser)
        
        # Example 1: Monitor button with retry logic
        print("\n=== Example 1: Button with Retry Logic ===")
        button_config = {
            'css_selector': 'button.submit-btn',  # Replace with actual selector
            'force_press': False
        }
        result = monitor_button_with_retry(checker, button_config, max_attempts=Config.MAX_RETRIES)
        
        # Example 2: Get detailed button information
        print("\n=== Example 2: Get Button Information ===")
        button = checker.find_button(text="Submit")  # Replace with actual button text
        if button:
            info = checker.get_button_info(button)
            print("Button Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            print("Button not found")
        
        # Example 3: Check multiple buttons
        print("\n=== Example 3: Check Multiple Buttons ===")
        buttons_to_check = [
            {'id': 'btn1', 'by': By.ID, 'value': 'submit-btn'},
            {'id': 'btn2', 'text': 'Click Here'},
            {'id': 'btn3', 'css_selector': '.action-button'}
        ]
        
        for btn_config in buttons_to_check:
            btn_id = btn_config.pop('id')
            print(f"\nChecking {btn_id}...")
            result = checker.check_and_press(**btn_config)
            print(f"  Found: {result['found']}")
            print(f"  Was Pressed: {result['was_pressed']}")
            print(f"  Action: {result['action_taken']}")
            print(f"  Success: {result['success']}")
        
        # Example 4: Conditional button pressing
        print("\n=== Example 4: Conditional Button Press ===")
        button = checker.find_button(xpath="//button[@type='submit']")
        if button:
            is_pressed = checker.is_button_pressed(button)
            print(f"Button is currently pressed: {is_pressed}")
            
            if not is_pressed:
                print("Button not pressed, pressing now...")
                success = checker.press_button(button, wait_after=Config.WAIT_AFTER_CLICK)
                print(f"Press successful: {success}")
            else:
                print("Button already pressed, skipping...")
        
        # Take timestamped screenshot
        if Config.SAVE_SCREENSHOTS:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(Config.SCREENSHOT_DIR, f"advanced_example_{timestamp}.png")
            browser.take_screenshot(screenshot_path)
            print(f"\nScreenshot saved to: {screenshot_path}")
        
        print("\n=== Advanced Example Completed ===")
    
    print("Browser closed automatically by context manager")


if __name__ == "__main__":
    main()

# Made with Bob
