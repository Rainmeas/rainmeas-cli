# Rainmeas CLI

Rainmeas is a package manager for Rainmeter skins that simplifies the installation, updating, and management of skin modules.

## Installation

To install Rainmeas, run:

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

## Registry

Rainmeas uses the [rainmeas-registry](https://github.com/Rainmeas/rainmeas-registry) for package information.