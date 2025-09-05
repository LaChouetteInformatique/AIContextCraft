"""Pattern manager for file filtering using pathspec."""
import pathspec
from typing import List, Iterable

class PatternMatcher:
    """Manages pattern matching for files using pathspec."""

    def __init__(self, config_manager=None):
        """
        Initializes the PatternMatcher.
        The config_manager is no longer used but kept for API compatibility.
        """
        pass

    def match(self, file_path: str, patterns: List[str]) -> bool:
        """
        Checks if a file path matches at least one of the patterns.
        
        Args:
            file_path: The file path to check (must use '/' as a separator).
            patterns: A list of .gitignore-style patterns.
            
        Returns:
            True if the path matches a pattern, False otherwise.
        """
        if not patterns:
            return False
        # 'gitwildmatch' is the matching style of .gitignore, which is intuitive for developers.
        spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        return spec.match_file(file_path)

    def filter_files(self, files: Iterable[str], patterns: List[str]) -> List[str]:
        """
        Filters a list of file paths based on the patterns.

        Args:
            files: An iterable of file paths.
            patterns: A list of .gitignore-style patterns.

        Returns:
            A list of files that match the patterns.
        """
        if not patterns:
            return []
        spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        return list(spec.match_files(files))