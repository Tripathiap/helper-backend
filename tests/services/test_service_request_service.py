from unittest.mock import MagicMock, patch

from app.core.config import settings
from app.core.enum import ServiceType
from app.schemas.service_request import ServiceRequestCreate
from app.services.service_request_service import create_service_request


def create_test_request() -> ServiceRequestCreate:
    return ServiceRequestCreate(
        requester_name="Test User",
        phone_number="9876543210",
        tower_number="A",
        flat_number="101",
        requester_address="Helper Test Address",
        problem_type=ServiceType.PLUMBING,
        problem_description="Kitchen sink is leaking",
        preferred_time_slot="10:00 AM - 12:00 PM",
    )


def test_create_service_request_notifies_provider():
    db = MagicMock()

    service_request = MagicMock()
    service_request.public_id = "test-request-id"
    service_request.requester_name = "Test User"
    service_request.problem_type = ServiceType.PLUMBING
    service_request.tower_number = "A"
    service_request.flat_number = "101"
    service_request.preferred_time_slot = "10:00 AM - 12:00 PM"

    provider = MagicMock()
    provider.service_provider_email = "adarsh@gmail.com"

    with (
        patch(
            "app.services.service_request_service.ServiceRequest",
            return_value=service_request,
        ),
        patch(
            "app.services.service_request_service.find_active_provider",
            return_value=provider,
        ),
        patch(
            "app.services.service_request_service.send_notification"
        ) as mock_send_notification,
    ):
        result = create_service_request(
            db=db,
            request=create_test_request(),
        )

    assert result is service_request

    mock_send_notification.assert_called_once()

    call = mock_send_notification.call_args

    assert call.kwargs["recipient"] == "adarsh@gmail.com"
    assert call.kwargs["channel"].value == "email"
    assert "Test User" in call.kwargs["message"]
    assert "Problem: plumbing." in call.kwargs["message"]


def test_create_service_request_uses_fallback_when_no_provider():
    db = MagicMock()

    service_request = MagicMock()
    service_request.public_id = "test-request-id"
    service_request.requester_name = "Test User"
    service_request.problem_type = ServiceType.PLUMBING
    service_request.tower_number = "A"
    service_request.flat_number = "101"
    service_request.preferred_time_slot = "10:00 AM - 12:00 PM"

    with (
        patch(
            "app.services.service_request_service.ServiceRequest",
            return_value=service_request,
        ),
        patch(
            "app.services.service_request_service.find_active_provider",
            return_value=None,
        ),
        patch(
            "app.services.service_request_service.send_notification"
        ) as mock_send_notification,
    ):
        result = create_service_request(
            db=db,
            request=create_test_request(),
        )

    assert result is service_request

    mock_send_notification.assert_called_once()

    call = mock_send_notification.call_args

    assert call.kwargs["recipient"] == settings.default_notification_recipient_email

    assert call.kwargs["channel"].value == "email"
    assert "Test User" in call.kwargs["message"]


def test_create_service_request_succeeds_when_notification_fails():
    db = MagicMock()

    service_request = MagicMock()
    service_request.public_id = "test-request-id"
    service_request.requester_name = "Test User"
    service_request.problem_type = ServiceType.PLUMBING
    service_request.tower_number = "A"
    service_request.flat_number = "101"
    service_request.preferred_time_slot = "10:00 AM - 12:00 PM"

    provider = MagicMock()
    provider.service_provider_email = "adarsh@gmail.com"

    with (
        patch(
            "app.services.service_request_service.ServiceRequest",
            return_value=service_request,
        ),
        patch(
            "app.services.service_request_service.find_active_provider",
            return_value=provider,
        ),
        patch(
            "app.services.service_request_service.send_notification",
            side_effect=Exception("SMTP connection failed"),
        ) as mock_send_notification,
    ):
        result = create_service_request(
            db=db,
            request=create_test_request(),
        )

    assert result is service_request

    mock_send_notification.assert_called_once()
