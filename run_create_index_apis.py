# run_create_index_apis.py

# run_create_index.py

import glob
from bs4 import BeautifulSoup
import simplejson as json
import pandas as pd

indices = glob.glob('data/01-raw-apis/api-listing-*.html')
local_files = list()

for fname in glob.glob('data/01-raw-apis/*.html'):
  local_files.append(fname.split('/')[-1])

apis = list()
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
  rows = table.select('tbody tr')
  print '..scraping %s rows' % len(rows)
  for row in rows:
    # print row
    data = dict()
    for index,cell in enumerate(row.find_all('td')):
      data[headers[index]] = cell.text.strip()
      if index == 0:
        data['url'] = 'http://programmableweb.com%s' % cell.a['href']
        # print data['url']
        keepcharacters = ('_', '-')
        filestring = data['url'].split('/')[-1]
        # Some of the API names e.g. start with a full stop (.). This results into a
        # non-valid filename
        filestring = ''.join(c for c in filestring if c.isalnum() or c in keepcharacters).rstrip()
        data['id'] = data['url'].split('/')[-1]
        data['filename'] = '%s.html' % filestring
    # Finally, checking whether such a file already exists
    data['available'] = data['filename'] in local_files
    # print data
    apis.append(data)

print 'In total %s apis extracted, serializing' % len(apis)
print 'Local files: %s' % len(local_files)

# with open('data/02-refined/api_index.json','w') as f:
#   json.dump(apis,f,indent=1)

with open('data/02-refined/api_index.json','w') as f:
  json.dump(apis, f, indent=1)

print 'Status:'
df_api = pd.DataFrame.from_dict(apis)
print df_api.available.value_counts()

print 'Files not available:'
print df_api[df_api.available == False].api_name
