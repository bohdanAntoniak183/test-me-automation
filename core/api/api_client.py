import time
import logging
import requests

class APIClient:
    def __init__(self, base_url: str, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.session = requests.Session()
        self.logger = logging.getLogger("APIClient")
        self.token = self.__create_workspace()

    def __create_workspace(self) -> str:
        url = f"{self.base_url}/api/workspaces"

        for attempt in range(self.max_retries + 1):
            response = self.session.post(url)
            
            if response.status_code == 429:
                retry_after = float(response.headers.get("Retry-After", 2))
                self.logger.warning(
                    f"[Rate Limit] Отримано 429 при створенні середовища. "
                    f"Спроба {attempt + 1}/{self.max_retries}. Очікування {retry_after} сек..."
                )
                if attempt == self.max_retries:
                    self.logger.error("Вичерпано всі спроби створення середовища через Soft Rate Limit.")
                    raise RuntimeError("Перевищено ліміт спроб через Soft Rate Limit (429) при створенні середовища.")

                time.sleep(retry_after)
                continue
                
            if response.status_code == 201:
                data = response.json()
                if "token" in data:
                    token = data["token"]
                    self.logger.info("Середовище успішно створено, токен отримано.")
                    return token
            
            self.logger.error(f"Не вдалося створити середовище. Статус: {response.status_code}, Відповідь: {response.text}")
            raise RuntimeError(f"Не вдалося створити середовище (статус {response.status_code}): {response.text}")

    def _get_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["X-Workspace-Token"] = self.token
        return headers

    def _request_with_retry(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs["headers"] = self._get_headers()

        self.logger.debug(f"Виконання запиту: {method} {url}")

        for attempt in range(self.max_retries + 1):
            response = self.session.request(method, url, **kwargs)

            if response.status_code == 429:
                retry_after = float(response.headers.get("Retry-After", 1))
                self.logger.warning(
                    f"[Rate Limit] Отримано 429 для {method} {endpoint}. "
                    f"Спроба {attempt + 1}/{self.max_retries}. Очікування {retry_after} сек..."
                )
                if attempt == self.max_retries:
                    self.logger.error(f"Вичерпано всі спроби для {method} {endpoint} через Soft Rate Limit.")
                    return response

                time.sleep(retry_after)
                continue

            self.logger.info(f"Отримано відповідь: {response.status_code} для {method} {endpoint}")
            return response

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        return self._request_with_retry("GET", endpoint, params=params)

    def post(self, endpoint: str, payload: dict = None) -> requests.Response:
        return self._request_with_retry("POST", endpoint, json=payload)