#!/usr/bin/env python3
"""
Git integration for AI Context Craft
Provides Git-aware file filtering
"""

import subprocess
from pathlib import Path
from typing import List, Optional, Set, Tuple
import logging

class GitManager:
    """Manages Git integration for the project"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.is_git_repo = self._check_git_repo()
        self.git_root = self._find_git_root() if self.is_git_repo else None
        
    def _check_git_repo(self) -> bool:
        """Checks if the current directory is in a Git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _find_git_root(self) -> Optional[Path]:
        """Finds the root of the Git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip())
        except subprocess.CalledProcessError:
            return None
    
    def get_tracked_files(self, relative_to: Optional[Path] = None) -> List[str]:
        """
        Gets all files tracked by Git
        
        Args:
            relative_to: Make paths relative to this directory
            
        Returns:
            List of file paths (using forward slashes)
        """
        if not self.is_git_repo:
            return []
        
        try:
            result = subprocess.run(
                ["git", "ls-files"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            files = result.stdout.strip().split('\n')
            files = [f for f in files if f]  # Remove empty lines
            
            if relative_to:
                relative_to = Path(relative_to).resolve()
                processed_files = []
                for file in files:
                    full_path = self.git_root / file
                    try:
                        rel_path = full_path.relative_to(relative_to)
                        processed_files.append(str(rel_path).replace('\\', '/'))
                    except ValueError:
                        # File is outside the relative_to directory
                        continue
                return processed_files
            
            return files
            
        except subprocess.CalledProcessError:
            return []
    
    def get_ignored_patterns(self) -> List[str]:
        """
        Gets patterns from .gitignore files
        
        Returns:
            List of gitignore patterns
        """
        patterns = []
        
        # Find all .gitignore files in the repository
        gitignore_files = []
        
        # Root .gitignore
        root_gitignore = self.repo_path / ".gitignore"
        if root_gitignore.exists():
            gitignore_files.append(root_gitignore)
        
        # Find nested .gitignore files
        for gitignore in self.repo_path.rglob(".gitignore"):
            if gitignore not in gitignore_files:
                gitignore_files.append(gitignore)
        
        # Parse each .gitignore file
        for gitignore_file in gitignore_files:
            try:
                with open(gitignore_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip comments and empty lines
                        if line and not line.startswith('#'):
                            # Handle directory-relative patterns
                            if gitignore_file.parent != self.repo_path:
                                rel_dir = gitignore_file.parent.relative_to(self.repo_path)
                                line = str(rel_dir / line).replace('\\', '/')
                            patterns.append(line)
            except Exception as e:
                logging.warning(f"Error reading {gitignore_file}: {e}")
        
        return patterns
    
    def get_status(self) -> dict:
        """
        Gets the current Git status
        
        Returns:
            Dictionary with Git status information
        """
        if not self.is_git_repo:
            return {'is_git_repo': False}
        
        status = {
            'is_git_repo': True,
            'root': str(self.git_root),
            'branch': self._get_current_branch(),
            'has_changes': False,
            'untracked_files': [],
            'modified_files': [],
            'staged_files': []
        }
        
        try:
            # Get porcelain status for easy parsing
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                status_code = line[:2]
                file_path = line[3:]
                
                if status_code[0] in ['A', 'M', 'D', 'R']:
                    status['staged_files'].append(file_path)
                if status_code[1] == 'M':
                    status['modified_files'].append(file_path)
                if status_code == '??':
                    status['untracked_files'].append(file_path)
            
            status['has_changes'] = bool(
                status['untracked_files'] or 
                status['modified_files'] or 
                status['staged_files']
            )
            
        except subprocess.CalledProcessError:
            pass
        
        return status
    
    def _get_current_branch(self) -> Optional[str]:
        """Gets the current Git branch name"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def filter_git_only(self, files: List[Tuple[str, str]], 
                        include_untracked: bool = False) -> List[Tuple[str, str]]:
        """
        Filters files to only include those tracked by Git
        
        Args:
            files: List of (absolute_path, relative_path) tuples
            include_untracked: Whether to include untracked files
            
        Returns:
            Filtered list of files
        """
        if not self.is_git_repo:
            return files
        
        tracked = set(self.get_tracked_files(relative_to=self.repo_path))
        
        if include_untracked:
            status = self.get_status()
            tracked.update(status['untracked_files'])
        
        filtered = []
        for abs_path, rel_path in files:
            # Normalize path for comparison
            normalized_path = rel_path.replace('\\', '/')
            if normalized_path in tracked:
                filtered.append((abs_path, rel_path))
        
        return filtered
    
    def get_info_for_header(self) -> List[str]:
        """Gets Git information for the output file header"""
        if not self.is_git_repo:
            return []
        
        lines = []
        status = self.get_status()
        
        lines.append(f"# Git Branch: {status['branch'] or 'detached'}")
        
        if status['has_changes']:
            changes = []
            if status['modified_files']:
                changes.append(f"{len(status['modified_files'])} modified")
            if status['staged_files']:
                changes.append(f"{len(status['staged_files'])} staged")
            if status['untracked_files']:
                changes.append(f"{len(status['untracked_files'])} untracked")
            lines.append(f"# Git Status: {', '.join(changes)}")
        else:
            lines.append("# Git Status: clean")
        
        # Add commit hash
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            lines.append(f"# Git Commit: {result.stdout.strip()}")
        except subprocess.CalledProcessError:
            pass
        
        return lines


# Enhanced FileProcessor integration
class GitAwareFileProcessor:
    """Extension of FileProcessor with Git integration"""
    
    def __init__(self, file_processor, git_manager: Optional[GitManager] = None):
        self.processor = file_processor
        self.git = git_manager
    
    def get_filtered_files(self, source_dir: str, 
                          debug: bool = False,
                          git_mode: Optional[str] = None) -> List[Tuple[str, str]]:
        """
        Gets filtered files with optional Git filtering
        
        Args:
            source_dir: Source directory
            debug: Debug mode
            git_mode: Git filtering mode ('tracked', 'all', None)
                     - 'tracked': Only Git-tracked files
                     - 'all': Tracked + untracked files
                     - None: No Git filtering
        """
        # Get base filtered files
        files = self.processor.get_filtered_files(source_dir, debug)
        
        # Apply Git filtering if requested
        if git_mode and self.git and self.git.is_git_repo:
            if debug:
                print(f"🔀 Applying Git filter: {git_mode}")
            
            if git_mode == 'tracked':
                files = self.git.filter_git_only(files, include_untracked=False)
            elif git_mode == 'all':
                files = self.git.filter_git_only(files, include_untracked=True)
            
            if debug:
                print(f"📊 Files after Git filtering: {len(files)}")
        
        return files


# Usage example for main.py:
"""
# Add to argparse:
parser.add_argument(
    "--git-only",
    action="store_true",
    help="Only include files tracked by Git"
)
parser.add_argument(
    "--git-all",
    action="store_true",
    help="Include Git tracked files and untracked files"
)

# In AIContextCraft.__init__:
from utils.git_manager import GitManager
self.git = GitManager(source_dir)

# In concat_files method:
if self.git.is_git_repo and (git_only or git_all):
    git_mode = 'tracked' if git_only else 'all'
    # Use GitAwareFileProcessor
else:
    git_mode = None

# Add Git info to output file header
if self.git.is_git_repo:
    git_info = self.git.get_info_for_header()
    # Add to file header
"""