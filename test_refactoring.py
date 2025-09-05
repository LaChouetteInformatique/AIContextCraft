#!/usr/bin/env python3
"""
Specific tests to validate the refactorings of Phases 1 & 2.
- Validates the new PatternMatcher based on pathspec.
- Validates the unified filtering logic.
"""
import sys
import unittest
from pathlib import Path

# Add the parent directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.pattern_matcher import PatternMatcher

class TestPatternMatcher(unittest.TestCase):

    def setUp(self):
        """Initializes the matcher and test files before each test."""
        self.matcher = PatternMatcher()
        self.files = [
            "README.md",
            "main.py",
            "src/component.js",
            "src/utils/helpers.py",
            "node_modules/lib/index.js",
            "build/output.css",
            ".env",
            "docs/guide.md",
            "test/test_helpers.py"
        ]

    def test_match_single_file(self):
        """Tests matching a single file."""
        self.assertTrue(self.matcher.match("main.py", ["*.py"]))
        self.assertFalse(self.matcher.match("main.py", ["*.js"]))
        self.assertTrue(self.matcher.match("src/component.js", ["src/*.js"]))

    def test_match_directory(self):
        """Tests matching directories."""
        self.assertTrue(self.matcher.match("node_modules/lib/index.js", ["node_modules/"]))
        self.assertFalse(self.matcher.match("src/component.js", ["node_modules/"]))

    def test_match_recursive(self):
        """Tests recursive matching (double asterisk)."""
        self.assertTrue(self.matcher.match("src/utils/helpers.py", ["**/*.py"]))
        self.assertTrue(self.matcher.match("test/test_helpers.py", ["**/*_helpers.py"]))

    def test_filter_files_include(self):
        """Tests filtering in include mode."""
        patterns = ["*.md", "**/*.py"]
        result = self.matcher.filter_files(self.files, patterns)
        
        # Use a set for more efficient and order-independent checks
        expected = {"README.md", "docs/guide.md", "main.py", "src/utils/helpers.py", "test/test_helpers.py"}
        self.assertEqual(set(result), expected)

    def test_filter_files_exclude(self):
        """Tests filtering in exclude mode (inverse logic)."""
        # Note: Exclusion is handled in FileProcessor, here we simulate that logic.
        exclude_patterns = ["node_modules/", "build/", ".env", "**/*.js"]
        
        included_files = [
            f for f in self.files 
            if not self.matcher.match(f, exclude_patterns)
        ]
        
        expected = {"README.md", "main.py", "src/utils/helpers.py", "docs/guide.md", "test/test_helpers.py"}
        self.assertEqual(set(included_files), expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)