import os
import json
import shutil
import sys
import urllib.request
import zipfile
import tempfile
from typing import Dict, Any, Optional

# Handle PyInstaller environment
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Dynamic imports to handle PyInstaller
def import_modules():
    """Dynamically import modules to handle PyInstaller bundling"""
    try:
        import registry
        import utils
        return registry, utils
    except ImportError:
        # Try alternative import paths for PyInstaller
        sys.path.append(resource_path('src'))
        import registry
        import utils
        return registry, utils

# Import modules
try:
    registry, utils = import_modules()
except Exception as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

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
        available_versions = self.registry.get_available_versions(package_name)
        if version not in available_versions:
            print(f"Version '{version}' not found for package '{package_name}'")
            print(f"Available versions: {', '.join(available_versions)}")
            return False
        
        # Get download URL
        download_url = self.registry.get_version_download_url(package_name, version)
        if not download_url:
            print(f"No download URL found for {package_name}@{version}")
            return False
        
        # Create modules directory if it doesn't exist
        os.makedirs(self.modules_dir, exist_ok=True)
        
        # Download and extract package
        print(f"Installing {package_name}@{version}...")
        print(f"Download URL: {download_url}")
        
        # Create a temporary file for the downloaded ZIP
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
            tmp_filename = tmp_file.name
        
        try:
            # Download the ZIP file
            print("Downloading package...")
            urllib.request.urlretrieve(download_url, tmp_filename)
            
            # Extract the ZIP file to the package directory
            print("Extracting package...")
            package_dir = os.path.join(self.modules_dir, package_name)
            
            # Remove existing package directory if it exists
            if os.path.exists(package_dir):
                shutil.rmtree(package_dir)
            
            # Extract ZIP file
            with zipfile.ZipFile(tmp_filename, 'r') as zip_ref:
                zip_ref.extractall(package_dir)
            
            # Clean up temporary file
            os.unlink(tmp_filename)
            
            print("Package downloaded and extracted successfully")
            
        except Exception as e:
            # Clean up temporary file if it exists
            if 'tmp_filename' in locals() and os.path.exists(tmp_filename):
                os.unlink(tmp_filename)
            
            print(f"Error downloading or extracting package: {e}")
            return False
        
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