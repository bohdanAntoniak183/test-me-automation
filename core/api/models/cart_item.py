from dataclasses import dataclass

@dataclass
class CartItem:
    product_id: str
    quantity: int

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data.get("product_id", ""),
            quantity=data.get("quantity", 0)
        )

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantity": self.quantity
        }