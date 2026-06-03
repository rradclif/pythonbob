"""
Projector Page Test: Automated tests for ProjectorPage.html
Tests the powerOn and powerOff button functionality.
"""

import sys
import os
import time

# Add parent directory to path to import the framework
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from browser_automation import BrowserController, ButtonChecker
from selenium.webdriver.common.by import By
from config import Config


class ProjectorPageTest:
    """
    Test automation for ProjectorPage.html
    """
    
    def __init__(self, page_path: str):
        """
        Initialize the projector page test automation.
        
        Args:
            page_path: Path to the ProjectorPage.html file
        """
        # Convert to file:// URL if it's a local path
        if not page_path.startswith('http'):
            page_path = f"file://{os.path.abspath(page_path)}"
        
        self.url = page_path
        self.browser = BrowserController(headless=Config.HEADLESS, implicit_wait=Config.IMPLICIT_WAIT)
        self.checker = None
        
    def setup(self):
        """Start browser and navigate to page."""
        print(f"Setting up test for {self.url}...")
        self.browser.start_browser()
        self.browser.navigate_to(self.url)
        self.checker = ButtonChecker(self.browser)
        print("Setup complete!")
        
    def test_power_on_button(self):
        """
        Test 1: Check and press the Power On button.
        Button ID: Btn_PowerOn
        """
        print("\n=== Test 1: Power On Button ===")
        
        # Find and press the Power On button by ID
        result = self.checker.check_and_press(
            by=By.ID,
            value="Btn_PowerOn"
        )
        
        print(f"Power On button found: {result['found']}")
        print(f"Power On button enabled: {result['enabled']}")
        print(f"Power On button pressed: {result['pressed']}")
        
        if result['found'] and not result['enabled']:
            print("Note: Power On button is currently disabled (projector may already be on)")
        
        # Take screenshot after pressing
        if Config.SAVE_SCREENSHOTS and result['found']:
            screenshot_path = os.path.join(
                Config.SCREENSHOT_DIR,
                "projector_power_on.png"
            )
            self.browser.take_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        
        return result
    
    def test_power_off_button(self):
        """
        Test 2: Check and press the Power Off button.
        Button ID: Btn_PowerOff
        Note: This button triggers a confirmation dialog in the browser.
        """
        print("\n=== Test 2: Power Off Button ===")
        
        # Find and press the Power Off button by ID
        result = self.checker.check_and_press(
            by=By.ID,
            value="Btn_PowerOff"
        )
        
        print(f"Power Off button found: {result['found']}")
        print(f"Power Off button enabled: {result['enabled']}")
        print(f"Power Off button pressed: {result['pressed']}")
        
        if result['found'] and not result['enabled']:
            print("Note: Power Off button is currently disabled (projector may already be off)")
        
        # Handle the confirmation dialog if button was pressed
        if result['pressed']:
            try:
                # Wait a moment for the alert to appear
                time.sleep(0.5)
                
                # Switch to the alert and accept it
                alert = self.browser.driver.switch_to.alert
                alert_text = alert.text
                print(f"Confirmation dialog appeared: '{alert_text}'")
                
                # Accept the alert (click OK)
                alert.accept()
                print("Confirmation dialog accepted")
                
            except Exception as e:
                print(f"No confirmation dialog appeared or error handling it: {e}")
        
        # Take screenshot after pressing
        if Config.SAVE_SCREENSHOTS and result['found']:
            screenshot_path = os.path.join(
                Config.SCREENSHOT_DIR,
                "projector_power_off.png"
            )
            self.browser.take_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        
        return result
    
    def run_all_tests(self):
        """
        Run all projector page tests.
        """
        try:
            self.setup()
            
            print("\n" + "="*50)
            print("Starting Projector Page Tests")
            print("="*50)
            
            # Test 1: Power On button
            power_on_result = self.test_power_on_button()
            
            # Wait between tests
            time.sleep(1)
            
            # Test 2: Power Off button
            power_off_result = self.test_power_off_button()
            
            # Summary
            print("\n" + "="*50)
            print("Test Summary")
            print("="*50)
            print(f"Power On Test - Found: {power_on_result['found']}, "
                  f"Enabled: {power_on_result['enabled']}, "
                  f"Pressed: {power_on_result['pressed']}")
            print(f"Power Off Test - Found: {power_off_result['found']}, "
                  f"Enabled: {power_off_result['enabled']}, "
                  f"Pressed: {power_off_result['pressed']}")
            print("="*50)
            
            print("\nAll tests completed!")
            
        except Exception as e:
            print(f"Error during testing: {e}")
            import traceback
            traceback.print_exc()
            
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
    Main function to run the projector page tests.
    """
    # Ensure necessary directories exist
    Config.ensure_directories()
    
    # Path to ProjectorPage.html (relative to this script)
    projector_page_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'ProjectorPage.html'
    )
    
    # Check if file exists
    if not os.path.exists(projector_page_path):
        print(f"Error: ProjectorPage.html not found at {projector_page_path}")
        print("Please ensure ProjectorPage.html is in the project root directory.")
        return
    
    print(f"Testing ProjectorPage.html at: {projector_page_path}")
    
    # Create and run tests
    test_automation = ProjectorPageTest(projector_page_path)
    test_automation.run_all_tests()


if __name__ == "__main__":
    main()

# Made with Bob