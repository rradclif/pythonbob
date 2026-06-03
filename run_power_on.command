#!/bin/bash
# Projector Power On Automation Launcher
# This script can be double-clicked from the Mac desktop to run the automation
# Updated June 2026 - Uses Python 3.12

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Use Python 3.12 for security and compatibility
PYTHON_CMD="/usr/local/bin/python3.12"

# Display banner
echo "=================================================="
echo "  Projector Power On Automation"
echo "=================================================="
echo ""

# Check if Python 3.12 is installed
if ! command -v "$PYTHON_CMD" &> /dev/null; then
    echo "ERROR: Python 3.12 is not installed at $PYTHON_CMD"
    echo "Falling back to system python3..."
    PYTHON_CMD="python3"
    if ! command -v "$PYTHON_CMD" &> /dev/null; then
        echo "ERROR: Python 3 is not installed."
        echo "Please install Python 3.12+ from https://www.python.org/"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Display Python version
echo "Using: $($PYTHON_CMD --version)"
echo ""

# Check if virtual environment exists, if not check for requirements
if [ ! -d "venv" ]; then
    echo "Note: No virtual environment found."
    echo "Installing/checking requirements..."
    "$PYTHON_CMD" -m pip install -r requirements.txt --quiet --user
    echo ""
fi

# Run the automation
echo "Starting Power On automation..."
echo ""
"$PYTHON_CMD" examples/automate_power_on.py

# Keep terminal open to see results
echo ""
echo "=================================================="
echo "Automation complete!"
echo "=================================================="
echo ""
read -p "Press Enter to close this window..."