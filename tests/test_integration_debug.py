#!/usr/bin/env python3
"""
Debug version of integration tests to see what's happening
"""

import pytest
import subprocess
from pathlib import Path
import os

class TestAIContextCraftDebug:
    """Debug integration tests"""
    
    @classmethod
    def setup_class(cls):
        """Setup test environment once"""
        cls.test_project = Path("/test-project")
        cls.docker_image = "aicontextcraft:test"
        
        # Check if running in container with Docker socket
        if not Path("/var/run/docker.sock").exists():
            pytest.skip("Docker socket not mounted")
    
    def run_docker_app(self, args: str, working_dir: Path = None) -> tuple:
        """
        Run the AI Context Craft Docker application with debug output
        """
        if working_dir is None:
            working_dir = self.test_project
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{working_dir}:/workspace",
            "-w", "/workspace",
            self.docker_image
        ] + args.split()
        
        print(f"\n🔧 DEBUG: Running command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"📊 Exit code: {result.returncode}")
        if result.stdout:
            print(f"📝 STDOUT:\n{result.stdout[:500]}")  # First 500 chars
        if result.stderr:
            print(f"❌ STDERR:\n{result.stderr[:500]}")  # First 500 chars
        
        return result.returncode, result.stdout, result.stderr
    
    def test_docker_available(self):
        """Test that Docker is available"""
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        print(f"Docker version: {result.stdout}")
        assert result.returncode == 0
    
    def test_image_exists(self):
        """Test that our image exists"""
        result = subprocess.run(
            ["docker", "image", "inspect", self.docker_image],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Image {self.docker_image} not found!")
            print("Available images:")
            subprocess.run(["docker", "images"], check=False)
        assert result.returncode == 0, f"Image {self.docker_image} not found"
    
    def test_test_project_exists(self):
        """Test that test project is mounted"""
        assert self.test_project.exists(), f"Test project not found at {self.test_project}"
        print(f"Test project contents: {list(self.test_project.iterdir())[:10]}")
    
    def test_simple_help(self):
        """Test simple help command with full debug"""
        exit_code, stdout, stderr = self.run_docker_app("--help")
        
        # Don't assert yet, just see what happens
        if exit_code != 0:
            print(f"⚠️  Help command failed with exit code {exit_code}")
            print(f"This might mean the application has an issue")
    
    def test_run_with_python(self):
        """Test running Python directly in the container"""
        cmd = [
            "docker", "run", "--rm",
            self.docker_image,
            "python", "--version"
        ]
        
        print(f"\n🔧 Testing Python in container: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Python version in container: {result.stdout}")
        print(f"Exit code: {result.returncode}")
        
    def test_run_app_directly(self):
        """Test running the app directly"""
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{self.test_project}:/workspace",
            self.docker_image,
            "python", "/app/main.py", "--help"
        ]
        
        print(f"\n🔧 Running app directly: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(f"Exit code: {result.returncode}")
        print(f"STDOUT: {result.stdout[:500] if result.stdout else 'None'}")
        print(f"STDERR: {result.stderr[:500] if result.stderr else 'None'}")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # -s to see print outputs