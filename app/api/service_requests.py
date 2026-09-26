from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ServiceRequest
from app.schemas.service_request import (
    ServiceRequestCreate,
    ServiceRequestResponse,
)


router = APIRouter(
    prefix="/api/v1/service-requests",
    tags=["Service Requests"],
)


@router.post(
    "",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service_request(
    request: ServiceRequestCreate,
    db: Session = Depends(get_db),
):
    service_request = ServiceRequest(
        requester_name=request.requester_name,
        phone_number=request.phone_number,
        tower_number=request.tower_number,
        flat_number=request.flat_number,
        requester_address=request.requester_address,
        problem_type=request.problem_type,
        problem_description=request.problem_description,
        preferred_time_slot=request.preferred_time_slot,
    )

    db.add(service_request)
    db.commit()
    db.refresh(service_request)

    return service_request
