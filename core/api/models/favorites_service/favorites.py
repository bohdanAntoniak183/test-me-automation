from dataclasses import dataclass
from typing import List

@dataclass
class Favorites:
    product_ids: List[str]

    @classmethod
    def from_dict(cls, data):
        return cls(product_ids=data.get("product_ids", []))

    def to_dict(self):
        return {"product_ids": self.product_ids}