#!/usr/bin/env python3
"""
Dependency manager for optional features in AI Context Craft
Handles installation prompts and remembers user preferences
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

class DependencyManager:
    """Manages optional dependencies with user preferences"""
    
    def __init__(self, config_manager=None):
        self.config_manager = config_manager
        self.config_file = Path("config.yaml")
        self.preferences = self._load_preferences()
        if self.preferences is None:
            self.preferences = {}
        
    def _load_preferences(self) -> Dict[str, Any]:
        """Load dependency preferences from config"""
        if self.config_manager:
            prefs = self.config_manager.get('dependencies', {})
            return prefs if prefs is not None else {}
        
        # Fallback: try to load directly
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = yaml.safe_load(f) or {}
                    prefs = config.get('dependencies', {})
                    return prefs if prefs is not None else {}
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
        
        return {}
    
    def _save_preference(self, key: str, value: Any) -> bool:
        """Save a preference to the config file"""
        try:
            # Load existing config
            config = {}
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = yaml.safe_load(f) or {}
            
            # Initialize dependencies section if not exists
            if 'dependencies' not in config:
                config['dependencies'] = {}
            
            # Update the preference
            config['dependencies'][key] = value
            
            # Save back to file
            with open(self.config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            # Update local cache
            if self.preferences is None:
                self.preferences = {}
            self.preferences[key] = value
            
            return True
        except Exception as e:
            print(f"⚠️  Could not save preference: {e}")
            return False
    
    def _check_package_installed(self, package_name: str) -> bool:
        """Check if a Python package is installed"""
        try:
            __import__(package_name)
            return True
        except ImportError:
            return False
    
    def _install_package(self, package_name: str) -> bool:
        """Install a Python package using pip"""
        try:
            print(f"📦 Installing {package_name}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ {package_name} installed successfully!")
                return True
            else:
                print(f"❌ Failed to install {package_name}")
                if result.stderr:
                    print(f"   Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False
    
    def _prompt_user(self, package_name: str, description: str) -> str:
        """Prompt user for installation preference"""
        print(f"\n{'='*60}")
        print(f"📦 Optional dependency: {package_name}")
        print(f"   {description}")
        print(f"{'='*60}")
        print("\nOptions:")
        print("  y - Install now")
        print("  n - Don't install")
        print("  a - Always install automatically (save preference)")
        print("  s - Never install automatically (save preference)")
        
        while True:
            choice = input("\nYour choice [y/n/a/s]: ").lower().strip()
            if choice in ['y', 'n', 'a', 's']:
                return choice
            print("Invalid choice. Please enter y, n, a, or s.")
    
    def check_tiktoken(self) -> bool:
        """
        Check and optionally install tiktoken for precise token counting
        
        Returns:
            True if tiktoken is available, False otherwise
        """
        # Check if already installed
        if self._check_package_installed('tiktoken'):
            return True
        
        # Check auto-install preference
        auto_install = self.preferences.get('auto_install_tiktoken', False)
        never_install = self.preferences.get('never_install_tiktoken', False)
        
        if never_install:
            return False
        
        if auto_install:
            print("📦 Auto-installing tiktoken (as per your preference)...")
            return self._install_package('tiktoken')
        
        # Check if we should prompt
        if self.preferences.get('silent_mode', False):
            return False
        
        # Prompt user
        choice = self._prompt_user(
            'tiktoken',
            'Provides precise token counting for OpenAI models.\n' +
            '   This will give you exact token counts instead of estimates.'
        )
        
        if choice == 'y':
            return self._install_package('tiktoken')
        elif choice == 'a':
            self._save_preference('auto_install_tiktoken', True)
            return self._install_package('tiktoken')
        elif choice == 's':
            self._save_preference('never_install_tiktoken', True)
            print("📝 Preference saved: tiktoken will not be installed automatically.")
            return False
        else:  # 'n'
            return False
    
    def check_clipboard_tools(self) -> bool:
        """
        Check and optionally install clipboard tools (Linux only)
        
        Returns:
            True if clipboard tools are available, False otherwise
        """
        import platform
        
        # Only relevant for Linux
        if platform.system() != "Linux":
            return True
        
        # Check if xclip or xsel is already installed
        has_xclip = self._command_exists('xclip')
        has_xsel = self._command_exists('xsel')
        
        if has_xclip or has_xsel:
            return True
        
        # Check if we're in SSH (no display)
        if not os.environ.get('DISPLAY'):
            return False
        
        # Check auto-install preference
        auto_install = self.preferences.get('auto_install_clipboard', False)
        never_install = self.preferences.get('never_install_clipboard', False)
        
        if never_install:
            print("📋 Clipboard tools installation skipped (as per your preference)")
            return False
        
        if auto_install:
            print("📋 Auto-installing clipboard support (as per your preference)...")
            return self._install_system_package('xclip')
        
        # Check if we should prompt
        if self.preferences.get('silent_mode', False):
            return False
        
        # Prompt user
        choice = self._prompt_user(
            'xclip',
            'Enables clipboard support on Linux.\n' +
            '   This allows copying output directly to clipboard.'
        )
        
        if choice == 'y':
            return self._install_system_package('xclip')
        elif choice == 'a':
            self._save_preference('auto_install_clipboard', True)
            return self._install_system_package('xclip')
        elif choice == 's':
            success = self._save_preference('never_install_clipboard', True)
            if success:
                print("📝 Preference saved: clipboard tools will not be installed automatically.")
            return False
        else:  # 'n'
            return False
    
    def _command_exists(self, command: str) -> bool:
        """Check if a system command exists"""
        try:
            subprocess.run(["which", command], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _detect_package_manager(self) -> Optional[str]:
        """Detect the Linux package manager"""
        for pm in ['apt-get', 'dnf', 'yum', 'pacman', 'zypper']:
            if self._command_exists(pm):
                return pm
        return None
    
    def _install_system_package(self, package: str) -> bool:
        """Install a system package using the detected package manager"""
        pm = self._detect_package_manager()
        if not pm:
            print("❌ Could not detect package manager")
            return False
        
        install_commands = {
            'apt-get': ['sudo', 'apt-get', 'install', '-y', package],
            'dnf': ['sudo', 'dnf', 'install', '-y', package],
            'yum': ['sudo', 'yum', 'install', '-y', package],
            'pacman': ['sudo', 'pacman', '-S', '--noconfirm', package],
            'zypper': ['sudo', 'zypper', 'install', '-y', package]
        }
        
        if pm not in install_commands:
            return False
        
        try:
            print(f"📦 Installing {package} using {pm}...")
            print("   Note: This requires sudo password")
            
            result = subprocess.run(
                install_commands[pm],
                capture_output=False,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully!")
                return True
            else:
                print(f"❌ Installation failed")
                return False
                
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False
    
    def reset_preferences(self):
        """Reset all dependency preferences"""
        try:
            config = {}
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = yaml.safe_load(f) or {}
            
            # Remove dependencies section
            if 'dependencies' in config:
                del config['dependencies']
            
            with open(self.config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            self.preferences = {}
            print("✅ Dependency preferences reset")
            return True
            
        except Exception as e:
            print(f"❌ Could not reset preferences: {e}")
            return False
    
    def show_preferences(self):
        """Display current dependency preferences"""
        print("\n📦 Current Dependency Preferences:")
        print("="*50)
        
        if not self.preferences:
            print("No preferences set yet.")
        else:
            for key, value in self.preferences.items():
                readable_key = key.replace('_', ' ').title()
                print(f"  {readable_key}: {value}")
        
        print("="*50)
        print("\nTo reset preferences, run:")
        print("  python3 -c \"from utils.dependency_manager import DependencyManager; DependencyManager().reset_preferences()\"")


# Utility function for standalone testing
if __name__ == "__main__":
    manager = DependencyManager()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "reset":
            manager.reset_preferences()
        elif sys.argv[1] == "show":
            manager.show_preferences()
        elif sys.argv[1] == "test-tiktoken":
            result = manager.check_tiktoken()
            print(f"\nTiktoken available: {result}")
        elif sys.argv[1] == "test-clipboard":
            result = manager.check_clipboard_tools()
            print(f"\nClipboard tools available: {result}")
    else:
        print("Dependency Manager Test")
        print("-" * 30)
        manager.show_preferences()
        print("\nUsage:")
        print("  python3 utils/dependency_manager.py show          # Show preferences")
        print("  python3 utils/dependency_manager.py reset         # Reset preferences")
        print("  python3 utils/dependency_manager.py test-tiktoken # Test tiktoken")
        print("  python3 utils/dependency_manager.py test-clipboard # Test clipboard")