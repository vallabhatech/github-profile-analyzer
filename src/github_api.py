import os
import time
from typing import Any
import requests

API = "https://api.github.com"

class GitHubAPI:
    def __init__(self, token: str | None = None):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        for attempt in range(4):
            response = self.session.get(f"{API}{path}", params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            if response.status_code in {403, 429}:
                reset = response.headers.get("X-RateLimit-Reset")
                wait = max(int(reset) - int(time.time()), 1) if reset and response.headers.get("X-RateLimit-Remaining") == "0" else 2 ** attempt
                time.sleep(min(wait, 30))
                continue
            if response.status_code == 404:
                return None
            response.raise_for_status()
        raise RuntimeError(f"GitHub API request failed after retries: {path}")

    def profile(self, username: str) -> dict | None:
        return self.get(f"/users/{username}")

    def repositories(self, username: str) -> list[dict]:
        repos = []
        page = 1
        while True:
            batch = self.get(f"/users/{username}/repos", {"per_page": 100, "page": page, "type": "owner", "sort": "updated"}) or []
            repos.extend(batch)
            if len(batch) < 100:
                return repos
            page += 1
