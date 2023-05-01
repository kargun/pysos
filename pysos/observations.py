import requests
import json
from pysos.querybuilder import Query


class ObservationManager:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers = {"Ocp-Apim-Subscription-Key": api_key}

    def get_count(self, query: Query) -> int:
        response = self.session.post(
            self.base_url + "/Observations/Count",
            data=json.dumps(query),
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return int(response.content)
