"""
Projector Power On Automation: Automate the Power On button action
"""

import sys
import os
import time

# Add parent directory to path to import the framework
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from browser_automation import BrowserController, ButtonChecker
from selenium.webdriver.common.by import By
from config import Config


class PowerOnAutomation:
    """
    Automation for Projector Power On button
    """
    
    def __init__(self, page_path: str):
        """
        Initialize the power on automation.
        
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
        print(f"Setting up Power On automation for {self.url}...")
        self.browser.start_browser()
        self.browser.navigate_to(self.url)
        self.checker = ButtonChecker(self.browser)
        print("Setup complete!")
        
    def automate_power_on_button(self):
        """
        Automate: Check and press the Power On button.
        Button ID: Btn_PowerOn
        """
        print("\n" + "="*50)
        print("Power On Button Automation")
        print("="*50)
        
        # Find and press the Power On button by ID
        result = self.checker.check_and_press(
            by=By.ID,
            value="Btn_PowerOn"
        )
        
        print(f"\nButton found: {result['found']}")
        print(f"Was already pressed: {result['was_pressed']}")
        print(f"Action taken: {result['action_taken']}")
        print(f"Success: {result['success']}")
        
        if result['found']:
            if result['was_pressed'] and result['action_taken'] == 'already_pressed':
                print("\nNote: Power On button was already pressed")
                print("This usually means the projector is already powered on")
            elif result['success'] and result['action_taken'] == 'pressed':
                print("\nSuccess: Power On button was clicked!")
                print("The projector should now be turning on")
            elif result['action_taken'] == 'press_failed':
                print("\nError: Failed to press the Power On button")
        
        # Take screenshot after pressing
        if Config.SAVE_SCREENSHOTS and result['found']:
            screenshot_path = os.path.join(
                Config.SCREENSHOT_DIR,
                "test_power_on.png"
            )
            self.browser.take_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
        
        print("="*50)
        
        return result
    
    def run(self):
        """
        Run the power on automation.
        """
        try:
            self.setup()
            
            # Wait a moment for page to fully load
            time.sleep(1)
            
            # Run the automation
            result = self.automate_power_on_button()
            
            # Summary
            print("\n" + "="*50)
            print("Automation Summary")
            print("="*50)
            if result['found']:
                if result['success'] and result['action_taken'] == 'pressed':
                    print("✓ SUCCESS: Power On button found and clicked")
                elif result['action_taken'] == 'already_pressed':
                    print("⚠ INFO: Power On button already pressed (projector may be on)")
                elif result['action_taken'] == 'press_failed':
                    print("✗ ERROR: Power On button found but failed to click")
                else:
                    print("⚠ INFO: Power On button found - " + result['action_taken'])
            else:
                print("✗ ERROR: Power On button not found")
            print("="*50)
            
        except Exception as e:
            print(f"\n✗ ERROR: Automation failed with exception: {e}")
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
    Main function to run the power on automation.
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
    
    print("="*50)
    print("Projector Power On Automation")
    print("="*50)
    print(f"Automating: {os.path.abspath(projector_page_path)}")
    print("="*50)
    
    # Create and run automation
    automation = PowerOnAutomation(projector_page_path)
    automation.run()


if __name__ == "__main__":
    main()

# Made with Bob