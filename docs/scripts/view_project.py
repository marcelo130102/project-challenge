# view_project.py
"""
Script to view the complete structure of the Briefcase project
"""

import os
import sys
from pathlib import Path

def print_tree(directory, prefix="", max_depth=3, current_depth=0):
    """Prints directory structure as a tree"""
    if current_depth >= max_depth:
        return
    
    items = sorted(Path(directory).iterdir(), key=lambda x: (x.is_file(), x.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "+-- " if is_last else "|-- "
        print(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir() and current_depth < max_depth - 1:
            next_prefix = prefix + ("    " if is_last else "|   ")
            print_tree(item, next_prefix, max_depth, current_depth + 1)

def main():
    print("COMPLETE BRIEFCASE PROJECT STRUCTURE")
    print("=" * 50)
    print()
    
    # Main structure
    print("Project Structure:")
    print_tree(".", max_depth=2)
    
    print("\n" + "=" * 50)
    print("PROJECT STATISTICS")
    print("=" * 50)
    
    # Count files by type
    file_types = {}
    total_files = 0
    total_lines = 0
    
    for root, dirs, files in os.walk("."):
        # Ignore system directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'venv']
        
        for file in files:
            if file.startswith('.'):
                continue
                
            ext = os.path.splitext(file)[1] or 'no_extension'
            file_types[ext] = file_types.get(ext, 0) + 1
            total_files += 1
            
            # Count lines
            try:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    total_lines += lines
            except:
                pass
    
    print(f"Total files: {total_files}")
    print(f"Total lines: {total_lines:,}")
    print()
    
    print("Files by type:")
    for ext, count in sorted(file_types.items()):
        icon = "[PY]" if ext == ".py" else "[MD]" if ext == ".md" else "[CSS]" if ext == ".css" else "[JS]" if ext == ".js" else "[HTML]" if ext == ".html" else "[TXT]" if ext == ".txt" else "[FILE]"
        print(f"  {icon} {ext or 'no_extension'}: {count}")
    
    print("\n" + "=" * 50)
    print("USEFUL COMMANDS")
    print("=" * 50)
    
    commands = [
        ("Run application", "python run.py"),
        ("Create test users", "python seed.py"),
        ("Verify installation", "python verify_installation.py"),
        ("Install dependencies", "pip install -r requirements.txt"),
        ("View structure", "python docs/scripts/view_project.py"),
        ("View documentation", "start README.md"),
    ]
    
    for desc, cmd in commands:
        print(f"{desc:<25} -> {cmd}")
    
    print("\n" + "=" * 50)
    print("NEXT STEPS")
    print("=" * 50)
    
    next_steps = [
        "1. Read README.md to understand the project",
        "2. Run 'python run.py' to start",
        "3. Run 'python seed.py' to create users",
        "4. Open http://localhost:8000 in your browser",
        "5. Login with alice@briefcase.com / password123",
        "6. Upload a document and test it",
        "7. Change user and download the document",
        "8. Customize the interface if you want",
    ]
    
    for step in next_steps:
        print(f"  {step}")
    
    print("\n" + "=" * 50)
    print("BRIEFCASE PROJECT READY TO USE!")
    print("=" * 50)

if __name__ == "__main__":
    main()
