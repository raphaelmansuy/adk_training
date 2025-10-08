#!/usr/bin/env python3
"""
Master Test Runner for ADK Tutorial Series
Runs all tutorial tests and generates comprehensive report.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Terminal colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TutorialTestRunner:
    """Runs tests for all ADK tutorials."""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.results = {}
        self.start_time = None
        self.end_time = None
        
    def print_header(self, text: str):
        """Print formatted header."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")
    
    def print_section(self, text: str):
        """Print formatted section."""
        print(f"\n{Colors.OKCYAN}{Colors.BOLD}{text}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}{'-'*len(text)}{Colors.ENDC}")
    
    def print_success(self, text: str):
        """Print success message."""
        print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")
    
    def print_failure(self, text: str):
        """Print failure message."""
        print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")
    
    def print_warning(self, text: str):
        """Print warning message."""
        print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")
    
    def print_info(self, text: str):
        """Print info message."""
        print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")
    
    def check_prerequisites(self) -> bool:
        """Check if required tools are installed."""
        self.print_section("Checking Prerequisites")
        
        # Check Python
        try:
            python_version = sys.version.split()[0]
            self.print_success(f"Python {python_version} found")
        except Exception as e:
            self.print_failure(f"Python check failed: {e}")
            return False
        
        # Check pytest
        try:
            result = subprocess.run(
                ["pytest", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip().split()[1]
                self.print_success(f"pytest {version} found")
            else:
                self.print_failure("pytest not found. Install with: pip install pytest")
                return False
        except FileNotFoundError:
            self.print_failure("pytest not found. Install with: pip install pytest")
            return False
        
        return True
    
    def find_test_directories(self) -> List[Tuple[str, Path]]:
        """Find all tutorial test directories."""
        test_dirs = []
        
        for item in sorted(self.base_dir.iterdir()):
            if item.is_dir() and item.name.startswith("tutorial") and item.name.endswith("_test"):
                # Extract tutorial number
                tutorial_num = item.name.replace("tutorial", "").replace("_test", "")
                test_dirs.append((tutorial_num, item))
        
        return test_dirs
    
    def run_tutorial_tests(self, tutorial_num: str, test_dir: Path) -> Dict:
        """Run tests for a specific tutorial."""
        result = {
            "tutorial": tutorial_num,
            "status": "unknown",
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "duration": 0.0,
            "output": "",
            "error": None
        }
        
        # Find backend directory
        backend_dir = test_dir / "backend"
        if not backend_dir.exists():
            result["status"] = "no_tests"
            result["error"] = "No backend directory found"
            return result
        
        # Check for test files
        test_files = list(backend_dir.glob("test_*.py"))
        if not test_files:
            result["status"] = "no_tests"
            result["error"] = "No test files found"
            return result
        
        # Check for requirements.txt and offer to install
        requirements_file = backend_dir / "requirements.txt"
        if requirements_file.exists():
            self.print_info(f"Found requirements.txt for tutorial {tutorial_num}")
        
        # Run pytest with JSON output
        try:
            cmd = [
                "pytest",
                ".",
                "-v",
                "--tb=short",
                "--json-report",
                "--json-report-file",
                "test_report.json"
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=backend_dir
            )
            
            result["output"] = process.stdout
            
            # Try to parse JSON report
            json_report_file = backend_dir / "test_report.json"
            if json_report_file.exists():
                try:
                    with open(json_report_file) as f:
                        json_data = json.load(f)
                        result["passed"] = json_data.get("summary", {}).get("passed", 0)
                        result["failed"] = json_data.get("summary", {}).get("failed", 0)
                        result["skipped"] = json_data.get("summary", {}).get("skipped", 0)
                        result["duration"] = json_data.get("duration", 0.0)
                except Exception as e:
                    self.print_warning(f"Could not parse JSON report: {e}")
            
            # Parse output for test counts if JSON not available
            if result["passed"] == 0 and result["failed"] == 0:
                output_lines = process.stdout.split("\n")
                for line in output_lines:
                    if "passed" in line.lower():
                        # Extract numbers from pytest summary line
                        import re
                        numbers = re.findall(r'(\d+) passed', line)
                        if numbers:
                            result["passed"] = int(numbers[0])
                        numbers = re.findall(r'(\d+) failed', line)
                        if numbers:
                            result["failed"] = int(numbers[0])
            
            if process.returncode == 0:
                result["status"] = "success"
            elif process.returncode == 5:  # No tests collected
                result["status"] = "no_tests"
            else:
                result["status"] = "failed"
                
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def generate_report(self):
        """Generate and print comprehensive test report."""
        self.print_header("Test Results Summary")
        
        total_tutorials = len(self.results)
        successful = sum(1 for r in self.results.values() if r["status"] == "success")
        failed = sum(1 for r in self.results.values() if r["status"] == "failed")
        no_tests = sum(1 for r in self.results.values() if r["status"] == "no_tests")
        errors = sum(1 for r in self.results.values() if r["status"] == "error")
        
        total_passed = sum(r["passed"] for r in self.results.values())
        total_failed = sum(r["failed"] for r in self.results.values())
        total_skipped = sum(r["skipped"] for r in self.results.values())
        total_duration = sum(r["duration"] for r in self.results.values())
        
        # Overall summary
        print(f"\n{Colors.BOLD}Overall Summary:{Colors.ENDC}")
        print(f"  Total Tutorials: {total_tutorials}")
        print(f"  Successful:      {Colors.OKGREEN}{successful}{Colors.ENDC}")
        print(f"  Failed:          {Colors.FAIL}{failed}{Colors.ENDC}")
        print(f"  No Tests:        {Colors.WARNING}{no_tests}{Colors.ENDC}")
        print(f"  Errors:          {Colors.FAIL}{errors}{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Test Statistics:{Colors.ENDC}")
        print(f"  Tests Passed:    {Colors.OKGREEN}{total_passed}{Colors.ENDC}")
        print(f"  Tests Failed:    {Colors.FAIL}{total_failed}{Colors.ENDC}")
        print(f"  Tests Skipped:   {Colors.WARNING}{total_skipped}{Colors.ENDC}")
        print(f"  Total Duration:  {total_duration:.2f}s")
        
        # Detailed results
        self.print_section("Detailed Results")
        
        for tutorial_num in sorted(self.results.keys(), key=lambda x: int(x)):
            result = self.results[tutorial_num]
            status = result["status"]
            
            print(f"\n{Colors.BOLD}Tutorial {tutorial_num}:{Colors.ENDC}")
            
            if status == "success":
                self.print_success(
                    f"All tests passed ({result['passed']} tests, {result['duration']:.2f}s)"
                )
            elif status == "failed":
                self.print_failure(
                    f"Tests failed ({result['passed']} passed, {result['failed']} failed)"
                )
            elif status == "no_tests":
                self.print_warning(f"No tests found or not implemented yet")
            elif status == "error":
                self.print_failure(f"Error running tests: {result['error']}")
        
        # Time summary
        if self.start_time and self.end_time:
            elapsed = (self.end_time - self.start_time).total_seconds()
            print(f"\n{Colors.BOLD}Total execution time: {elapsed:.2f}s{Colors.ENDC}")
        
        # Save report to file
        self.save_report_to_file()
        
        return failed == 0 and errors == 0
    
    def save_report_to_file(self):
        """Save test report to JSON file."""
        report_file = self.base_dir / "test_report.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tutorials": len(self.results),
                "successful": sum(1 for r in self.results.values() if r["status"] == "success"),
                "failed": sum(1 for r in self.results.values() if r["status"] == "failed"),
                "no_tests": sum(1 for r in self.results.values() if r["status"] == "no_tests"),
                "errors": sum(1 for r in self.results.values() if r["status"] == "error"),
                "total_passed": sum(r["passed"] for r in self.results.values()),
                "total_failed": sum(r["failed"] for r in self.results.values()),
                "total_skipped": sum(r["skipped"] for r in self.results.values()),
                "total_duration": sum(r["duration"] for r in self.results.values())
            },
            "results": self.results
        }
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            self.print_success(f"Report saved to {report_file}")
        except Exception as e:
            self.print_warning(f"Could not save report: {e}")
    
    def run_all_tests(self) -> bool:
        """Run all tutorial tests."""
        self.start_time = datetime.now()
        
        self.print_header("ADK Tutorial Test Runner")
        
        # Check prerequisites
        if not self.check_prerequisites():
            self.print_failure("Prerequisites check failed")
            return False
        
        # Find test directories
        test_dirs = self.find_test_directories()
        
        if not test_dirs:
            self.print_warning("No test directories found")
            return False
        
        self.print_section(f"Found {len(test_dirs)} Tutorial Test(s)")
        for tutorial_num, test_dir in test_dirs:
            self.print_info(f"Tutorial {tutorial_num}: {test_dir}")
        
        # Run tests for each tutorial
        for tutorial_num, test_dir in test_dirs:
            self.print_section(f"Running Tests for Tutorial {tutorial_num}")
            result = self.run_tutorial_tests(tutorial_num, test_dir)
            self.results[tutorial_num] = result
            
            if result["status"] == "success":
                self.print_success(f"Tutorial {tutorial_num} tests passed")
            elif result["status"] == "failed":
                self.print_failure(f"Tutorial {tutorial_num} tests failed")
            elif result["status"] == "no_tests":
                self.print_warning(f"Tutorial {tutorial_num} has no tests")
            else:
                self.print_failure(f"Tutorial {tutorial_num} error: {result['error']}")
        
        self.end_time = datetime.now()
        
        # Generate final report
        return self.generate_report()


def main():
    """Main entry point."""
    runner = TutorialTestRunner()
    success = runner.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
