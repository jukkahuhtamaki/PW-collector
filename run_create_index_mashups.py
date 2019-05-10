# run_create_index.py

import glob
from bs4 import BeautifulSoup
import json

indices = glob.glob('data/01-raw/mashups-page-*.html')
local_files = list()

for fname in glob.glob('data/01-raw-mashups/*.html'):
  local_files.append(fname.split('/')[-1])

mashups = list()
for fname in indices:
  print fname
  with open(fname) as f:
    content = f.read()
  soup = BeautifulSoup(content)
  # print soup.select('div.content')
  table = soup.find_all('table')[2]
  headers = list()
  for header in table.select('thead tr th'):
    headers.append(header.text.strip().lower().replace(' ','_'))
  # print headers
  for row in table.select('tbody tr'):
    data = dict()
    for index,cell in enumerate(row.find_all('td')):
      data[headers[index]] = cell.text.strip()
      if index == 0:
        data['url'] = 'http://programmableweb.com%s' % cell.a['href']
        # print data['url']
        data['filename'] = '%s.html' % data['url'].split('/')[-1]
    # Finally, checking whether such a file already exists
    data['available'] = data['filename'] in local_files 
    # print data
    mashups.append(data)

print 'In total %s mashups extracted, serializing' % len(mashups)

with open('data/02-refined/mashup_index.json','w') as f:
  json.dump(mashups,f,indent=1)
