from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
import uuid


class ForgeryLog(Base):
    __tablename__ = "forgery_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    reason = Column(String, nullable=False)

    metadata_snapshot = Column(JSON, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())