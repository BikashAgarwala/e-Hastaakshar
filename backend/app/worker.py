import hashlib
import time
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.transaction import Transaction, TransactionStatus, FailureStep
from app.services.ipfs_service import ipfs_client


def process_signature_workflow(transaction_id: str, data: dict):
    db: Session = SessionLocal()
    print(f"--- [WORKER] Starting workflow for Txn: {transaction_id} ---")

    try:
        txn_record = db.query(Transaction).filter(Transaction.id == transaction_id).first()

        if not txn_record:
            print(f"❌ [ERROR] Transaction {transaction_id} not found in DB.")
            return

        txn_record.status = TransactionStatus.PROCESSING
        db.commit()

        ml_confidence_score = _simulate_ml_check(
            data['evidence']['signature_image_b64'],
            data['evidence']['front_camera_image_b64']
        )
        txn_record.ml_confidence_score = ml_confidence_score

        if ml_confidence_score < 0.80:
            print(f"❌ [FAIL] ML Score {ml_confidence_score} too low.")
            txn_record.status = TransactionStatus.REJECTED
            txn_record.failure_step = FailureStep.LIVENESS_CHECK
            txn_record.rejection_reason = "Signature ML check failed."
            db.commit()
            return

        print(f"✅ [PASS] ML Validation passed. Score: {ml_confidence_score}")

        digital_seal = _generate_digital_seal(data)
        txn_record.digital_seal_hash = digital_seal

        ipfs_payload = {
            "transaction_id": transaction_id,
            "seal_hash": digital_seal,
            "timestamp": str(data['timestamp']),
            "location": data['location'],
            "device_info": data['device_info'],
            "verification_score": ml_confidence_score
        }

        cid = ipfs_client.upload_json_metadata(transaction_id, ipfs_payload)

        if not cid:
            print("❌ [FAIL] IPFS Upload failed (Metadata).")
            txn_record.status = TransactionStatus.REJECTED
            txn_record.rejection_reason = "IPFS Connection Failed"
            db.commit()
            return

        txn_record.ipfs_cid = cid

        txn_record.status = TransactionStatus.PENDING_PARTNER_REVIEW
        db.commit()

        print(f"⏸️ [WAIT] Txn {transaction_id} paused. Waiting for Partner Approval.")

    except Exception as e:
        print(f"🔥 [CRITICAL WORKER ERROR] {str(e)}")
        db.rollback()
    finally:
        db.close()


def _simulate_ml_check(sig_img: str, face_img: str) -> float:
    time.sleep(2)
    return 0.95


def _generate_digital_seal(data: dict) -> str:
    raw_string = (
        f"{data['device_info']['mac_address']}"
        f"{str(data['timestamp'])}"
        f"{data['location']['latitude']}"
        f"{data['location']['longitude']}"
        f"{data['evidence']['signature_image_b64']}"
    )
    return hashlib.sha256(raw_string.encode()).hexdigest()