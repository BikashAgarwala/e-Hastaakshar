from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {"message": "Auth endpoint active (Logic to be implemented)"}