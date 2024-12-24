import requests
from typing import Dict, Any
from .config import config

class APIClient:
    def __init__(self):
        self.base_url = config.api_url
        self.session = requests.Session()
        
    def get(self, endpoint: str, params: Dict[str, Any] = None):
        return self.session.get(f"{self.base_url}{endpoint}", params=params)
        
    def post(self, endpoint: str, data: Dict[str, Any] = None):
        return self.session.post(f"{self.base_url}{endpoint}", json=data)

    def put(self, endpoint: str, data: Dict[str, Any] = None):
        return self.session.put(f"{self.base_url}{endpoint}", json=data)

    def delete(self, endpoint: str):
        """Send a DELETE request to the API."""
        return self.session.delete(f"{self.base_url}{endpoint}")

    def patch(self, endpoint: str, data: Dict[str, Any] = None):
        """Send a PATCH request to the API for partial updates."""
        return self.session.patch(f"{self.base_url}{endpoint}", json=data)