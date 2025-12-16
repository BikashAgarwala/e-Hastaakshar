import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate

router = APIRouter()

class LoginRequest(BaseModel):
    email: str


@router.post("/register", response_model=UserResponse)
def register_user(
        user_in: UserCreate,
        db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        id=f"user_{uuid.uuid4().hex[:8]}",
        full_name=user_in.full_name,
        email=user_in.email,
        # hashed_password=hash(user_in.password), # TODO: Add Hashing later

        registered_mac_address=user_in.device_info.mac_address,
        registered_device_id=user_in.device_info.device_id,

        base_latitude=user_in.location.latitude,
        base_longitude=user_in.location.longitude,

        is_active=True
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
def login_user(
        login_data: LoginRequest,
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not registered")

    return {
        "message": "Login Successful",
        "user_id": user.id,
        "full_name": user.full_name,
        "config": {
            "registered_mac": user.registered_mac_address,
            "base_latitude": user.base_latitude,
            "base_longitude": user.base_longitude
        }
    }