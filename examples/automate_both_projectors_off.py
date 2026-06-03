"""
Both Projectors Power Off Automation
Controls both left and right projectors simultaneously
Left: http://192.168.1.21/PJControl.html
Right: http://192.168.1.20/PJControl.html
"""

import sys
import os
import time
import threading
from typing import Dict, Any

# Add parent directory to path to import the framework
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from browser_automation import BrowserController, ButtonChecker
from selenium.webdriver.common.by import By
from config import Config


class ProjectorController:
    """Control a single projector."""
    
    def __init__(self, name: str, url: str):
        """Initialize projector controller."""
        self.name = name
        self.url = url
        self.result = None
        
    def power_off(self) -> Dict[str, Any]:
        """Power off the projector."""
        browser = None
        try:
            print(f"\n[{self.name}] Starting automation...")
            print(f"[{self.name}] URL: {self.url}")
            
            # Initialize browser
            browser = BrowserController(headless=Config.HEADLESS, implicit_wait=Config.IMPLICIT_WAIT)
            browser.start_browser()
            browser.navigate_to(self.url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Find and press Power Off button
            checker = ButtonChecker(browser)
            result = checker.check_and_press(by=By.ID, value="Btn_PowerOff")
            
            # Handle confirmation dialog
            if result['found'] and result['success'] and result['action_taken'] == 'pressed':
                try:
                    time.sleep(0.5)
                    alert = browser.driver.switch_to.alert
                    alert_text = alert.text
                    print(f"[{self.name}] Confirmation dialog: '{alert_text}'")
                    alert.accept()
                    print(f"[{self.name}] Confirmation accepted")
                except Exception as e:
                    print(f"[{self.name}] No confirmation dialog or error: {e}")
            
            # Take screenshot
            if Config.SAVE_SCREENSHOTS and result['found']:
                screenshot_name = f"{self.name.lower().replace(' ', '_')}_power_off.png"
                screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_name)
                browser.take_screenshot(screenshot_path)
                result['screenshot'] = screenshot_path
            
            self.result = result
            
            # Print result
            if result['found']:
                if result['success'] and result['action_taken'] == 'pressed':
                    print(f"[{self.name}] ✓ SUCCESS: Power Off button clicked!")
                elif result['action_taken'] == 'already_pressed':
                    print(f"[{self.name}] ⚠ INFO: Already powered off")
                else:
                    print(f"[{self.name}] ✗ ERROR: {result['action_taken']}")
            else:
                print(f"[{self.name}] ✗ ERROR: Power Off button not found")
            
            return result
            
        except Exception as e:
            print(f"[{self.name}] ✗ ERROR: {e}")
            self.result = {'found': False, 'success': False, 'error': str(e)}
            return self.result
            
        finally:
            if browser:
                browser.close_browser()


def control_projector_threaded(controller: ProjectorController):
    """Run projector control in a thread."""
    controller.power_off()


def main():
    """Main function to control both projectors."""
    # Ensure necessary directories exist
    Config.ensure_directories()
    
    print("="*60)
    print("Both Projectors Power Off Automation")
    print("="*60)
    print("Left Projector:  http://192.168.1.21/PJControl.html")
    print("Right Projector: http://192.168.1.20/PJControl.html")
    print("="*60)
    
    # Create controllers
    left_controller = ProjectorController("Left Projector", "http://192.168.1.21/PJControl.html")
    right_controller = ProjectorController("Right Projector", "http://192.168.1.20/PJControl.html")
    
    # Run both in parallel using threads
    left_thread = threading.Thread(target=control_projector_threaded, args=(left_controller,))
    right_thread = threading.Thread(target=control_projector_threaded, args=(right_controller,))
    
    # Start both threads
    left_thread.start()
    right_thread.start()
    
    # Wait for both to complete
    left_thread.join()
    right_thread.join()
    
    # Summary
    print("\n" + "="*60)
    print("Automation Summary")
    print("="*60)
    
    # Left projector summary
    if left_controller.result and left_controller.result.get('found'):
        if left_controller.result.get('success') and left_controller.result.get('action_taken') == 'pressed':
            print("Left Projector:  ✓ Powered Off Successfully")
        elif left_controller.result.get('action_taken') == 'already_pressed':
            print("Left Projector:  ⚠ Already Off")
        else:
            print("Left Projector:  ✗ Failed")
    else:
        print("Left Projector:  ✗ Error")
    
    # Right projector summary
    if right_controller.result and right_controller.result.get('found'):
        if right_controller.result.get('success') and right_controller.result.get('action_taken') == 'pressed':
            print("Right Projector: ✓ Powered Off Successfully")
        elif right_controller.result.get('action_taken') == 'already_pressed':
            print("Right Projector: ⚠ Already Off")
        else:
            print("Right Projector: ✗ Failed")
    else:
        print("Right Projector: ✗ Error")
    
    print("="*60)


if __name__ == "__main__":
    main()

# Made with Bob