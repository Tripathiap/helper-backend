import logging

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.service_providers import router as service_provider_router
from app.api.service_requests import router as service_request_router
from app.db.database import get_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


app = FastAPI(
    title="Helper API",
    description="Backend API for Helper service requests",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to Helper API"}


app.include_router(service_request_router)
app.include_router(service_provider_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/health/database")
def database_health_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }
