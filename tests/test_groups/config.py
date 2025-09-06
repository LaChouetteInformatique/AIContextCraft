#!/usr/bin/env python3
"""
Configuration tests for AI Context Craft
"""

from pathlib import Path
from typing import Any
import tempfile
import yaml

def run_tests(tester: Any) -> None:
    """Run configuration tests"""
    
    print("\n[bold magenta]═══ Configuration Tests ═══[/bold magenta]")
    
    # Create test configurations
    configs_dir = tester.test_configs
    configs_dir.mkdir(exist_ok=True)
    
    # Config 1: Python only
    python_config = configs_dir / "python-only.yaml"
    with open(python_config, 'w') as f:
        yaml.dump({
            'concat_project_files': {
                'mode': 'include',
                'include': ['**/*.py'],
                'exclude': ['venv/**', '__pycache__/**']
            }
        }, f)
    
    # Config 2: JavaScript only
    js_config = configs_dir / "javascript-only.yaml"
    with open(js_config, 'w') as f:
        yaml.dump({
            'concat_project_files': {
                'mode': 'include',
                'include': ['**/*.js', '**/*.jsx', '**/*.ts', '**/*.tsx'],
                'exclude': ['node_modules/**', 'build/**', 'dist/**']
            }
        }, f)
    
    # Config 3: Documentation only
    docs_config = configs_dir / "docs-only.yaml"
    with open(docs_config, 'w') as f:
        yaml.dump({
            'concat_project_files': {
                'mode': 'include',
                'include': ['**/*.md', 'docs/**'],
                'exclude': ['node_modules/**']
            }
        }, f)
    
    # Config 4: Exclude mode
    exclude_config = configs_dir / "exclude-mode.yaml"
    with open(exclude_config, 'w') as f:
        yaml.dump({
            'concat_project_files': {
                'mode': 'exclude',
                'exclude': [
                    '**/*.log', '**/*.pyc', '.env*',
                    'venv/**', 'node_modules/**', '__pycache__/**',
                    'build/**', 'dist/**', '.git/**'
                ]
            }
        }, f)
    
    # Config 5: Complex patterns
    complex_config = configs_dir / "complex-patterns.yaml"
    with open(complex_config, 'w') as f:
        yaml.dump({
            'concat_project_files': {
                'mode': 'include',
                'include': [
                    'backend/**/*.py',
                    'frontend/src/**/*.jsx',
                    'frontend/src/**/*.tsx',
                    '*.md',
                    'config.yaml'
                ],
                'exclude': [
                    '**/tests/**',
                    '**/*.test.*',
                    '**/*.spec.*'
                ]
            }
        }, f)
    
    # Test 1: Python-only config
    tester.run_test(
        name="config-python-only",
        group="config",
        description="Use Python-only configuration",
        command=".",
        config_file=python_config,
        expected_exit_code=0,
        validate_output=lambda out: ".py" in out and ".jsx" not in out and ".js" not in out
    )
    
    # Test 2: JavaScript-only config
    tester.run_test(
        name="config-js-only",
        group="config",
        description="Use JavaScript-only configuration",
        command=".",
        config_file=js_config,
        expected_exit_code=0,
        validate_output=lambda out: (".jsx" in out or ".js" in out) and ".py" not in out
    )
    
    # Test 3: Documentation-only config
    tester.run_test(
        name="config-docs-only",
        group="config",
        description="Use documentation-only configuration",
        command=".",
        config_file=docs_config,
        expected_exit_code=0,
        validate_output=lambda out: "README.md" in out or ".md" in out
    )
    
    # Test 4: Exclude mode config
    tester.run_test(
        name="config-exclude-mode",
        group="config",
        description="Use exclude mode configuration",
        command=".",
        config_file=exclude_config,
        expected_exit_code=0,
        validate_output=lambda out: "node_modules" not in out and "__pycache__" not in out
    )
    
    # Test 5: Complex patterns config
    tester.run_test(
        name="config-complex",
        group="config",
        description="Use complex pattern configuration",
        command=".",
        config_file=complex_config,
        expected_exit_code=0,
        validate_output=lambda out: "backend" in out and "frontend/src" in out and "tests" not in out
    )
    
    # Test 6: Override config with CLI
    tester.run_test(
        name="config-cli-override",
        group="config",
        description="Override config with CLI arguments",
        command=". --include **/*.md",
        config_file=python_config,
        expected_exit_code=0,
        validate_output=lambda out: ".md" in out  # Should include MD files despite Python-only config
    )
    
    # Test 7: Invalid config handling
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: content: !!!")
        invalid_config = Path(f.name)
    
    tester.run_test(
        name="config-invalid",
        group="config",
        description="Handle invalid configuration gracefully",
        command=".",
        config_file=invalid_config,
        expected_exit_code=1,  # Should fail
        validate_output=lambda out: True  # Any output is fine, we expect it to fail
    )
    invalid_config.unlink()  # Clean up
    
    # Test 8: Missing config file
    tester.run_test(
        name="config-missing",
        group="config",
        description="Handle missing config file",
        command=". --config /nonexistent/config.yaml",
        expected_exit_code=1,  # Should fail
        validate_output=lambda out: True
    )
    
    # Test 9: Empty config
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("")
        empty_config = Path(f.name)
    
    tester.run_test(
        name="config-empty",
        group="config",
        description="Handle empty configuration",
        command=".",
        config_file=empty_config,
        expected_exit_code=0,  # Should work with defaults
        validate_output=lambda out: len(out) > 100  # Should produce output
    )
    empty_config.unlink()  # Clean up
    
    # Test 10: Config with only includes
    include_only_config = configs_dir / "include-only.yaml"
    with open(include_only_config, 'w') as f:
        yaml.dump({
            'concat_project_files': {
                'mode': 'include',
                'include': ['backend/main.py']
            }
        }, f)
    
    tester.run_test(
        name="config-include-only",
        group="config",
        description="Config with only specific file",
        command=".",
        config_file=include_only_config,
        expected_exit_code=0,
        validate_output=lambda out: "main.py" in out and out.count("backend") >= 1
    )
    
    # Test 11: Config with deep patterns
    deep_config = configs_dir / "deep-patterns.yaml"
    with open(deep_config, 'w') as f:
        yaml.dump({
            'concat_project_files': {
                'mode': 'include',
                'include': ['backend/api/v1/*.py']
            }
        }, f)
    
    tester.run_test(
        name="config-deep-patterns",
        group="config",
        description="Config with deep directory patterns",
        command=".",
        config_file=deep_config,
        expected_exit_code=0,
        validate_output=lambda out: "endpoints.py" in out or "api/v1" in out
    )
    
    # Test 12: Config validation via validate_config.py
    tester.run_test(
        name="config-validation-script",
        group="config",
        description="Validate configuration using validation script",
        command="python validate_config.py",
        expected_exit_code=0,
        validate_output=lambda out: "valid" in out.lower() or not "error" in out.lower()
    )