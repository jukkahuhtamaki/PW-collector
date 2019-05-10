# run_scrape_mashups.py
from bs4 import BeautifulSoup
import simplejson as json

with open('data/02-refined/api_index.json') as f:
  api_index = json.load(f)

apis = list()
for index, api in enumerate(api_index):
  api['status'] = 'indexed'
  print index, api['id']
  if api['available']:
    fpath = 'data/01-raw-apis/%s' % api['filename']
    api['status'] = 'available'
    print fpath
    with open(fpath) as f:
      content = f.read()
    soup = BeautifulSoup(content)
    # print soup.select('div.content')
    div = soup.select('div.specs')
    if len(div) > 0:
      fields = dict()
      for field in div[0].select('div.field'):
        name = field.label.text.lower().replace(' ','_')
        values = list()
        for value in field.select('a'):
          values.append({
            'label': value.text,
            'key': value['href']
          })
        fields[name] = values
          # print value['href']
          # if name == 'url':
          #   fields[name] = value['href']
          # elif name == 'related_apis'
      api['details'] = fields
      if len(fields.keys()) > 0:
        api['status'] = 'details'
      apis.append(api)

with open('data/02-refined/apis.json','w') as f:
  json.dump(apis,f,indent=1)

