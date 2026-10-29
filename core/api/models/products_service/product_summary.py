from dataclasses import dataclass

from core.api.models.products_service.sort_type import SortType

@dataclass
class ProductSummary:
    id: str
    name: str
    price: int
    category: str
    sort: SortType
    stock: int

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            price=data.get("price", 0),
            category=data.get("category", ""),
            sort=SortType(data.get("sort", SortType.FEATURED)),
            stock=data.get("stock", 0)
        )
