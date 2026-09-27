from abc import ABC, abstractmethod


class NotificationProvider(ABC):

    @abstractmethod
    def send(
        self,
        recipient: str,
        subject: str,
        message: str,
    ) -> None:
        pass
