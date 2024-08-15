import getpass
import os
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import requests
from colorama import Fore, Style, init
from dotenv import load_dotenv
from pandas import DataFrame
from tzlocal import get_localzone

# Initialize colorama
init(autoreset=True)

# 获取系统的本地时区
local_timezone = get_localzone()


class ApiClient:
    def __init__(
        self, *, api_url: str = "https://api.protium.space/v1/workflow/", api_token: Optional[str] = None
    ) -> None:
        dotenv_path: Path = Path.home() / ".ptmrc"
        load_dotenv(dotenv_path)

        if api_token:
            self.api_token: str = api_token
            # self._save_api_token(dotenv_path, api_token)
        else:
            self.api_token: str = self._get_api_token(dotenv_path)

        self.api_url: str = api_url
        self.headers: Dict[str, str] = {"Authorization": f"Bearer {self.api_token}"}

    def _get_api_token(self, dotenv_path: Path) -> str:
        api_token: Optional[str] = os.getenv("API_TOKEN")
        if api_token is None:
            api_token = getpass.getpass("Please enter your API token: ")
            self._save_api_token(dotenv_path, api_token)
            print(f"{Fore.MAGENTA}{Style.BRIGHT}API token received and saved.")
        else:
            display_value: str = api_token[:4] + "**" * 4 + api_token[-4:]
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Init with API token: {display_value}")

        return api_token

    def _save_api_token(self, dotenv_path: Path, api_token: str) -> None:
        with open(dotenv_path, "a") as f:
            f.write(f"\nAPI_TOKEN={api_token}")

    def list(self) -> DataFrame | None:
        try:
            response: requests.Response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}{Style.BRIGHT}Error: {e}")
            return None
        data = response.json()
        if isinstance(data, list):
            # Process the data to hide uuid and add workflow_url
            for item in data:
                del item["uuid"]

            dataframe = pd.DataFrame(data)
            dataframe["created_at"] = pd.to_datetime(dataframe["created_at"])
            dataframe["updated_at"] = pd.to_datetime(dataframe["updated_at"])
            dataframe["created_at"] = (
                dataframe["created_at"].dt.tz_convert(local_timezone).dt.strftime("%Y-%m-%d %H:%M:%S")
            )
            dataframe["updated_at"] = (
                dataframe["updated_at"].dt.tz_convert(local_timezone).dt.strftime("%Y-%m-%d %H:%M:%S")
            )

            return dataframe
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Error: Unexpected response format.")
            return None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response: requests.Response = requests.post(self.api_url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
