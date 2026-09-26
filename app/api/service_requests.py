from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.service_request import (ServiceRequestCreate,
                                         ServiceRequestResponse)
from app.services.service_request_service import create_service_request

router = APIRouter(
    prefix="/api/v1/service-requests",
    tags=["Service Requests"],
)


@router.post(
    "",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service_request_endpoint(
    request: ServiceRequestCreate,
    db: Session = Depends(get_db),
):
    return create_service_request(
        db=db,
        request=request,
    )
