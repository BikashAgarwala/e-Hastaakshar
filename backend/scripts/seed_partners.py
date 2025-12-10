import sys
import os

sys.path.append(os.getcwd())

from app.db.session import SessionLocal, engine
from app.models.partner import Partner
from app.db.base import Base


def seed_partners():
    print("🌱 Seeding Partners...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    partners_data = [
        {
            "id": "partner_hdfc",
            "name": "HDFC Bank",
            "api_callback_url": "https://api.hdfc.com/verify/callback",
            "logo_url": "https://logo.clearbit.com/hdfcbank.com"
        },
        {
            "id": "partner_sbi",
            "name": "State Bank of India (SBI)",
            "api_callback_url": "https://api.sbi.co.in/callback",
            "logo_url": "https://logo.clearbit.com/sbi.co.in"
        },
        {
            "id": "partner_notary",
            "name": "Govt. Notary Office (Delhi)",
            "api_callback_url": None,
            "logo_url": "https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg"
        }
    ]

    try:
        for p_data in partners_data:
            existing = db.query(Partner).filter(Partner.id == p_data["id"]).first()
            if not existing:
                new_partner = Partner(
                    id=p_data["id"],
                    name=p_data["name"],
                    api_callback_url=p_data["api_callback_url"],
                    logo_url=p_data["logo_url"],
                    is_active=True
                )
                db.add(new_partner)
                print(f"   ✅ Partner '{p_data['name']}' created.")
            else:
                print(f"   ⚠️ Partner '{p_data['name']}' already exists.")

        db.commit()
        print("✨ Partner seeding complete!")

    except Exception as e:
        print(f"   ❌ Error seeding partners: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_partners()