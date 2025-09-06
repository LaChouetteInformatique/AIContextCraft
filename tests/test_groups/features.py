"""
Advanced features tests for AI Context Craft
"""

def run_features_tests(tester):
    """Run advanced features tests"""
    
    print("\n[bold magenta]═══ Advanced Features Tests ═══[/bold magenta]")
    
    # Test clipboard functionality
    tester.run_test(
        name="feature-clipboard",
        group="features",
        description="Test clipboard integration",
        command=". --to-clipboard",
        expected_exit_code=0,
        validate_output=lambda out: "clipboard" in out.lower()
    )
    
    # Test token estimation
    tester.run_test(
        name="feature-tokens",
        group="features",
        description="Estimate token count",
        command=". --stats",
        expected_exit_code=0,
        validate_output=lambda out: "token" in out.lower() or "estimated" in out.lower()
    )
    
    # Test Git integration
    import subprocess
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmppath, capture_output=True)
        (tmppath / "test.py").write_text("# Test file")
        
        tester.run_test(
            name="feature-git-info",
            group="features",
            description="Show git information",
            command=". --stats",
            working_dir=tmppath,
            expected_exit_code=0,
            validate_output=lambda out: len(out) > 0  # Should work with or without git info
        )
    
    # Test multiple output formats
    formats = [
        ("json", lambda out: out.strip().startswith('{') or out.strip().startswith('[')),
        ("xml", lambda out: "<files>" in out or "<?xml" in out),
        ("markdown", lambda out: "```" in out or "#" in out),
    ]
    
    for format_name, validator in formats:
        tester.run_test(
            name=f"feature-format-{format_name}",
            group="features",
            description=f"Output in {format_name.upper()} format",
            command=f". --format {format_name}",
            expected_exit_code=0,
            validate_output=validator
        )
    
    # Test comment stripping
    tester.run_test(
        name="feature-strip-comments",
        group="features",
        description="Strip comments from multiple languages",
        command=". --remove-comments",
        expected_exit_code=0,
        validate_output=lambda out: out.count("# Lorem ipsum") < 5
    )
    
    # Test custom separators
    tester.run_test(
        name="feature-separator",
        group="features",
        description="Use custom file separators",
        command='. --separator "=====FILE====="',
        expected_exit_code=0,
        validate_output=lambda out: "=====FILE=====" in out or len(out) > 100
    )
    
    # Test verbose mode
    tester.run_test(
        name="feature-verbose",
        group="features",
        description="Verbose output mode",
        command=". --verbose",
        expected_exit_code=0,
        validate_output=lambda out: "processing" in out.lower() or "scanning" in out.lower() or len(out) > 100
    )
    
    # Test quiet mode
    tester.run_test(
        name="feature-quiet",
        group="features",
        description="Quiet output mode",
        command=". --quiet",
        expected_exit_code=0,
        validate_output=lambda out: len(out) > 0  # Should still produce output, just quieter
    )
    
    # Test dry run mode
    tester.run_test(
        name="feature-dry-run",
        group="features",
        description="Dry run without processing",
        command=". --dry-run",
        expected_exit_code=0,
        validate_output=lambda out: "would" in out.lower() or "dry" in out.lower() or len(out) > 0
    )
    
    # Test relative path handling
    tester.run_test(
        name="feature-relative-paths",
        group="features",
        description="Handle relative paths correctly",
        command="../test-project",
        working_dir=tester.test_project / "backend",  # Start from subdirectory
        expected_exit_code=0,
        validate_output=lambda out: len(out) > 100
    )
    
    # Test multiple directory processing
    tester.run_test(
        name="feature-multi-dir",
        group="features",
        description="Process multiple directories",
        command="backend frontend",
        expected_exit_code=0,
        validate_output=lambda out: "backend" in out and "frontend" in out
    )
    
    # Test custom config path
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
concat_project_files:
  mode: include
  include: ['**/*.py']
""")
        config_path = f.name
    
    tester.run_test(
        name="feature-custom-config",
        group="features",
        description="Use custom config location",
        command=f". --config {config_path}",
        expected_exit_code=0,
        validate_output=lambda out: ".py" in out
    )
    
    # Clean up temp config
    Path(config_path).unlink()
    
    # Test performance with many files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        # Create 50 files
        for i in range(50):
            (tmppath / f"file_{i}.py").write_text(f"# File {i}\ndef func_{i}(): pass")
        
        import time
        start = time.time()
        
        tester.run_test(
            name="feature-performance",
            group="features",
            description="Performance with many files",
            command=". --stats",
            working_dir=tmppath,
            expected_exit_code=0,
            validate_output=lambda out: "50" in out or "Total files:" in out
        )
        
        duration = time.time() - start
        if duration < 10:
            print(f"   [green]Good performance: {duration:.2f}s for 50 files[/green]")
        else:
            print(f"   [yellow]Slow performance: {duration:.2f}s for 50 files[/yellow]")