#!/usr/bin/env python3
"""
Simplified test runner that doesn't rebuild Docker images
Assumes images are already built by the Makefile
"""

import sys
import subprocess
import json
import time
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class TestResult:
    """Test result data class"""
    name: str
    group: str
    passed: bool
    duration: float
    output: str
    error: str = ""

class SimpleTestRunner:
    """Simplified test runner for AI Context Craft"""
    
    def __init__(self):
        self.test_dir = Path("/app/tests")
        self.test_project = self.test_dir / "test-project"
        self.results_dir = self.test_dir / "test-results"
        self.results: List[TestResult] = []
        self.docker_image = "aicontextcraft:test"
        
        # Create directories
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def run_docker_command(self, command: str, timeout: int = 30) -> Tuple[int, str, str]:
        """Run a command in the aicontextcraft:test container"""
        
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{self.test_project}:/workspace",
            "-w", "/workspace",
            self.docker_image,
            *command.split()
        ]
        
        try:
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 124, "", "Command timed out"
        except Exception as e:
            return 1, "", str(e)
    
    def run_test(self, name: str, group: str, description: str, 
                 command: str, expected_exit_code: int = 0) -> TestResult:
        """Run a single test"""
        
        print(f"🧪 Testing: {name}")
        print(f"   {description}")
        
        start_time = time.time()
        exit_code, stdout, stderr = self.run_docker_command(command)
        duration = time.time() - start_time
        
        passed = (exit_code == expected_exit_code)
        
        result = TestResult(
            name=name,
            group=group,
            passed=passed,
            duration=duration,
            output=stdout,
            error=stderr if not passed else ""
        )
        
        self.results.append(result)
        
        if passed:
            print(f"   ✅ PASSED ({duration:.2f}s)")
        else:
            print(f"   ❌ FAILED ({duration:.2f}s)")
            if stderr:
                print(f"   Error: {stderr[:200]}")
        
        return result
    
    def run_basic_tests(self):
        """Run basic functionality tests"""
        print("\n═══ Basic Tests ═══\n")
        
        # Test 1: Help command
        self.run_test(
            name="basic-help",
            group="basic",
            description="Check help command",
            command="--help",
            expected_exit_code=0
        )
        
        # Test 2: Process directory
        self.run_test(
            name="basic-process",
            group="basic",
            description="Process test project",
            command=".",
            expected_exit_code=0
        )
        
        # Test 3: Tree generation
        self.run_test(
            name="basic-tree",
            group="basic",
            description="Generate tree",
            command=". --tree-only",
            expected_exit_code=0
        )
    
    def save_results(self):
        """Save test results to JSON"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_file = self.results_dir / f"results-{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump([{
                "name": r.name,
                "group": r.group,
                "passed": r.passed,
                "duration": r.duration,
                "error": r.error
            } for r in self.results], f, indent=2)
        
        print(f"\nResults saved to: {output_file}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n═══════════════════════════════════════")
        print("           TEST SUMMARY")
        print("═══════════════════════════════════════\n")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if failed > 0:
            print("\nFailed Tests:")
            for r in self.results:
                if not r.passed:
                    print(f"  • {r.name}")
        
        return passed == total

def main():
    """Main entry point"""
    print("AI Context Craft - Simple Test Runner")
    print("=====================================\n")
    
    runner = SimpleTestRunner()
    
    # Check if test project exists
    if not runner.test_project.exists():
        print("❌ Test project not found at:", runner.test_project)
        print("Please run: bash tests/test-project-setup.sh")
        sys.exit(1)
    
    # Run tests
    runner.run_basic_tests()
    
    # Save results and print summary
    runner.save_results()
    success = runner.print_summary()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()