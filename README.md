# Rainmeas CLI

Rainmeas is a package manager for Rainmeter skins that simplifies the installation, updating, and management of skin modules.

## Installation

### Using the Installer (Recommended)

Download the latest installer (`rainmeas-setup.exe`) from the releases page and run it to install Rainmeas with automatic PATH integration.

### Manual Installation

To install Rainmeas manually, run:

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

## Usage

Initialize Rainmeas in a Rainmeter skin directory:

```bash
rainmeas init
```

### Commands

- `init` - Initialize Rainmeas in a Rainmeter skin
- `install <package>` - Install a package
- `install <package>@<version>` - Install a specific version of a package
- `remove <package>` - Remove a package
- `update` - Update all packages
- `update <package>` - Update a specific package
- `list` - List installed packages
- `search <query>` - Search for packages
- `info <package>` - Show package information
- `verify` - Verify package integrity
- `clean` - Clean unused modules
- `version` - Show CLI version
- `help` - Show help

### Examples

```bash
# Install a package
rainmeas install freshweather

# Install a specific version
rainmeas install freshweather@1.3.0

# List installed packages
rainmeas list

# Search for packages
rainmeas search weather
```

## Building from Source

### Prerequisites

- Python 3.6 or higher
- PyInstaller (automatically installed if missing)
- NSIS (optional, for creating installer)

### Build Process

To build the executable and installer:

```bash
# On Windows
powershell -ExecutionPolicy Bypass -File Build.ps1
```

This will:
1. Create a standalone executable using PyInstaller
2. Build an NSIS installer (if NSIS is installed)

If NSIS is not installed, only the executable will be created. You can install NSIS from [NSIS Official Website](https://nsis.sourceforge.io/Download).

### Manual Build Steps

1. Build the executable:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --console --icon="assets/icon.ico" --name="rainmeas" --distpath="dist" run_cli.py
   ```

2. Build the installer (requires NSIS):
   ```bash
   # If NSIS is in your PATH
   makensis nsi-installer/setup.nsi
   
   # Or use the full path (common locations)
   "C:\Program Files (x86)\NSIS\makensis.exe" nsi-installer/setup.nsi
   "C:\Program Files\NSIS\makensis.exe" nsi-installer/setup.nsi
   ```

### Testing the Build

You can verify that the build process works correctly by running:

```bash
# Test the executable
dist\rainmeas.exe --version

# Test the installer build (if NSIS is installed)
powershell -ExecutionPolicy Bypass -File TestInstallerBuild.ps1

# Check the final installer
powershell -ExecutionPolicy Bypass -File TestInstaller.ps1
```

## Registry

Rainmeas uses the [rainmeas-registry](https://github.com/Rainmeas/rainmeas-registry) for package information.