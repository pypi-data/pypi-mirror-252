%load_ext autoreload
%autoreload 2

import os
import tonita
from tqdm import tqdm

tonita.api_key = "AIzaSyDQpEZnJ39eo_J-ta2FMYF9AusiCyTxhLo"
tonita.api_key = "AIzaSyBLIeq2bMBjBwX5o9ReqUi1Dcf7TTSd6Gc"
tonita.corpus_id = "edmunds"
tonita.corpus_id = "usa"
tonita.base_url="http://localhost:5000"

json_path =  '~/gcs/shopping_crawls/cars/edmunds/final_listing_jsons'
json_path = os.path.abspath(os.path.expanduser(json_path))

# json_path =  '~/gcs/shopping_crawls/cars/edmunds/final_listing_jsons/acura_vigor_pr.json'
# json_path = os.path.abspath(os.path.expanduser(json_path))


import requests
session = requests.Session()
tonita.listings.add(json_path=json_path, session=session)


from time import perf_counter

start = perf_counter()
tonita.listings.add(json_path=json_path)
print(perf_counter() - start)

all_file_names = os.listdir(json_path)
for fn in tqdm(all_file_names):
    tonita.listings.add(json_path=os.path.join(json_path, fn))
