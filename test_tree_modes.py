#!/usr/bin/env python3
"""Test script to verify the different tree modes and concatenation."""

import sys
import os
import shutil
import unittest
import subprocess
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import AIContextCraft

def create_test_structure(test_dir_path: Path):
    """Creates a robust test structure to verify the modes."""
    if test_dir_path.exists():
        shutil.rmtree(test_dir_path)
    
    files = {
        "README.md": "# Test Project",
        "src/main.py": "def main(): pass",
        "src/components/button.js": "export default Button",
        "src/utils/helpers.py": "def help(): pass",
        "tests/test_main.py": "def test(): pass",
        "docs/guide.md": "# Guide",
        "node_modules/package.json": "{}",
        ".venv/lib/python.py": "venv file", # File in a subdirectory
        ".gitignore": "node_modules/\n.venv/"
    }
    
    # --- FIX ---
    # For each file to be created, ensure its parent folder exists.
    for file_path, content in files.items():
        full_path = test_dir_path / file_path
        # Create the parent directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        # Write the file
        full_path.write_text(content, encoding='utf-8')

class TestTreeModes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Creates the test structure once for the entire class."""
        cls.test_dir = Path("test_project_trees")
        create_test_structure(cls.test_dir)
        cls.craft = AIContextCraft(source_dir=str(cls.test_dir))

    @classmethod
    def tearDownClass(cls):
        """Cleans up the test structure at the end."""
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)

    def test_01_generate_tree_only_modes(self):
        """Tests standalone tree generation for each mode."""
        results = {}
        for mode in ['normal', 'full', 'custom']:
            with self.subTest(mode=mode):
                output_file = self.test_dir / "build" / f"tree_{mode}.txt"
                self.craft.generate_tree(output_file=str(output_file), mode=mode)
                
                self.assertTrue(output_file.exists())
                content = output_file.read_text()
                results[mode] = len(content.splitlines())
        
        self.assertGreater(results['full'], results['custom'])
        self.assertGreater(results['custom'], results['normal'])

    def test_02_concatenation_with_tree_modes(self):
        """Tests concatenation with the different tree modes."""
        for tree_mode in ['normal', 'full', 'custom']:
            with self.subTest(mode=tree_mode):
                output_file = self.test_dir / "build" / f"concat_{tree_mode}.txt"
                
                # The concatenation will create its own result and its own stats
                self.craft.concat_files(
                    output_file=str(output_file),
                    tree_mode=tree_mode,
                    no_timestamp=True
                )
                
                self.assertTrue(output_file.exists())
                content = output_file.read_text()
                
                self.assertIn("# PROJECT STRUCTURE", content)
                self.assertIn("# FILE CONTENTS", content)

    def test_03_cli_help_output(self):
        """Checks that the tree options are in the command-line help."""
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            capture_output=True, text=True, check=True
        )
        help_text = result.stdout
        options = ["--with-tree", "--with-tree-full", "--with-tree-custom", "--tree-only", "--tree-mode"]
        
        for option in options:
            with self.subTest(option=option):
                self.assertIn(option, help_text, f"The {option} option should be in the help.")

if __name__ == "__main__":
    unittest.main(verbosity=2)