from sqlalchemy import Column, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    registered_mac_address = Column(String, nullable=True)
    registered_device_id = Column(String, nullable=True)

    base_latitude = Column(Float, nullable=True)
    base_longitude = Column(Float, nullable=True)

    reference_face_encoding = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())