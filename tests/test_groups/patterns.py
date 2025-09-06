"""
Pattern matching tests for AI Context Craft
"""

def run_patterns_tests(tester):
    """Run pattern matching tests"""
    
    print("\n[bold magenta]═══ Pattern Matching Tests ═══[/bold magenta]")
    
    # Test wildcard patterns
    tester.run_test(
        name="pattern-wildcard",
        group="patterns",
        description="Match files with wildcards",
        command=". --include **/*.py --include **/*.md",
        expected_exit_code=0,
        validate_output=lambda out: ".py" in out and ".md" in out
    )
    
    # Test specific directory patterns
    tester.run_test(
        name="pattern-specific-dir",
        group="patterns",
        description="Match files in specific directories",
        command=". --include backend/**/*.py",
        expected_exit_code=0,
        validate_output=lambda out: "backend" in out and "frontend" not in out
    )
    
    # Test exclude patterns
    tester.run_test(
        name="pattern-exclude",
        group="patterns",
        description="Exclude specific patterns",
        command=". --exclude **/*.log --exclude **/*.pyc",
        expected_exit_code=0,
        validate_output=lambda out: ".log" not in out and ".pyc" not in out
    )
    
    # Test mixed include/exclude
    tester.run_test(
        name="pattern-mixed",
        group="patterns",
        description="Mix include and exclude patterns",
        command=". --include **/*.py --exclude **/tests/**",
        expected_exit_code=0,
        validate_output=lambda out: ".py" in out and "/tests/" not in out
    )
    
    # Test extension-based patterns
    tester.run_test(
        name="pattern-extensions",
        group="patterns",
        description="Match by file extensions",
        command=". --include *.yaml --include *.json",
        expected_exit_code=0,
        validate_output=lambda out: (".yaml" in out or "config.yaml" in out) and ".json" in out
    )
    
    # Test deep directory patterns
    tester.run_test(
        name="pattern-deep",
        group="patterns",
        description="Match deeply nested files",
        command=". --include backend/api/v1/*.py",
        expected_exit_code=0,
        validate_output=lambda out: "endpoints.py" in out or "api/v1" in out
    )
    
    # Test root-only patterns
    tester.run_test(
        name="pattern-root",
        group="patterns",
        description="Match only root directory files",
        command=". --include *.md",
        expected_exit_code=0,
        validate_output=lambda out: "README.md" in out and "docs/" not in out.lower()
    )
    
    # Test complex glob patterns
    tester.run_test(
        name="pattern-glob-complex",
        group="patterns",
        description="Complex glob pattern matching",
        command=". --include frontend/src/**/*.{jsx,tsx}",
        expected_exit_code=0,
        validate_output=lambda out: ".jsx" in out or ".tsx" in out
    )
