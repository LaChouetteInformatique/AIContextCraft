#!/usr/bin/env python3
"""
Clipboard utility for AI Context Craft
Cross-platform clipboard support with auto-detection
"""

import subprocess
import sys
import platform
import os
from pathlib import Path
from typing import Optional

class ClipboardManager:
    """Manages clipboard operations across different platforms"""
    
    def __init__(self, auto_install=False):
        self.system = platform.system()
        self.clipboard_available = self._check_clipboard_availability()
        self.auto_install = auto_install
        
        # Try to auto-install if requested and not available
        if not self.clipboard_available and self.auto_install and self.system == "Linux":
            self._try_auto_install()
            # Re-check availability after installation attempt
            self.clipboard_available = self._check_clipboard_availability()
    
    def _check_clipboard_availability(self) -> bool:
        """Checks if clipboard tools are available"""
        if self.system == "Darwin":  # macOS
            return self._command_exists("pbcopy")
        elif self.system == "Linux":
            # Also check if we're in SSH or headless environment
            if not os.environ.get('DISPLAY'):
                return False  # No X11 display available
            return self._command_exists("xclip") or self._command_exists("xsel")
        elif self.system == "Windows":
            return True  # Windows has built-in clip command
        return False
    
    def _command_exists(self, command: str) -> bool:
        """Checks if a command exists in the system"""
        try:
            subprocess.run(["which", command], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _detect_package_manager(self) -> Optional[str]:
        """Detects the Linux package manager"""
        package_managers = {
            'apt-get': ['ubuntu', 'debian', 'mint'],
            'dnf': ['fedora', 'rhel', 'centos'],
            'yum': ['rhel', 'centos'],
            'pacman': ['arch', 'manjaro'],
            'zypper': ['opensuse', 'suse']
        }
        
        # Check which package manager is available
        for pm in ['apt-get', 'dnf', 'yum', 'pacman', 'zypper']:
            if self._command_exists(pm):
                return pm
        
        # Try to detect from /etc/os-release
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                for pm, distros in package_managers.items():
                    if any(distro in content for distro in distros):
                        if self._command_exists(pm):
                            return pm
        except:
            pass
        
        return None
    
    def _try_auto_install(self):
        """Attempts to automatically install clipboard support"""
        print("📋 Clipboard support not found. Attempting to install...")
        
        pm = self._detect_package_manager()
        if not pm:
            print("❌ Could not detect package manager")
            return False
        
        install_commands = {
            'apt-get': ['sudo', 'apt-get', 'install', '-y', 'xclip'],
            'dnf': ['sudo', 'dnf', 'install', '-y', 'xclip'],
            'yum': ['sudo', 'yum', 'install', '-y', 'xclip'],
            'pacman': ['sudo', 'pacman', '-S', '--noconfirm', 'xclip'],
            'zypper': ['sudo', 'zypper', 'install', '-y', 'xclip']
        }
        
        if pm not in install_commands:
            return False
        
        try:
            # Check if we have sudo rights
            if os.geteuid() != 0:  # Not root
                print(f"📦 Installing xclip using {pm}...")
                print("   Note: This requires sudo password")
            
            result = subprocess.run(
                install_commands[pm],
                capture_output=False,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ xclip installed successfully!")
                return True
            else:
                print("❌ Installation failed")
                return False
                
        except Exception as e:
            print(f"❌ Installation error: {e}")
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
            if self.system == "Darwin":  # macOS
                subprocess.run(["pbcopy"], input=text.encode(), check=True)
            elif self.system == "Linux":
                # Check for SSH/headless environment
                if not os.environ.get('DISPLAY'):
                    return False
                    
                if self._command_exists("xclip"):
                    subprocess.run(["xclip", "-selection", "clipboard"], 
                                 input=text.encode(), check=True)
                elif self._command_exists("xsel"):
                    subprocess.run(["xsel", "--clipboard", "--input"], 
                                 input=text.encode(), check=True)
            elif self.system == "Windows":
                subprocess.run(["clip"], input=text.encode(), check=True, shell=True)
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
        if not self.clipboard_available:
            # Check if we're in SSH
            if self.system == "Linux" and not os.environ.get('DISPLAY'):
                return "No X11 display (SSH session or headless environment)"
            
            if self.system == "Linux":
                pm = self._detect_package_manager()
                if pm == 'apt-get':
                    return "Install xclip or xsel: sudo apt-get install xclip"
                elif pm == 'dnf':
                    return "Install xclip: sudo dnf install xclip"
                elif pm == 'yum':
                    return "Install xclip: sudo yum install xclip"
                elif pm == 'pacman':
                    return "Install xclip: sudo pacman -S xclip"
                elif pm == 'zypper':
                    return "Install xclip: sudo zypper install xclip"
                else:
                    return "Install xclip or xsel using your package manager"
            return f"Clipboard not available on {self.system}"
        
        if self.system == "Darwin":
            return "Using pbcopy (macOS)"
        elif self.system == "Linux":
            if self._command_exists("xclip"):
                return "Using xclip"
            elif self._command_exists("xsel"):
                return "Using xsel"
        elif self.system == "Windows":
            return "Using clip (Windows)"
        
        return "Clipboard status unknown"
    
    def test_clipboard(self) -> bool:
        """Tests if clipboard is working by copying and verifying a test string"""
        test_string = "AI Context Craft clipboard test"
        
        if not self.clipboard_available:
            print(f"❌ Clipboard not available: {self.get_clipboard_info()}")
            return False
        
        try:
            # Try to copy
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
    # Test the clipboard
    clipboard = ClipboardManager(auto_install=False)  # Set to True to attempt auto-install
    
    print(f"System: {clipboard.system}")
    print(f"Available: {clipboard.clipboard_available}")
    print(f"Info: {clipboard.get_clipboard_info()}")
    
    if clipboard.clipboard_available:
        print("\nTesting clipboard...")
        clipboard.test_clipboard()
    else:
        print("\n💡 To enable clipboard support:")
        print(f"   {clipboard.get_clipboard_info()}")