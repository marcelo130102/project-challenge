"""
Script to populate database with test users
"""
from database import SessionLocal, init_db
from models import User
from auth import get_password_hash
import sys
import io

# Configure UTF-8 output for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def seed_database():
    """Creates test users in the database"""
    
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    # Check if users already exist
    existing_users = db.query(User).count()
    if existing_users > 0:
        print(f"[!] {existing_users} users already exist in database")
        response = input("Do you want to continue and add more users? (y/n): ")
        if response.lower() != 'y':
            print("[X] Operation cancelled")
            db.close()
            return
    
    # Test users
    test_users = [
        {
            "email": "alice@briefcase.com",
            "username": "alice",
            "password": "password123"
        },
        {
            "email": "bob@briefcase.com",
            "username": "bob",
            "password": "password123"
        },
        {
            "email": "charlie@briefcase.com",
            "username": "charlie",
            "password": "password123"
        }
    ]
    
    print("\n[*] Creating test users...\n")
    
    for user_data in test_users:
        # Check if user already exists
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"[!] User {user_data['email']} already exists, skipping...")
            continue
        
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            hashed_password=get_password_hash(user_data["password"])
        )
        db.add(user)
        print(f"[OK] User created: {user_data['username']} ({user_data['email']})")
    
    db.commit()
    
    print("\n" + "="*50)
    print("[OK] Database populated successfully!")
    print("="*50)
    print("\n[INFO] Test credentials:\n")
    
    for user_data in test_users:
        print(f"Email:    {user_data['email']}")
        print(f"Password: {user_data['password']}")
        print("-" * 40)
    
    db.close()


if __name__ == "__main__":
    seed_database()

