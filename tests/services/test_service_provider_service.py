from unittest.mock import MagicMock

from app.core.enum import ServiceType
from app.db.models import ServiceProvider
from app.services.service_provider_service import find_active_provider


def test_find_active_provider_returns_provider():
    db = MagicMock()

    provider = ServiceProvider(
        service_provider_name="Adarsh",
        service_provider_phone_number="9876543210",
        service_provider_email="adarsh@gmail.com",
        service_type=ServiceType.PLUMBING,
        is_active=True,
    )

    db.scalar.return_value = provider

    result = find_active_provider(
        db=db,
        service_type=ServiceType.PLUMBING,
    )

    assert result is provider
    assert result.service_provider_name == "Adarsh"
    assert result.service_provider_email == "adarsh@gmail.com"

    db.scalar.assert_called_once()


def test_find_active_provider_returns_none_when_no_provider():
    db = MagicMock()

    db.scalar.return_value = None

    result = find_active_provider(
        db=db,
        service_type=ServiceType.PLUMBING,
    )

    assert result is None

    db.scalar.assert_called_once()
