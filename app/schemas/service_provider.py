from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.enum import ServiceType


class ServiceProviderCreate(BaseModel):
    service_provider_name: str = Field(
        min_length=2,
        max_length=100,
    )

    service_provider_phone_number: str = Field(
        min_length=10,
        max_length=20,
    )

    service_provider_email: str = Field(
        min_length=5,
        max_length=255,
    )

    service_type: ServiceType


class ServiceProviderResponse(BaseModel):
    public_id: UUID
    service_provider_name: str
    service_provider_phone_number: str
    service_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    service_provider_email: str

    model_config = {"from_attributes": True}
