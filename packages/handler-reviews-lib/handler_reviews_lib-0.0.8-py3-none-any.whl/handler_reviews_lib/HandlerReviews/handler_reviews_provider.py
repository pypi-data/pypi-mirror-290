import enum
from abc import ABC
from handler_reviews_lib.enums_type import HandlerType
from handler_reviews_lib.gpt_reviews_handler import GPTReviewsHandler
from handler_reviews_lib.template_reviews_handler import TemplateReviewsHandler
from handler_reviews_lib.interface_handler_reviews import IHandlerReviews
from handler_reviews_lib.interface_reviews_handler_provider import IHandlerProvider


class HandlerReviewsProvider(IHandlerProvider, ABC):
    def fetch_handler(self, handler_type: enum, **kwargs) -> IHandlerReviews:
        if handler_type == HandlerType.TEMPLATEHANDLER:
            return TemplateReviewsHandler(**kwargs)
        elif handler_type == HandlerType.GPTHANDLER:
            return GPTReviewsHandler(**kwargs)
        else:
            raise ValueError("Handler type not found")



