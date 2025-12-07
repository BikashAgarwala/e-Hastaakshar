from fastapi import APIRouter
from app.api.v1.endpoints import auth, signatures, verification, upload

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(signatures.router, prefix="/signatures", tags=["Signatures"])
api_router.include_router(verification.router, prefix="/verify", tags=["Verification"])
api_router.include_router(upload.router, prefix="/uplod", tags=["Upload Files"])