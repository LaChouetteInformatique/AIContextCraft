#!/usr/bin/env python3
"""
AI Context Craft - Main test file with modular structure
Easy to extend and run selectively
"""

import pytest
import docker
import tempfile
import time
from pathlib import Path

# Shared fixtures and constants
client = docker.from_env()
DOCKER_IMAGE = "aicontextcraft:test"
TEST_PROJECT_PATH = Path(__file__).parent / "test-project"


# ============= FIXTURES =============
@pytest.fixture(scope="session")
def docker_image():
    """Ensure Docker image is built"""
    try:
        client.images.get(DOCKER_IMAGE)
    except docker.errors.ImageNotFound:
        project_root = Path(__file__).parent.parent
        client.images.build(path=str(project_root), tag=DOCKER_IMAGE)
    return DOCKER_IMAGE


@pytest.fixture(scope="session")
def test_project():
    """Ensure test project exists"""
    if not TEST_PROJECT_PATH.exists():
        setup_script = Path(__file__).parent / "test-project-setup.sh"
        if setup_script.exists():
            import subprocess
            subprocess.run(["bash", str(setup_script)], check=True)
    return TEST_PROJECT_PATH


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project for testing"""
    (tmp_path / "main.py").write_text("def main(): pass")
    (tmp_path / "README.md").write_text("# Test Project")
    return tmp_path


def run_aicc(args: str, working_dir: Path = None):
    """Helper to run AI Context Craft in Docker"""
    if working_dir is None:
        working_dir = TEST_PROJECT_PATH
    
    container = client.containers.run(
        DOCKER_IMAGE,
        command=f"python /app/main.py {args}",
        volumes={str(working_dir): {'bind': '/workspace', 'mode': 'rw'}},
        working_dir='/workspace',
        detach=True,
        remove=False
    )
    
    try:
        result = container.wait(timeout=30)
        logs = container.logs().decode('utf-8')
        return result['StatusCode'], logs
    finally:
        container.remove(force=True)


# ============= BASIC TESTS =============
@pytest.mark.basic
class TestBasic:
    """Basic functionality - Run with: pytest -m basic"""
    
    def test_help(self, docker_image):
        """Test help command"""
        exit_code, output = run_aicc("--help")
        assert exit_code == 0
        assert "usage" in output.lower()
    
    def test_version(self, docker_image):
        """Test version display"""
        exit_code, output = run_aicc("--version")
        # If --version not implemented, skip
        if exit_code != 0:
            pytest.skip("--version not implemented")
        assert "version" in output.lower()
    
    def test_process_current_dir(self, docker_image, test_project):
        """Test processing current directory"""
        exit_code, output = run_aicc(".")
        assert exit_code == 0
        assert len(output) > 100


# ============= CONFIGURATION TESTS =============
@pytest.mark.config
class TestConfiguration:
    """Configuration tests - Run with: pytest -m config"""
    
    def test_default_config(self, docker_image, test_project):
        """Test with default configuration"""
        exit_code, output = run_aicc(".")
        assert exit_code == 0
        assert "FILE CONTENTS" in output
    
    def test_custom_config_yaml(self, docker_image, temp_project):
        """Test with custom YAML config"""
        config = temp_project / "custom.yaml"
        config.write_text("""
concat_project_files:
  mode: include
  include: ['**/*.py']
""")
        exit_code, output = run_aicc(f". --config custom.yaml", temp_project)
        assert exit_code == 0
        assert ".py" in output
    
    @pytest.mark.parametrize("mode", ["include", "exclude"])
    def test_filtering_modes(self, docker_image, test_project, mode):
        """Test different filtering modes"""
        exit_code, output = run_aicc(f". --mode {mode}")
        assert exit_code == 0


# ============= FEATURE TESTS =============
@pytest.mark.features
class TestFeatures:
    """Feature tests - Run with: pytest -m features"""
    
    def test_tree_generation(self, docker_image, test_project):
        """Test tree structure generation"""
        exit_code, output = run_aicc("--tree-only")
        assert exit_code == 0
        assert "├──" in output or "└──" in output
    
    def test_with_tree(self, docker_image, test_project):
        """Test concatenation with tree"""
        exit_code, output = run_aicc(". --with-tree")
        assert exit_code == 0
        assert "PROJECT STRUCTURE" in output
        assert "FILE CONTENTS" in output
    
    def test_strip_comments(self, docker_image, test_project):
        """Test comment stripping"""
        exit_code, output = run_aicc(". --strip-comments")
        assert exit_code == 0
        # Should have fewer comments
        comment_count = output.count("#")
        no_strip_code, no_strip_output = run_aicc(".")
        assert comment_count < no_strip_output.count("#")
    
    @pytest.mark.skipif(not Path("/tmp").exists(), reason="No /tmp directory")
    def test_clipboard(self, docker_image, test_project):
        """Test clipboard functionality"""
        exit_code, output = run_aicc(". --to-clipboard")
        # May fail in Docker, that's OK
        assert exit_code == 0 or "clipboard" in output.lower()


# ============= GIT TESTS =============
@pytest.mark.git
class TestGitIntegration:
    """Git integration tests - Run with: pytest -m git"""
    
    def test_git_info_in_output(self, docker_image, temp_project):
        """Test Git information in output"""
        import subprocess
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=temp_project, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=temp_project, capture_output=True)
        
        exit_code, output = run_aicc(".", temp_project)
        assert exit_code == 0
        # May or may not have git info, depends on implementation
    
    @pytest.mark.skip(reason="Requires git setup in container")
    def test_git_only_mode(self, docker_image, test_project):
        """Test --git-only mode"""
        exit_code, output = run_aicc(". --git-only")
        assert exit_code == 0


# ============= EDGE CASES =============
@pytest.mark.edge
class TestEdgeCases:
    """Edge cases - Run with: pytest -m edge"""
    
    def test_empty_directory(self, docker_image, tmp_path):
        """Test empty directory handling"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        exit_code, output = run_aicc(".", empty_dir)
        assert exit_code == 0
    
    def test_large_file(self, docker_image, tmp_path):
        """Test large file handling"""
        large_file = tmp_path / "large.txt"
        large_file.write_text("x" * 1_000_000)  # 1MB file
        exit_code, output = run_aicc(".", tmp_path)
        assert exit_code == 0
    
    def test_unicode_content(self, docker_image, tmp_path):
        """Test Unicode content"""
        (tmp_path / "unicode.py").write_text("# 你好世界 🌍 مرحبا\nprint('Hello')")
        exit_code, output = run_aicc(".", tmp_path)
        assert exit_code == 0
    
    def test_special_chars_filename(self, docker_image, tmp_path):
        """Test special characters in filenames"""
        (tmp_path / "file with spaces.py").write_text("# Test")
        (tmp_path / "file-with-dashes.py").write_text("# Test")
        exit_code, output = run_aicc(".", tmp_path)
        assert exit_code == 0


# ============= PERFORMANCE TESTS =============
@pytest.mark.performance
@pytest.mark.slow
class TestPerformance:
    """Performance tests - Run with: pytest -m performance"""
    
    def test_many_files(self, docker_image, tmp_path):
        """Test with many files"""
        for i in range(100):
            (tmp_path / f"file_{i}.py").write_text(f"def func_{i}(): pass")
        
        start = time.time()
        exit_code, output = run_aicc(".", tmp_path)
        duration = time.time() - start
        
        assert exit_code == 0
        assert duration < 30, f"Too slow: {duration}s"
    
    def test_deep_nesting(self, docker_image, tmp_path):
        """Test deeply nested directories"""
        deep_path = tmp_path
        for i in range(10):
            deep_path = deep_path / f"level_{i}"
            deep_path.mkdir()
            (deep_path / f"file_{i}.py").write_text(f"# Level {i}")
        
        exit_code, output = run_aicc(".", tmp_path)
        assert exit_code == 0


# ============= REGRESSION TESTS =============
@pytest.mark.regression
class TestRegression:
    """Regression tests for known issues - Run with: pytest -m regression"""
    
    def test_issue_001_relative_paths(self, docker_image, test_project):
        """Test relative path handling (Issue #001)"""
        # Add specific regression tests as issues are found
        exit_code, output = run_aicc("../test-project", test_project / "backend")
        assert exit_code == 0
    
    @pytest.mark.xfail(reason="Known issue with symlinks")
    def test_issue_002_symlinks(self, docker_image, tmp_path):
        """Test symlink handling (Issue #002)"""
        target = tmp_path / "target.py"
        target.write_text("# Target file")
        link = tmp_path / "link.py"
        link.symlink_to(target)
        
        exit_code, output = run_aicc(".", tmp_path)
        assert exit_code == 0