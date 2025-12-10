from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class TransactionStatus(str, enum.Enum):
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    PROCESSING = "PROCESSING"
    PENDING_PARTNER_REVIEW = "PENDING_PARTNER_REVIEW"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    FAILED_UPLOAD = "FAILED_UPLOAD"

class FailureStep(str, enum.Enum):
    NONE = "NONE"
    DEVICE_INTEGRITY = "DEVICE_INTEGRITY"
    IDENTITY_MATCH = "IDENTITY_MATCH"
    GEO_FENCING = "GEO_FENCING"
    LIVENESS_CHECK = "LIVENESS_CHECK"
    PARTNER_REJECTION = "PARTNER_REJECTION"


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

    partner_id = Column(String, ForeignKey("partners.id"), nullable=True)

    metadata_snapshot = Column(JSON, nullable=True)
    rejection_reason = Column(String, nullable=True)
    failure_step = Column(String, default=FailureStep.NONE)

    final_stamped_image_cid = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())