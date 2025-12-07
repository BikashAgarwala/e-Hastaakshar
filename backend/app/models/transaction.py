from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class TransactionStatus(str, enum.Enum):
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    PROCESSING = "PROCESSING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    FAILED_UPLOAD = "FAILED_UPLOAD"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    document_id = Column(String, nullable=False, index=True)
    status = Column(String, default=TransactionStatus.PENDING_VERIFICATION)

    ml_confidence_score = Column(Float, nullable=True)
    digital_seal_hash = Column(String, nullable=True)

    ipfs_cid = Column(String, nullable=True)
    ipfs_public_url = Column(String, nullable=True)

    metadata_snapshot = Column(JSON, nullable=True)
    rejection_reason = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())