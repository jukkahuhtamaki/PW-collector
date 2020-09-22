# run_insert_regions.py

import simplejson as json
import pandas as pd 

with open('data/02-refined/apis-with-location-geocoded-dict.json', 'r') as f:
  apis = json.load(f)

with open('data/04-geo/startup-regions-location-lookup.json', 'r') as f:
  regions = json.load(f)

with open('data/04-geo/global-region-lookup.json', 'r') as f:
  global_regions = json.load(f)

print

for api in apis.values():
  if api.has_key('location_string'):
    if regions.has_key(api['location_string']):
      api['region_string'] = regions[api['location_string']]['resolution']

  if api.has_key('location.location_country_code') and api['location.location_country_code'] != None:
    # TODO: Remove the hard-coded data patch once the data is fixed upstream
    if api['location.location_country_code'] == 'Slovakia (Slovak Republic)':
      api['location.location_country_code'] = 'SVK'
    api['global_region_name'] = global_regions[api['location.location_country_code']]['Region'] 

with open('data/02-refined/apis-with-region.json', 'w') as f:
  json.dump(apis, f, indent=1)

df_apis = pd.DataFrame.from_dict(apis, orient='index')
# print df_apis.head()

print 'APIs total: ', len(df_apis.index)
df_apis_with_region = df_apis[pd.notnull(df_apis.region_string)]
print 'APIs with region: ', len(df_apis_with_region.index)

print df_apis_with_region.head()

with open('data/02-refined/apis-with-region-filtered.json', 'w') as f:
  json.dump(df_apis_with_region.to_dict(orient='index'), f, indent=1)
# print df_apis.head()