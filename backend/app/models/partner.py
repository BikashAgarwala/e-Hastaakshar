from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Partner(Base):
    __tablename__ = "partners"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    api_callback_url = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())