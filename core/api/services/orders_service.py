from core.api.api_client import APIClient
from core.api.models.orders_service.orders_payload import OrdersPayload

class OrdersService:
    def __init__(self, client: APIClient):
        self.client = client

    def create_order(self, payload: OrdersPayload):
        return self.client.post("api/orders", payload=payload.to_dict())

    def cancel_order(self, order_id: str):
        return self.client.post(f"api/orders/{order_id}/cancel")

    def get_order_details(self, order_id: str):
        return self.client.get(f"api/orders/{order_id}")