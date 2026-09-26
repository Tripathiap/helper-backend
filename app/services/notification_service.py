import logging

logger = logging.getLogger(__name__)


def notify_service_provider(
    provider_name: str,
    message: str,
) -> None:

    logger.info(
        "Notification to provider '%s': %s",
        provider_name,
        message,
    )
