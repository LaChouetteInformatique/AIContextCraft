#!/usr/bin/env python3
"""Debug tests for AI Context Craft"""

import pytest
import docker
import subprocess
from pathlib import Path

client = docker.from_env()
DOCKER_IMAGE = "aicontextcraft:test"
TEST_PROJECT = Path("/test-project")  # Path inside container


class TestAIContextCraftDebug:
    """Debug tests to identify issues"""
    
    def test_docker_available(self):
        """Check Docker is available"""
        version = client.version()
        print(f"Docker version: {version['Version']}")
        assert version is not None
    
    def test_image_exists(self):
        """Check our image exists"""
        try:
            image = client.images.get(DOCKER_IMAGE)
            assert image is not None
        except docker.errors.ImageNotFound:
            pytest.fail(f"Image {DOCKER_IMAGE} not found")
    
    def test_test_project_exists(self):
        """Check test project is mounted"""
        # This runs inside the test container
        assert TEST_PROJECT.exists()
        print(f"Test project contents: {list(TEST_PROJECT.iterdir())}")
    
    def test_simple_help(self):
        """Test help command with proper path"""
        print(f"\n🔧 DEBUG: Running help command with app at /app/main.py")
        
        # FIX: Use absolute path to main.py
        container = client.containers.run(
            DOCKER_IMAGE,
            command="python /app/main.py --help",  # Absolute path
            volumes={
                str(Path.cwd() / "tests/test-project"): {
                    'bind': '/workspace',
                    'mode': 'rw'
                }
            },
            working_dir='/workspace',
            remove=True,
            detach=False,
            stdout=True,
            stderr=True
        )
        
        output = container.decode('utf-8')
        print(f"📊 Output: {output[:500]}")
        assert "usage" in output.lower() or "help" in output.lower()
    
    def test_process_test_project(self):
        """Test processing the test project"""
        print("\n🔧 DEBUG: Processing test project")
        
        container_output = client.containers.run(
            DOCKER_IMAGE,
            command="python /app/main.py . --debug",
            volumes={
                str(Path.cwd() / "tests/test-project"): {
                    'bind': '/workspace',
                    'mode': 'rw'
                }
            },
            working_dir='/workspace',
            remove=True,
            stdout=True,
            stderr=True
        )
        
        output = container_output.decode('utf-8')
        print(f"Output length: {len(output)} bytes")
        print(f"First 200 chars: {output[:200]}")
        
        # Should process files
        assert len(output) > 100
        assert "backend" in output or "frontend" in output or "Processing" in output