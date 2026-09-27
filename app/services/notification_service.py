import logging
from enum import Enum

from app.notifications.email import EmailNotificationProvider

logger = logging.getLogger(__name__)


class NotificationChannel(str, Enum):
    WHATSAPP = "whatsapp"
    SMS = "sms"
    EMAIL = "email"


email_provider = EmailNotificationProvider()


def send_notification(
    recipient: str,
    channel: NotificationChannel,
    subject: str,
    message: str,
) -> None:

    if channel == NotificationChannel.EMAIL:
        email_provider.send(
            recipient=recipient,
            subject=subject,
            message=message,
        )
        return

    raise ValueError(f"Unsupported notification channel: {channel}")
