#!/usr/bin/env python3
"""
SBS Mapping System - Automated Setup Script
============================================

This script automates the setup process for the SBS Mapping System.

Usage:
    python setup.py
    python setup.py --check-only
    python setup.py --install-dev
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 3.7+ required. Found: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_pip():
    """Check if pip is available"""
    print("Checking pip installation...")
    try:
        import pip
        print(f"✅ pip is installed")
        return True
    except ImportError:
        print("❌ pip not found")
        return False

def install_dependencies(dev=False):
    """Install required packages"""
    print("Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        
        # Install requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        
        if dev:
            print("\nInstalling development dependencies...")
            dev_packages = [
                "pytest>=7.0.0",
                "black>=22.0.0",
                "pylint>=2.13.0",
                "mypy>=0.950"
            ]
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + dev_packages)
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def verify_installation():
    """Verify that all components are working"""
    print("\nVerifying installation...")
    
    checks = []
    
    # Check imports
    print("  Testing imports...")
    try:
        from sbs_ai_mapping_system import (
            SBSMappingEngine,
            MappingValidator,
            SimilarityCalculator,
            TextNormalizer
        )
        print("    ✅ Core modules")
        checks.append(True)
    except ImportError as e:
        print(f"    ❌ Core modules: {e}")
        checks.append(False)
    
    # Check pandas
    print("  Testing pandas...")
    try:
        import pandas as pd
        print("    ✅ pandas")
        checks.append(True)
    except ImportError as e:
        print(f"    ❌ pandas: {e}")
        checks.append(False)
    
    # Check numpy
    print("  Testing numpy...")
    try:
        import numpy as np
        print("    ✅ numpy")
        checks.append(True)
    except ImportError as e:
        print(f"    ❌ numpy: {e}")
        checks.append(False)
    
    # Check openpyxl
    print("  Testing openpyxl...")
    try:
        import openpyxl
        print("    ✅ openpyxl")
        checks.append(True)
    except ImportError as e:
        print(f"    ❌ openpyxl: {e}")
        checks.append(False)
    
    # Check matplotlib
    print("  Testing matplotlib...")
    try:
        import matplotlib
        print("    ✅ matplotlib")
        checks.append(True)
    except ImportError as e:
        print(f"    ❌ matplotlib: {e}")
        checks.append(False)
    
    # Check CLI
    print("  Testing CLI...")
    try:
        result = subprocess.run(
            [sys.executable, "sbs_mapping_cli.py", "--help"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("    ✅ CLI interface")
            checks.append(True)
        else:
            print("    ❌ CLI interface")
            checks.append(False)
    except Exception as e:
        print(f"    ❌ CLI interface: {e}")
        checks.append(False)
    
    success_rate = sum(checks) / len(checks) * 100
    print(f"\n  Overall: {sum(checks)}/{len(checks)} checks passed ({success_rate:.0f}%)")
    
    return all(checks)

def create_sample_structure():
    """Create sample directory structure"""
    print("\nCreating sample directory structure...")
    
    directories = [
        "data/input",
        "data/output",
        "examples",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created: {directory}/")
    
    return True

def print_next_steps():
    """Print next steps for user"""
    print_header("Setup Complete! 🎉")
    
    print("Next Steps:")
    print("\n1. Prepare your data:")
    print("   - Place SBS V2-V3 mapping file in data/input/")
    print("   - Place your price list in data/input/")
    
    print("\n2. Run your first mapping:")
    print("   python sbs_mapping_cli.py \\")
    print("       --v2v3-file data/input/SBS_V2_to_V3_Map.xlsx \\")
    print("       --pricelist data/input/your_pricelist.xlsx \\")
    print("       --output-dir data/output")
    
    print("\n3. Or use the interactive notebook:")
    print("   jupyter notebook sbs_mapping_notebook.ipynb")
    
    print("\n4. Read the documentation:")
    print("   - Quick Start: QUICK_START_GUIDE.md")
    print("   - Complete Docs: SBS_MAPPING_DOCUMENTATION.md")
    
    print("\n" + "=" * 60 + "\n")

def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup SBS Mapping System')
    parser.add_argument('--check-only', action='store_true',
                      help='Only check system requirements')
    parser.add_argument('--install-dev', action='store_true',
                      help='Install development dependencies')
    
    args = parser.parse_args()
    
    print_header("SBS Mapping System Setup")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check pip
    if not check_pip():
        print("\nPlease install pip and try again.")
        print("Visit: https://pip.pypa.io/en/stable/installation/")
        sys.exit(1)
    
    if args.check_only:
        print("\n✅ System requirements check passed!")
        sys.exit(0)
    
    # Install dependencies
    if not install_dependencies(dev=args.install_dev):
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️  Some components failed verification.")
        print("The system may still work, but please check the errors above.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Create directory structure
    create_sample_structure()
    
    # Print next steps
    print_next_steps()
    
    print("Setup completed successfully! ✅")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nSetup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
