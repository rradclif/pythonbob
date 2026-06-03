"""
Projector Power Off Automation: Automate the Power Off button action
"""

import sys
import os
import time

# Add parent directory to path to import the framework
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from browser_automation import BrowserController, ButtonChecker
from selenium.webdriver.common.by import By
from config import Config


class PowerOffAutomation:
    """
    Automation for Projector Power Off button
    """
    
    def __init__(self, page_path: str):
        """
        Initialize the power off automation.
        
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
        print(f"Setting up Power Off automation for {self.url}...")
        self.browser.start_browser()
        self.browser.navigate_to(self.url)
        self.checker = ButtonChecker(self.browser)
        print("Setup complete!")
        
    def automate_power_off_button(self):
        """
        Automate: Check and press the Power Off button.
        Button ID: Btn_PowerOff
        Note: This button triggers a confirmation dialog.
        """
        print("\n" + "="*50)
        print("Power Off Button Automation")
        print("="*50)
        
        # Find and press the Power Off button by ID
        result = self.checker.check_and_press(
            by=By.ID,
            value="Btn_PowerOff"
        )
        
        print(f"\nButton found: {result['found']}")
        print(f"Was already pressed: {result['was_pressed']}")
        print(f"Action taken: {result['action_taken']}")
        print(f"Success: {result['success']}")
        
        if result['found']:
            if result['was_pressed'] and result['action_taken'] == 'already_pressed':
                print("\nNote: Power Off button was already pressed")
                print("This usually means the projector is already powered off")
            elif result['success'] and result['action_taken'] == 'pressed':
                print("\nSuccess: Power Off button was clicked!")
                
                # Handle the confirmation dialog if button was pressed
                try:
                    # Wait a moment for the alert to appear
                    time.sleep(0.5)
                    
                    # Switch to the alert and accept it
                    alert = self.browser.driver.switch_to.alert
                    alert_text = alert.text
                    print(f"\nConfirmation dialog appeared: '{alert_text}'")
                    
                    # Accept the alert (click OK)
                    alert.accept()
                    print("Confirmation dialog accepted - projector should now be turning off")
                    
                except Exception as e:
                    print(f"\nNote: No confirmation dialog appeared or error handling it: {e}")
            elif result['action_taken'] == 'press_failed':
                print("\nError: Failed to press the Power Off button")
        
        # Take screenshot after pressing
        if Config.SAVE_SCREENSHOTS and result['found']:
            screenshot_path = os.path.join(
                Config.SCREENSHOT_DIR,
                "test_power_off.png"
            )
            self.browser.take_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
        
        print("="*50)
        
        return result
    
    def run(self):
        """
        Run the power off automation.
        """
        try:
            self.setup()
            
            # Wait a moment for page to fully load
            time.sleep(1)
            
            # Run the automation
            result = self.automate_power_off_button()
            
            # Summary
            print("\n" + "="*50)
            print("Automation Summary")
            print("="*50)
            if result['found']:
                if result['success'] and result['action_taken'] == 'pressed':
                    print("✓ SUCCESS: Power Off button found and clicked")
                elif result['action_taken'] == 'already_pressed':
                    print("⚠ INFO: Power Off button already pressed (projector may be off)")
                elif result['action_taken'] == 'press_failed':
                    print("✗ ERROR: Power Off button found but failed to click")
                else:
                    print("⚠ INFO: Power Off button found - " + result['action_taken'])
            else:
                print("✗ ERROR: Power Off button not found")
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
    Main function to run the power off automation.
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
    print("Projector Power Off Automation")
    print("="*50)
    print(f"Automating: {os.path.abspath(projector_page_path)}")
    print("="*50)
    
    # Create and run automation
    automation = PowerOffAutomation(projector_page_path)
    automation.run()


if __name__ == "__main__":
    main()

# Made with Bob