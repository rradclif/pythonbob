"""
Basic Example: Check and press a button on a webpage.
This example demonstrates the basic usage of the browser automation framework.
"""

import sys
import os

# Add parent directory to path to import the framework
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from browser_automation import BrowserController, ButtonChecker
from selenium.webdriver.common.by import By
from config import Config


def main():
    """
    Basic example: Navigate to a page and check/press a button.
    """
    # Ensure necessary directories exist
    Config.ensure_directories()
    
    # Initialize browser controller
    browser = BrowserController(headless=Config.HEADLESS, implicit_wait=Config.IMPLICIT_WAIT)
    
    try:
        # Start the browser
        print("Starting browser...")
        browser.start_browser()
        
        # Navigate to a webpage (replace with your target URL)
        url = "https://example.com"  # Replace with your target URL
        print(f"Navigating to {url}...")
        browser.navigate_to(url)
        
        # Initialize button checker
        checker = ButtonChecker(browser)
        
        # Example 1: Find button by ID
        print("\nExample 1: Finding button by ID...")
        result = checker.check_and_press(
            by=By.ID,
            value="submit-button"  # Replace with actual button ID
        )
        print(f"Result: {result}")
        
        # Example 2: Find button by text
        print("\nExample 2: Finding button by text...")
        result = checker.check_and_press(
            text="Click Me"  # Replace with actual button text
        )
        print(f"Result: {result}")
        
        # Example 3: Find button by CSS selector
        print("\nExample 3: Finding button by CSS selector...")
        result = checker.check_and_press(
            css_selector="button.primary-btn"  # Replace with actual CSS selector
        )
        print(f"Result: {result}")
        
        # Example 4: Find button by XPath
        print("\nExample 4: Finding button by XPath...")
        result = checker.check_and_press(
            xpath="//button[@type='submit']"  # Replace with actual XPath
        )
        print(f"Result: {result}")
        
        # Take a screenshot
        if Config.SAVE_SCREENSHOTS:
            screenshot_path = os.path.join(Config.SCREENSHOT_DIR, "basic_example.png")
            browser.take_screenshot(screenshot_path)
            print(f"\nScreenshot saved to: {screenshot_path}")
        
        print("\nExample completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        # Always close the browser
        print("\nClosing browser...")
        browser.close_browser()


if __name__ == "__main__":
    main()

# Made with Bob
