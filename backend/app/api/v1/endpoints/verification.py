from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.transaction import Transaction, TransactionStatus

router = APIRouter()

@router.get("/status/{transaction_id}")
def check_verification_status(
        transaction_id: str,
        db: Session = Depends(get_db)
):
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    response = {
        "transaction_id": txn.id,
        "status": txn.status,
        "updated_at": txn.updated_at
    }

    if txn.status == TransactionStatus.VERIFIED:
        response["ipfs_public_url"] = txn.ipfs_public_url
        response["digital_seal_hash"] = txn.digital_seal_hash
        response["ml_confidence"] = txn.ml_confidence_score

    if txn.status == TransactionStatus.REJECTED:
        response["rejection_reason"] = txn.rejection_reason

    return response