import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from colorama import Fore, Style, init
from dotenv import load_dotenv

# Initialize colorama
init(autoreset=True)


class ApiClient:
    def __init__(
        self, *, api_url: str = "https://api.protium.space/v1/workflow/", api_token: Optional[str] = None
    ) -> None:
        dotenv_path: Path = Path.home() / ".protium"
        load_dotenv(dotenv_path)

        if api_token:
            self.api_token: str = api_token
            self._save_api_token(dotenv_path, api_token)
        else:
            self.api_token: str = self._get_api_token(dotenv_path)

        self.api_url: str = api_url
        self.headers: Dict[str, str] = {"Authorization": f"Bearer {self.api_token}"}

    def _get_api_token(self, dotenv_path: Path) -> str:
        api_token: Optional[str] = os.getenv("API_TOKEN")
        if api_token is None:
            api_token = input("Please enter your API token: ")
            self._save_api_token(dotenv_path, api_token)
            print(f"{Fore.MAGENTA}{Style.BRIGHT}API token received and saved.")
        else:
            display_value: str = api_token[:4] + "**" * 4 + api_token[-4:]
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Init with API token: {display_value}")

        return api_token

    def _save_api_token(self, dotenv_path: Path, api_token: str) -> None:
        with open(dotenv_path, "a") as f:
            f.write(f"\nAPI_TOKEN={api_token}")

    def list(self) -> Optional[Dict[str, Any]]:
        try:
            response: requests.Response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}{Style.BRIGHT}Error: {e}")
            return None
        return response.json()

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response: requests.Response = requests.post(self.api_url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
