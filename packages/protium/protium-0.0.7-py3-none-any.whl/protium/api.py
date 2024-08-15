import os
from pathlib import Path

from colorama import Fore, Style, init
from dotenv import load_dotenv

# Initialize colorama
init(autoreset=True)


class ApiClient:
    def __init__(self, api_url="http://api.protium.space/v1/workflow/", api_token=None):
        self.api_url = api_url
        self.api_token = api_token or self._get_api_token()
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def _get_api_token(self):
        dotenv_path = Path.home() / ".protium"
        load_dotenv(dotenv_path)

        api_token = os.getenv("API_TOKEN")
        if api_token is None:
            api_token = input("Please enter your API token: ")
            with open(dotenv_path, "a") as f:
                f.write(f"\nAPI_TOKEN={api_token}")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}API token received and saved.")
        else:
            display_value = api_token[:4] + "**" * (len(api_token) - 8) + api_token[-4:]
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Read API token: {display_value}")

        return api_token
