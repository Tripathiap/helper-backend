from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.enum import ServiceType


class ServiceRequestCreate(BaseModel):
    requester_name: str = Field(
        min_length=5,
        max_length=100,
    )

    phone_number: str = Field(
        min_length=10,
        max_length=20,
    )

    tower_number: str = Field(
        min_length=1,
        max_length=20,
    )

    flat_number: str = Field(
        min_length=1,
        max_length=20,
    )

    requester_address: str = Field(
        min_length=5,
        max_length=255,
    )

    problem_type: ServiceType

    problem_description: str | None = Field(
        default=None,
        max_length=1000,
    )

    preferred_time_slot: str = Field(
        min_length=1,
        max_length=50,
    )


class ServiceRequestResponse(BaseModel):
    public_id: UUID
    requester_name: str
    phone_number: str
    tower_number: str
    flat_number: str
    requester_address: str
    problem_type: str
    problem_description: str | None
    preferred_time_slot: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
