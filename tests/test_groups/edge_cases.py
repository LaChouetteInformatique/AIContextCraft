"""
Edge case tests for AI Context Craft
"""

import tempfile
import os
from pathlib import Path

def run_edge_cases_tests(tester):
    """Run edge case tests"""
    
    print("\n[bold magenta]═══ Edge Cases Tests ═══[/bold magenta]")
    
    # Test empty directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tester.run_test(
            name="edge-empty-dir",
            group="edge",
            description="Handle empty directory",
            command=".",
            working_dir=Path(tmpdir),
            expected_exit_code=0,
            validate_output=lambda out: True  # Should handle gracefully
        )
    
    # Test non-existent directory
    tester.run_test(
        name="edge-nonexistent-dir",
        group="edge",
        description="Handle non-existent directory",
        command="/nonexistent/path",
        expected_exit_code=1,  # Should fail
        validate_output=lambda out: True
    )
    
    # Test directory without permissions
    with tempfile.TemporaryDirectory() as tmpdir:
        noperm_dir = Path(tmpdir) / "noperm"
        noperm_dir.mkdir()
        noperm_dir.chmod(0o000)
        
        tester.run_test(
            name="edge-no-permissions",
            group="edge",
            description="Handle directory without read permissions",
            command=".",
            working_dir=noperm_dir,
            expected_exit_code=1,  # Should fail gracefully
            validate_output=lambda out: True
        )
        
        # Restore permissions for cleanup
        noperm_dir.chmod(0o755)
    
    # Test circular symlinks
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        # Create circular symlink
        (tmppath / "circular").symlink_to(tmppath)
        
        tester.run_test(
            name="edge-circular-symlink",
            group="edge",
            description="Handle circular symbolic links",
            command=".",
            working_dir=tmppath,
            expected_exit_code=0,  # Should handle without infinite loop
            validate_output=lambda out: True,
            timeout=5  # Ensure it doesn't hang
        )
    
    # Test very long filenames
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        long_name = "a" * 255  # Max filename length on most systems
        (tmppath / f"{long_name}.py").write_text("# Test")
        
        tester.run_test(
            name="edge-long-filename",
            group="edge",
            description="Handle very long filenames",
            command=".",
            working_dir=tmppath,
            expected_exit_code=0,
            validate_output=lambda out: len(out) > 0
        )
    
    # Test special characters in filenames
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        # Create files with special characters
        (tmppath / "file with spaces.py").write_text("# Test")
        (tmppath / "file@#$%.py").write_text("# Test")
        (tmppath / "file'with\"quotes.py").write_text("# Test")
        
        tester.run_test(
            name="edge-special-chars",
            group="edge",
            description="Handle special characters in filenames",
            command=".",
            working_dir=tmppath,
            expected_exit_code=0,
            validate_output=lambda out: len(out) > 0
        )
    
    # Test binary files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        # Create a binary file
        (tmppath / "binary.dat").write_bytes(b'\x00\x01\x02\x03\x04')
        
        tester.run_test(
            name="edge-binary-files",
            group="edge",
            description="Handle binary files appropriately",
            command=". --include **/*.dat",
            working_dir=tmppath,
            expected_exit_code=0,
            validate_output=lambda out: "binary" in out.lower() or "skipped" in out.lower() or len(out) > 0
        )
    
    # Test very large file
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        # Create a large file (10MB)
        large_content = "x" * (10 * 1024 * 1024)
        (tmppath / "large.txt").write_text(large_content)
        
        tester.run_test(
            name="edge-large-file",
            group="edge",
            description="Handle very large files",
            command=".",
            working_dir=tmppath,
            expected_exit_code=0,
            validate_output=lambda out: len(out) > 1000,
            timeout=30  # Give more time for large file
        )
    
    # Test Unicode content
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        # Create file with Unicode content
        (tmppath / "unicode.py").write_text(
            "# 你好世界 🌍 Здравствуй мир\n"
            "def hello():\n"
            "    return '안녕하세요'"
        )
        
        tester.run_test(
            name="edge-unicode",
            group="edge",
            description="Handle Unicode content properly",
            command=".",
            working_dir=tmppath,
            expected_exit_code=0,
            validate_output=lambda out: "你好世界" in out or "hello" in out
        )
    
    # Test mixed line endings
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        # Create file with mixed line endings
        with open(tmppath / "mixed.txt", "wb") as f:
            f.write(b"line1\r\nline2\nline3\r\n")
        
        tester.run_test(
            name="edge-line-endings",
            group="edge",
            description="Handle mixed line endings (CRLF/LF)",
            command=".",
            working_dir=tmppath,
            expected_exit_code=0,
            validate_output=lambda out: "line1" in out and "line2" in out
        )