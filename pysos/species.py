import requests


class SpeciesManager:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers = {
            "X-Api-Version": "1.5",
            "Ocp-Apim-Subscription-Key": api_key,
        }

    def get_taxon_id(self, species_name: str) -> int:
        params: dict[str, int | str] = {
            "searchString": species_name,
        }
        response = self.session.get(
            self.base_url + "/search",
            params=params,
        )
        response.raise_for_status()
        response_records: list[dict] = response.json()
        for species_record in response_records:
            return species_record["taxonId"]
        raise RuntimeError("Taxon not found")
