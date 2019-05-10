# run_crawl_apis.py

import simplejson as json
import requests
from requests.exceptions import TooManyRedirects
import time 
import random

with open('data/02-refined/api_index.json') as f:
  apis = json.load(f)

datadir = 'data/01-raw-apis/'

for index, api in enumerate(apis):
  if not api['available']:
    try:
      page = requests.get(api['url'])
    except TooManyRedirects:
      print 'Too many redirects when reading %s' % api['url']
      continue
    # fname = '%s.html' % api['url'].split('/')[-1]
    fpath = 'data/01-raw-apis/%s' % api['filename']
    print index,len(apis),fpath
    with open(fpath,'w') as f:
      f.write(page.content)
    time.sleep(10+random.random()*10)


