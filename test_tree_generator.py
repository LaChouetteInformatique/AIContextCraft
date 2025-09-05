#!/usr/bin/env python3
"""Test script to verify the TreeGenerator and its integration."""

import sys
import unittest
import shutil
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import AIContextCraft
from utils.config_manager import ConfigManager
from utils.tree_generator import TreeGenerator

class TestTreeGenerator(unittest.TestCase):

    def setUp(self):
        """Prepares the test environment."""
        self.test_output_dir = Path("build/test_generator_output")
        self.test_output_dir.mkdir(parents=True, exist_ok=True)
        # Use the default configuration for tests
        self.config = ConfigManager("config.yaml") 
        self.tree_gen = TreeGenerator(self.config)
        self.craft = AIContextCraft()

    def tearDown(self):
        """Cleans up the test environment."""
        if self.test_output_dir.exists():
            shutil.rmtree(self.test_output_dir)

    def test_tree_generation_standalone(self):
        """Tests standalone tree generation for the current directory."""
        tree_output = self.tree_gen.generate_tree(".")
        
        self.assertIsNotNone(tree_output)
        self.assertGreater(len(tree_output.splitlines()), 3, "The generated tree should contain several lines.")
        self.assertIn("main.py", tree_output, "The tree should contain the main.py file.")
        self.assertIn("# Tree mode: normal", tree_output, "The tree mode header should be present.")

    def test_concatenation_with_tree_option(self):
        """Tests the tree_mode='normal' option in concatenation."""
        test_output_file = self.test_output_dir / "test_with_tree.txt"
        
        # Call correction: Replacing with_tree=True with tree_mode='normal'
        self.craft.concat_files(
            output_file=str(test_output_file), 
            tree_mode='normal', 
            debug=False,
            no_timestamp=True
        )
        
        self.assertTrue(test_output_file.exists(), "The output file must be created.")
        
        with open(test_output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.assertIn("# PROJECT STRUCTURE", content, "The PROJECT STRUCTURE section must be present.")
        self.assertIn("# FILE CONTENTS", content, "The FILE CONTENTS section must be present.")
        
        # Check that there is content in the tree section
        tree_section = content.split("# PROJECT STRUCTURE")[1].split("# FILE CONTENTS")[0]
        self.assertGreater(len(tree_section.splitlines()), 5, "The tree section should not be empty.")

if __name__ == "__main__":
    unittest.main(verbosity=2)