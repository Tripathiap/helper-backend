from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enum import ServiceType
from app.db.models import ServiceProvider
from app.schemas.service_provider import ServiceProviderCreate


def create_service_provider(
    db: Session,
    request: ServiceProviderCreate,
) -> ServiceProvider:
    service_provider = ServiceProvider(
        service_provider_name=request.service_provider_name,
        service_provider_phone_number=request.service_provider_phone_number,
        service_type=request.service_type,
    )

    db.add(service_provider)
    db.commit()
    db.refresh(service_provider)

    return service_provider


def find_active_provider(
    db: Session,
    service_type: ServiceType,
) -> ServiceProvider | None:
    statement = (
        select(ServiceProvider)
        .where(
            ServiceProvider.service_type == service_type,
            ServiceProvider.is_active.is_(True),
        )
        .limit(1)
    )

    return db.scalar(statement)
