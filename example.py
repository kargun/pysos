from dotenv import load_dotenv
import os
import json
from datetime import date, timedelta
from pysos.querybuilder import Query
from pysos.observations import ObservationManager
from pysos.species import SpeciesManager

load_dotenv()

api_key = os.environ.get("API_KEY")

if api_key is None:
    raise ValueError("API_KEY environment variable not set")

om = ObservationManager(
    "https://api.artdatabanken.se/species-observation-system/v1",
    api_key,
)
sm = SpeciesManager(
    "https://api.artdatabanken.se/information/v1/speciesdataservice/v1/speciesdata",
    api_key,
)

province_id = om.get_area_id("Province", "Småland")
taxon_id = sm.get_taxon_id("Ormvråk")

q = Query(
    provinces=[province_id],
    taxons=[taxon_id],
    start_date=date.today() - timedelta(days=1),
    end_date=date.today(),
)

print(json.dumps(q))

records = om.get_observations(q)

with open("data/results.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(records, indent=4, ensure_ascii=False))
