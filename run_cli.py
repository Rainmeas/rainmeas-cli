#!/usr/bin/env python3
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the CLI
from cli import RainmeasCLI

def main():
    cli = RainmeasCLI()
    exit_code = cli.run(sys.argv[1:])
    sys.exit(exit_code)

if __name__ == "__main__":
    main()