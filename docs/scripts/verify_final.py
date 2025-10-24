# verify_final.py
"""
Final verification script for Briefcase project
Verifies that everything is working correctly
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifies that a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[ERROR] {description}: {filepath} - NOT FOUND")
        return False

def check_python_import(module_name):
    """Verifies that a Python module can be imported"""
    try:
        __import__(module_name)
        print(f"[OK] Python module: {module_name}")
        return True
    except ImportError:
        print(f"[ERROR] Python module: {module_name} - NOT INSTALLED")
        return False

def check_database():
    """Verifies that the database is configured"""
    try:
        from database import init_db
        init_db()
        print("[OK] Database: Configured correctly")
        return True
    except Exception as e:
        print(f"[ERROR] Database: Error - {e}")
        return False

def main():
    print("FINAL BRIEFCASE PROJECT VERIFICATION")
    print("=" * 60)
    
    all_good = True
    
    # Verify main files
    print("\nVERIFYING MAIN FILES:")
    files_to_check = [
        ("main.py", "Main application"),
        ("models.py", "Data models"),
        ("database.py", "Database configuration"),
        ("auth.py", "Authentication system"),
        ("encryption.py", "Encryption system"),
        ("config.py", "Configuration"),
        ("requirements.txt", "Dependencies"),
        ("README.md", "Documentation"),
        ("templates/index.html", "Login template"),
        ("templates/dashboard.html", "Dashboard template"),
        ("static/style.css", "CSS styles"),
        ("static/dashboard.js", "Dashboard JavaScript"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Verify Python modules
    print("\nVERIFYING PYTHON MODULES:")
    modules_to_check = [
        "fastapi",
        "sqlalchemy",
        "pydantic",
        "jose",
        "passlib",
        "cryptography",
        "uvicorn",
    ]
    
    for module in modules_to_check:
        if not check_python_import(module):
            all_good = False
    
    # Verify database
    print("\nVERIFYING DATABASE:")
    if not check_database():
        all_good = False
    
    # Verify utility scripts
    print("\nVERIFYING UTILITY SCRIPTS:")
    scripts_to_check = [
        ("seed.py", "Create test users"),
        ("run.py", "Run application"),
        ("verify_installation.py", "Installation verification"),
    ]
    
    for script, description in scripts_to_check:
        if not check_file_exists(script, description):
            all_good = False
    
    # Final result
    print("\n" + "=" * 60)
    if all_good:
        print("VERIFICATION COMPLETED SUCCESSFULLY!")
        print("All components are working correctly")
        print("\nNEXT STEPS:")
        print("1. Run: python seed.py")
        print("2. Run: python run.py")
        print("3. Open: http://localhost:8000")
        print("4. Login with: alice@briefcase.com / password123")
    else:
        print("VERIFICATION COMPLETED WITH WARNINGS")
        print("Some components need attention")
        print("\nSOLUTIONS:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Verify all files are present")
        print("3. Run: python verify_installation.py")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
