"""Create initial admin user."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password

def create_admin():
    """Create admin user."""
    db = SessionLocal()

    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("Admin user already exists!")
            return

        # Create admin user
        admin = User(
            email="admin@yourcompany.com",
            username="admin",
            hashed_password=hash_password("Admin123!"),
            full_name="System Administrator",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("✅ Admin user created successfully!")
        print(f"   Email: {admin.email}")
        print(f"   Username: {admin.username}")
        print("   Password: Admin123!")
        print("\n⚠️  CHANGE THE PASSWORD AFTER FIRST LOGIN!")

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
