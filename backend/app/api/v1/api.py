from fastapi import APIRouter
from app.api.v1.endpoints import auth, signatures, verification, upload,partners

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(signatures.router, prefix="/signatures", tags=["Signatures"])
api_router.include_router(verification.router, prefix="/verify", tags=["Verification"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload Files"])
api_router.include_router(partners.router, prefix="/partner", tags=["Partner Review"])