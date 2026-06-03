# Dual Projector Control Setup

This document explains how to control both the left and right projectors using the browser automation framework.

## Projector Configuration

### Left Projector
- **URL**: http://192.168.1.21/PJControl.html
- **Label**: Left Projector
- **IP Address**: 192.168.1.21

### Right Projector
- **URL**: http://192.168.1.20/PJControl.html
- **Label**: Right Projector
- **IP Address**: 192.168.1.20

## Quick Start - Desktop Launchers

The easiest way to control the projectors is using the desktop launcher scripts. Simply double-click any of these files:

### Control Both Projectors (Recommended)
- **`run_both_projectors_on.command`** - Turn on BOTH projectors simultaneously ⚡
- **`run_both_projectors_off.command`** - Turn off BOTH projectors simultaneously ⚡

### Left Projector Controls
- **`run_left_projector_on.command`** - Turn on the left projector only
- **`run_left_projector_off.command`** - Turn off the left projector only

### Right Projector Controls
- **`run_right_projector_on.command`** - Turn on the right projector only
- **`run_right_projector_off.command`** - Turn off the right projector only

### Original Test Controls (Local HTML)
- **`run_power_on.command`** - Test with local ProjectorPage.html
- **`run_power_off.command`** - Test with local ProjectorPage.html

## Python Scripts

If you prefer to run the scripts directly with Python:

### Both Projectors (Simultaneous Control)
```bash
# Power On Both
python3 examples/automate_both_projectors_on.py

# Power Off Both
python3 examples/automate_both_projectors_off.py
```

### Left Projector
```bash
# Power On
python3 examples/automate_left_projector_on.py

# Power Off
python3 examples/automate_left_projector_off.py
```

### Right Projector
```bash
# Power On
python3 examples/automate_right_projector_on.py

# Power Off
python3 examples/automate_right_projector_off.py
```

## How It Works

### Button IDs
Both projectors use the same web interface with these button IDs:
- **Power On Button**: `Btn_PowerOn`
- **Power Off Button**: `Btn_PowerOff`

### Power Off Confirmation
When turning off a projector, the web interface displays a JavaScript confirmation dialog asking "Turn off the projector?". The automation scripts automatically:
1. Click the Power Off button
2. Wait for the confirmation dialog
3. Accept the dialog (click OK)
4. Confirm the projector is turning off

### Screenshots
By default, screenshots are saved after each operation to the `screenshots/` directory:
- `left_projector_power_on.png`
- `left_projector_power_off.png`
- `right_projector_power_on.png`
- `right_projector_power_off.png`

## Network Requirements

### Prerequisites
1. **Network Access**: Your computer must be on the same network as the projectors
2. **IP Addresses**: The projectors must be accessible at:
   - 192.168.1.21 (Left Projector)
   - 192.168.1.20 (Right Projector)
3. **HTTP Access**: The projectors' web interfaces must be accessible via HTTP

### Testing Network Connectivity

Test if you can reach the projectors:

```bash
# Test left projector
curl -I http://192.168.1.21/PJControl.html

# Test right projector
curl -I http://192.168.1.20/PJControl.html
```

Or open the URLs in your web browser:
- http://192.168.1.21/PJControl.html
- http://192.168.1.20/PJControl.html

## Configuration

### Environment Variables

You can customize behavior by creating a `.env` file (copy from `.env.example`):

```bash
# Projector URLs (already configured)
LEFT_PROJECTOR_URL=http://192.168.1.21/PJControl.html
RIGHT_PROJECTOR_URL=http://192.168.1.20/PJControl.html

# Browser Settings
HEADLESS=False              # Set to True to run without visible browser
IMPLICIT_WAIT=10            # Seconds to wait for elements
PAGE_LOAD_TIMEOUT=30        # Seconds to wait for page load

# Screenshot Settings
SCREENSHOT_DIR=screenshots  # Directory for screenshots
SAVE_SCREENSHOTS=True       # Set to False to disable screenshots

# Button Interaction Settings
WAIT_AFTER_CLICK=0.5       # Seconds to wait after clicking
MAX_RETRIES=3              # Number of retry attempts
RETRY_DELAY=1.0            # Seconds between retries

# Logging Settings
LOG_LEVEL=INFO             # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=browser_automation.log
```

### Headless Mode

To run without opening a visible browser window, set `HEADLESS=True` in your `.env` file. This is useful for:
- Running from cron jobs or scheduled tasks
- Server environments without displays
- Faster execution

## Troubleshooting

### Common Issues

#### 1. Cannot Connect to Projector
**Error**: Connection timeout or refused
**Solutions**:
- Verify projector is powered on and connected to network
- Check IP addresses are correct (192.168.1.21 and 192.168.1.20)
- Ensure your computer is on the same network
- Try accessing the URL in a web browser first

#### 2. Button Not Found
**Error**: "Power On button not found" or "Power Off button not found"
**Solutions**:
- Verify the projector's web interface is loading correctly
- Check that the button IDs haven't changed (`Btn_PowerOn`, `Btn_PowerOff`)
- Increase `IMPLICIT_WAIT` in `.env` to give page more time to load

#### 3. Button Already Pressed
**Info**: "Power On button already pressed"
**Meaning**: The projector is already in the desired state
- For Power On: Projector is already on
- For Power Off: Projector is already off

#### 4. Permission Denied on .command Files
**Error**: Cannot execute .command file
**Solution**:
```bash
chmod +x run_left_projector_on.command
chmod +x run_left_projector_off.command
chmod +x run_right_projector_on.command
chmod +x run_right_projector_off.command
```

#### 5. Python Not Found
**Error**: Python 3.12 not found
**Solutions**:
- Install Python 3.12+ from https://www.python.org/
- Or the script will fall back to system `python3`
- Verify installation: `python3 --version`

## Advanced Usage

### Controlling Both Projectors Simultaneously

The framework includes built-in scripts to control both projectors at once using multi-threading for faster execution:

```bash
# Turn on both projectors simultaneously
python3 examples/automate_both_projectors_on.py

# Turn off both projectors simultaneously
python3 examples/automate_both_projectors_off.py
```

These scripts use Python threading to control both projectors in parallel, making the operation much faster than running them sequentially.

### Scheduled Automation

Use cron (macOS/Linux) to schedule projector control:

```bash
# Edit crontab
crontab -e

# Turn on projectors at 8 AM weekdays
0 8 * * 1-5 cd /path/to/pythonbob && python3 examples/automate_left_projector_on.py
0 8 * * 1-5 cd /path/to/pythonbob && python3 examples/automate_right_projector_on.py

# Turn off projectors at 6 PM weekdays
0 18 * * 1-5 cd /path/to/pythonbob && python3 examples/automate_left_projector_off.py
0 18 * * 1-5 cd /path/to/pythonbob && python3 examples/automate_right_projector_off.py
```

## Security Considerations

### Network Security
- The projectors use HTTP (not HTTPS), so traffic is unencrypted
- Ensure the projector network is properly secured
- Consider using a VPN if accessing remotely

### Access Control
- The automation scripts have full control over the projectors
- Restrict access to the scripts and .command files
- Consider implementing authentication if needed

## File Structure

```
pythonbob/
├── examples/
│   ├── automate_both_projectors_on.py     # Both projectors power on (parallel)
│   ├── automate_both_projectors_off.py    # Both projectors power off (parallel)
│   ├── automate_left_projector_on.py      # Left projector power on
│   ├── automate_left_projector_off.py     # Left projector power off
│   ├── automate_right_projector_on.py     # Right projector power on
│   ├── automate_right_projector_off.py    # Right projector power off
│   ├── automate_power_on.py               # Original test (local HTML)
│   └── automate_power_off.py              # Original test (local HTML)
├── run_both_projectors_on.command         # Desktop launcher (both)
├── run_both_projectors_off.command        # Desktop launcher (both)
├── run_left_projector_on.command          # Desktop launcher (left)
├── run_left_projector_off.command         # Desktop launcher (left)
├── run_right_projector_on.command         # Desktop launcher (right)
├── run_right_projector_off.command        # Desktop launcher (right)
├── run_power_on.command                   # Original test launcher
├── run_power_off.command                  # Original test launcher
├── config.py                              # Configuration settings
├── .env.example                           # Environment variables template
└── DUAL_PROJECTOR_SETUP.md               # This file
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the main README.md for general framework documentation
3. Check the browser automation logs in `browser_automation.log`
4. Verify network connectivity to the projectors

## Summary

### Quick Reference

| Action | Both Projectors | Left Projector | Right Projector |
|--------|----------------|---------------|-----------------|
| Power On | `run_both_projectors_on.command` ⚡ | `run_left_projector_on.command` | `run_right_projector_on.command` |
| Power Off | `run_both_projectors_off.command` ⚡ | `run_left_projector_off.command` | `run_right_projector_off.command` |
| URL | Both simultaneously | http://192.168.1.21/PJControl.html | http://192.168.1.20/PJControl.html |
| IP Address | 192.168.1.21 & .20 | 192.168.1.21 | 192.168.1.20 |

⚡ = Simultaneous control using multi-threading (faster)

---

*Last Updated: June 2026*
*Made with Bob*