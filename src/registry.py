import json
import os
from typing import Dict, Any, Optional

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
        index = self.load_index()
        package_info = index.get(package_name)
        
        if not package_info:
            return None
        
        return package_info.get("latest")
    
    def list_all_packages(self) -> Dict[str, Any]:
        """List all available packages"""
        return self.load_index()