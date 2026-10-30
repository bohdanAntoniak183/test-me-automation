from dataclasses import dataclass

from core.api.models.products_service.review_payload import ReviewPayload

@dataclass
class ReviewResponse:
    review: ReviewPayload

    @classmethod
    def from_dict(cls, data):
        return cls(
            review=ReviewPayload.from_dict(data.get("review", {}))
        )