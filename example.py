from dotenv import load_dotenv
import os
import json
from datetime import date, timedelta
from pysos.querybuilder import Query
from pysos.observations import ObservationManager

load_dotenv()

api_key = os.environ.get("API_KEY")

if api_key is None:
    raise ValueError("API_KEY environment variable not set")

base_url = "https://api.artdatabanken.se/species-observation-system/v1"

om = ObservationManager(base_url, api_key)

q = Query(
    provinces=["1"],
    taxons=[102942],
    start_date=date.today() - timedelta(days=1),
    end_date=date.today(),
)

print(json.dumps(q))

records = om.get_observations(q)

with open("data/results.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(records, indent=4, ensure_ascii=False))
