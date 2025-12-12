import json
import os
from typing import Dict, Any, Optional, List

class Registry:
    def __init__(self, registry_path: str = "d:/GITHUB/Rainmeter/Skins/rainmeas-registry"):
        self.registry_path = registry_path
        self.index_file = os.path.join(registry_path, "index.json")
        self.packages_dir = os.path.join(registry_path, "packages")
    
    def load_index(self) -> Dict[str, Any]:
        """Load the registry index file"""
        if not os.path.exists(self.index_file):
            return {}
        
        with open(self.index_file, 'r') as f:
            return json.load(f)
    
    def get_package_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific package"""
        package_file = os.path.join(self.packages_dir, f"{package_name}.json")
        
        if not os.path.exists(package_file):
            return None
        
        with open(package_file, 'r') as f:
            return json.load(f)
    
    def search_packages(self, query: str) -> Dict[str, Any]:
        """Search for packages matching a query"""
        index = self.load_index()
        results = {}
        
        for package_name, package_info in index.items():
            if query.lower() in package_name.lower():
                results[package_name] = package_info
            else:
                # Check package details for matches
                package_details = self.get_package_info(package_name)
                if package_details and (
                    query.lower() in package_details.get("description", "").lower() or
                    query.lower() in package_details.get("author", "").lower()
                ):
                    results[package_name] = package_info
        
        return results
    
    def get_latest_version(self, package_name: str) -> Optional[str]:
        """Get the latest version of a package"""
        package_info = self.get_package_info(package_name)
        
        if not package_info:
            return None
        
        # Get latest version from the package file, not index.json
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
    
    def list_all_packages(self) -> Dict[str, Any]:
        """List all available packages"""
        return self.load_index()