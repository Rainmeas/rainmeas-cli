import json
import os
import sys
from typing import Dict, Any, Optional, List

# Handle PyInstaller environment
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Registry:
    def __init__(self, registry_path: str = "d:/GITHUB/Rainmeter/Skins/rainmeas-registry"):
        self.registry_path = registry_path
        self.packages_dir = os.path.join(registry_path, "packages")
    
    def list_all_package_names(self) -> List[str]:
        """List all package names by scanning the packages directory"""
        if not os.path.exists(self.packages_dir):
            return []
        
        package_names = []
        for filename in os.listdir(self.packages_dir):
            if filename.endswith(".json"):
                package_names.append(filename[:-5])  # Remove .json extension
        
        return package_names
    
    def get_package_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific package"""
        package_file = os.path.join(self.packages_dir, f"{package_name}.json")
        
        if not os.path.exists(package_file):
            return None
        
        with open(package_file, 'r') as f:
            return json.load(f)
    
    def search_packages(self, query: str) -> Dict[str, Any]:
        """Search for packages matching a query"""
        results = {}
        
        # Scan all package files directly
        for package_name in self.list_all_package_names():
            package_info = self.get_package_info(package_name)
            if not package_info:
                continue
            
            # Match by package name
            if query.lower() in package_name.lower():
                # Create a simplified info object for search results
                latest_version = self.get_latest_version(package_name)
                versions = self.get_available_versions(package_name)
                results[package_name] = {
                    "latest": latest_version or "unknown",
                    "versions": versions
                }
            else:
                # Match by package details
                if (query.lower() in package_info.get("description", "").lower() or
                    query.lower() in package_info.get("author", "").lower()):
                    # Create a simplified info object for search results
                    latest_version = self.get_latest_version(package_name)
                    versions = self.get_available_versions(package_name)
                    results[package_name] = {
                        "latest": latest_version or "unknown",
                        "versions": versions
                    }
        
        return results
    
    def get_latest_version(self, package_name: str) -> Optional[str]:
        """Get the latest version of a package"""
        package_info = self.get_package_info(package_name)
        
        if not package_info:
            return None
        
        # Get latest version from the package file
        versions = package_info.get("versions", {})
        if "latest" in versions:
            return versions["latest"]
        
        # If no explicit "latest" key, return the highest version
        version_keys = [k for k in versions.keys() if k != "latest"]
        if version_keys:
            # Simple version sorting (in a real implementation, you'd want proper semver sorting)
            return sorted(version_keys)[-1]
        
        return None
    
    def get_available_versions(self, package_name: str) -> List[str]:
        """Get all available versions of a package"""
        package_info = self.get_package_info(package_name)
        
        if not package_info:
            return []
        
        versions = package_info.get("versions", {})
        # Return all version keys except "latest"
        return [k for k in versions.keys() if k != "latest"]
    
    def get_version_download_url(self, package_name: str, version: str) -> Optional[str]:
        """Get the download URL for a specific package version"""
        package_info = self.get_package_info(package_name)
        
        if not package_info:
            return None
        
        versions = package_info.get("versions", {})
        if version in versions and isinstance(versions[version], dict):
            return versions[version].get("download")
        
        return None