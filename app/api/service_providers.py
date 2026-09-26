from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.service_provider import (ServiceProviderCreate,
                                          ServiceProviderResponse)
from app.services.service_provider_service import create_service_provider

router = APIRouter(
    prefix="/api/v1/service-providers",
    tags=["Service Providers"],
)


@router.post(
    "",
    response_model=ServiceProviderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service_provider_endpoint(
    request: ServiceProviderCreate,
    db: Session = Depends(get_db),
):
    return create_service_provider(
        db=db,
        request=request,
    )
