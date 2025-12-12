import sys
import os
from typing import Tuple

# Handle PyInstaller environment
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def parse_version(version: str) -> Tuple[int, ...]:
    """Parse a version string into a tuple of integers"""
    # Remove 'v' prefix if present
    if version.startswith('v'):
        version = version[1:]
    
    # Split by dots and convert to integers
    return tuple(map(int, version.split('.')))

def compare_versions(version1: str, version2: str) -> int:
    """Compare two version strings
    
    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2
    """
    v1_parts = parse_version(version1)
    v2_parts = parse_version(version2)
    
    # Compare each part
    for i in range(min(len(v1_parts), len(v2_parts))):
        if v1_parts[i] < v2_parts[i]:
            return -1
        elif v1_parts[i] > v2_parts[i]:
            return 1
    
    # If we get here, the common parts are equal
    # The longer version is greater
    if len(v1_parts) < len(v2_parts):
        return -1
    elif len(v1_parts) > len(v2_parts):
        return 1
    else:
        return 0

def is_valid_version(version: str) -> bool:
    """Check if a string is a valid version"""
    try:
        parse_version(version)
        return True
    except (ValueError, AttributeError):
        return False