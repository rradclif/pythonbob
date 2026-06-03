#!/usr/bin/env python3
"""
Package Update Checker and Security Scanner
Automatically checks for package updates and security vulnerabilities.
Run weekly to keep your project secure and up-to-date.
"""

import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path


class PackageUpdateChecker:
    """Check for package updates and security vulnerabilities."""
    
    def __init__(self):
        self.has_updates = False
        self.has_vulnerabilities = False
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'outdated_packages': [],
            'vulnerabilities': [],
            'pip_version': None
        }
    
    def print_header(self, text):
        """Print a formatted header."""
        print(f"\n{'='*70}")
        print(f"  {text}")
        print(f"{'='*70}\n")
    
    def print_section(self, text):
        """Print a formatted section header."""
        print(f"\n{'-'*70}")
        print(f"  {text}")
        print(f"{'-'*70}\n")
    
    def check_pip_version(self):
        """Check if pip itself needs updating."""
        try:
            result = subprocess.run(
                ['pip', '--version'],
                capture_output=True,
                text=True,
                check=True
            )
            self.results['pip_version'] = result.stdout.strip()
            print(f"✓ Current pip: {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error checking pip version: {e}")
    
    def check_outdated_packages(self):
        """Check for outdated packages."""
        self.print_section("Checking for Outdated Packages")
        
        try:
            result = subprocess.run(
                ['pip', 'list', '--outdated', '--format=json'],
                capture_output=True,
                text=True,
                check=True
            )
            
            outdated = json.loads(result.stdout)
            self.results['outdated_packages'] = outdated
            
            if outdated:
                self.has_updates = True
                print(f"⚠️  Found {len(outdated)} outdated package(s):\n")
                
                # Print table header
                print(f"{'Package':<25} {'Current':<15} {'Latest':<15} {'Type':<10}")
                print(f"{'-'*70}")
                
                # Print each outdated package
                for pkg in outdated:
                    name = pkg['name']
                    current = pkg['version']
                    latest = pkg['latest_version']
                    pkg_type = pkg.get('latest_filetype', 'wheel')
                    print(f"{name:<25} {current:<15} {latest:<15} {pkg_type:<10}")
                
                print(f"\n💡 To update all packages, run:")
                print(f"   pip install --upgrade -r requirements.txt")
                print(f"\n💡 To update specific packages, run:")
                print(f"   pip install --upgrade <package_name>")
            else:
                print("✓ All packages are up-to-date!")
                
        except subprocess.CalledProcessError as e:
            print(f"✗ Error checking outdated packages: {e}")
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing package list: {e}")
    
    def check_security_vulnerabilities(self):
        """Check for security vulnerabilities using pip-audit."""
        self.print_section("Checking for Security Vulnerabilities")
        
        # First check if pip-audit is installed
        try:
            subprocess.run(
                ['pip-audit', '--version'],
                capture_output=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  pip-audit is not installed.")
            print("   Install it with: pip install pip-audit")
            return
        
        try:
            result = subprocess.run(
                ['pip-audit', '--format=json'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✓ No known security vulnerabilities found!")
                self.results['vulnerabilities'] = []
            else:
                self.has_vulnerabilities = True
                try:
                    vulns = json.loads(result.stdout)
                    self.results['vulnerabilities'] = vulns.get('dependencies', [])
                    
                    print(f"🚨 SECURITY ALERT: Found vulnerabilities!\n")
                    
                    # Parse and display vulnerabilities
                    if 'dependencies' in vulns:
                        for dep in vulns['dependencies']:
                            pkg_name = dep.get('name', 'Unknown')
                            pkg_version = dep.get('version', 'Unknown')
                            
                            print(f"Package: {pkg_name} (v{pkg_version})")
                            
                            for vuln in dep.get('vulns', []):
                                vuln_id = vuln.get('id', 'Unknown')
                                description = vuln.get('description', 'No description')
                                fix_versions = vuln.get('fix_versions', [])
                                
                                print(f"  ⚠️  {vuln_id}")
                                print(f"      {description}")
                                if fix_versions:
                                    print(f"      Fix: Upgrade to {', '.join(fix_versions)}")
                                print()
                    
                    print(f"🔧 IMMEDIATE ACTION REQUIRED:")
                    print(f"   Update vulnerable packages immediately!")
                    
                except json.JSONDecodeError:
                    # Fallback to text output
                    print(result.stdout)
                    
        except Exception as e:
            print(f"✗ Error running security check: {e}")
    
    def check_requirements_file(self):
        """Check if requirements.txt exists and is readable."""
        self.print_section("Checking Requirements File")
        
        req_file = Path('requirements.txt')
        if req_file.exists():
            print(f"✓ Found requirements.txt")
            try:
                with open(req_file, 'r') as f:
                    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
                    print(f"✓ Contains {len(lines)} package specifications")
            except Exception as e:
                print(f"✗ Error reading requirements.txt: {e}")
        else:
            print(f"⚠️  requirements.txt not found in current directory")
    
    def test_imports(self):
        """Test that core modules can be imported."""
        self.print_section("Testing Core Module Imports")
        
        try:
            # Test browser_automation imports
            from browser_automation import BrowserController, ButtonChecker
            print("✓ browser_automation imports successful")
            print("  - BrowserController")
            print("  - ButtonChecker")
        except ImportError as e:
            print(f"✗ Import error: {e}")
    
    def generate_summary(self):
        """Generate a summary of findings."""
        self.print_header("Summary")
        
        if not self.has_updates and not self.has_vulnerabilities:
            print("✅ EXCELLENT! Your project is secure and up-to-date.")
            print("   No action required at this time.")
        else:
            if self.has_vulnerabilities:
                print("🚨 CRITICAL: Security vulnerabilities detected!")
                print("   Action: Update vulnerable packages immediately")
                print()
            
            if self.has_updates:
                print("⚠️  Package updates available")
                print("   Action: Review and update packages when convenient")
                print()
            
            print("Recommended actions:")
            if self.has_vulnerabilities:
                print("  1. Update vulnerable packages (URGENT)")
            if self.has_updates:
                print("  2. Review outdated packages")
                print("  3. Update non-critical packages")
            print("  4. Test functionality after updates")
            print("  5. Run this check again to verify")
        
        print(f"\n📅 Next check recommended: {self._get_next_check_date()}")
    
    def _get_next_check_date(self):
        """Calculate next recommended check date (1 week from now)."""
        from datetime import timedelta
        next_date = datetime.now() + timedelta(days=7)
        return next_date.strftime("%Y-%m-%d")
    
    def save_report(self):
        """Save results to a JSON file."""
        report_file = Path('package_check_report.json')
        try:
            with open(report_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\n📄 Detailed report saved to: {report_file}")
        except Exception as e:
            print(f"\n⚠️  Could not save report: {e}")
    
    def run(self):
        """Run all checks."""
        self.print_header("Package Update & Security Check")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Directory: {Path.cwd()}")
        
        self.check_pip_version()
        self.check_requirements_file()
        self.check_outdated_packages()
        self.check_security_vulnerabilities()
        self.test_imports()
        self.generate_summary()
        self.save_report()
        
        print(f"\n{'='*70}\n")
        
        # Return exit code based on findings
        if self.has_vulnerabilities:
            return 2  # Critical issues
        elif self.has_updates:
            return 1  # Updates available
        else:
            return 0  # All good


def main():
    """Main entry point."""
    checker = PackageUpdateChecker()
    exit_code = checker.run()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

# Made with Bob
