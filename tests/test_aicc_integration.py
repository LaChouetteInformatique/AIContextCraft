#!/usr/bin/env python3
"""
AI Context Craft - Pytest Integration Tests
This file shows how to use pytest for more formal testing
"""

import pytest
import subprocess
import json
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Tuple
import docker
import time

# Docker client
client = docker.from_env()

# Constants
DOCKER_IMAGE = "aicontextcraft:test"
TEST_PROJECT_PATH = Path(__file__).parent / "test-project"
TIMEOUT = 30

@pytest.fixture(scope="session")
def docker_image():
    """Ensure Docker image is built"""
    try:
        client.images.get(DOCKER_IMAGE)
    except docker.errors.ImageNotFound:
        # Build image
        project_root = Path(__file__).parent.parent
        client.images.build(path=str(project_root), tag=DOCKER_IMAGE)
    
    return DOCKER_IMAGE

@pytest.fixture(scope="session")
def test_project():
    """Ensure test project exists"""
    if not TEST_PROJECT_PATH.exists():
        # Run setup script
        setup_script = Path(__file__).parent / "test-project-setup.sh"
        if setup_script.exists():
            subprocess.run(["bash", str(setup_script)], check=True)
    
    assert TEST_PROJECT_PATH.exists(), "Test project not created"
    return TEST_PROJECT_PATH

@pytest.fixture
def temp_workspace() -> Generator[Path, None, None]:
    """Create a temporary workspace for testing"""
    temp_dir = Path(tempfile.mkdtemp(prefix="aicc_test_"))
    
    # Create some test files
    (temp_dir / "test.py").write_text("""
# Test Python file
def hello():
    return "Hello, World!"
""")
    
    (temp_dir / "test.js").write_text("""
// Test JavaScript file
function hello() {
    return "Hello, World!";
}
""")
    
    (temp_dir / "README.md").write_text("""
# Test Project
This is a test project for AI Context Craft.
""")
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)

def run_aicc(args: str, 
             working_dir: Path,
             timeout: int = TIMEOUT) -> Tuple[int, str, str]:
    """Run AI Context Craft in Docker"""
    
    container = client.containers.run(
        DOCKER_IMAGE,
        command=args,
        volumes={str(working_dir): {'bind': '/workspace', 'mode': 'rw'}},
        working_dir='/workspace',
        detach=True,
        remove=False
    )
    
    try:
        result = container.wait(timeout=timeout)
        logs = container.logs(stdout=True, stderr=True).decode('utf-8')
        exit_code = result['StatusCode']
        
        # Split stdout and stderr (simplified)
        stdout = logs
        stderr = ""
        
        return exit_code, stdout, stderr
        
    except Exception as e:
        container.kill()
        raise e
    finally:
        container.remove(force=True)

class TestBasicFunctionality:
    """Test basic AI Context Craft functionality"""
    
    def test_help_command(self, docker_image):
        """Test that help command works"""
        exit_code, stdout, stderr = run_aicc("--help", Path.cwd())
        
        assert exit_code == 0
        assert "usage" in stdout.lower() or "help" in stdout.lower()
    
    def test_process_directory(self, docker_image, test_project):
        """Test processing a directory"""
        exit_code, stdout, stderr = run_aicc(".", test_project)
        
        assert exit_code == 0
        assert len(stdout) > 100
        assert "backend" in stdout or "frontend" in stdout
    
    def test_tree_generation(self, docker_image, test_project):
        """Test tree structure generation"""
        exit_code, stdout, stderr = run_aicc("--tree", test_project)
        
        assert exit_code == 0
        assert "├──" in stdout or "└──" in stdout
    
    def test_json_output(self, docker_image, temp_workspace):
        """Test JSON output format"""
        exit_code, stdout, stderr = run_aicc(". --format json", temp_workspace)
        
        assert exit_code == 0
        
        # Try to parse JSON
        try:
            data = json.loads(stdout)
            assert isinstance(data, (dict, list))
        except json.JSONDecodeError:
            # JSON might be wrapped in other output
            for line in stdout.split('\n'):
                if line.strip().startswith('{') or line.strip().startswith('['):
                    data = json.loads(line)
                    break
            else:
                pytest.fail("No valid JSON found in output")
    
    def test_line_numbers(self, docker_image, temp_workspace):
        """Test line numbers in output"""
        exit_code, stdout, stderr = run_aicc(". --line-numbers", temp_workspace)
        
        assert exit_code == 0
        
        # Check for line numbers
        lines = stdout.split('\n')
        has_line_numbers = any(
            line.strip().startswith(str(i)) 
            for i in range(1, 10) 
            for line in lines
        )
        assert has_line_numbers, "No line numbers found in output"

class TestConfiguration:
    """Test configuration handling"""
    
    @pytest.fixture
    def config_file(self, tmp_path) -> Path:
        """Create a test configuration file"""
        config = tmp_path / "test-config.yaml"
        config.write_text("""
concat_project_files:
  mode: include
  include:
    - '**/*.py'
  exclude:
    - 'venv/**'
    - '__pycache__/**'
""")
        return config
    
    def test_custom_config(self, docker_image, test_project, config_file):
        """Test using custom configuration"""
        container = client.containers.run(
            DOCKER_IMAGE,
            command=".",
            volumes={
                str(test_project): {'bind': '/workspace', 'mode': 'rw'},
                str(config_file): {'bind': '/workspace/config.yaml', 'mode': 'ro'}
            },
            working_dir='/workspace',
            detach=True,
            remove=False
        )
        
        try:
            result = container.wait(timeout=TIMEOUT)
            logs = container.logs().decode('utf-8')
            
            assert result['StatusCode'] == 0
            assert ".py" in logs
            assert ".js" not in logs  # Should be excluded by config
            
        finally:
            container.remove(force=True)
    
    def test_invalid_config(self, docker_image, tmp_path):
        """Test handling of invalid configuration"""
        invalid_config = tmp_path / "invalid.yaml"
        invalid_config.write_text("invalid: yaml: content: !!!")
        
        container = client.containers.run(
            DOCKER_IMAGE,
            command=".",
            volumes={
                str(tmp_path): {'bind': '/workspace', 'mode': 'rw'},
                str(invalid_config): {'bind': '/workspace/config.yaml', 'mode': 'ro'}
            },
            working_dir='/workspace',
            detach=True,
            remove=False
        )
        
        try:
            result = container.wait(timeout=TIMEOUT)
            # Should fail with invalid config
            assert result['StatusCode'] != 0
            
        finally:
            container.remove(force=True)

class TestPatterns:
    """Test pattern matching functionality"""
    
    def test_include_patterns(self, docker_image, test_project):
        """Test include patterns"""
        exit_code, stdout, stderr = run_aicc(
            ". --include **/*.py --include **/*.md",
            test_project
        )
        
        assert exit_code == 0
        assert ".py" in stdout
        assert ".md" in stdout
        assert ".jsx" not in stdout
    
    def test_exclude_patterns(self, docker_image, test_project):
        """Test exclude patterns"""
        exit_code, stdout, stderr = run_aicc(
            ". --exclude **/*.log --exclude **/tests/**",
            test_project
        )
        
        assert exit_code == 0
        assert ".log" not in stdout
        assert "/tests/" not in stdout
    
    def test_directory_specific_patterns(self, docker_image, test_project):
        """Test directory-specific patterns"""
        exit_code, stdout, stderr = run_aicc(
            ". --include backend/**/*.py",
            test_project
        )
        
        assert exit_code == 0
        assert "backend" in stdout
        assert "frontend" not in stdout

class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_directory(self, docker_image, tmp_path):
        """Test handling of empty directory"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        exit_code, stdout, stderr = run_aicc(".", empty_dir)
        
        # Should handle gracefully
        assert exit_code == 0 or "empty" in stdout.lower() or "no files" in stdout.lower()
    
    def test_nonexistent_directory(self, docker_image):
        """Test handling of non-existent directory"""
        exit_code, stdout, stderr = run_aicc(
            "/nonexistent/path",
            Path.cwd()
        )
        
        assert exit_code != 0
    
    def test_special_characters_in_filenames(self, docker_image, tmp_path):
        """Test handling of special characters in filenames"""
        # Create files with special characters
        (tmp_path / "file with spaces.py").write_text("# Test")
        (tmp_path / "file@special#chars$.py").write_text("# Test")
        
        exit_code, stdout, stderr = run_aicc(".", tmp_path)
        
        assert exit_code == 0
        assert len(stdout) > 0
    
    def test_unicode_content(self, docker_image, tmp_path):
        """Test handling of Unicode content"""
        unicode_file = tmp_path / "unicode.py"
        unicode_file.write_text("# 你好世界 🌍 Здравствуй мир\nprint('Hello')")
        
        exit_code, stdout, stderr = run_aicc(".", tmp_path)
        
        assert exit_code == 0
        assert "你好世界" in stdout or "Hello" in stdout

class TestPerformance:
    """Test performance with larger datasets"""
    
    def test_many_files(self, docker_image, tmp_path):
        """Test handling many files"""
        # Create 100 test files
        for i in range(100):
            (tmp_path / f"file_{i}.py").write_text(f"# File {i}\ndef func_{i}(): pass")
        
        start_time = time.time()
        exit_code, stdout, stderr = run_aicc(". --stats", tmp_path, timeout=60)
        duration = time.time() - start_time
        
        assert exit_code == 0
        assert "100" in stdout or "Total files:" in stdout
        assert duration < 30, f"Processing took too long: {duration}s"
    
    @pytest.mark.slow
    def test_large_files(self, docker_image, tmp_path):
        """Test handling large files"""
        # Create a large file (5MB)
        large_content = "# Large file\n" + ("x" * 80 + "\n") * 65536
        (tmp_path / "large.py").write_text(large_content)
        
        exit_code, stdout, stderr = run_aicc(".", tmp_path, timeout=60)
        
        assert exit_code == 0
        assert len(stdout) > 1000

# Parametrized tests for multiple scenarios
@pytest.mark.parametrize("format_type,expected", [
    ("json", lambda x: json.loads(x) is not None),
    ("xml", lambda x: "<files>" in x or "<?xml" in x),
    ("markdown", lambda x: "```" in x or "#" in x),
])
def test_output_formats(docker_image, temp_workspace, format_type, expected):
    """Test different output formats"""
    exit_code, stdout, stderr = run_aicc(
        f". --format {format_type}",
        temp_workspace
    )
    
    assert exit_code == 0
    
    try:
        assert expected(stdout)
    except:
        pytest.fail(f"Output format {format_type} validation failed")

# Integration test scenarios
class TestScenarios:
    """Complex integration scenarios"""
    
    def test_developer_workflow(self, docker_image, test_project):
        """Test typical developer workflow"""
        
        # Step 1: Get project structure
        exit_code, stdout, stderr = run_aicc("--tree", test_project)
        assert exit_code == 0
        assert "├──" in stdout
        
        # Step 2: Get backend code
        exit_code, stdout, stderr = run_aicc(
            "backend --include **/*.py --remove-comments",
            test_project
        )
        assert exit_code == 0
        assert "backend" in stdout
        assert stdout.count("# Lorem ipsum") < 5  # Comments removed
        
        # Step 3: Get statistics
        exit_code, stdout, stderr = run_aicc(". --stats", test_project)
        assert exit_code == 0
        assert "Total files:" in stdout or "total" in stdout.lower()
    
    def test_documentation_generation(self, docker_image, test_project):
        """Test documentation extraction workflow"""
        
        # Extract all markdown files
        exit_code, stdout, stderr = run_aicc(
            ". --include **/*.md --format markdown",
            test_project
        )
        
        assert exit_code == 0
        assert ".md" in stdout or "README" in stdout
        assert "```" in stdout  # Markdown format

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])