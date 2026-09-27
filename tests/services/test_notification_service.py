from unittest.mock import patch

from app.services.notification_service import (NotificationChannel,
                                               send_notification)


def test_send_notification_email():
    with patch("app.services.notification_service.email_provider.send") as mock_send:

        send_notification(
            recipient="test@example.com",
            channel=NotificationChannel.EMAIL,
            subject="Test Subject",
            message="Test notification",
        )

        mock_send.assert_called_once_with(
            recipient="test@example.com",
            subject="Test Subject",
            message="Test notification",
        )
