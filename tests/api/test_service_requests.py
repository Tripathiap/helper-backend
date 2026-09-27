from datetime import datetime
from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_service_request_endpoint():
    public_id = uuid4()
    now = datetime.utcnow()

    mock_service_request = {
        "public_id": public_id,
        "requester_name": "Test User",
        "phone_number": "9876543210",
        "tower_number": "A",
        "flat_number": "101",
        "requester_address": "Helper Test Address",
        "problem_type": "plumbing",
        "problem_description": "Kitchen sink is leaking",
        "preferred_time_slot": "10:00 AM - 12:00 PM",
        "status": "submitted",
        "created_at": now,
        "updated_at": now,
    }

    with patch(
        "app.api.service_requests.create_service_request",
        return_value=mock_service_request,
    ) as mock_create:

        response = client.post(
            "/api/v1/service-requests",
            json={
                "requester_name": "Test User",
                "phone_number": "9876543210",
                "tower_number": "A",
                "flat_number": "101",
                "requester_address": "Helper Test Address",
                "problem_type": "plumbing",
                "problem_description": "Kitchen sink is leaking",
                "preferred_time_slot": "10:00 AM - 12:00 PM",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["public_id"] == str(public_id)
    assert data["requester_name"] == "Test User"
    assert data["phone_number"] == "9876543210"
    assert data["problem_type"] == "plumbing"
    assert data["status"] == "submitted"

    mock_create.assert_called_once()


def test_create_service_request_rejects_invalid_requester_name():
    response = client.post(
        "/api/v1/service-requests",
        json={
            "requester_name": "Tom",
            "phone_number": "9876543210",
            "tower_number": "A",
            "flat_number": "101",
            "requester_address": "Helper Test Address",
            "problem_type": "plumbing",
            "problem_description": "Kitchen sink is leaking",
            "preferred_time_slot": "10:00 AM - 12:00 PM",
        },
    )

    assert response.status_code == 422
