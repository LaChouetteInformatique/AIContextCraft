#!/usr/bin/env python3
"""
Basic functionality tests for AI Context Craft
"""

import json
from pathlib import Path
from typing import Any

def run_tests(tester: Any) -> None:
    """Run basic functionality tests"""
    
    print("\n[bold magenta]═══ Basic Functionality Tests ═══[/bold magenta]")
    
    # Test 1: Help command
    tester.run_test(
        name="basic-help",
        group="basic",
        description="Check if help command works",
        command="--help",
        expected_exit_code=0,
        validate_output=lambda out: "usage" in out.lower() or "help" in out.lower()
    )
    
    # Test 2: Process current directory
    tester.run_test(
        name="basic-process-dir",
        group="basic",
        description="Process test project directory",
        command=".",
        expected_exit_code=0,
        validate_output=lambda out: len(out) > 100  # Should have content
    )
    
    # Test 3: Tree generation
    tester.run_test(
        name="basic-tree",
        group="basic",
        description="Generate directory tree",
        command="--tree",
        expected_exit_code=0,
        validate_output=lambda out: "├──" in out or "└──" in out
    )
    
    # Test 4: Concat mode
    tester.run_test(
        name="basic-concat",
        group="basic",
        description="Concatenate files",
        command="--concat",
        expected_exit_code=0,
        validate_output=lambda out: "backend" in out and "frontend" in out
    )
    
    # Test 5: Output to file
    def validate_output_file(out):
        # Check if file was created
        output_file = Path("/tmp/test-output.txt")
        if output_file.exists():
            output_file.unlink()  # Clean up
            return True
        return "written to" in out.lower() or "saved to" in out.lower()
    
    tester.run_test(
        name="basic-output-file",
        group="basic",
        description="Output to specific file",
        command=". --output /tmp/test-output.txt",
        expected_exit_code=0,
        validate_output=validate_output_file
    )
    
    # Test 6: Line numbers
    tester.run_test(
        name="basic-line-numbers",
        group="basic",
        description="Include line numbers in output",
        command=". --line-numbers",
        expected_exit_code=0,
        validate_output=lambda out: any(line.strip().startswith(str(i)) 
                                       for i in range(1, 10) 
                                       for line in out.split('\n'))
    )
    
    # Test 7: Remove comments
    tester.run_test(
        name="basic-remove-comments",
        group="basic",
        description="Remove comments from code",
        command=". --remove-comments",
        expected_exit_code=0,
        validate_output=lambda out: out.count("# Lorem ipsum") < 5  # Most comments removed
    )
    
    # Test 8: Statistics
    tester.run_test(
        name="basic-stats",
        group="basic",
        description="Show file statistics",
        command=". --stats",
        expected_exit_code=0,
        validate_output=lambda out: "Total files:" in out or "total files:" in out.lower()
    )
    
    # Test 9: JSON output format
    def validate_json_output(out):
        try:
            json.loads(out)
            return True
        except json.JSONDecodeError:
            # Sometimes JSON might be wrapped in other output
            # Try to find JSON-like content
            if out.strip().startswith('{') or out.strip().startswith('['):
                # Try to extract JSON part
                for line in out.split('\n'):
                    if line.strip().startswith('{') or line.strip().startswith('['):
                        try:
                            json.loads(line)
                            return True
                        except:
                            continue
            return False
    
    tester.run_test(
        name="basic-json-format",
        group="basic",
        description="Output in JSON format",
        command=". --format json",
        expected_exit_code=0,
        validate_output=validate_json_output
    )
    
    # Test 10: XML output format
    tester.run_test(
        name="basic-xml-format",
        group="basic",
        description="Output in XML format",
        command=". --format xml",
        expected_exit_code=0,
        validate_output=lambda out: "<files>" in out or "<?xml" in out
    )
    
    # Test 11: Markdown output format
    tester.run_test(
        name="basic-markdown-format",
        group="basic",
        description="Output in Markdown format",
        command=". --format markdown",
        expected_exit_code=0,
        validate_output=lambda out: "```" in out or "#" in out
    )
    
    # Test 12: Process specific file
    tester.run_test(
        name="basic-specific-file",
        group="basic",
        description="Process specific file",
        command="backend/main.py",
        expected_exit_code=0,
        validate_output=lambda out: "LoremApplication" in out
    )
    
    # Test 13: Process multiple directories
    tester.run_test(
        name="basic-multi-dir",
        group="basic",
        description="Process multiple directories",
        command="backend frontend",
        expected_exit_code=0,
        validate_output=lambda out: "backend" in out and "frontend" in out
    )
    
    # Test 14: Verbose mode
    tester.run_test(
        name="basic-verbose",
        group="basic",
        description="Verbose output mode",
        command=". --verbose",
        expected_exit_code=0,
        validate_output=lambda out: "processing" in out.lower() or "scanning" in out.lower()
    )
    
    # Test 15: Dry run
    tester.run_test(
        name="basic-dry-run",
        group="basic",
        description="Dry run without processing",
        command=". --dry-run",
        expected_exit_code=0,
        validate_output=lambda out: "would process" in out.lower() or "dry run" in out.lower()
    )