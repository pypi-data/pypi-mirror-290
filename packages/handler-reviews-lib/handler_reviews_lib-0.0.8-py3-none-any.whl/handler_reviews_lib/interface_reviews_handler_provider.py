import enum
from abc import ABC, abstractmethod
from .interface_handler_reviews import IHandlerReviews


class IHandlerProvider(ABC):
    @abstractmethod
    def fetch_handler(self, handler_type: enum, **kwargs) -> IHandlerReviews:
        pass

