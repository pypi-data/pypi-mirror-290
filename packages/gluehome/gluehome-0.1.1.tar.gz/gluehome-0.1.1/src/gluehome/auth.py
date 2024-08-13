import requests
from .const import API_URL, USER_AGENT

class GlueAuth:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def issue_api_key(self):
        response = requests.post(
            f'{API_URL}/v1/api-keys',
            json={
                'name': 'homeassistant',
                'scopes': ['locks.write', 'locks.read', 'events.read']
            },
            auth=(self.username, self.password),
            headers={'User-Agent': USER_AGENT}
        )
        response.raise_for_status()
        return response.json()['apiKey']
