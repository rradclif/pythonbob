"""
Button Checker Module
Provides functionality to check and interact with buttons on web pages.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException
)
from typing import Optional, Dict, Any
import time


class ButtonChecker:
    """
    A class for checking button states and interacting with them.
    Works with various button identification strategies.
    """
    
    def __init__(self, browser_controller):
        """
        Initialize the button checker.
        
        Args:
            browser_controller: Instance of BrowserController
        """
        self.browser = browser_controller
        
    def find_button(
        self,
        by: By = By.ID,
        value: str = None,
        text: str = None,
        css_selector: str = None,
        xpath: str = None
    ) -> Optional[WebElement]:
        """
        Find a button using various strategies.
        
        Args:
            by: Selenium By locator strategy (default: By.ID)
            value: The locator value
            text: Button text to search for
            css_selector: CSS selector for the button
            xpath: XPath expression for the button
            
        Returns:
            WebElement if found, None otherwise
        """
        try:
            # Priority order: xpath > css_selector > text > by+value
            if xpath:
                return self.browser.find_element(By.XPATH, xpath)
            elif css_selector:
                return self.browser.find_element(By.CSS_SELECTOR, css_selector)
            elif text:
                # Try to find button by text content
                xpath_text = f"//button[contains(text(), '{text}')] | //input[@type='button' and contains(@value, '{text}')] | //input[@type='submit' and contains(@value, '{text}')]"
                return self.browser.find_element(By.XPATH, xpath_text)
            elif value:
                return self.browser.find_element(by, value)
            else:
                raise ValueError("Must provide at least one search criterion")
                
        except NoSuchElementException:
            return None
    
    def is_button_pressed(self, button: WebElement) -> bool:
        """
        Check if a button appears to be in a "pressed" state.
        This checks various attributes that might indicate pressed state.
        
        Args:
            button: The button WebElement to check
            
        Returns:
            True if button appears pressed, False otherwise
        """
        if not button:
            return False
        
        # Check common attributes that indicate pressed state
        aria_pressed = button.get_attribute("aria-pressed")
        if aria_pressed and aria_pressed.lower() == "true":
            return True
        
        # Check if button has "active" or "pressed" class
        class_attr = button.get_attribute("class") or ""
        if any(cls in class_attr.lower() for cls in ["active", "pressed", "selected"]):
            return True
        
        # Check disabled state (some buttons become disabled when pressed)
        if button.get_attribute("disabled"):
            return True
        
        # Check data attributes
        data_pressed = button.get_attribute("data-pressed")
        if data_pressed and data_pressed.lower() == "true":
            return True
        
        return False
    
    def press_button(self, button: WebElement, wait_after: float = 0.5) -> bool:
        """
        Press (click) a button.
        
        Args:
            button: The button WebElement to press
            wait_after: Time to wait after pressing (seconds)
            
        Returns:
            True if successful, False otherwise
        """
        if not button:
            return False
        
        try:
            # Scroll to button if needed
            self.browser.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.3)  # Brief pause after scroll
            
            # Click the button
            button.click()
            
            # Wait after clicking
            if wait_after > 0:
                time.sleep(wait_after)
            
            return True
            
        except ElementNotInteractableException:
            # Try JavaScript click as fallback
            try:
                self.browser.driver.execute_script("arguments[0].click();", button)
                if wait_after > 0:
                    time.sleep(wait_after)
                return True
            except Exception:
                return False
        except Exception:
            return False
    
    def check_and_press(
        self,
        by: By = By.ID,
        value: str = None,
        text: str = None,
        css_selector: str = None,
        xpath: str = None,
        force_press: bool = False
    ) -> Dict[str, Any]:
        """
        Check if a button is pressed, and press it if not.
        
        Args:
            by: Selenium By locator strategy
            value: The locator value
            text: Button text to search for
            css_selector: CSS selector for the button
            xpath: XPath expression for the button
            force_press: Press button even if it appears already pressed
            
        Returns:
            Dictionary with status information:
            {
                'found': bool,
                'was_pressed': bool,
                'action_taken': str,
                'success': bool
            }
        """
        result = {
            'found': False,
            'was_pressed': False,
            'action_taken': 'none',
            'success': False
        }
        
        # Find the button
        button = self.find_button(by, value, text, css_selector, xpath)
        
        if not button:
            result['action_taken'] = 'button_not_found'
            return result
        
        result['found'] = True
        
        # Check if already pressed
        is_pressed = self.is_button_pressed(button)
        result['was_pressed'] = is_pressed
        
        # Decide whether to press
        if not is_pressed or force_press:
            success = self.press_button(button)
            result['success'] = success
            result['action_taken'] = 'pressed' if success else 'press_failed'
        else:
            result['success'] = True
            result['action_taken'] = 'already_pressed'
        
        return result
    
    def get_button_info(self, button: WebElement) -> Dict[str, Any]:
        """
        Get detailed information about a button.
        
        Args:
            button: The button WebElement
            
        Returns:
            Dictionary with button information
        """
        if not button:
            return {}
        
        return {
            'tag': button.tag_name,
            'text': button.text,
            'id': button.get_attribute('id'),
            'class': button.get_attribute('class'),
            'type': button.get_attribute('type'),
            'value': button.get_attribute('value'),
            'aria_pressed': button.get_attribute('aria-pressed'),
            'disabled': button.get_attribute('disabled'),
            'is_displayed': button.is_displayed(),
            'is_enabled': button.is_enabled()
        }

# Made with Bob
