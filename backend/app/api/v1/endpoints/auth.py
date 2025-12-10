from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User

router = APIRouter()

class LoginRequest(BaseModel):
    email: str


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