import logging
from enum import Enum

logger = logging.getLogger(__name__)


class NotificationChannel(str, Enum):
    WHATSAPP = "whatsapp"
    SMS = "sms"
    EMAIL = "email"


def send_notification(
    recipient: str,
    channel: NotificationChannel,
    message: str,
) -> None:
    logger.info(
        "Notification | channel=%s | recipient=%s | message=%s",
        channel.value,
        recipient,
        message,
    )
