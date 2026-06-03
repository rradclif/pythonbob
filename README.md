# Browser Automation Framework

A flexible and reusable Python framework for browser automation, specifically designed to automate button interactions on web pages.

## Features

- 🚀 Easy-to-use browser automation with Selenium
- 🔘 Smart button detection and interaction
- 🔄 Automatic retry logic with configurable attempts
- 📸 Screenshot capture capabilities
- ⚙️ Configurable settings via environment variables
- 🎯 Multiple button locator strategies (ID, text, CSS, XPath)
- 🧩 Modular design for easy customization
- 🔒 Context manager support for automatic cleanup
- 🛡️ Security-focused with input validation and safe defaults
- 📦 Updated dependencies with latest security patches

## Project Structure

```
pythonbob/
├── browser_automation/          # Main framework package
│   ├── __init__.py             # Package initialization
│   ├── browser_controller.py   # Browser management
│   └── button_checker.py       # Button interaction logic
├── examples/                    # Usage examples
│   ├── basic_example.py        # Simple usage example
│   ├── advanced_example.py     # Advanced patterns
│   ├── custom_page_example.py  # Template for custom pages
│   ├── automate_power_on.py    # Projector Power On automation
│   ├── automate_power_off.py   # Projector Power Off automation
│   ├── projector_page_test.py  # Combined projector tests (sample)
│   └── PROJECTOR_AUTOMATION_README.md # Projector automation documentation
├── config.py                    # Configuration management
├── ProjectorPage.html           # Projector control page
├── .env.example                 # Example environment variables
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

## Quick Start

### Basic Usage

```python
from browser_automation import BrowserController, ButtonChecker
from selenium.webdriver.common.by import By

# Initialize browser
browser = BrowserController(headless=False)
browser.start_browser()

# Navigate to your page
browser.navigate_to("https://example.com")

# Check and press a button
checker = ButtonChecker(browser)
result = checker.check_and_press(text="Click Me")

print(f"Button found: {result['found']}")
print(f"Action taken: {result['action_taken']}")

# Cleanup
browser.close_browser()
```

### Using Context Manager

```python
from browser_automation import BrowserController, ButtonChecker

with BrowserController() as browser:
    browser.navigate_to("https://example.com")
    checker = ButtonChecker(browser)
    result = checker.check_and_press(css_selector="button.submit")
    print(result)
# Browser automatically closes
```

## Button Locator Strategies

The framework supports multiple ways to find buttons:

### 1. By ID
```python
result = checker.check_and_press(by=By.ID, value="submit-button")
```

### 2. By Text Content
```python
result = checker.check_and_press(text="Submit")
```

### 3. By CSS Selector
```python
result = checker.check_and_press(css_selector="button.primary-btn")
```

### 4. By XPath
```python
result = checker.check_and_press(xpath="//button[@type='submit']")
```

## Configuration

Configure the framework by setting environment variables in a `.env` file:

```bash
# Browser Settings
HEADLESS=False              # Run browser in headless mode
IMPLICIT_WAIT=10           # Default wait time for elements (seconds)
PAGE_LOAD_TIMEOUT=30       # Page load timeout (seconds)

# Screenshot Settings
SCREENSHOT_DIR=screenshots  # Directory for screenshots
SAVE_SCREENSHOTS=True      # Enable/disable screenshots

# Button Interaction
WAIT_AFTER_CLICK=0.5       # Wait time after clicking (seconds)
MAX_RETRIES=3              # Maximum retry attempts
RETRY_DELAY=1.0            # Delay between retries (seconds)

# Logging
LOG_LEVEL=INFO             # Logging level
LOG_FILE=browser_automation.log  # Log file path
```

## API Reference

### BrowserController

Main class for browser management.

**Methods:**
- `start_browser()` - Initialize and start the browser
- `navigate_to(url)` - Navigate to a URL
- `find_element(by, value)` - Find a single element
- `find_elements(by, value)` - Find multiple elements
- `wait_for_element(by, value, timeout)` - Wait for element to appear
- `take_screenshot(filename)` - Capture screenshot
- `close_browser()` - Close browser and cleanup

### ButtonChecker

Class for button detection and interaction.

**Methods:**
- `find_button(by, value, text, css_selector, xpath)` - Find a button
- `is_button_pressed(button)` - Check if button is in pressed state
- `press_button(button, wait_after)` - Click a button
- `check_and_press(**kwargs)` - Find and press button if not already pressed
- `get_button_info(button)` - Get detailed button information

**check_and_press() Return Value:**
```python
{
    'found': bool,           # Whether button was found
    'was_pressed': bool,     # Whether button was already pressed
    'action_taken': str,     # Action performed
    'success': bool          # Whether operation succeeded
}
```

## Examples

### Example 1: Basic Button Check
```python
from browser_automation import BrowserController, ButtonChecker

browser = BrowserController()
browser.start_browser()
browser.navigate_to("https://example.com")

checker = ButtonChecker(browser)
result = checker.check_and_press(text="Login")

if result['success']:
    print("Button pressed successfully!")
else:
    print(f"Failed: {result['action_taken']}")

browser.close_browser()
```

### Example 2: Multiple Button Checks
```python
buttons = [
    {'text': 'Submit'},
    {'css_selector': '.action-btn'},
    {'xpath': '//button[@id="confirm"]'}
]

for btn_config in buttons:
    result = checker.check_and_press(**btn_config)
    print(f"Result: {result}")
```

### Example 3: Custom Page Automation
See [`examples/custom_page_example.py`](examples/custom_page_example.py) for a complete template.

### Example 4: Projector Page Automation
Real-world automation for ProjectorPage.html control interface:

```python
# Automate Power On button
python examples/automate_power_on.py

# Automate Power Off button
python examples/automate_power_off.py

# Sample test script (for testing purposes)
python examples/projector_page_test.py
```

See [`examples/PROJECTOR_AUTOMATION_README.md`](examples/PROJECTOR_AUTOMATION_README.md) for detailed documentation.

## Running Examples

```bash
# Basic example
python examples/basic_example.py

# Advanced example with retry logic
python examples/advanced_example.py

# Custom page template
python examples/custom_page_example.py

# Projector control automation
python examples/automate_power_on.py      # Automate Power On button
python examples/automate_power_off.py     # Automate Power Off button
python examples/projector_page_test.py    # Sample test script
```

## Troubleshooting

### Chrome Driver Issues
The framework uses `webdriver-manager` to automatically download and manage ChromeDriver. If you encounter issues:
- Ensure Chrome browser is installed
- Check your internet connection
- Try running with `headless=False` to see what's happening

### Button Not Found
If buttons aren't being found:
1. Verify the page has loaded completely
2. Try different locator strategies
3. Use browser DevTools to inspect the button element
4. Increase `IMPLICIT_WAIT` in configuration
5. Use `wait_for_element()` for dynamic content

### Element Not Interactable
If clicks fail:
- The element might be covered by another element
- Try scrolling to the element first
- Use `force_press=True` to attempt JavaScript click
- Check if the button is disabled

## Best Practices

1. **Always use context managers** when possible for automatic cleanup
2. **Start with specific locators** (ID) before falling back to generic ones (text)
3. **Add appropriate waits** for dynamic content
4. **Take screenshots** when debugging issues
5. **Use retry logic** for unreliable elements
6. **Create page-specific classes** for complex workflows

## Requirements

- Python 3.7+
- Chrome browser
- See [`requirements.txt`](requirements.txt) for Python packages
## Keeping Your Project Secure

### Weekly Update Checks

Run the automated update checker to ensure your packages are secure and up-to-date:

```bash
# Command line
python3 check_updates.py

# Or double-click (macOS)
run_update_check.command
```

The checker will:
- ✓ Scan for security vulnerabilities
- ✓ List outdated packages
- ✓ Test module imports
- ✓ Generate detailed reports

**Recommended**: Run weekly or before deployments.

See [`WEEKLY_UPDATE_CHECK.md`](WEEKLY_UPDATE_CHECK.md) for detailed instructions and automation options.


## Security

This project follows security best practices:
- ✅ Updated dependencies (Selenium 4.40.0, latest as of Jan 2026)
- ✅ Input validation and sanitization
- ✅ Secure file permissions for screenshots
- ✅ Path traversal protection
- ✅ Environment variable validation
- ✅ SSL certificate validation with updated certifi

See [`SECURITY.md`](SECURITY.md) for detailed security information and best practices.

### Security Scanning

Run security checks on dependencies:
```bash
pip install pip-audit
pip-audit
```

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to extend and customize this framework for your specific needs. The modular design makes it easy to add new features or modify existing behavior.

## Support

For issues or questions:
1. Check the examples in the `examples/` directory
2. Review the API reference above
3. Inspect browser behavior with `headless=False`
4. Enable debug logging in configuration