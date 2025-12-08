import sys
import os

sys.path.append(os.getcwd())

from app.db.session import SessionLocal, engine
from app.models.user import User
from app.db.base import Base


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.email == "bikash@example.com").first()

        if existing_user:
            print(f"⚠️  User already exists: {existing_user.full_name} ({existing_user.id})")
            user_id = existing_user.id
        else:
            print("🌱 Seeding new Test User...")

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
            db.refresh(new_user)
            print(f"✅ User Created: {new_user.full_name}")
            user_id = new_user.id

        print("\n" + "=" * 50)
        print("🚀  READY TO TEST! COPY THIS JSON:")
        print("=" * 50)

        payload = {
            "user_id": user_id,
            "document_id": "doc_demo_999",
            "timestamp": "2025-12-08T10:00:00Z",
            "location": {
                "latitude": 28.6139,
                "longitude": 77.2090,
                "accuracy": 10.5,
                "altitude": 200.0
            },
            "device_info": {
                "device_id": "android_device_001",
                "mac_address": "00:1B:44:11:3A:B7",
                "ip_address": "192.168.1.105",
                "os_version": "Android 14",
                "is_rooted": False
            },
            "evidence": {
                "signature_image_b64": "dummy_base64_signature_string_xyz",
                "front_camera_image_b64": "dummy_base64_face_string_abc"
            }
        }

        import json
        print(json.dumps(payload, indent=4))
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🔌 Connecting to Database...")
    init_db()