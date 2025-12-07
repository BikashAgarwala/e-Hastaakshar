from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
from app.schemas.signature import SignatureCreate
from app.core.celery_app import celery_worker


def validate_metadata(data: SignatureCreate) -> bool:
    # Logic to check if MAC address matches known device patterns
    # Or if Location is within acceptable bounds
    return True


async def process_submission(db: Session, data: SignatureCreate, bg_tasks: BackgroundTasks):
    unique_hash = _generate_hash(data)

    db_record = _create_db_entry(db, data, unique_hash, status="PROCESSING")

    bg_tasks.add_task(celery_worker.verify_and_upload, db_record.id, data.dict())

    return {
        "transaction_id": db_record.id,
        "status": "PROCESSING",
        "message": "Signature received. Verification and IPFS pinning in progress."
    }


def _generate_hash(data):
    # Implementation of hashing logic
    pass