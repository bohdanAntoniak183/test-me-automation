from core.api.api_client import APIClient

class FavoritesService:
    def __init__(self, client: APIClient):
        self.client = client

    def get_favorites(self):
        return self.client.get("api/favorites")

    def add_to_favorites(self, favorites):
        return self.client.put("api/favorites", payload=favorites.to_dict())