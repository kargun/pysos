import json
import os
from datetime import date, timedelta

from pysos.observations import ObservationManager
from pysos.querybuilder import Query
from pysos.species import SpeciesManager

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
    start_date=date.today() - timedelta(days=365 * 3),
    end_date=date.today(),
)

print(json.dumps(q))

om.download_csv(q, "data/results.csv", zip=False)
