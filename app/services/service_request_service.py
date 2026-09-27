import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import ServiceRequest
from app.schemas.service_request import ServiceRequestCreate
from app.services.notification_service import (NotificationChannel,
                                               send_notification)
from app.services.service_provider_service import find_active_provider

logger = logging.getLogger(__name__)


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

    subject = f"New Service Request"

    message = (
        f"New service request #{service_request.public_id}."
        f"Customer: {service_request.requester_name}. "
        f"Problem: {service_request.problem_type}. "
        f"Tower: {service_request.tower_number}, "
        f"Flat: {service_request.flat_number}. "
        f"Complete Address: {service_request.requester_address}"
        f"Preferred time: {service_request.preferred_time_slot}."
    )

    try:
        provider = find_active_provider(
            db=db,
            service_type=service_request.problem_type,
        )

        send_notification(
            recipient=(
                provider.service_provider_email
                if provider
                else settings.default_notification_recipient_email
            ),
            channel=NotificationChannel.EMAIL,
            subject=subject,
            message=message,
        )

    except Exception:
        logger.exception(
            "Failed to notify service provider for request %s",
            service_request.public_id,
        )

    return service_request
