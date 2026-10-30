from core.api.api_client import APIClient

class ProductsService:
    def __init__(self, client: APIClient):
        self.client = client

    def get_products(
        self,
        category = None,
        sort = None,
        in_stock = None,
        min_price = None,
        max_price = None,
        limit = 20
    ):
        params = {
            key: value
            for key, value in {
                "category": category,
                "sort": sort,
                "in_stock": in_stock,
                "min_price": min_price,
                "max_price": max_price,
                "limit": limit
            }.items()
            if value is not None
        }

        return self.client.get("api/products", params=params)

    def get_product_review(self, product_id):
        return self.client.get(f"api/products/{product_id}/review")

    def leave_product_review(self, product_id, review_payload):
        return self.client.post(f"api/products/{product_id}/review", payload=review_payload.to_dict())
