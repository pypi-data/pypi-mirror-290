import requests
from typing import Dict, Any, Optional, List, Union

class IntegrationOSModel:
    def __init__(self, model_name: str, connection_key: str, secret_key: str):
        self.model_name = model_name
        self.connection_key = connection_key
        self.secret_key = secret_key
        self.base_url = "https://api.integrationos.com/v1/unified"

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        headers = {
            "X-INTEGRATIONOS-CONNECTION-KEY": self.connection_key,
            "X-INTEGRATIONOS-SECRET": self.secret_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/{self.model_name}/{endpoint}".rstrip('/')
        
        response = requests.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def list(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._make_request("GET", "", params)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", "", data)

    def count(self) -> int:
        return self._make_request("GET", "count")["count"]

    def get(self, id: Union[str, int]) -> Dict[str, Any]:
        return self._make_request("GET", str(id))

    def delete(self, id: Union[str, int]) -> Dict[str, Any]:
        return self._make_request("DELETE", str(id))

    def update(self, id: Union[str, int], data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("PATCH", str(id), data)

class IntegrationOS:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def __call__(self, model_name: str, connection_key: str) -> IntegrationOSModel:
        return IntegrationOSModel(model_name, connection_key, self.secret_key)