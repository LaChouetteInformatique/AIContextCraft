"""Project tree generator using anytree library"""
from pathlib import Path
from typing import Dict, Optional
from anytree import Node, RenderTree
from anytree.exporter import DictExporter
from anytree.render import AbstractStyle, ContRoundStyle, AsciiStyle
from .pattern_matcher import PatternMatcher


class TreeGenerator:
    """Generates a tree representation of the project using anytree"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.pattern_matcher = PatternMatcher(config_manager)
        # Choose tree style (can be configured)
        self.tree_style = ContRoundStyle()  # ├── └── style
        # Alternative styles:
        # self.tree_style = AsciiStyle()  # +-- style for better compatibility
    
    def generate_tree(self, source_dir: str, mode: str = 'normal') -> str:
        """
        Generates the project tree according to the specified mode
        
        Args:
            source_dir: Source directory
            mode: Generation mode ('normal', 'full', 'custom')
        """
        source_path = Path(source_dir).resolve()
        config = self._get_config_for_mode(mode)
        
        # Build header
        header = f"# Tree mode: {mode}\n"
        if mode != 'normal':
            config_section = self._get_config_section_name(mode)
            header += f"# Using config section: {config_section}\n"
        header += f"# {'='*40}\n\n"
        
        # Build tree using anytree
        root_node = self._build_tree(source_path, config)
        
        # Render tree
        lines = [header]
        for pre, _, node in RenderTree(root_node, style=self.tree_style):
            lines.append(f"{pre}{node.name}")
        
        return '\n'.join(lines)
    
    def _build_tree(self, root_path: Path, config: dict) -> Node:
        """
        Build anytree structure from filesystem
        
        Args:
            root_path: Root directory path
            config: Filter configuration
            
        Returns:
            Root node of the tree
        """
        # Create root node with directory name and trailing slash
        root_node = Node(f"{root_path.name}/")
        
        # Build tree recursively
        self._add_children(root_node, root_path, root_path, config)
        
        return root_node
    
    def _add_children(self, parent_node: Node, path: Path, root_path: Path, config: dict):
        """
        Recursively add children to the tree
        
        Args:
            parent_node: Parent node in the tree
            path: Current directory path
            root_path: Original root path for relative calculations
            config: Filter configuration
        """
        try:
            items = []
            
            # Collect items that should be included
            for item in sorted(path.iterdir()):
                if self._should_include(item, root_path, config):
                    items.append(item)
            
            # Sort: directories first, then files, alphabetically
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            # Add items as nodes
            for item in items:
                if item.is_dir():
                    # Directory node with trailing slash
                    dir_node = Node(f"{item.name}/", parent=parent_node)
                    # Recursively add children
                    self._add_children(dir_node, item, root_path, config)
                else:
                    # File node with size
                    size_str = self._format_size(item.stat().st_size)
                    Node(f"{item.name} ({size_str})", parent=parent_node)
                    
        except PermissionError:
            Node("[Permission Denied]", parent=parent_node)
    
    def _should_include(self, item: Path, root_path: Path, config: dict) -> bool:
        """
        Determines if an item should be included in the tree
        
        Args:
            item: Path to check
            root_path: Root path for relative calculations
            config: Filter configuration
            
        Returns:
            True if item should be included
        """
        # Handle hidden files/directories
        if item.name.startswith('.'):
            # Special cases for important hidden files
            important_hidden = {'.gitignore', '.dockerignore', '.env.example', '.github'}
            if item.name not in important_hidden and not item.is_dir():
                return False
            if item.is_dir() and item.name not in {'.github'}:
                # Skip most hidden directories
                return False
        
        # Skip common system directories early
        if item.is_dir() and item.name in {'__pycache__', 'node_modules', 'venv', '.venv', '.git'}:
            return False
        
        # Advanced filtering if configured
        if not self.config.is_advanced_format():
            return self._should_include_legacy(item)
        
        # Calculate relative path for pattern matching
        try:
            rel_path = str(item.relative_to(root_path)).replace('\\', '/')
        except ValueError:
            rel_path = item.name
        
        mode = config.get('mode', 'exclude')
        
        if mode == 'include':
            include_patterns = config.get('include', [])
            exclude_patterns = config.get('exclude', [])
            
            if item.is_dir():
                # Check if directory might contain included files
                dir_pattern = f"{rel_path}/**"
                for pattern in include_patterns:
                    if (pattern.startswith(f"{rel_path}/") or 
                        self.pattern_matcher.match(dir_pattern, [pattern]) or
                        '**' in pattern):
                        # Check exclusions
                        if exclude_patterns and self.pattern_matcher.match(rel_path, exclude_patterns):
                            return False
                        return True
                return False
            else:
                # Check file against patterns
                if self.pattern_matcher.match(rel_path, include_patterns):
                    if exclude_patterns and self.pattern_matcher.match(rel_path, exclude_patterns):
                        return False
                    return True
                return False
        else:  # exclude mode
            exclude_patterns = config.get('exclude', [])
            if item.is_dir():
                dir_patterns = [rel_path, f"{rel_path}/"]
                return not any(self.pattern_matcher.match(p, exclude_patterns) for p in dir_patterns)
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
    
    def _format_size(self, size: int) -> str:
        """Formats a size into a readable format"""
        if size < 1024:
            return f"{size}B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f}KB"
        else:
            return f"{size/(1024*1024):.1f}MB"
    
    def _get_config_for_mode(self, mode: str) -> dict:
        """
        Returns the appropriate configuration according to the mode.
        """
        if mode == 'normal':
            return self.config.get_concat_config()
        elif mode == 'full':
            if 'tree_project_files' in self.config.config:
                return self.config.config.get('tree_project_files', {})
            else:
                # Fallback: minimal exclusions for full view
                return {
                    'mode': 'exclude',
                    'exclude': ['venv/**', '.venv/**', 'node_modules/**', '__pycache__/**', 
                               '.git/**', '*.pyc', '*.log']
                }
        elif mode == 'custom':
            if 'custom_tree_files' in self.config.config:
                return self.config.config.get('custom_tree_files', {})
            else:
                # Fallback: reasonable intermediate configuration
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
    
    def export_json(self, source_dir: str, mode: str = 'normal') -> dict:
        """
        Export tree as JSON structure (bonus feature with anytree)
        
        Args:
            source_dir: Source directory
            mode: Generation mode
            
        Returns:
            Dictionary representation of the tree
        """
        source_path = Path(source_dir).resolve()
        config = self._get_config_for_mode(mode)
        root_node = self._build_tree(source_path, config)
        
        exporter = DictExporter()
        return exporter.export(root_node)
    
    def generate_tree_with_stats(self, source_dir: str, mode: str = 'normal') -> str:
        """
        Generate tree with statistics (file count, total size per directory)
        
        Args:
            source_dir: Source directory
            mode: Generation mode
            
        Returns:
            Tree with statistics
        """
        source_path = Path(source_dir).resolve()
        config = self._get_config_for_mode(mode)
        
        # Build tree with stats
        root_node = self._build_tree_with_stats(source_path, config)
        
        # Build header
        header = f"# Tree mode: {mode} (with statistics)\n"
        header += f"# {'='*40}\n\n"
        
        # Render tree
        lines = [header]
        for pre, _, node in RenderTree(root_node, style=self.tree_style):
            if hasattr(node, 'stats'):
                stats = node.stats
                lines.append(f"{pre}{node.name} [{stats['files']} files, {self._format_size(stats['size'])}]")
            else:
                lines.append(f"{pre}{node.name}")
        
        return '\n'.join(lines)
    
    def _build_tree_with_stats(self, root_path: Path, config: dict) -> Node:
        """Build tree with statistics"""
        root_node = Node(f"{root_path.name}/")
        root_node.stats = {'files': 0, 'size': 0}
        
        self._add_children_with_stats(root_node, root_path, root_path, config)
        
        return root_node
    
    def _add_children_with_stats(self, parent_node: Node, path: Path, root_path: Path, config: dict):
        """Add children with statistics calculation"""
        try:
            items = []
            
            for item in sorted(path.iterdir()):
                if self._should_include(item, root_path, config):
                    items.append(item)
            
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for item in items:
                if item.is_dir():
                    dir_node = Node(f"{item.name}/", parent=parent_node)
                    dir_node.stats = {'files': 0, 'size': 0}
                    self._add_children_with_stats(dir_node, item, root_path, config)
                    # Propagate stats up
                    parent_node.stats['files'] += dir_node.stats['files']
                    parent_node.stats['size'] += dir_node.stats['size']
                else:
                    size = item.stat().st_size
                    Node(f"{item.name} ({self._format_size(size)})", parent=parent_node)
                    parent_node.stats['files'] += 1
                    parent_node.stats['size'] += size
                    
        except PermissionError:
            Node("[Permission Denied]", parent=parent_node)