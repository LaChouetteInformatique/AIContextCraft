"""Project tree generator"""
from pathlib import Path
from typing import List, Optional
from .pattern_matcher import PatternMatcher

class TreeGenerator:
    """Generates a tree representation of the project"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.pattern_matcher = PatternMatcher(config_manager)
        self.tree_chars = {
            'branch': '├── ',
            'last': '└── ',
            'vertical': '│   ',
            'space': '    '
        }
    
    def generate_tree(self, source_dir: str, mode: str = 'normal') -> str:
        """
        Generates the project tree according to the specified mode
        
        Args:
            source_dir: Source directory
            mode: Generation mode ('normal', 'full', 'custom')
        """
        source_path = Path(source_dir).resolve()
        
        config = self._get_config_for_mode(mode)
        
        header = f"# Tree mode: {mode}\n"
        if mode != 'normal':
            config_section = self._get_config_section_name(mode)
            header += f"# Using config section: {config_section}\n"
        header += f"# {'='*40}\n"
        
        lines = [header, f"{source_path.name}/"]
        self._build_tree_recursive(source_path, lines, "", config)
        
        return '\n'.join(lines)
    
    def _get_config_for_mode(self, mode: str) -> dict:
        """
        Returns the appropriate configuration according to the mode.
        This allows for different levels of detail in the tree view.
        """
        if mode == 'normal':
            return self.config.get_concat_config()
        elif mode == 'full':
            if 'tree_project_files' in self.config.config:
                return self.config.config.get('tree_project_files', {})
            else:
                # Fallback: exclude mode with only common system/build folders
                return {
                    'mode': 'exclude',
                    'exclude': ['venv/**', '.venv/**', 'node_modules/**', '__pycache__/**', 
                               '.git/**', 'build/**', 'dist/**', '*.pyc', '.env', '*.log']
                }
        elif mode == 'custom':
            if 'custom_tree_files' in self.config.config:
                return self.config.config.get('custom_tree_files', {})
            else:
                # Fallback: a reasonable intermediate configuration
                return {
                    'mode': 'exclude',
                    'exclude': ['venv/**', '.venv/**', 'node_modules/**', '__pycache__/**', 
                               '.git/**', '*.pyc', '*.log', '*.min.js', '*.min.css']
                }
        else:
            return self.config.get_concat_config()
    
    def _get_config_section_name(self, mode: str) -> str:
        """Returns the name of the config section used"""
        if mode == 'full':
            return 'tree_project_files'
        elif mode == 'custom':
            return 'custom_tree_files'
        else:
            return 'concat_project_files'
    
    def _build_tree_recursive(self, path: Path, lines: List[str], prefix: str, config: dict):
        """Builds the tree recursively"""
        
        try:
            items = []
            for item in sorted(path.iterdir()):
                # Special handling for hidden files/dirs to balance visibility and noise.
                if item.name.startswith('.'):
                    # Always include certain important config files.
                    if item.name not in ['.env.example', '.gitignore', '.github', '.dockerignore']:
                        if item.is_dir() and item.name != '.github':
                            continue
                        if item.is_file() and not self._should_include_item(item, path, config):
                            continue
                
                if self._should_include_item(item, path, config):
                    items.append(item)
                    
        except PermissionError:
            lines.append(f"{prefix}[Permission Denied]")
            return
        
        # Sort to display folders first, then files, alphabetically.
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
        
        for i, item in enumerate(items):
            is_last_item = (i == len(items) - 1)
            
            if is_last_item:
                connector = self.tree_chars['last']
                new_prefix = prefix + self.tree_chars['space']
            else:
                connector = self.tree_chars['branch']
                new_prefix = prefix + self.tree_chars['vertical']
            
            if item.is_dir():
                lines.append(f"{prefix}{connector}{item.name}/")
                self._build_tree_recursive(item, lines, new_prefix, config)
            else:
                try:
                    size = item.stat().st_size
                    size_str = self._format_size(size)
                    lines.append(f"{prefix}{connector}{item.name} ({size_str})")
                except:
                    lines.append(f"{prefix}{connector}{item.name}")
    
    def _format_size(self, size: int) -> str:
        """Formats a size into a readable format"""
        if size < 1024:
            return f"{size}B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f}KB"
        else:
            return f"{size/(1024*1024):.1f}MB"
    
    def _should_include_item(self, item: Path, base_path: Path, config: dict) -> bool:
        """Determines if an item should be included in the tree"""
        
        if not self.config.is_advanced_format():
            return self._should_include_legacy(item)
        
        try:
            rel_path = str(item.relative_to(base_path))
        except ValueError:
            rel_path = item.name
        
        mode = config.get('mode', 'exclude')
        
        if mode == 'include':
            include_patterns = config.get('include', [])
            exclude_patterns = config.get('exclude', [])
            
            if item.is_dir():
                # For directories, check if they could potentially contain included files.
                dir_pattern = f"{rel_path}/**"
                for pattern in include_patterns:
                    if (pattern.startswith(rel_path) or 
                        self.pattern_matcher.match(dir_pattern, [pattern]) or
                        self.pattern_matcher.match(rel_path, [pattern])):
                        if exclude_patterns and self.pattern_matcher.match(rel_path, exclude_patterns):
                            return False
                        return True
                return False
            else:
                if self.pattern_matcher.match(rel_path, include_patterns):
                    if exclude_patterns and self.pattern_matcher.match(rel_path, exclude_patterns):
                        return False
                    return True
                return False
        else:  # exclude mode
            exclude_patterns = config.get('exclude', [])
            if item.is_dir():
                dir_pattern = f"{rel_path}/"
                return not self.pattern_matcher.match(dir_pattern, exclude_patterns)
            else:
                return not self.pattern_matcher.match(rel_path, exclude_patterns)
    
    def _should_include_legacy(self, item: Path) -> bool:
        """Legacy filtering based on extensions and excluded directories"""
        exclude_dirs = self.config.get('exclude_dirs', [])
        
        if item.is_dir():
            return item.name not in exclude_dirs
        else:
            include_ext = self.config.get('include_extensions', [])
            exclude_files = self.config.get('exclude_files', [])
            
            if item.name in exclude_files:
                return False
            
            if include_ext:
                return item.suffix in include_ext or item.name in include_ext
            
            return True