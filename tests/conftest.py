#!/usr/bin/env python3
"""
tests/conftest.py - Pytest configuration with AI-friendly reports
Generates both HTML and text/markdown reports
"""

import pytest
import json
from datetime import datetime
from pathlib import Path

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")

class AIReportPlugin:
    """Generate AI-friendly test reports in text/markdown format"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.total_duration = 0
    
    def pytest_sessionstart(self):
        self.start_time = datetime.now()
    
    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            self.results.append({
                'test': report.nodeid,
                'outcome': report.outcome,
                'duration': report.duration,
                'error': str(report.longrepr) if report.failed else None
            })
    
    def pytest_sessionfinish(self, session):
        self.total_duration = (datetime.now() - self.start_time).total_seconds()
        self.generate_reports(session)
    
    def generate_reports(self, session):
        """Generate multiple report formats"""
        report_dir = Path("tests/test-results")
        report_dir.mkdir(exist_ok=True, parents=True)
        
        # Generate text report for AI
        self.generate_text_report(report_dir / "report.txt")
        
        # Generate markdown report
        self.generate_markdown_report(report_dir / "report.md")
        
        # Generate JSON report for parsing
        self.generate_json_report(report_dir / "report.json")
    
    def generate_text_report(self, filepath):
        """Generate plain text report optimized for AI analysis"""
        passed = [r for r in self.results if r['outcome'] == 'passed']
        failed = [r for r in self.results if r['outcome'] == 'failed']
        
        with open(filepath, 'w') as f:
            f.write("AI CONTEXT CRAFT - TEST REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary
            f.write(f"SUMMARY:\n")
            f.write(f"Total tests: {len(self.results)}\n")
            f.write(f"Passed: {len(passed)}\n")
            f.write(f"Failed: {len(failed)}\n")
            f.write(f"Pass rate: {len(passed)/len(self.results)*100:.1f}%\n")
            f.write(f"Duration: {self.total_duration:.2f}s\n\n")
            
            # Failed tests details
            if failed:
                f.write("FAILED TESTS:\n")
                f.write("-" * 30 + "\n")
                for test in failed:
                    f.write(f"\nTest: {test['test']}\n")
                    f.write(f"Error: {test['error']}\n")
            
            # All tests list
            f.write("\nALL TESTS:\n")
            f.write("-" * 30 + "\n")
            for test in self.results:
                status = "✓" if test['outcome'] == 'passed' else "✗"
                f.write(f"{status} {test['test']} ({test['duration']:.3f}s)\n")
    
    def generate_markdown_report(self, filepath):
        """Generate markdown report for documentation"""
        passed = [r for r in self.results if r['outcome'] == 'passed']
        failed = [r for r in self.results if r['outcome'] == 'failed']
        
        with open(filepath, 'w') as f:
            f.write("# Test Report - AI Context Craft\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary table
            f.write("## Summary\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| Total Tests | {len(self.results)} |\n")
            f.write(f"| Passed | {len(passed)} ✅ |\n")
            f.write(f"| Failed | {len(failed)} ❌ |\n")
            f.write(f"| Pass Rate | {len(passed)/len(self.results)*100:.1f}% |\n")
            f.write(f"| Duration | {self.total_duration:.2f}s |\n\n")
            
            # Failed tests
            if failed:
                f.write("## Failed Tests\n\n")
                for test in failed:
                    f.write(f"### ❌ {test['test']}\n")
                    f.write("```\n")
                    f.write(f"{test['error']}\n")
                    f.write("```\n\n")
            
            # Test details
            f.write("## Test Details\n\n")
            for test in self.results:
                emoji = "✅" if test['outcome'] == 'passed' else "❌"
                f.write(f"- {emoji} `{test['test']}` - {test['duration']:.3f}s\n")
    
    def generate_json_report(self, filepath):
        """Generate JSON report for programmatic analysis"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(self.results),
                'passed': len([r for r in self.results if r['outcome'] == 'passed']),
                'failed': len([r for r in self.results if r['outcome'] == 'failed']),
                'duration': self.total_duration
            },
            'tests': self.results
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)

# Register the plugin
ai_report = AIReportPlugin()

def pytest_configure(config):
    """Register our custom plugin"""
    config.pluginmanager.register(ai_report, "ai_report")

@pytest.fixture(scope="session")
def project_root():
    """Return project root directory"""
    return Path(__file__).parent.parent

@pytest.fixture(scope="session")
def test_dir():
    """Return test directory"""
    return Path(__file__).parent