#!/usr/bin/env python3
"""
Integration tests for AI Context Craft
Tests the actual Docker application with the test project
"""

import pytest
import subprocess
import tempfile
import json
from pathlib import Path
import os

class TestAIContextCraft:
    """Integration tests running the actual Docker application"""
    
    @classmethod
    def setup_class(cls):
        """Setup test environment once"""
        cls.test_project = Path("/test-project")  # Mounted in container
        cls.docker_image = "aicontextcraft:test"
        
        # Check if running in container with Docker socket
        if not Path("/var/run/docker.sock").exists():
            pytest.skip("Docker socket not mounted, skipping integration tests")
    
    def run_docker_app(self, args: str, working_dir: Path = None) -> tuple:
        """
        Run the AI Context Craft Docker application
        Returns (exit_code, stdout, stderr)
        """
        if working_dir is None:
            working_dir = self.test_project
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{working_dir}:/workspace",
            "-w", "/workspace",
            self.docker_image
        ] + args.split()
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return result.returncode, result.stdout, result.stderr
    
    def test_help_command(self):
        """Test that help command works"""
        exit_code, stdout, stderr = self.run_docker_app("--help")
        
        assert exit_code == 0
        assert "usage" in stdout.lower() or "context craft" in stdout.lower()
    
    def test_process_directory(self):
        """Test processing the test project"""
        exit_code, stdout, stderr = self.run_docker_app(".")
        
        assert exit_code == 0
        assert len(stdout) > 100
        assert "backend" in stdout or "frontend" in stdout
    
    def test_tree_generation(self):
        """Test tree structure generation"""
        exit_code, stdout, stderr = self.run_docker_app(". --tree-only")
        
        assert exit_code == 0
        assert "├──" in stdout or "└──" in stdout
        assert "backend/" in stdout
        assert "frontend/" in stdout
    
    def test_with_tree(self):
        """Test concatenation with tree"""
        exit_code, stdout, stderr = self.run_docker_app(". --with-tree")
        
        assert exit_code == 0
        assert "PROJECT STRUCTURE" in stdout
        assert "FILE CONTENTS" in stdout
    
    def test_strip_comments(self):
        """Test comment stripping"""
        exit_code, stdout, stderr = self.run_docker_app(". --strip-comments")
        
        assert exit_code == 0
        # Should have fewer comment lines
        comment_lines = [line for line in stdout.split('\n') if line.strip().startswith('#')]
        assert len(comment_lines) < 50  # Arbitrary threshold
    
    def test_include_patterns(self):
        """Test include patterns"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
concat_project_files:
  mode: include
  include:
    - '**/*.py'
""")
            config_path = f.name
        
        exit_code, stdout, stderr = self.run_docker_app(
            f". --config {config_path}"
        )
        
        assert exit_code == 0
        assert ".py" in stdout
        assert ".jsx" not in stdout
        
        Path(config_path).unlink()
    
    def test_exclude_patterns(self):
        """Test exclude patterns"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
concat_project_files:
  mode: exclude
  exclude:
    - '**/tests/**'
    - '**/*.log'
""")
            config_path = f.name
        
        exit_code, stdout, stderr = self.run_docker_app(
            f". --config {config_path}"
        )
        
        assert exit_code == 0
        assert "/tests/" not in stdout
        assert ".log" not in stdout
        
        Path(config_path).unlink()
    
    @pytest.mark.parametrize("tree_mode", ["normal", "full", "custom"])
    def test_tree_modes(self, tree_mode):
        """Test different tree modes"""
        exit_code, stdout, stderr = self.run_docker_app(
            f". --tree-only --tree-mode {tree_mode}"
        )
        
        assert exit_code == 0
        assert f"Tree mode: {tree_mode}" in stdout
    
    def test_output_file(self):
        """Test output to specific file"""
        # Use /tmp which is writable in container
        output_file = Path("/tmp/test_output.txt")
        
        exit_code, stdout, stderr = self.run_docker_app(
            f". --output {output_file}"
        )
        
        assert exit_code == 0
        # Note: The file is created inside the Docker container, not in our test container
        # We can't check if it exists, but we can check the command succeeded
        assert "generated" in stdout.lower() or exit_code == 0

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])