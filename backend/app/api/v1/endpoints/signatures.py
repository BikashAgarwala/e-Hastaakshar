from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.signature import SignatureSubmission, SignatureResponse
from app.services.forgery_service import forgery_checker
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
        forgery_checker.log_forgery_event(db, data.user_id, "Rooted Device", {})
        raise HTTPException(status_code=403, detail="Security Alert: Rooted devices are not supported.")

    registered_mac = "00:1B:44:11:3A:B7"
    registered_lat = 28.6139
    registered_lon = 77.2090

    if forgery_checker.is_mac_mismatched(registered_mac, data.device_info.mac_address):
        forgery_checker.log_forgery_event(db, data.user_id, "MAC Mismatch", data.device_info.dict())
        raise HTTPException(status_code=403, detail="Security Alert: Device not recognized.")

    if forgery_checker.is_location_suspicious(
            registered_lat, registered_lon,
            data.location.latitude, data.location.longitude
    ):
        forgery_checker.log_forgery_event(db, data.user_id, "Location Anomaly", data.location.dict())
        raise HTTPException(status_code=403, detail="Security Alert: Signing location unauthorized.")

    # TODO: new_txn = crud.transaction.create(db, obj_in=data)
    # transaction_id = new_txn.id
    transaction_id = "txn_" + data.document_id + "_" + data.user_id

    background_tasks.add_task(
        process_signature_workflow,
        transaction_id,
        data.model_dump()
    )

    return SignatureResponse(
        transaction_id=transaction_id,
        status="PENDING_VERIFICATION",
        message="Security checks passed. Signature sent for forensic analysis and blockchain sealing."
    )