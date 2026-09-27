import logging
import smtplib
from email.message import EmailMessage

from app.core.config import settings
from app.notifications.base import NotificationProvider

logger = logging.getLogger(__name__)


class EmailNotificationProvider(NotificationProvider):

    def send(
        self,
        recipient: str,
        message: str,
    ) -> None:
        email = EmailMessage()

        email["From"] = settings.smtp_from_email
        email["To"] = recipient
        email["Subject"] = "New Helper Service Request"
        email.set_content(message)

        with smtplib.SMTP(
            settings.smtp_host,
            settings.smtp_port,
        ) as smtp:
            smtp.starttls()
            smtp.login(
                settings.smtp_username,
                settings.smtp_password,
            )
            smtp.send_message(email)

        logger.info(
            "Email notification sent | recipient=%s",
            recipient,
        )
