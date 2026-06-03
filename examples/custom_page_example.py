"""
Custom Page Example: Template for creating page-specific automation.
Copy and modify this template for your specific webpage needs.
"""

import sys
import os

# Add parent directory to path to import the framework
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from browser_automation import BrowserController, ButtonChecker
from selenium.webdriver.common.by import By
from config import Config


class CustomPageAutomation:
    """
    Template class for page-specific automation.
    Customize this for your specific webpage.
    """
    
    def __init__(self, url: str):
        """
        Initialize the custom page automation.
        
        Args:
            url: The URL of the page to automate
        """
        self.url = url
        self.browser = BrowserController(headless=Config.HEADLESS)
        self.checker = None
        
    def setup(self):
        """Start browser and navigate to page."""
        print(f"Setting up automation for {self.url}...")
        self.browser.start_browser()
        self.browser.navigate_to(self.url)
        self.checker = ButtonChecker(self.browser)
        print("Setup complete!")
        
    def check_login_button(self):
        """
        Example: Check and press a login button.
        Customize this method for your specific button.
        """
        print("\nChecking login button...")
        
        # Try multiple strategies to find the button
        result = self.checker.check_and_press(
            # Try by ID first
            by=By.ID,
            value="login-button"
        )
        
        if not result['found']:
            # Try by text if ID didn't work
            result = self.checker.check_and_press(text="Login")
        
        if not result['found']:
            # Try by CSS selector as last resort
            result = self.checker.check_and_press(
                css_selector="button[type='submit']"
            )
        
        return result
    
    def check_submit_button(self):
        """
        Example: Check and press a submit button.
        Customize this method for your specific button.
        """
        print("\nChecking submit button...")
        
        result = self.checker.check_and_press(
            xpath="//button[contains(text(), 'Submit')]"
        )
        
        return result
    
    def check_custom_button(self, **kwargs):
        """
        Generic method to check any button.
        
        Args:
            **kwargs: Button locator parameters (by, value, text, css_selector, xpath)
            
        Returns:
            Result dictionary
        """
        print(f"\nChecking custom button with params: {kwargs}")
        return self.checker.check_and_press(**kwargs)
    
    def run_automation(self):
        """
        Main automation workflow.
        Customize this to define your automation sequence.
        """
        try:
            self.setup()
            
            # Example workflow - customize as needed
            print("\n=== Starting Automation Workflow ===")
            
            # Step 1: Check login button
            login_result = self.check_login_button()
            print(f"Login button result: {login_result}")
            
            # Step 2: Wait a bit (if needed)
            import time
            time.sleep(1)
            
            # Step 3: Check submit button
            submit_result = self.check_submit_button()
            print(f"Submit button result: {submit_result}")
            
            # Step 4: Take screenshot
            if Config.SAVE_SCREENSHOTS:
                screenshot_path = os.path.join(
                    Config.SCREENSHOT_DIR,
                    "custom_page_automation.png"
                )
                self.browser.take_screenshot(screenshot_path)
                print(f"\nScreenshot saved: {screenshot_path}")
            
            print("\n=== Automation Workflow Complete ===")
            
        except Exception as e:
            print(f"Error during automation: {e}")
            
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("\nCleaning up...")
        if self.browser:
            self.browser.close_browser()
        print("Cleanup complete!")


def main():
    """
    Main function to run the custom page automation.
    """
    Config.ensure_directories()
    
    # Replace with your target URL
    target_url = "https://example.com"
    
    # Create and run automation
    automation = CustomPageAutomation(target_url)
    automation.run_automation()


if __name__ == "__main__":
    main()

# Made with Bob
