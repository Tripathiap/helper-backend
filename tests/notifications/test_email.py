from unittest.mock import MagicMock, patch

from app.core.config import settings
from app.notifications.email import EmailNotificationProvider


def test_send_email():
    provider = EmailNotificationProvider()

    recipient = "test@example.com"
    message = "Test service request"

    with patch("app.notifications.email.smtplib.SMTP") as mock_smtp:
        mock_connection = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_connection

        provider.send(
            recipient=recipient,
            message=message,
        )

        mock_smtp.assert_called_once_with(
            settings.smtp_host,
            settings.smtp_port,
        )

        mock_connection.starttls.assert_called_once()

        mock_connection.login.assert_called_once_with(
            settings.smtp_username,
            settings.smtp_password,
        )

        mock_connection.send_message.assert_called_once()

        sent_email = mock_connection.send_message.call_args.args[0]

        assert sent_email["From"] == settings.smtp_from_email
        assert sent_email["To"] == recipient
        assert sent_email["Subject"] == "New Helper Service Request"
        assert sent_email.get_content().strip() == message
