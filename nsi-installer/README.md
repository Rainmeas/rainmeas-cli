# NSIS Installer for Rainmeas

This directory contains the NSIS (Nullsoft Scriptable Install System) installer script and assets for Rainmeas.

## Files

- `setup.nsi` - The main NSIS installer script
- `assets/` - Directory containing installer assets:
  - `installer.ico` - Installer icon
  - `uninstall.ico` - Uninstaller icon
  - `header.bmp` - Header image for installer pages
  - `Untitled design.bmp` - Additional design asset

## Building the Installer

To build the installer, you need to have NSIS installed on your system. You can download it from [NSIS Official Website](https://nsis.sourceforge.io/Download).

After installing NSIS, you can build the installer by running:

```cmd
makensis setup.nsi
```

Or simply run the main Build.ps1 script in the parent directory, which will automatically build both the executable and the installer if NSIS is detected.

## Installer Features

The installer includes:
- Main application files
- Option to add Rainmeas to system PATH
- Option to create a desktop shortcut
- Standard Windows uninstaller
- Registry entries for Add/Remove Programs