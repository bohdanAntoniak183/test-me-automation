from dataclasses import dataclass
from typing import List, Optional

from core.api.models.cart_item import CartItem
from core.api.models.delivery_type import DeliveryType

@dataclass
class QuotePayload:
    items: List[CartItem]
    coupon: Optional[str] = None
    delivery_type: DeliveryType = DeliveryType.STANDARD

    def to_dict(self):
        data = {
            "items": [item.to_dict() for item in self.items],
            "delivery_type": self.delivery_type.value
        }

        if self.coupon:
            data["coupon"] = self.coupon

        return data