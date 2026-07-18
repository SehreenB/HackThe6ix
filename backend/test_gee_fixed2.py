import ee
import os
from google.oauth2 import service_account

key_file = os.path.join(os.path.dirname(''), os.getenv("GEE_KEY_FILE", "gee-key.json"))
credentials = service_account.Credentials.from_service_account_file(key_file, scopes=["https://www.googleapis.com/auth/earthengine"])
ee.Initialize(credentials)

liberia = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq("ADM0_NAME", "Liberia"))
worldpop = ee.ImageCollection("WorldPop/GP/100m/pop").filter(ee.Filter.eq("country", "LBR")).filter(ee.Filter.eq("year", 2020)).first()
accessibility = ee.Image("projects/malariaatlasproject/assets/accessibility/accessibility_to_healthcare/2019").select(0)

st_total = worldpop.reduceRegion(reducer=ee.Reducer.sum(), geometry=liberia.geometry(), scale=100, maxPixels=1e13).getInfo()
print("SUCCESS TOTAL:", st_total)
