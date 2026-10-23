from core.api.api_client import APIClient

class ProductsService:
    def __init__(self, client: APIClient):
        self.client = client

    def get_products(self):
        return self.client.get("api/products")