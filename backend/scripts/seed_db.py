import sys
import os

sys.path.append(os.getcwd())

from app.db.session import SessionLocal, engine
from app.models.user import User
from app.db.base import Base


def seed_users():
    print("🌱 Seeding Users...")
    Base.metadata.create_all(bind=engine)  # Ensure tables exist

    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == "bikash@example.com").first()
        if existing_user:
            print(f"   ⚠️ User 'Bikash' already exists.")
        else:
            new_user = User(
                id="user_123456",
                full_name="Bikash - Test Account",
                email="bikash@example.com",
                registered_mac_address="00:1B:44:11:3A:B7",
                registered_device_id="android_device_001",
                base_latitude=28.6139,
                base_longitude=77.2090,
                is_active=True
            )
            db.add(new_user)
            db.commit()
            print("   ✅ User 'Bikash' created.")
    except Exception as e:
        print(f"   ❌ Error seeding users: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_users()