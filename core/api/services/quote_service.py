from core.api.api_client import APIClient
from core.api.models.quote_service.quote_payload import QuotePayload

class QuoteService:
    def __init__(self, client: APIClient):
        self.client = client

    def calculate_quote(self, payload: QuotePayload):
        return self.client.post("api/quote", payload=payload.to_dict())