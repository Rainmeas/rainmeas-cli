# Build script for rainmeas CLI tool
# This script creates a standalone executable using PyInstaller

# Define paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AssetsDir = Join-Path $ScriptDir "assets"
$SrcDir = Join-Path $ScriptDir "src"
$OutputDir = Join-Path $ScriptDir "dist"
$IconPath = Join-Path $AssetsDir "icon.ico"
$EntryPoint = Join-Path $ScriptDir "run_cli.py"

# Check if required files exist
if (-not (Test-Path $EntryPoint)) {
    Write-Error "Entry point script not found: $EntryPoint"
    exit 1
}

if (-not (Test-Path $IconPath)) {
    Write-Error "Icon file not found: $IconPath"
    exit 1
}

# Create output directory if it doesn't exist
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

# Check if PyInstaller is installed
try {
    $pyinstallerVersion = & pip show pyinstaller | Select-String "Version"
    if ($null -eq $pyinstallerVersion) {
        throw "PyInstaller not found"
    }
    Write-Host "Found PyInstaller: $pyinstallerVersion"
} catch {
    Write-Host "PyInstaller not found. Installing..."
    & pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install PyInstaller"
        exit 1
    }
}

# Build the executable with proper module inclusion
Write-Host "Building rainmeas executable..."
& pyinstaller --onefile --console --icon="$IconPath" --name="rainmeas" --distpath="$OutputDir" --workpath="$ScriptDir\build" --specpath="$ScriptDir" --add-data="$SrcDir;src" --add-data="$AssetsDir;assets" "$EntryPoint"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build executable"
    exit 1
}

Write-Host "Build successful!"
Write-Host "Executable location: $(Join-Path $OutputDir "rainmeas.exe")"