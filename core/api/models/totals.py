from dataclasses import dataclass

@dataclass
class Totals:
    subtotal: int
    discount: int
    shipping: int
    total: int
    currency: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            subtotal=data.get("subtotal", 0),
            discount=data.get("discount", 0),
            shipping=data.get("shipping", 0),
            total=data.get("total", 0),
            currency=data.get("currency", "UAH")
        )