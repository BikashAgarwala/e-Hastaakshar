from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.signature import SignatureSubmission, SignatureResponse
from app.services.forgery_service import forgery_checker
from app.models.transaction import Transaction, TransactionStatus
from app.models.user import User
from app.worker import process_signature_workflow

router = APIRouter()


@router.post("/submit", response_model=SignatureResponse)
async def submit_signature(
        *,
        db: Session = Depends(get_db),
        data: SignatureSubmission,
        background_tasks: BackgroundTasks
):
    if data.device_info.is_rooted:
        forgery_checker.log_forgery_event(
            db,
            data.user_id,
            "Rooted Device",
            data.device_info.model_dump(mode='json')
        )
        raise HTTPException(status_code=403, detail="Security Alert: Rooted devices are not supported.")

    user_record = db.query(User).filter(User.id == data.user_id).first()

    if not user_record:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")

    if forgery_checker.is_mac_mismatched(user_record.registered_mac_address, data.device_info.mac_address):
        forgery_checker.log_forgery_event(
            db,
            data.user_id,
            "MAC Mismatch",
            data.device_info.model_dump(mode='json')
        )
        raise HTTPException(status_code=403, detail="Security Alert: Device not recognized.")

    if user_record.base_latitude and user_record.base_longitude:
        if forgery_checker.is_location_suspicious(
                user_record.base_latitude, user_record.base_longitude,
                data.location.latitude, data.location.longitude
        ):
            forgery_checker.log_forgery_event(
                db,
                data.user_id,
                "Location Anomaly",
                data.location.model_dump(mode='json')
            )
            raise HTTPException(status_code=403, detail="Security Alert: Signing location unauthorized.")

    transaction_id = f"txn_{data.document_id}_{data.user_id}"

    new_transaction = Transaction(
        id=transaction_id,
        user_id=data.user_id,
        document_id=data.document_id,
        partner_id=data.partner_id,
        status=TransactionStatus.PENDING_VERIFICATION,
        metadata_snapshot=data.device_info.model_dump(mode='json')
    )

    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
    except Exception as e:
        db.rollback()
        print(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Could not save transaction.")

    background_tasks.add_task(
        process_signature_workflow,
        transaction_id,
        data.model_dump(mode='json')
    )

    return SignatureResponse(
        transaction_id=transaction_id,
        status="PENDING_VERIFICATION",
        message="Security checks passed. Signature sent for forensic analysis and blockchain sealing."
    )