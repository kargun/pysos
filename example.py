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
q1 = Query(municipalities=["781"], taxons=[102942])
q2 = Query(
    provinces=["1"],
    taxons=[102942],
    start_date=date.today() - timedelta(days=1),
    end_date=date.today(),
)
print(json.dumps(q1))
print(json.dumps(q2))

res = om.get_count(q2)
print(res)
