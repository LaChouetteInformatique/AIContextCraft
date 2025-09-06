#!/usr/bin/env python3
"""
Clipboard utility for AI Context Craft - Docker version
Simplified for Docker environment (Linux only)
"""

import subprocess
from pathlib import Path
from typing import Optional

class ClipboardManager:
    """Manages clipboard operations in Docker environment"""
    
    def __init__(self):
        # In Docker, we're always on Linux with xclip pre-installed
        self.clipboard_available = self._check_xclip_availability()
    
    def _check_xclip_availability(self) -> bool:
        """Checks if xclip is available"""
        try:
            # Check if xclip exists
            subprocess.run(["which", "xclip"], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def copy_to_clipboard(self, text: str) -> bool:
        """
        Copies text to the system clipboard
        
        Returns:
            True if successful, False otherwise
        """
        if not self.clipboard_available:
            return False
        
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], 
                         input=text.encode(), check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def copy_file_to_clipboard(self, file_path: Path) -> bool:
        """
        Copies the content of a file to clipboard
        
        Args:
            file_path: Path to the file to copy
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.copy_to_clipboard(content)
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    
    def get_clipboard_info(self) -> str:
        """Returns information about clipboard availability"""
        if self.clipboard_available:
            return "Using xclip (Docker environment)"
        else:
            return "xclip not available in container"
    
    def test_clipboard(self) -> bool:
        """Tests if clipboard is working"""
        test_string = "AI Context Craft clipboard test"
        
        if not self.clipboard_available:
            print(f"❌ Clipboard not available: {self.get_clipboard_info()}")
            return False
        
        try:
            if self.copy_to_clipboard(test_string):
                print(f"✅ Clipboard is working! ({self.get_clipboard_info()})")
                return True
            else:
                print("❌ Clipboard copy failed")
                return False
        except Exception as e:
            print(f"❌ Clipboard test error: {e}")
            return False

# Utility function for testing
if __name__ == "__main__":
    clipboard = ClipboardManager()
    
    print(f"Available: {clipboard.clipboard_available}")
    print(f"Info: {clipboard.get_clipboard_info()}")
    
    if clipboard.clipboard_available:
        print("\nTesting clipboard...")
        clipboard.test_clipboard()