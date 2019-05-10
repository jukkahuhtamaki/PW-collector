# run_scrape_mashups.py
from bs4 import BeautifulSoup
import simplejson as json

with open('data/02-refined/mashup_index.json') as f:
  index = json.load(f)

mashups = list()
for mashup in index:
  if mashup['available']:
    mashup['id'] =  mashup['url'].split('/')[-1]
    fpath = 'data/01-raw-mashups/%s' % mashup['filename']
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
      mashup['details'] = fields
      # print json.dumps(mashup['details'], indent=1)
      if mashup['details'].has_key('related_apis'):
        for api in mashup['details']['related_apis']:
          api['id'] =  api['key'].split('/')[-1]
      mashups.append(mashup)

with open('data/02-refined/mashups.json','w') as f:
  json.dump(mashups,f,indent=1)

