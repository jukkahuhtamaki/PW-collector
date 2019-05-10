README.md

I am running this in CSC cloud cPouta (and on my Macbook)

First, let's set up the virtual environment (Python 3.6.4)

	python -m venv VENV
	source VENV/bin/activate
	pip install -r requirements.txt 

Creating data folders. One might want to automize this:

	mkdir data
	mkdir data/01-raw-api-listings
	mkdir data/01-raw-mashup-listings

Collect pages including API and mashup listings. Do note that list length is hard-coded. In all, this code is guaranteed not to work as you might think. It is developed for a one-off data collecting process a couple years ago 

	python run_crawl_listings.py

Create directories for API and mashup pages

	mkdir data/01-raw-apis
	mkdir data/01-raw-mashups

Create indices for APIs and mashups

	python run_create_index_apis.py
	python run_create_index_mashups.py

Crawl pages representing API and mashup data

	python run_crawl_apis.py
	python run_crawl_mashups.py

The index file must be reset at this point. For now, the API and mashup listings are re-scraped. TODO: Some optimization remains to be done.

	python run_create_index_apis.py
	python run_create_index_mashups.py

Scrape the data from API and mashup pages

	python run_scrape_apis.py
	python run_scrape_mashups.py


  mkdir data/02-refined



ETC

	run_scrape_apis.py
	
	run_resolve_locations.py
	
	run_geocode.py
	
	run_insert_regions.py
