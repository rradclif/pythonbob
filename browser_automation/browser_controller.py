"""
Browser Controller Module
Handles browser initialization and basic operations.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional
import time


class BrowserController:
    """
    A controller class for managing browser automation tasks.
    Supports Chrome browser with automatic driver management.
    """
    
    def __init__(self, headless: bool = False, implicit_wait: int = 10):
        """
        Initialize the browser controller.
        
        Args:
            headless: Run browser in headless mode (no GUI)
            implicit_wait: Default wait time in seconds for elements
        """
        self.headless = headless
        self.implicit_wait = implicit_wait
        self.driver: Optional[webdriver.Chrome] = None
        
    def start_browser(self) -> webdriver.Chrome:
        """
        Start the Chrome browser with configured options.
        
        Returns:
            WebDriver instance
        """
        chrome_options = Options()
        
        if self.headless:
            # Use new headless mode for Selenium 4.8+
            chrome_options.add_argument("--headless=new")
        
        # Additional options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Allow access to local/private network addresses (for projector control)
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-insecure-localhost")
        chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        
        # Set preferences to allow private network access
        prefs = {
            "profile.default_content_setting_values.insecure_private_network": 1
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Initialize driver with automatic driver management
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(self.implicit_wait)
        
        return self.driver
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.
        
        Args:
            url: The URL to navigate to
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        
        self.driver.get(url)
        
    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        """
        Wait for an element to be present and visible.
        
        Args:
            by: Selenium By locator strategy
            value: The locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement if found
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        return element
    
    def find_element(self, by: By, value: str):
        """
        Find a single element.
        
        Args:
            by: Selenium By locator strategy
            value: The locator value
            
        Returns:
            WebElement if found, None otherwise
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        
        try:
            return self.driver.find_element(by, value)
        except Exception:
            return None
    
    def find_elements(self, by: By, value: str):
        """
        Find multiple elements.
        
        Args:
            by: Selenium By locator strategy
            value: The locator value
            
        Returns:
            List of WebElements
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        
        return self.driver.find_elements(by, value)
    
    def take_screenshot(self, filename: str) -> bool:
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Path to save the screenshot
            
        Returns:
            True if successful, False otherwise
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        
        return self.driver.save_screenshot(filename)
    
    def close_browser(self) -> None:
        """
        Close the browser and clean up resources.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def __enter__(self):
        """Context manager entry."""
        self.start_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_browser()

# Made with Bob
