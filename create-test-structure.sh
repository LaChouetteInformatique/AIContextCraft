#!/bin/bash
# Setup script to create the Python-based test structure for AI Context Craft

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Setting up Python-based test structure...${NC}"

# Create directory structure
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p tests/test_groups
mkdir -p tests/test-configs
mkdir -p tests/test-results
mkdir -p tests/scenario-results

# Create empty Python test files
echo -e "${YELLOW}Creating Python test files...${NC}"

# Main test runner
touch tests/test_runner.py
chmod +x tests/test_runner.py

# Test groups as Python modules
touch tests/test_groups/__init__.py
touch tests/test_groups/basic.py
touch tests/test_groups/config.py
touch tests/test_groups/patterns.py
touch tests/test_groups/edge_cases.py
touch tests/test_groups/features.py

# Pytest integration
touch tests/test_aicc_integration.py
touch tests/conftest.py
touch tests/pytest.ini

# Docker files
touch tests/Dockerfile.test
touch docker-compose.test.yml

# Bash launcher
touch run-tests.sh
chmod +x run-tests.sh

# Test project setup (keep this in bash for simplicity)
touch tests/test-project-setup.sh
chmod +x tests/test-project-setup.sh

# Root Makefile
touch Makefile

# Create pytest.ini configuration
cat > tests/pytest.ini << 'EOF'
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --color=yes
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
EOF

# Create conftest.py for pytest fixtures
cat > tests/conftest.py << 'EOF'
"""
Pytest configuration and fixtures for AI Context Craft tests
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure pytest
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

# Shared fixtures can be added here
@pytest.fixture(scope="session")
def project_root():
    """Return project root directory"""
    return Path(__file__).parent.parent

@pytest.fixture(scope="session")
def test_dir():
    """Return test directory"""
    return Path(__file__).parent
EOF

# Create __init__.py for test_groups
cat > tests/test_groups/__init__.py << 'EOF'
"""
Test groups for AI Context Craft
Each module contains a group of related tests
"""

from . import basic
from . import config
from . import patterns
from . import edge_cases
from . import features

__all__ = ['basic', 'config', 'patterns', 'edge_cases', 'features']
EOF

# Create requirements for test environment
cat > tests/requirements-test.txt << 'EOF'
# Test dependencies
pytest==7.4.0
pytest-cov==4.1.0
pytest-timeout==2.1.0
pytest-xdist==3.3.1
pytest-html==3.2.0
pytest-docker==2.0.1
click==8.1.3
rich==13.5.2
pyyaml==6.0
docker==6.1.3
requests==2.31.0
psutil==5.9.5
EOF

# Create a simple Python test example
cat > tests/test_example.py << 'EOF'
"""
Example test file to verify pytest is working
"""

import pytest

def test_example_passing():
    """Example test that passes"""
    assert 1 + 1 == 2

def test_example_with_fixture(project_root):
    """Example test using a fixture"""
    assert project_root.exists()
    assert (project_root / "tests").exists()

@pytest.mark.slow
def test_example_slow():
    """Example slow test (marked for easy filtering)"""
    import time
    time.sleep(0.1)
    assert True

class TestExampleClass:
    """Example test class"""
    
    def test_in_class(self):
        """Test method in a class"""
        assert "ai-context-craft".replace("-", "_") == "ai_context_craft"
EOF

# Display created structure
echo -e "\n${GREEN}✅ Python test structure created!${NC}\n"
echo "Structure:"
echo "tests/"
echo "├── test_runner.py           # Main test orchestrator"
echo "├── test_groups/             # Test modules"
echo "│   ├── __init__.py"
echo "│   ├── basic.py            # Basic functionality tests"
echo "│   ├── config.py           # Configuration tests"
echo "│   ├── patterns.py         # Pattern matching tests"
echo "│   ├── edge_cases.py       # Edge case tests"
echo "│   └── features.py         # Feature tests"
echo "├── test_aicc_integration.py # Pytest integration tests"
echo "├── test_example.py          # Example pytest tests"
echo "├── conftest.py              # Pytest configuration"
echo "├── pytest.ini               # Pytest settings"
echo "├── requirements-test.txt    # Test dependencies"
echo "├── Dockerfile.test          # Test runner Docker image"
echo "└── test-project-setup.sh    # Test project creation"
echo ""
echo "Root files:"
echo "├── run-tests.sh             # Test launcher script"
echo "├── docker-compose.test.yml  # Docker compose config"
echo "└── Makefile                 # Make commands"

echo -e "\n${YELLOW}Files to populate:${NC}"
echo "1. tests/test_runner.py      → Copy from artifact: python-test-runner"
echo "2. tests/test_groups/basic.py → Copy from artifact: python-test-basic"
echo "3. tests/test_groups/config.py → Copy from artifact: python-test-config"
echo "4. tests/test_aicc_integration.py → Copy from artifact: pytest-integration"
echo "5. tests/Dockerfile.test     → Copy from artifact: python-test-dockerfile"
echo "6. docker-compose.test.yml   → Copy from artifact: python-test-docker-compose"
echo "7. run-tests.sh              → Copy from artifact: python-test-launcher"
echo "8. Makefile                  → Copy from artifact: python-test-makefile"
echo "9. tests/test-project-setup.sh → Copy from artifact: test-project-structure"

echo -e "\n${BLUE}Next steps:${NC}"
echo "1. Copy content from artifacts to files"
echo "2. Run: make setup"
echo "3. Run: make test"
echo ""
echo -e "${GREEN}Python test system ready for content!${NC}"