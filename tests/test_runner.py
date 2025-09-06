#!/usr/bin/env python3
"""
AI Context Craft - Test Runner
Main test orchestrator using Python and pytest
"""

import os
import sys
import json
import time
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import pytest
import click
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich import print as rprint

# Initialize Rich console for beautiful output
console = Console()

@dataclass
class TestResult:
    """Test result data class"""
    name: str
    group: str
    passed: bool
    duration: float
    output: str
    error: Optional[str] = None

class AIContextCraftTester:
    """Main test orchestrator for AI Context Craft"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_dir = project_root / "tests"
        self.test_project = self.test_dir / "test-project"
        self.test_configs = self.test_dir / "test-configs"
        self.results_dir = self.test_dir / "test-results"
        self.results: List[TestResult] = []
        
        # Create directories
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Docker image name
        self.docker_image = "aicontextcraft:test"
        
    def setup_environment(self) -> bool:
        """Setup test environment"""
        console.print("[bold blue]Setting up test environment...[/bold blue]")
        
        # Check if test project exists
        if not self.test_project.exists():
            console.print("[yellow]Test project not found. Creating...[/yellow]")
            if not self.create_test_project():
                return False
        
        # Build Docker image
        if not self.build_docker_image():
            return False
            
        console.print("[green]✅ Environment ready![/green]")
        return True
    
    def create_test_project(self) -> bool:
        """Create the Lorem Ipsum test project"""
        setup_script = self.test_dir / "test-project-setup.sh"
        if setup_script.exists():
            result = subprocess.run(
                ["bash", str(setup_script)],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        else:
            console.print("[red]test-project-setup.sh not found![/red]")
            return False
    
    def build_docker_image(self) -> bool:
        """Build Docker test image"""
        console.print("[yellow]Building Docker image...[/yellow]")
        
        result = subprocess.run(
            ["docker", "build", "-t", self.docker_image, str(self.project_root)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print(f"[green]✅ Docker image {self.docker_image} built[/green]")
            return True
        else:
            console.print(f"[red]Failed to build Docker image: {result.stderr}[/red]")
            return False
    
    def run_docker_command(self, 
                          command: str, 
                          working_dir: Optional[Path] = None,
                          config_file: Optional[Path] = None,
                          timeout: int = 30) -> Tuple[int, str, str]:
        """
        Run a command in Docker container
        
        Returns: (exit_code, stdout, stderr)
        """
        if working_dir is None:
            working_dir = self.test_project
            
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{working_dir}:/workspace",
        ]
        
        # Add config file if specified
        if config_file:
            docker_cmd.extend([
                "-v", f"{config_file}:/workspace/config.yaml:ro"
            ])
        
        docker_cmd.extend([
            self.docker_image,
            *command.split()
        ])
        
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
    
    def run_test(self, 
                 name: str, 
                 group: str,
                 description: str,
                 command: str,
                 expected_exit_code: int = 0,
                 config_file: Optional[Path] = None,
                 validate_output: Optional[callable] = None) -> TestResult:
        """Run a single test"""
        
        console.print(f"[cyan]🧪 Testing: {name}[/cyan]")
        console.print(f"   {description}")
        
        start_time = time.time()
        
        # Run command
        exit_code, stdout, stderr = self.run_docker_command(
            command, 
            config_file=config_file
        )
        
        duration = time.time() - start_time
        
        # Check basic success
        passed = (exit_code == expected_exit_code)
        
        # Additional output validation if provided
        if passed and validate_output:
            try:
                passed = validate_output(stdout)
            except Exception as e:
                passed = False
                stderr += f"\nValidation error: {str(e)}"
        
        # Create result
        result = TestResult(
            name=name,
            group=group,
            passed=passed,
            duration=duration,
            output=stdout,
            error=stderr if not passed else None
        )
        
        self.results.append(result)
        
        # Display result
        if passed:
            console.print(f"   [green]✅ PASSED ({duration:.2f}s)[/green]")
        else:
            console.print(f"   [red]❌ FAILED ({duration:.2f}s)[/red]")
            if stderr:
                console.print(f"   [red]Error: {stderr[:200]}[/red]")
        
        return result
    
    def save_results(self, format: str = "json"):
        """Save test results"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        
        if format == "json":
            output_file = self.results_dir / f"results-{timestamp}.json"
            with open(output_file, 'w') as f:
                json.dump([{
                    "name": r.name,
                    "group": r.group,
                    "passed": r.passed,
                    "duration": r.duration,
                    "error": r.error
                } for r in self.results], f, indent=2)
        
        elif format == "html":
            # Generate HTML report
            output_file = self.results_dir / f"report-{timestamp}.html"
            self.generate_html_report(output_file)
        
        console.print(f"[blue]Results saved to: {output_file}[/blue]")
        return output_file
    
    def generate_html_report(self, output_file: Path):
        """Generate HTML test report"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Context Craft - Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                .summary { background: #f0f0f0; padding: 10px; margin: 20px 0; }
                .passed { color: green; }
                .failed { color: red; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background: #4CAF50; color: white; }
                tr:nth-child(even) { background: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>AI Context Craft - Test Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total: {total}</p>
                <p class="passed">Passed: {passed}</p>
                <p class="failed">Failed: {failed}</p>
                <p>Pass Rate: {pass_rate:.1f}%</p>
            </div>
            <table>
                <tr>
                    <th>Test</th>
                    <th>Group</th>
                    <th>Status</th>
                    <th>Duration</th>
                    <th>Error</th>
                </tr>
                {rows}
            </table>
        </body>
        </html>
        """
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        rows = ""
        for r in self.results:
            status = "✅ PASS" if r.passed else "❌ FAIL"
            status_class = "passed" if r.passed else "failed"
            error = r.error[:100] if r.error else ""
            rows += f"""
                <tr>
                    <td>{r.name}</td>
                    <td>{r.group}</td>
                    <td class="{status_class}">{status}</td>
                    <td>{r.duration:.2f}s</td>
                    <td>{error}</td>
                </tr>
            """
        
        html = html_content.format(
            total=total,
            passed=passed,
            failed=failed,
            pass_rate=pass_rate,
            rows=rows
        )
        
        with open(output_file, 'w') as f:
            f.write(html)
    
    def print_summary(self):
        """Print test summary"""
        console.print("\n[bold blue]═══════════════════════════════════════[/bold blue]")
        console.print("[bold blue]           TEST SUMMARY[/bold blue]")
        console.print("[bold blue]═══════════════════════════════════════[/bold blue]\n")
        
        # Create summary table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        pass_rate = (passed / total * 100) if total > 0 else 0
        total_duration = sum(r.duration for r in self.results)
        
        table.add_row("Total Tests", str(total))
        table.add_row("Passed", f"[green]{passed}[/green]")
        table.add_row("Failed", f"[red]{failed}[/red]" if failed > 0 else "0")
        table.add_row("Pass Rate", f"{pass_rate:.1f}%")
        table.add_row("Total Duration", f"{total_duration:.2f}s")
        
        console.print(table)
        
        # Show failed tests if any
        if failed > 0:
            console.print("\n[red]Failed Tests:[/red]")
            for r in self.results:
                if not r.passed:
                    console.print(f"  • {r.name}: {r.error[:100] if r.error else 'Unknown error'}")
        
        return pass_rate == 100

@click.command()
@click.option('--setup', is_flag=True, help='Setup test environment only')
@click.option('--groups', '-g', multiple=True, help='Test groups to run')
@click.option('--quick', is_flag=True, help='Run quick tests only')
@click.option('--full', is_flag=True, help='Run all tests')
@click.option('--report', type=click.Choice(['json', 'html']), default='json', help='Report format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(setup, groups, quick, full, report, verbose):
    """AI Context Craft Test Runner"""
    
    # Determine project root
    project_root = Path(__file__).parent.parent
    
    # Create tester instance
    tester = AIContextCraftTester(project_root)
    
    # Setup environment
    if not tester.setup_environment():
        console.print("[red]Failed to setup environment![/red]")
        sys.exit(1)
    
    if setup:
        console.print("[green]Setup complete![/green]")
        return
    
    # Import test groups
    from test_groups import basic, config, patterns, edge_cases, features
    
    # Determine which groups to run
    if groups:
        test_modules = []
        for g in groups:
            if g == 'basic':
                test_modules.append(basic)
            elif g == 'config':
                test_modules.append(config)
            elif g == 'patterns':
                test_modules.append(patterns)
            elif g == 'edge':
                test_modules.append(edge_cases)
            elif g == 'features':
                test_modules.append(features)
    elif quick:
        test_modules = [basic]
    elif full:
        test_modules = [basic, config, patterns, edge_cases, features]
    else:
        test_modules = [basic, config, patterns]
    
    # Run tests from each module
    for module in test_modules:
        module.run_tests(tester)
    
    # Print summary
    success = tester.print_summary()
    
    # Save results
    tester.save_results(format=report)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()