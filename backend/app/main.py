from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import user, transaction

app = FastAPI(title="e-Hastaakshar API")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("--- [DB] Tables Created / Verified ---")

@app.get("/")
def root():
    return {"message": "System Operational"}