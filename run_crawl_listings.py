import requests
import time
import random

# page = requests.get('http://www.programmableweb.com/mashup/getsentiment-restaurant-reviews')

# print page.content

for listing_index in range(0,761):
  print(listing_index)
  url = 'http://www.programmableweb.com/category/all/apis?page=%s' % listing_index
  print(url)
  page = requests.get(url)
  fname = 'data/01-raw-api-listings/api-listing-%03d.html' % listing_index
  print(fname)
  with open(fname,'wb') as f:
    f.write(page.content)
  time.sleep(5+random.random()*3)

for listing_index in range(0,257):
  print(listing_index)
  url = 'http://www.programmableweb.com/category/all/mashups?page=%s' % listing_index
  print(url)
  page = requests.get(url)
  fname = 'data/01-raw-mashup-listings/mashups-listing-%03d.html' % listing_index
  print(fname)
  with open(fname,'wb') as f:
    f.write(page.content)
  time.sleep(10+random.random()*10)
