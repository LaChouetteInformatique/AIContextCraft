"""Configuration manager for AI Context Craft"""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """Manages the project configuration"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.config_format = self._detect_format()
    
    def _load_config(self) -> Dict[str, Any]:
        """Loads the configuration from the YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
                return config
        except FileNotFoundError:
            print(f"⚠️ Configuration file '{self.config_path}' not found. Using default values.")
            return self._get_default_config()
        except yaml.YAMLError as e:
            print(f"❌ Error loading the configuration: {e}")
            return self._get_default_config()
    
    def _detect_format(self) -> str:
        """Detects the configuration format (legacy or advanced)"""
        # Check for the presence of any advanced section
        advanced_sections = ['concat_project_files', 'tree_project_files', 'custom_tree_files']
        if any(section in self.config for section in advanced_sections):
            return 'advanced'
        return 'legacy'
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Returns a default configuration"""
        return {
            'include_extensions': ['.py', '.js', '.jsx', '.ts', '.tsx', '.md', '.yaml', '.yml', '.json'],
            'exclude_dirs': ['node_modules', '__pycache__', '.git', 'build', 'dist', '.venv', 'venv'],
            'exclude_files': ['.env', '.env.local', 'package-lock.json', 'yarn.lock']
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a configuration value"""
        return self.config.get(key, default)
    
    def get_concat_config(self) -> Dict:
        """Returns the configuration for concatenation"""
        if self.config_format == 'advanced':
            return self.config.get('concat_project_files', {})
        else:
            # Convert legacy config to advanced format
            return {
                'mode': 'include',
                'include': [f"**/*{ext}" for ext in self.config.get('include_extensions', [])],
                'exclude': [f"{dir}/**" for dir in self.config.get('exclude_dirs', [])]
            }
    
    def get_tree_config(self, mode: str = 'normal') -> Dict:
        """
        Returns the configuration for the tree according to the mode
        
        Args:
            mode: Tree mode ('normal', 'full', 'custom')
        """
        if mode == 'normal':
            return self.get_concat_config()
        elif mode == 'full' and 'tree_project_files' in self.config:
            return self.config.get('tree_project_files', {})
        elif mode == 'custom' and 'custom_tree_files' in self.config:
            return self.config.get('custom_tree_files', {})
        else:
            # Fallback to concat config
            return self.get_concat_config()
    
    def is_advanced_format(self) -> bool:
        """Checks if the configuration uses the advanced format"""
        return self.config_format == 'advanced'
    
    def set_mode(self, mode: str):
        """Forces the filtering mode"""
        if self.config_format == 'advanced':
            if 'concat_project_files' not in self.config:
                self.config['concat_project_files'] = {}
            self.config['concat_project_files']['mode'] = mode
    
    def force_legacy(self):
        """Forces the use of the legacy format"""
        self.config_format = 'legacy'
    
    def has_tree_config(self) -> bool:
        """Checks if a tree_project_files configuration exists"""
        return 'tree_project_files' in self.config
    
    def has_custom_tree_config(self) -> bool:
        """Checks if a custom_tree_files configuration exists"""
        return 'custom_tree_files' in self.config