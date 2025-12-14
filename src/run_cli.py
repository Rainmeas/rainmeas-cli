#!/usr/bin/env python3
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Add the src directory to the Python path
# Handle both development and PyInstaller environments
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    src_path = resource_path('src')
else:
    # Running as script
    src_path = os.path.join(os.path.dirname(__file__), 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import and run the CLI
from cli import RainmeasCLI

def main():
    cli = RainmeasCLI()
    exit_code = cli.run(sys.argv[1:])
    sys.exit(exit_code)

if __name__ == "__main__":
    main()