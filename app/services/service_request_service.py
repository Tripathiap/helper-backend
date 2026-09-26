from sqlalchemy.orm import Session

from app.db.models import ServiceRequest
from app.schemas.service_request import ServiceRequestCreate


def create_service_request(
    db: Session,
    request: ServiceRequestCreate,
) -> ServiceRequest:
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
