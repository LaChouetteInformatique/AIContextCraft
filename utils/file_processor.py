"""File processing module"""
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import logging
from .pattern_matcher import PatternMatcher
from .comment_stripper import CommentStripper

class FileProcessor:
    """Processes and filters project files"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.pattern_matcher = PatternMatcher(config_manager)
        self.comment_stripper = CommentStripper()
        self.logger: Optional[logging.Logger] = None
        self.git_manager = None  # Will be set externally if needed
        
    def set_logger(self, logger: logging.Logger):
        """Configures the logger for this processor"""
        self.logger = logger
        
    def set_git_manager(self, git_manager):
        """Sets the Git manager for Git-aware filtering"""
        self.git_manager = git_manager
        
    def _log(self, message: str, level: str = "info"):
        """Logs a message if a logger is configured"""
        if self.logger:
            getattr(self.logger, level, self.logger.info)(message)
                
    def get_filtered_files(self, source_dir: str, debug: bool = False, 
                          git_mode: str = None) -> List[Tuple[str, str]]:
        """
        Returns the list of filtered files according to the unified configuration.
        
        Args:
            source_dir: Source directory path
            debug: Enable debug logging
            git_mode: Git filtering mode ('tracked', 'all', None)
                     - 'tracked': Only Git-tracked files
                     - 'all': Tracked + untracked files
                     - None: No Git filtering
        
        Returns:
            List of tuples (absolute_path, relative_path)
        """
        all_files = []
        source_path = Path(source_dir).resolve()
        self._log(f"🔍 Collecting files in: {source_path}")
        
        skip_dirs = self._get_skip_directories()
        if skip_dirs:
            self._log(f"⏭️  Directories to skip completely: {', '.join(sorted(skip_dirs))}")
        
        for file_path in self._walk_directory(source_path, skip_dirs):
            if file_path.is_file():
                # Ensure relative paths use '/' for compatibility with pathspec
                relative_path = str(file_path.relative_to(source_path)).replace('\\', '/')
                all_files.append((str(file_path), relative_path))
        
        self._log(f"📂 Total files found before filtering: {len(all_files)}")
        
        # Apply Git filtering if requested
        if git_mode and self.git_manager:
            all_files = self._apply_git_filtering(all_files, source_path, git_mode, debug)
        
        # Get the filtering configuration, which handles legacy mode internally
        config = self.config.get_concat_config()
        mode = config.get('mode', 'exclude')
        self._log(f"🔧 Filtering mode: {mode.upper()}")
        
        filtered = []
        if mode == 'include':
            patterns = config.get('include', [])
            self._log(f"📋 Applying {len(patterns)} INCLUSION patterns.", "debug")
            for abs_path, rel_path in all_files:
                if self.pattern_matcher.match(rel_path, patterns):
                    filtered.append((abs_path, rel_path))
                    self._log(f"  [✅ INCLUDED] {rel_path}", "debug")
                else:
                    self._log(f"  [❌ NOT-INCLUDED] {rel_path}", "debug")
        else:  # 'exclude' mode
            patterns = config.get('exclude', [])
            self._log(f"📋 Applying {len(patterns)} EXCLUSION patterns.", "debug")
            for abs_path, rel_path in all_files:
                if not self.pattern_matcher.match(rel_path, patterns):
                    filtered.append((abs_path, rel_path))
                    self._log(f"  [✅ INCLUDED] {rel_path}", "debug")
                else:
                    self._log(f"  [❌ EXCLUDED] {rel_path}", "debug")
        
        self._log(f"📊 Files after filtering: {len(filtered)}")
        return filtered
    
    def _apply_git_filtering(self, all_files: List[Tuple[str, str]], 
                           source_path: Path, git_mode: str, 
                           debug: bool) -> List[Tuple[str, str]]:
        """
        Applies Git-based filtering to the file list
        
        Args:
            all_files: List of (absolute_path, relative_path) tuples
            source_path: Source directory path
            git_mode: 'tracked' or 'all'
            debug: Debug mode
            
        Returns:
            Filtered list of files
        """
        if not self.git_manager or not self.git_manager.is_git_repo:
            self._log("⚠️  Git filtering requested but not in a Git repository", "warning")
            return all_files
        
        self._log(f"🔀 Applying Git filter: {git_mode}")
        
        # Get tracked files
        tracked_files = set(self.git_manager.get_tracked_files(relative_to=source_path))
        
        if git_mode == 'all':
            # Also include untracked files (but not ignored)
            status = self.git_manager.get_status()
            for untracked in status.get('untracked_files', []):
                # Convert to forward slashes for consistency
                tracked_files.add(untracked.replace('\\', '/'))
        
        # Filter the files
        filtered = []
        for abs_path, rel_path in all_files:
            if rel_path in tracked_files:
                filtered.append((abs_path, rel_path))
                if debug:
                    self._log(f"  [GIT ✅] {rel_path}", "debug")
            else:
                if debug:
                    self._log(f"  [GIT ❌] {rel_path}", "debug")
        
        self._log(f"📊 Files after Git filtering: {len(filtered)} (was {len(all_files)})")
        return filtered
    
    def _get_skip_directories(self) -> set:
        """Determines the directories to completely ignore during traversal."""
        skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', '.venv'}
        config = self.config.get_concat_config()
        
        # Only exclusion patterns can define directories to ignore
        patterns = config.get('exclude', [])
        
        for pattern in patterns:
            if pattern.endswith('/'):
                skip_dirs.add(pattern[:-1])
            elif pattern.endswith('/**'):
                skip_dirs.add(pattern[:-3])
            elif '/' not in pattern and '*' not in pattern and '?' not in pattern:
                 skip_dirs.add(pattern)
        return skip_dirs
    
    def _walk_directory(self, path: Path, skip_dirs: set):
        """Recursively traverses the directory, avoiding excluded folders."""
        try:
            for item in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
                if item.name in skip_dirs:
                    self._log(f"  ⏭️  Skipped (skip_dirs): {item.relative_to(path.parent)}", "debug")
                    continue
                if item.is_dir():
                    yield from self._walk_directory(item, skip_dirs)
                else:
                    yield item
        except PermissionError:
            self._log(f"  ⚠️ No permission for: {path}", "warning")

    def process_directory(self, source_dir: str, debug: bool = False, 
                         strip_comments: bool = False,
                         git_mode: str = None) -> Dict[str, Any]:
        """
        Processes a directory, filters files, and reads their content.
        
        Args:
            source_dir: Source directory path
            debug: Enable debug logging
            strip_comments: Remove comments from code
            git_mode: Git filtering mode ('tracked', 'all', None)
            
        Returns:
            Dictionary with processed files data
        """
        source_path = Path(source_dir).resolve()
        self._log(f"📂 Analyzing: {source_path}")
        
        filtered_files = self.get_filtered_files(str(source_path), debug, git_mode)
        
        files_data = []
        total_size = 0
        errors = []
        
        self._log(f"\n📝 Reading {len(filtered_files)} files...")
        for abs_path, rel_path in filtered_files:
            try:
                with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if strip_comments:
                    original_size = len(content)
                    content = self.comment_stripper.strip_comments(content, abs_path)
                    if len(content) < original_size:
                        self._log(f"  💬 Stripped comments from {rel_path} "
                                f"({original_size} → {len(content)} bytes)", "debug")
                
                files_data.append({
                    'path': rel_path, 
                    'content': content, 
                    'size': len(content)
                })
                total_size += len(content)
                
            except Exception as e:
                error_msg = f"Error with {rel_path}: {e}"
                errors.append(error_msg)
                self._log(f"  ⚠️ {error_msg}", "warning")
        
        self._log(f"✅ Reading complete: {len(files_data)} files, {total_size:,} bytes")
        
        # Add Git information if available
        git_info = {}
        if self.git_manager and self.git_manager.is_git_repo:
            git_status = self.git_manager.get_status()
            git_info = {
                'is_git_repo': True,
                'branch': git_status.get('branch', 'unknown'),
                'has_changes': git_status.get('has_changes', False),
                'git_mode': git_mode
            }
        
        return {
            'files': files_data,
            'file_count': len(files_data),
            'total_size': total_size,
            'source_dir': str(source_path),
            'errors': errors,
            'git_info': git_info
        }