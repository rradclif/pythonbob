#!/bin/bash
# Weekly Package Update Check - macOS Desktop Launcher
# Double-click this file to run the update check
# Updated June 2026 - Uses Python 3.12

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project directory
cd "$DIR"

# Use Python 3.12 for security and compatibility
PYTHON_CMD="/usr/local/bin/python3.12"

# Check if Python 3.12 is installed, fallback to python3
if ! command -v "$PYTHON_CMD" &> /dev/null; then
    PYTHON_CMD="python3"
fi

# Clear the screen
clear

# Print header
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         Browser Automation - Weekly Update Check                  ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Using: $($PYTHON_CMD --version)"
echo ""
echo "Running package update and security check..."
echo ""

# Run the update check script
"$PYTHON_CMD" check_updates.py

# Capture the exit code
EXIT_CODE=$?

echo ""
echo "────────────────────────────────────────────────────────────────────"
echo ""

# Provide feedback based on exit code
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ SUCCESS: Your project is secure and up-to-date!"
    echo ""
    echo "No action required. Check again next week."
elif [ $EXIT_CODE -eq 1 ]; then
    echo "⚠️  UPDATES AVAILABLE: Some packages have newer versions."
    echo ""
    echo "Action: Review and update packages when convenient."
    echo ""
    echo "To update all packages, run:"
    echo "  pip install --upgrade -r requirements.txt"
elif [ $EXIT_CODE -eq 2 ]; then
    echo "🚨 CRITICAL: Security vulnerabilities detected!"
    echo ""
    echo "IMMEDIATE ACTION REQUIRED: Update vulnerable packages now!"
    echo ""
    echo "Follow the instructions above to fix security issues."
else
    echo "⚠️  An error occurred during the check."
    echo ""
    echo "Please review the output above for details."
fi

echo ""
echo "────────────────────────────────────────────────────────────────────"
echo ""
echo "📄 Detailed report saved to: package_check_report.json"
echo "📅 Next check recommended: $(date -v+7d '+%Y-%m-%d')"
echo ""
echo "Press any key to close this window..."

# Wait for user input before closing
read -n 1 -s

exit $EXIT_CODE