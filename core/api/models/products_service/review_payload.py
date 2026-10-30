from dataclasses import dataclass

@dataclass
class ReviewPayload:
    rating: int
    text: str

    def to_dict(self):
        return {
            "rating": self.rating,
            "text": self.text
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            rating=data.get("rating", 0),
            text=data.get("text", "")
        )