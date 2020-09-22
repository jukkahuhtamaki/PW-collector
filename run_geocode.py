# run_geocode.py

import simplejson as json
import pandas as pd 
# Geocoding the address data
from geopy.geocoders import Nominatim
geolocator = Nominatim()

with open('data/02-refined/apis-with-location.json') as f:
  apis = json.load(f)

def location_string(location):
  location_bits = list()
  if 'location_city' in location.keys() and location['location_city'] != None:
    location_bits.append(location['location_city'])
  else:
    return None

  if location.has_key('location_country_code') and location['location_country_code'] == 'USA':
    if 'location_region' in location.keys() and location['location_region'] != None:
      location_bits.append(location['location_region'])
    else: 
      return None

  if 'location_country_code' in location.keys() and location['location_country_code'] != None:
    location_bits.append(location['location_country_name'])
  else: 
    return None

  return ' '.join(location_bits)

location_mapping = {
  'New York New York United States': 'New York United States',
}

for index, api in enumerate(apis):
  # print api['location']
  print index, api['api_provider']
  if api['location'] != None:
    location_str = location_string(api['location'])
    if location_str != None:
      # pprint(dir(location))
      if location_mapping.has_key(location_str):
        location_str =  location_mapping[location_str]
      api['location_string'] = location_str
      # if location != None:
      #   api['full_location'] = True
      #   print location_str, location.latitude, location.longitude
    else:
      api['full_location'] = False

df_apis = pd.DataFrame.from_dict(apis)
print df_apis.head()

location_strings =  df_apis.location_string.unique()
# print location_strings

with open('data/02-refined/geolocation-cache.json') as f:
  cache = json.load(f)

# cache = dict()

from pprint import pprint
import time

locations = dict()

for index, location_string in enumerate(location_strings):
  print '%s/%s: %s' % (index, len(location_strings), location_string)

  if location_string in location_mapping.keys(): 
    print 'Switching %s location_string to %s' % (location_string, location_mapping[location_string])
    location_string = location_mapping[location_string]

  if cache.has_key(location_string):
    locations[location_string] = cache[location_string]
  else:
    location = geolocator.geocode(location_string, timeout=None)
    if location != None:
      locations[location_string] = location.raw
      cache[location_string] = location.raw
      pprint(location.raw)
    else:
      print 'No location for %s' % location_string
    #   time.sleep(10)
    # time.sleep(3)
  if index % 10 == 0:
    with open('data/02-refined/geolocation-cache.json', 'w') as cachefile:
      json.dump(cache, cachefile, indent=1)

  print

with open('data/02-refined/geolocation-cache.json', 'w') as cachefile:
  json.dump(cache, cachefile, indent=1)

for api in apis:
  if api.has_key('location_string') and locations.has_key(api['location_string']):
    api['geolocation'] = locations[api['location_string']]


with open('data/02-refined/apis-with-location-geocoded.json', 'w') as f:
  json.dump(apis, f, indent=1)

api_dict = dict()
for api in apis:
  api['id'] = api['url'].split('/')[-1]
  api_dict[api['id']] = api

with open('data/02-refined/apis-with-location-geocoded-dict.json', 'w') as f:
  json.dump(api_dict, f, indent=1)  
