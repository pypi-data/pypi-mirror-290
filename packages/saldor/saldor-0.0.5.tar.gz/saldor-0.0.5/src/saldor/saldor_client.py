from typing import List
import requests


class SaldorClient:
    def __init__(self, api_key: str, base_url="https://api.saldor.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"APIKey {api_key}"}

    def _handle_response(self, response: requests.Response):
        # Check if the request was successful
        if response.status_code == 200:
            # Assuming the response contains a JSON array of strings
            return response.json()["data"]
        else:
            # Handle error appropriately
            response.raise_for_status()

        return []

    def scrape(self, url: str, params: dict) -> List[str]:
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

        payload = {"url": url, "params": params}

        # Use the base_url variable
        response = requests.post(
            f"{self.base_url}/scrape", json=payload, headers=headers
        )

        return self._handle_response(response)

    def crawl(self, url: str, goal="", max_pages="1", max_depth="0"):
        payload = {
            "url": url,
            "goal": goal,
            "max_pages": max_pages,
            "max_depth": max_depth,
        }

        response = requests.post(
            f"{self.base_url}/crawl",
            json=payload,
            headers=self.headers,
        )

        return self._handle_response(response)

    def get_crawl(self, crawl_id: str):
        response = requests.get(
            f"{self.base_url}/crawl/{crawl_id}",
            headers=self.headers,
        )

        return self._handle_response(response)

    def list_crawls(self, state: str = ""):
        response = requests.get(
            f"{self.base_url}/crawl/", json={"state": state}, headers=self.headers
        )
        return self._handle_response(response)
