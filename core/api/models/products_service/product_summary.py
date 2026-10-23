from dataclasses import dataclass

@dataclass
class ProductSummary:
    id: str
    name: str
    price: int

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            price=data.get("price", 0)
        )
