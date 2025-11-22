#!/usr/bin/env python3

"""
Documentation Validator Script

This script validates that all documentation files exist and are properly formatted.
"""

import os
import sys
from pathlib import Path

def validate_documentation():
    """Validate all documentation files"""
    
    # Define required documentation files
    required_files = [
        "README.md",
        "docs/user_guide.md",
        "docs/admin_guide.md",
        "docs/deployment_checklist.md",
        "docs/test_matrix.md",
        "docs/qa_report.md",
        "docs/ui_components.md",
        "requirements.txt"
    ]
    
    # Check if all files exist
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing documentation files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print("✅ All documentation files are present")
    
    # Check README.md for required sections
    readme_content = Path("README.md").read_text()
    required_sections = [
        "Features",
        "Prerequisites",
        "Installation",
        "Running the Application",
        "Documentation"
    ]
    
    missing_sections = []
    for section in required_sections:
        if f"## {section}" not in readme_content and f"# {section}" not in readme_content:
            missing_sections.append(section)
    
    if missing_sections:
        print("❌ Missing sections in README.md:")
        for section in missing_sections:
            print(f"  - {section}")
        return False
    
    print("✅ README.md contains all required sections")
    
    # Check that requirements.txt is not empty
    requirements_content = Path("requirements.txt").read_text().strip()
    if not requirements_content:
        print("❌ requirements.txt is empty")
        return False
    
    print("✅ requirements.txt is properly populated")
    
    return True

if __name__ == "__main__":
    print("Validating PetRescue documentation...")
    
    if validate_documentation():
        print("\n✅ All documentation validation checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Documentation validation failed!")
        sys.exit(1)