from fastapi import APIRouter

router = APIRouter()

@router.get("/status/{transaction_id}")
def check_verification_status(transaction_id: str):
    return {"status": "PENDING", "transaction_id": transaction_id}