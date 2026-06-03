# Projector Page Automation Documentation

This document describes the automation scripts for `ProjectorPage.html`.

## Overview

Two separate automation scripts provide automated control for the projector interface:
- `automate_power_on.py` - Automates the Power On button
- `automate_power_off.py` - Automates the Power Off button

Each automation can be run independently.

## Automation Scripts

### Script 1: Power On Button (`automate_power_on.py`)
- **Button ID**: `Btn_PowerOn`
- **Location**: Line 206 in ProjectorPage.html
- **Action**: Automatically locates and clicks the Power On button
- **Expected Behavior**:
  - Button should be found on the page
  - Button may be disabled if projector is already on
  - If enabled, clicking will trigger the `powerOn()` JavaScript function

### Script 2: Power Off Button (`automate_power_off.py`)
- **Button ID**: `Btn_PowerOff`
- **Location**: Line 208 in ProjectorPage.html
- **Action**: Automatically locates and clicks the Power Off button
- **Expected Behavior**:
  - Button should be found on the page
  - Button may be disabled if projector is already off
  - If enabled, clicking will trigger a confirmation dialog
  - The automation automatically accepts the confirmation dialog

## Running the Automation Scripts

### Prerequisites
Make sure you have installed all dependencies:
```bash
pip install -r requirements.txt
```

### Execute Automation Scripts Independently

**Run Power On Automation:**
```bash
python examples/automate_power_on.py
```

**Run Power Off Automation:**
```bash
python examples/automate_power_off.py
```

**Run from examples directory:**
```bash
cd examples
python automate_power_on.py
python automate_power_off.py
```

## Automation Output

Each automation script provides detailed output including:
- Setup confirmation
- Automation execution status
- Button state (found, enabled, pressed)
- Screenshot location (if enabled in config)
- Automation summary with success/error status

### Example Output - Power On Automation
```
==================================================
Projector Power On Automation
==================================================
Automating: /path/to/ProjectorPage.html
==================================================
Setting up Power On automation for file:///path/to/ProjectorPage.html...
Setup complete!

==================================================
Power On Button Automation
==================================================

Button found: True
Button enabled: True
Button pressed: True

Success: Power On button was clicked!
The projector should now be turning on

Screenshot saved: screenshots/automate_power_on.png
==================================================

==================================================
Automation Summary
==================================================
✓ SUCCESS: Power On button found and clicked
==================================================
```

### Example Output - Power Off Automation
```
==================================================
Projector Power Off Automation
==================================================
Automating: /path/to/ProjectorPage.html
==================================================
Setting up Power Off automation for file:///path/to/ProjectorPage.html...
Setup complete!

==================================================
Power Off Button Automation
==================================================

Button found: True
Button enabled: True
Button pressed: True

Success: Power Off button was clicked!

Confirmation dialog appeared: 'Turn off the projector?'
Confirmation dialog accepted - projector should now be turning off

Screenshot saved: screenshots/automate_power_off.png
==================================================

==================================================
Automation Summary
==================================================
✓ SUCCESS: Power Off button found and clicked
==================================================
```

## Configuration

Automation scripts use settings from `config.py`:
- `HEADLESS`: Set to `False` to see the browser window during automation
- `IMPLICIT_WAIT`: Wait time for elements to load (default: 10 seconds)
- `SAVE_SCREENSHOTS`: Enable/disable screenshot capture

## Screenshots

If `SAVE_SCREENSHOTS` is enabled in config, the following screenshots are captured:
- `screenshots/automate_power_on.png` - After Power On button automation
- `screenshots/automate_power_off.png` - After Power Off button automation

## Notes

1. **Button State**: The buttons may be disabled depending on the projector's current power state. This is normal behavior controlled by the page's JavaScript.

2. **Confirmation Dialog**: The Power Off button triggers a JavaScript confirmation dialog ("Turn off the projector?"). The automation automatically handles this by accepting the dialog.

3. **Local File Automation**: The automation opens ProjectorPage.html as a local file using the `file://` protocol. Some JavaScript features that require server communication may not work in this mode.

4. **JavaScript Dependencies**: The page references external resources:
   - `/dpjctrl.css` - Stylesheet
   - `/showpath.js` - JavaScript file
   - `/VvkLogo.png` - Logo image
   
   These may not load when testing the HTML file locally, but the button tests will still work.

## Troubleshooting

### File Not Found Error
If you see "ProjectorPage.html not found", ensure:
- The file exists in the project root directory
- You're running the script from the correct location

### Selenium/ChromeDriver Issues
If you encounter browser driver issues:
```bash
pip install --upgrade selenium webdriver-manager
```

### Button Not Found
If buttons aren't found:
- Check that ProjectorPage.html hasn't been modified
- Verify button IDs are still `Btn_PowerOn` and `Btn_PowerOff`
- Increase `IMPLICIT_WAIT` in config.py

## Extending the Automation

To add more button automation, follow this pattern:

```python
def automate_new_button(self):
    """Automate a new button."""
    print("\n=== Automation: New Button ===")
    
    result = self.checker.check_and_press(
        by=By.ID,
        value="Button_ID_Here"
    )
    
    print(f"Button found: {result['found']}")
    print(f"Button enabled: {result['enabled']}")
    print(f"Button pressed: {result['pressed']}")
    
    return result
```

Then add the automation to your script's `run()` method.

## Made with Bob