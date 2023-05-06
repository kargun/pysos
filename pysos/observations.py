import requests
import json
from pysos.querybuilder import Query

OBSERVATION_LIMIT = 10000
OBSERVATION_TAKE = 1000


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

    def get_observations(self, query: Query) -> list[dict]:
        count = self.get_count(query)
        if count == 0:
            raise RuntimeError("No records returned")
        elif count > OBSERVATION_LIMIT:
            raise RuntimeError("Too many records returned")
        else:
            query.update(
                {
                    "output": {
                        "fields": [
                            "datasetName",
                            "location.province",
                            "location.county",
                            "location.municipality",
                            "location.locality",
                            "taxon.vernacularName",
                            "occurrence.occurrenceId",
                            "occurrence.individualCount",
                            "occurrence.sex",
                            "occurrence.lifeStage",
                            "occurrence.activity",
                            "occurrence.occurrenceRemarks",
                            "event.startDate",
                            "event.endDate",
                        ]
                    }
                }
            )

            skip = 0
            records: list[dict] = []

            while skip < count:
                response = self.session.post(
                    self.base_url + "/Observations/Search",
                    params={"skip": skip, "take": OBSERVATION_TAKE},
                    data=json.dumps(query),
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                response_record: dict = response.json()["records"]
                records.extend(response_record)
                skip += OBSERVATION_TAKE

            return records
