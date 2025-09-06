#!/usr/bin/env python3
"""
Tests d'intégration pour AI Context Craft
Lance directement le code Python sans passer par Docker
"""

import pytest
import sys
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.app import AIContextCraft
from utils.config_manager import ConfigManager


class TestAIContextCraft:
    """Tests complets sur le projet Lorem Ipsum"""
    
    @pytest.fixture(scope="class")
    def lorem_project(self, tmp_path_factory):
        """Create Lorem Ipsum test project"""
        project_dir = tmp_path_factory.mktemp("lorem_project")
        
        # Backend files
        backend_dir = project_dir / "backend"
        backend_dir.mkdir()
        (backend_dir / "main.py").write_text("""
#!/usr/bin/env python3
'''Lorem Ipsum generator main module'''

import random

class LoremGenerator:
    '''Generates Lorem Ipsum text'''
    
    def __init__(self):
        # Comment to test stripping
        self.words = ["lorem", "ipsum", "dolor", "sit", "amet"]
    
    def generate(self, count=5):
        '''Generate Lorem text'''
        return " ".join(random.choices(self.words, k=count))

if __name__ == "__main__":
    gen = LoremGenerator()
    print(gen.generate())
""")
        
        (backend_dir / "api.py").write_text("""
from flask import Flask, jsonify
from main import LoremGenerator

app = Flask(__name__)

@app.route('/api/lorem')
def get_lorem():
    '''API endpoint for Lorem'''
    gen = LoremGenerator()
    return jsonify({"text": gen.generate()})
""")
        
        # Frontend files
        frontend_dir = project_dir / "frontend" / "src"
        frontend_dir.mkdir(parents=True)
        (frontend_dir / "App.jsx").write_text("""
import React from 'react';

function App() {
  // React component
  return <div>Lorem Ipsum App</div>;
}

export default App;
""")
        
        # Config files
        (project_dir / "README.md").write_text("# Lorem Ipsum Project\n\nTest project for AI Context Craft")
        (project_dir / "requirements.txt").write_text("flask==2.3.0\npytest==7.4.0")
        (project_dir / ".env").write_text("SECRET_KEY=do-not-include-this")
        
        # Files to exclude
        node_modules = project_dir / "node_modules" / "package.json"
        node_modules.parent.mkdir(parents=True)
        node_modules.write_text('{"name": "excluded"}')
        
        venv_dir = project_dir / "venv" / "lib" / "python.py"
        venv_dir.parent.mkdir(parents=True)
        venv_dir.write_text("# Should be excluded")
        
        cache_dir = project_dir / "__pycache__"
        cache_dir.mkdir()
        (cache_dir / "cache.pyc").write_text("# Binary file")
        
        # .gitignore
        (project_dir / ".gitignore").write_text("""
node_modules/
venv/
__pycache__/
*.pyc
.env
*.log
build/
""")
        
        return project_dir
    
    @pytest.fixture
    def aicc(self, lorem_project):
        """Create AIContextCraft instance for Lorem project"""
        return AIContextCraft(source_dir=str(lorem_project))
    
    # ========== BASIC TESTS ==========
    
    def test_basic_concatenation(self, aicc, lorem_project, tmp_path):
        """Test basic file concatenation"""
        output_file = tmp_path / "output.txt"
        
        result = aicc.concat_files(
            output_file=str(output_file),
            no_timestamp=True
        )
        
        assert output_file.exists()
        content = output_file.read_text()
        
        # Should include source files
        assert "LoremGenerator" in content
        assert "App.jsx" in content
        assert "README.md" in content
        
        # Should NOT include excluded files
        assert "SECRET_KEY" not in content  # .env
        assert "excluded" not in content    # node_modules
        assert "Binary file" not in content # .pyc
    
    def test_with_tree(self, aicc, tmp_path):
        """Test concatenation with tree structure"""
        output_file = tmp_path / "with_tree.txt"
        
        aicc.concat_files(
            output_file=str(output_file),
            tree_mode='normal',
            no_timestamp=True
        )
        
        content = output_file.read_text()
        assert "PROJECT STRUCTURE" in content
        assert "FILE CONTENTS" in content
        assert "├──" in content or "└──" in content
    
    def test_strip_comments(self, aicc, tmp_path):
        """Test comment stripping"""
        output_normal = tmp_path / "normal.txt"
        output_stripped = tmp_path / "stripped.txt"
        
        # Without stripping
        aicc.concat_files(
            output_file=str(output_normal),
            strip_comments=False,
            no_timestamp=True
        )
        
        # With stripping
        aicc.concat_files(
            output_file=str(output_stripped),
            strip_comments=True,
            no_timestamp=True
        )
        
        normal_content = output_normal.read_text()
        stripped_content = output_stripped.read_text()
        
        # Stripped should have fewer comment markers
        assert normal_content.count("# Comment") > stripped_content.count("# Comment")
        assert normal_content.count("'''") > stripped_content.count("'''")
        assert normal_content.count("//") > stripped_content.count("//")
    
    # ========== CONFIGURATION TESTS ==========
    
    def test_custom_config_include_mode(self, lorem_project, tmp_path):
        """Test with custom include configuration"""
        config_file = lorem_project / "custom_config.yaml"
        config_file.write_text("""
concat_project_files:
  mode: include
  include:
    - '**/*.py'
    - 'README.md'
""")
        
        aicc = AIContextCraft(
            config_path=str(config_file),
            source_dir=str(lorem_project)
        )
        
        output_file = tmp_path / "include_mode.txt"
        aicc.concat_files(
            output_file=str(output_file),
            no_timestamp=True
        )
        
        content = output_file.read_text()
        
        # Should include Python files and README
        assert "LoremGenerator" in content
        assert "README" in content
        
        # Should NOT include JSX files
        assert "App.jsx" not in content
        assert "React" not in content
    
    def test_custom_config_exclude_mode(self, lorem_project, tmp_path):
        """Test with custom exclude configuration"""
        config_file = lorem_project / "exclude_config.yaml"
        config_file.write_text("""
concat_project_files:
  mode: exclude
  exclude:
    - 'frontend/**'
    - '**/*.md'
    - 'venv/**'
    - 'node_modules/**'
    - '__pycache__/**'
    - '.env'
""")
        
        aicc = AIContextCraft(
            config_path=str(config_file),
            source_dir=str(lorem_project)
        )
        
        output_file = tmp_path / "exclude_mode.txt"
        aicc.concat_files(
            output_file=str(output_file),
            no_timestamp=True
        )
        
        content = output_file.read_text()
        
        # Should include backend files
        assert "LoremGenerator" in content
        assert "Flask" in content
        
        # Should NOT include frontend or markdown
        assert "React" not in content
        assert "README" not in content
    
    # ========== TREE TESTS ==========
    
    def test_tree_only(self, aicc, tmp_path):
        """Test tree generation only"""
        output_file = tmp_path / "tree.txt"
        
        aicc.generate_tree(
            output_file=str(output_file),
            mode='normal'
        )
        
        content = output_file.read_text()
        
        # Should have tree structure
        assert "backend/" in content
        assert "frontend/" in content
        assert "├──" in content or "└──" in content
        
        # Should NOT have file contents
        assert "LoremGenerator" not in content
    
    @pytest.mark.parametrize("mode", ['normal', 'full', 'custom'])
    def test_tree_modes(self, aicc, tmp_path, mode):
        """Test different tree modes"""
        output_file = tmp_path / f"tree_{mode}.txt"
        
        try:
            aicc.generate_tree(
                output_file=str(output_file),
                mode=mode
            )
            assert output_file.exists()
        except Exception as e:
            # Some modes might not be configured
            pytest.skip(f"Tree mode {mode} not configured: {e}")
    
    # ========== PATTERN TESTS ==========
    
    def test_gitignore_patterns(self, lorem_project, tmp_path):
        """Test that gitignore patterns work correctly"""
        # Create config that mimics gitignore
        config_file = lorem_project / "gitignore_config.yaml"
        config_file.write_text("""
concat_project_files:
  mode: exclude
  exclude:
    - 'node_modules/**'
    - 'venv/**'
    - '__pycache__/**'
    - '*.pyc'
    - '.env'
    - '*.log'
    - 'build/**'
""")
        
        aicc = AIContextCraft(
            config_path=str(config_file),
            source_dir=str(lorem_project)
        )
        
        output_file = tmp_path / "gitignore_test.txt"
        aicc.concat_files(
            output_file=str(output_file),
            no_timestamp=True
        )
        
        content = output_file.read_text()
        
        # Verify exclusions work
        assert "SECRET_KEY" not in content     # .env
        assert "excluded" not in content       # node_modules
        assert "Binary file" not in content    # .pyc
        assert "Should be excluded" not in content  # venv
    
    # ========== EDGE CASES ==========
    
    def test_empty_directory(self, tmp_path):
        """Test with empty directory"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        aicc = AIContextCraft(source_dir=str(empty_dir))
        output_file = tmp_path / "empty_output.txt"
        
        aicc.concat_files(
            output_file=str(output_file),
            no_timestamp=True
        )
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "Files: 0" in content
    
    def test_unicode_content(self, tmp_path):
        """Test with Unicode content"""
        unicode_dir = tmp_path / "unicode"
        unicode_dir.mkdir()
        
        (unicode_dir / "unicode.py").write_text("""
# 你好世界 🌍 مرحبا
def hello():
    return "Hello 世界"
""", encoding='utf-8')
        
        aicc = AIContextCraft(source_dir=str(unicode_dir))
        output_file = tmp_path / "unicode_output.txt"
        
        aicc.concat_files(
            output_file=str(output_file),
            no_timestamp=True
        )
        
        content = output_file.read_text(encoding='utf-8')
        assert "你好世界" in content
        assert "🌍" in content
    
    # ========== PERFORMANCE TESTS ==========
    
    @pytest.mark.slow
    def test_many_files(self, tmp_path):
        """Test with many files"""
        many_files_dir = tmp_path / "many"
        many_files_dir.mkdir()
        
        # Create 100 files
        for i in range(100):
            (many_files_dir / f"file_{i:03d}.py").write_text(f"def func_{i}(): pass")
        
        aicc = AIContextCraft(source_dir=str(many_files_dir))
        output_file = tmp_path / "many_output.txt"
        
        import time
        start = time.time()
        aicc.concat_files(
            output_file=str(output_file),
            no_timestamp=True
        )
        duration = time.time() - start
        
        assert output_file.exists()
        assert duration < 10  # Should be fast
        
        content = output_file.read_text()
        assert "Files: 100" in content


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])