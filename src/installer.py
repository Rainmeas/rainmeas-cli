import os
import json
import shutil
from typing import Dict, Any, Optional
import registry
import utils

class Installer:
    def __init__(self, skin_root: str, registry: registry.Registry):
        self.skin_root = skin_root
        self.registry = registry
        self.modules_dir = os.path.join(skin_root, "@Resources", "@rainmeas-modules")
    
    def install_package(self, package_name: str, version: str = "latest") -> bool:
        """Install a package"""
        # Get package info from registry
        package_info = self.registry.get_package_info(package_name)
        if not package_info:
            print(f"Package '{package_name}' not found in registry")
            return False
        
        # Resolve version
        if version == "latest":
            version = self.registry.get_latest_version(package_name)
            if not version:
                print(f"Could not determine latest version for package '{package_name}'")
                return False
        
        # Check if version exists
        if version not in package_info.get("versions", {}):
            print(f"Version '{version}' not found for package '{package_name}'")
            return False
        
        # Create modules directory if it doesn't exist
        os.makedirs(self.modules_dir, exist_ok=True)
        
        # Download and extract package (placeholder implementation)
        print(f"Installing {package_name}@{version}...")
        # In a real implementation, we would download and extract the package here
        
        # For now, just create a placeholder directory
        package_dir = os.path.join(self.modules_dir, package_name)
        os.makedirs(package_dir, exist_ok=True)
        
        # Create a placeholder file
        placeholder_file = os.path.join(package_dir, "README.md")
        with open(placeholder_file, "w") as f:
            f.write(f"# {package_name}\n\nInstalled version: {version}\n")
        
        # Update rainmeas config
        self._update_config(package_name, version)
        
        print(f"Successfully installed {package_name}@{version}")
        return True
    
    def remove_package(self, package_name: str) -> bool:
        """Remove a package"""
        # Check if package is installed
        installed_packages = self._get_installed_packages()
        if package_name not in installed_packages:
            print(f"Package '{package_name}' is not installed")
            return False
        
        # Remove package directory
        package_dir = os.path.join(self.modules_dir, package_name)
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
            print(f"Removed package directory: {package_dir}")
        
        # Update rainmeas config
        self._remove_from_config(package_name)
        
        print(f"Successfully removed {package_name}")
        return True
    
    def _get_installed_packages(self) -> Dict[str, str]:
        """Get installed packages from config"""
        config = utils.load_rainmeas_config(self.skin_root)
        return config.get("packages", {})
    
    def _update_config(self, package_name: str, version: str) -> None:
        """Update rainmeas config with installed package"""
        config = utils.load_rainmeas_config(self.skin_root)
        
        if "packages" not in config:
            config["packages"] = {}
        
        config["packages"][package_name] = version
        
        utils.save_rainmeas_config(self.skin_root, config)
    
    def _remove_from_config(self, package_name: str) -> None:
        """Remove package from rainmeas config"""
        config = utils.load_rainmeas_config(self.skin_root)
        
        if "packages" in config and package_name in config["packages"]:
            del config["packages"][package_name]
        
        utils.save_rainmeas_config(self.skin_root, config)
    
    def list_installed_packages(self) -> Dict[str, str]:
        """List all installed packages"""
        return self._get_installed_packages()