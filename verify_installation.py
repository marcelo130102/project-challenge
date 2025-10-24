"""
Script to verify that installation is complete and working
"""
import sys
import io

# Configure UTF-8 output for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify_modules():
    """Verifies that all required modules are installed"""
    required_modules = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'pydantic_settings',
        'jose',
        'passlib',
        'cryptography',
        'jinja2',
        'aiofiles'
    ]
    
    print("\n" + "="*60)
    print("[*] Verifying installed modules...")
    print("="*60 + "\n")
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"[OK] {module}")
        except ImportError:
            print(f"[X] {module} - NOT FOUND")
            missing_modules.append(module)
    
    return missing_modules


def verify_files():
    """Verifies that all required files exist"""
    import os
    
    required_files = [
        'main.py',
        'models.py',
        'database.py',
        'auth.py',
        'encryption.py',
        'config.py',
        'seed.py',
        'requirements.txt',
        'templates/index.html',
        'templates/dashboard.html',
        'static/style.css',
        'static/dashboard.js'
    ]
    
    print("\n" + "="*60)
    print("[*] Verifying project files...")
    print("="*60 + "\n")
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file}")
        else:
            print(f"[X] {file} - NOT FOUND")
            missing_files.append(file)
    
    return missing_files


def verify_database():
    """Verifies that the database is initialized"""
    import os
    
    print("\n" + "="*60)
    print("[*] Verifying database...")
    print("="*60 + "\n")
    
    if os.path.exists('briefcase.db'):
        print("[OK] Database found: briefcase.db")
        
        # Try to connect and count users
        try:
            from database import SessionLocal
            from models import User
            
            db = SessionLocal()
            user_count = db.query(User).count()
            db.close()
            
            print(f"[OK] Users in database: {user_count}")
            
            if user_count == 0:
                print("[!] No users found. Run: python seed.py")
                return False
            
            return True
            
        except Exception as e:
            print(f"[X] Error connecting to database: {e}")
            return False
    else:
        print("[!] Database not found")
        print("[INFO] Run 'python seed.py' to create it")
        return False


def main():
    print("""
    ========================================================
            BRIEFCASE INSTALLATION VERIFICATION
    ========================================================
    """)
    
    # Verify modules
    missing_modules = verify_modules()
    
    # Verify files
    missing_files = verify_files()
    
    # Verify database
    db_ok = verify_database()
    
    # Summary
    print("\n" + "="*60)
    print("[*] SUMMARY")
    print("="*60 + "\n")
    
    errors = []
    
    if missing_modules:
        print(f"[X] {len(missing_modules)} missing modules")
        print("    Run: pip install -r requirements.txt")
        errors.append("modules")
    else:
        print("[OK] All modules are installed")
    
    if missing_files:
        print(f"[X] {len(missing_files)} missing files")
        errors.append("files")
    else:
        print("[OK] All project files exist")
    
    if not db_ok:
        print("[!] Database needs initialization")
        print("    Run: python seed.py")
        errors.append("database")
    else:
        print("[OK] Database configured correctly")
    
    print("\n" + "="*60)
    
    if not errors:
        print("[OK] INSTALLATION COMPLETE AND READY!")
        print("="*60)
        print("\n[INFO] To start the server run:")
        print("    python run.py")
        print("\n[INFO] Then open in your browser:")
        print("    http://localhost:8000")
        print()
        return True
    else:
        print("[!] INSTALLATION INCOMPLETE")
        print("="*60)
        print(f"\n[!] Problems found: {', '.join(errors)}")
        print("[INFO] Check previous messages for more details\n")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

