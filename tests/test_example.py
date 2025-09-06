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
