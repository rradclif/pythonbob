# Mac Desktop Icon Setup Guide

This guide explains how to create desktop icons on macOS to run the projector automation scripts with a simple double-click.

## Quick Start

The project includes two command files that can be used as desktop launchers:
- `run_power_on.command` - Launches the Power On automation
- `run_power_off.command` - Launches the Power Off automation

## Method 1: Create Desktop Aliases (Recommended)

This is the easiest method and allows you to run the scripts directly from your desktop.

### Steps:

1. **Open Finder** and navigate to your project folder:
   ```
   /Users/rosalindradcliffe/pythonbob
   ```

2. **Locate the command files**:
   - `run_power_on.command`
   - `run_power_off.command`

3. **Create aliases on Desktop**:
   - Right-click on `run_power_on.command`
   - Select "Make Alias"
   - Drag the alias to your Desktop
   - Rename it to "Projector Power ON" (optional)
   
   - Repeat for `run_power_off.command`
   - Rename its alias to "Projector Power OFF" (optional)

4. **Double-click to run**:
   - Simply double-click the desktop icon to run the automation
   - A Terminal window will open and execute the script
   - The window will stay open so you can see the results

### First Time Setup:

The first time you double-click a `.command` file, macOS may ask for permission:

1. If you see "cannot be opened because it is from an unidentified developer":
   - Right-click the file and select "Open"
   - Click "Open" in the dialog that appears
   - This only needs to be done once per file

2. The Terminal app may need permission to run:
   - Go to System Preferences → Security & Privacy → Privacy
   - Select "Automation" or "Full Disk Access"
   - Enable Terminal if prompted

## Method 2: Create Custom App Icons (Advanced)

For a more polished look, you can create custom application icons.

### Using Automator:

1. **Open Automator** (Applications → Automator)

2. **Create New Document**:
   - Select "Application"
   - Click "Choose"

3. **Add Shell Script Action**:
   - Search for "Run Shell Script" in the actions library
   - Drag it to the workflow area
   - Change "Pass input" to "as arguments"
   - Enter this script:
   ```bash
   cd /Users/rosalindradcliffe/pythonbob
   ./run_power_on.command
   ```

4. **Save the Application**:
   - File → Save
   - Name it "Projector Power ON"
   - Save location: Desktop
   - File format: Application

5. **Repeat for Power Off**:
   - Create another Automator application
   - Use `./run_power_off.command` in the script
   - Name it "Projector Power OFF"

### Adding Custom Icons (Optional):

1. Find or create an icon image (PNG or ICNS format)
2. Right-click the application → Get Info
3. Drag your icon image onto the small icon in the top-left corner
4. The custom icon will now appear on your desktop

## Method 3: Terminal Command

You can also run the scripts directly from Terminal:

```bash
# Power On
cd /Users/rosalindradcliffe/pythonbob
./run_power_on.command

# Power Off
cd /Users/rosalindradcliffe/pythonbob
./run_power_off.command
```

## Troubleshooting

### "Permission Denied" Error

If you get a permission denied error:
```bash
chmod +x /Users/rosalindradcliffe/pythonbob/run_power_on.command
chmod +x /Users/rosalindradcliffe/pythonbob/run_power_off.command
```

### Python Not Found

If the script says Python 3 is not installed:
1. Install Python 3 from https://www.python.org/downloads/
2. Or install via Homebrew: `brew install python3`

### Dependencies Not Installed

The scripts will automatically try to install dependencies, but you can also install them manually:
```bash
cd /Users/rosalindradcliffe/pythonbob
pip3 install -r requirements.txt
```

### Browser Not Opening

If Chrome doesn't open:
1. Make sure Google Chrome is installed
2. Check that the `HEADLESS` setting in `config.py` is set to `False` if you want to see the browser

### Script Runs But Nothing Happens

1. Check that `ProjectorPage.html` exists in the project root
2. Verify the file path in the automation scripts
3. Run with `HEADLESS=False` in config to see what's happening

## Configuration

You can customize the automation behavior by editing `config.py`:

```python
# Show browser window (recommended for desktop use)
HEADLESS = False

# Wait time for elements
IMPLICIT_WAIT = 10

# Save screenshots
SAVE_SCREENSHOTS = True
SCREENSHOT_DIR = "screenshots"
```

## Security Notes

- The `.command` files are shell scripts that run Python code
- They only execute the automation scripts in the project folder
- No external network connections are made (except to load the local HTML file)
- You can review the script contents at any time by opening them in a text editor

## Tips

1. **Keep Terminal Open**: The scripts pause at the end so you can see the results. Press Enter to close.

2. **Create a Dock Icon**: Drag the desktop alias to your Dock for even quicker access.

3. **Keyboard Shortcuts**: You can assign keyboard shortcuts to the Automator applications in System Preferences.

4. **Multiple Monitors**: The automation will use your primary display by default.

5. **Background Running**: If you set `HEADLESS=True` in config, the browser runs invisibly in the background.

## What the Scripts Do

### run_power_on.command
1. Opens a Terminal window
2. Navigates to the project directory
3. Checks for Python 3 installation
4. Installs/verifies dependencies
5. Runs the Power On automation
6. Displays results
7. Waits for you to press Enter before closing

### run_power_off.command
1. Same as Power On, but runs the Power Off automation
2. Automatically handles the confirmation dialog

## Need Help?

If you encounter issues:
1. Check the Terminal output for error messages
2. Review the `examples/PROJECTOR_AUTOMATION_README.md` file
3. Verify all dependencies are installed: `pip3 list`
4. Test the Python scripts directly: `python3 examples/automate_power_on.py`

---

**Made with Bob** - Your automation assistant