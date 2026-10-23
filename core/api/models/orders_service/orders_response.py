from dataclasses import dataclass
from typing import List

from core.api.models.totals import Totals
from core.api.models.cart_item import CartItem
from core.api.models.orders_service.order_status import OrderStatus

@dataclass
class OrdersResponse:
    id: str
    status: OrderStatus
    items: List[CartItem]
    totals: Totals
    created_at: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", ""),
            status=OrderStatus(data.get("status", "")),
            items=[CartItem.from_dict(item) for item in data.get("items", [])],
            totals=Totals.from_dict(data.get("totals", {})),
            created_at=data.get("created_at", "")
        )
