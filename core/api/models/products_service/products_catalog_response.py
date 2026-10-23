from dataclasses import dataclass
from typing import List

from core.api.models.products_service.product_summary import ProductSummary

@dataclass
class ProductsCatalogResponse:
    items: List[ProductSummary]
    total: int
    page: int
    limit: int

    @classmethod
    def from_dict(cls, data):
        raw_items = data.get("items", [])
        return cls(
            items=[ProductSummary.from_dict(item) for item in raw_items],
            total=data.get("total", 0),
            page=data.get("page", 0),
            limit=data.get("limit", 0)
        )