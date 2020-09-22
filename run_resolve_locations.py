# run_resolve_locations.py

import simplejson as json
import pandas as pd
import time
from urlparse import urlparse
from pprint import pprint

with open('data/01-source/company-locations.json') as f:
  locations = json.load(f)
# locations = pd.read_csv('data/01-source/company-locations.csv')
# print locations.homepage_domain.value_counts()
# locations = locations.set_index('homepage_domain')
# print locations.head()
# print locations.head(5).to_dict(orient='index')

with open('data/02-refined/apis.json') as f:
  apis = json.load(f)

for api in apis:
  if api['details'].has_key('api_provider') and len(api['details']['api_provider']) > 0: 
    api['api_provider'] = api['details']['api_provider'][0]['key']
  elif api['details'].has_key('api_endpoint') and len(api['details']['api_endpoint']) > 0:
    api['api_provider'] = urlparse(api['details']['api_endpoint'][0]['key']).netloc
  else:
    api['api_provider'] = None 
    print api

  if api['api_provider'] != None: 
    print api['api_name'], api['api_provider']
    domain_split = urlparse(api['api_provider']).netloc.split('.')
    domain = '.'.join(domain_split)
    while not locations.has_key(domain) and len(domain_split) > 1:
      domain = '.'.join(domain_split)
      domain_split.pop(0)

    if locations.has_key(domain):
      print domain, locations[domain]
      location = locations[domain]
      # Replacing Pandas' nans with Nones
      for key in location.keys():
        if not pd.notnull(location[key]):
          location[key] = None
      api['location'] = locations[domain]
      for key in location.keys():
        api['location.%s' % key] = location[key]
    else: 
      print '...domain %s not found' % urlparse(api['api_provider']).netloc
      api['location'] = None
  else: 
    print '... provider information not available'
    api['location'] = None
  print 

# Geocoding the address data
from geopy.geocoders import Nominatim
geolocator = Nominatim()
import time

# df_country_codes = pd.read_csv('data/01-source/iso_3166_2_countries.csv')
# df_country_codes['country_code'] = df_country_codes[u'ISO 3166-1 3 Letter Code']
# # print county_codes.columns
# print df_country_codes.head()
# country_codes = df_country_codes.set_index('country_code').to_dict(orient='index')
# pprint(country_codes)
with open('data/04-geo/country-code-lookup.json') as f:
  country_codes = json.load(f)

for api in apis:
  if api['location'] != None:
    if api['location']['location_country_code'] != None:
      country_code = api['location']['location_country_code']
      if country_code == 'Slovakia (Slovak Republic)':
        api['location']['location_country_name'] = 'Slovakia'
        api['location']['location_country_code'] = 'SVK'
      else:
        api['location']['location_country'] = country_codes[country_code]
        # if country_codes[country_code][Coral Sea Islands]
        api['location']['location_country_name'] = country_codes[country_code]['name']
      print country_code, api['location']['location_country_name']
      
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

  # if 'location_city' in location.keys() and 'location_country_code' in location.keys():
  #   if location['location_city'] != None and location['location_country_code'] != None:
  #     print '%s %s' % (location['location_city'], location['location_country_code'])

from pprint import pprint


# # raise Exception()


#     if index 


    # if 'location_city' in api['location'].keys() and 'location_country_code' in api['location'].keys():
    #   print '%s %s' % (api['location']['location_city'], api['location']['location_country_code'])
  # if   
  # location = geolocator.geocode("175 5th Avenue NYC")

  # while domain
  # pprint(api['api_provider'])
  # domain = urlparse(api['api_provider']).netloc 
  # time.sleep(3)

# def city(location):

#   return location['location_city']

with open('data/02-refined/apis-with-location.json', 'w') as f:
  json.dump(apis, f, indent=1)

# print len(data)
# print json.dumps(data[0],indent=1)
