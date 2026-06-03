# Weekly Package Update Check Guide

This guide explains how to use the automated package update checker to keep your project secure.

## Quick Start

Run the update checker script:

```bash
python3 check_updates.py
```

Or make it executable and run directly:

```bash
chmod +x check_updates.py
./check_updates.py
```

## What It Checks

The script performs the following checks:

1. **Pip Version** - Ensures pip itself is up-to-date
2. **Requirements File** - Verifies requirements.txt exists and is readable
3. **Outdated Packages** - Lists all packages with newer versions available
4. **Security Vulnerabilities** - Scans for known CVEs using pip-audit
5. **Module Imports** - Tests that core modules can be imported successfully

## Understanding the Output

### Exit Codes

The script returns different exit codes based on findings:

- **0** - All good! No updates or vulnerabilities
- **1** - Package updates available (non-critical)
- **2** - Security vulnerabilities detected (CRITICAL)

### Status Indicators

- ✓ - Success/OK
- ⚠️ - Warning/Updates available
- 🚨 - Critical security issue
- ✗ - Error

## Recommended Schedule

### Weekly Check (Recommended)
```bash
# Run every Monday morning
python3 check_updates.py
```

### After Major Updates
```bash
# After updating packages
python3 check_updates.py
```

### Before Deployment
```bash
# Always check before deploying
python3 check_updates.py
```

## Automation Options

### Option 1: Cron Job (macOS/Linux)

Add to your crontab (`crontab -e`):

```bash
# Run every Monday at 9 AM
0 9 * * 1 cd /Users/rosalindradcliffe/pythonbob && /usr/local/bin/python3 check_updates.py >> update_check.log 2>&1
```

### Option 2: macOS Launch Agent

Create `~/Library/LaunchAgents/com.pythonbob.updatecheck.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.pythonbob.updatecheck</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/rosalindradcliffe/pythonbob/check_updates.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/rosalindradcliffe/pythonbob/update_check.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/rosalindradcliffe/pythonbob/update_check_error.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.pythonbob.updatecheck.plist
```

### Option 3: Manual Reminder

Set a calendar reminder for every Monday to run the check manually.

## Responding to Findings

### If Security Vulnerabilities Found (🚨)

**IMMEDIATE ACTION REQUIRED:**

1. Review the vulnerability details
2. Update affected packages immediately:
   ```bash
   pip install --upgrade <vulnerable-package>
   ```
3. Test your application
4. Run the check again to verify fix

### If Package Updates Available (⚠️)

**Action within 1-2 weeks:**

1. Review the outdated packages list
2. Check changelogs for breaking changes
3. Update packages:
   ```bash
   # Update all
   pip install --upgrade -r requirements.txt
   
   # Or update specific packages
   pip install --upgrade selenium python-dotenv
   ```
4. Test your application thoroughly
5. Update requirements.txt if needed
6. Run the check again to verify

### If All Clear (✓)

**No action needed:**

- Your project is secure and up-to-date
- Check again next week
- Continue normal development

## Output Files

The script generates:

### package_check_report.json
Detailed JSON report with:
- Timestamp
- List of outdated packages
- Security vulnerabilities
- Pip version information

Example:
```json
{
  "timestamp": "2026-03-10T09:22:38.123456",
  "outdated_packages": [...],
  "vulnerabilities": [],
  "pip_version": "pip 26.0.1"
}
```

## Prerequisites

### Required
- Python 3.7+
- pip (latest version recommended)

### Optional but Recommended
- pip-audit (for security scanning)
  ```bash
  pip install pip-audit
  ```

## Troubleshooting

### "pip-audit not found"
Install pip-audit:
```bash
pip install pip-audit
```

### "Permission denied"
Make the script executable:
```bash
chmod +x check_updates.py
```

### "Module not found"
Ensure you're in the project directory:
```bash
cd /Users/rosalindradcliffe/pythonbob
python3 check_updates.py
```

## Integration with CI/CD

Add to your CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Check for vulnerabilities
  run: |
    pip install pip-audit
    python3 check_updates.py
  continue-on-error: false
```

## Best Practices

1. **Run weekly** - Set a recurring reminder
2. **Act on vulnerabilities immediately** - Don't delay security updates
3. **Test after updates** - Always verify functionality
4. **Keep pip updated** - Update pip itself regularly
5. **Review changelogs** - Check for breaking changes before updating
6. **Document updates** - Keep PACKAGE_UPDATES.md current
7. **Backup before major updates** - Commit changes before updating

## Quick Reference Commands

```bash
# Run the check
python3 check_updates.py

# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade <package-name>

# Check for vulnerabilities only
pip-audit

# List outdated packages
pip list --outdated

# Update pip itself
pip install --upgrade pip
```

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the script output for error messages
3. Ensure all prerequisites are installed
4. Check that you're in the correct directory

---

**Remember**: Security is not a one-time task. Regular checks keep your project safe!

**Next check recommended**: Run weekly, every Monday