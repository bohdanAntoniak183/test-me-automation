from dataclasses import dataclass
from typing import List, Optional
from core.api.models.delivery_type import DeliveryType
from core.api.models.cart_item import CartItem
from core.api.models.orders_service.payment_status import PaymentStatus

@dataclass
class OrdersPayload:
    items: List[CartItem]
    name: str = ""
    email: str = ""
    address: str = ""
    coupon: Optional[str] = None
    delivery: DeliveryType = DeliveryType.STANDARD
    payment: PaymentStatus = PaymentStatus.APPROVED

    def to_dict(self) -> dict:
        data = {
            "items": [item.to_dict() for item in self.items],
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "delivery": self.delivery.value,
            "payment": self.payment.value
        }
        if self.coupon:
            data["coupon"] = self.coupon
        return data