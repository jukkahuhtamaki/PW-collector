# run_crawl_mashups.py

import simplejson as json
import requests
import time 
import random

with open('data/02-refined/mashup_index.json') as f:
  mashups = json.load(f)

datadir = 'data/01-raw-mashups/'

# # Checking whether local copies of pages exist.
# # And creating file names while going through the list
# for mashup in mashups:
#   page = requests.get(mashup['url'])
#   fname = '%s.html' % mashup['url'].split('/')[-1]
#   mashup['filename'] = fname

# with open('data/02-refined/mashup_index.json','w') as f:
#   json.dump(f,mashups,indent=1)

for index,mashup in enumerate(mashups):
  if not mashup['available']:
    page = requests.get(mashup['url'])
    fname = '%s.html' % mashup['url'].split('/')[-1]
    fpath = 'data/01-raw-mashups/%s' % fname
    print index,len(mashups),fpath
    with open(fpath,'w') as f:
      f.write(page.content)
    time.sleep(10+random.random()*10)


