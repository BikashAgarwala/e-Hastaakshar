from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.transaction import Transaction, TransactionStatus
from app.services.image_service import image_processor
from app.services.ipfs_service import ipfs_client

router = APIRouter()


@router.post("/review/{transaction_id}")
async def review_transaction(
        transaction_id: str,
        decision: str,
        db: Session = Depends(get_db)
):
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not txn:
        raise HTTPException(404, "Transaction not found")

    if txn.status != TransactionStatus.PENDING_PARTNER_REVIEW:
        raise HTTPException(400, "Transaction is not pending partner review")

    if decision == "REJECT":
        txn.status = TransactionStatus.REJECTED
        txn.failure_step = "PARTNER_REJECTION"
        db.commit()
        return {"status": "Rejected"}


    verification_url = f"https://ehastaakshar-portal.com/verify/{txn.id}"

    raw_image = txn.metadata_snapshot['evidence']['signature_image_b64']
    final_b64 = image_processor.generate_stamped_document(raw_image, verification_url)
    image_cid = ipfs_client.upload_file(final_b64)

    txn.final_stamped_image_cid = image_cid
    txn.status = TransactionStatus.VERIFIED

    db.commit()

    return {
        "status": "APPROVED",
        "final_image_url": ipfs_client.generate_public_url(image_cid)
    }