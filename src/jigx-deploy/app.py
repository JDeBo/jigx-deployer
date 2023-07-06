import yaml
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

org_id = os.getenv("ORGANIZATION_ID")
solution_id = os.getenv("SOLUTION_ID")
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

jigx_dirs = ['databases', 'functions', 'jigs'] # List of dirs to parse through
req_body = {}

with open("../index.jigx", 'r') as index_in:
    index_object = yaml.safe_load(index_in) # yaml_object will be a list or a dict
    req_body = index_object
for dir in jigx_dirs:
    files = os.listdir(f'../{dir}')
    dir_object = {}
    for file in files:
        file_base = file.split('.jigx')[0] # Trim off extension for json obj
        with open(f"../{dir}/{file}", 'r') as file_in:
            file_object = yaml.safe_load(file_in)
            if file_object is None:
                file_object = {}
            dir_object[file_base] = file_object
    req_body[dir] = dir_object

with open("req_body.json", "w") as json_out:
    json.dump(req_body, json_out)

patch_url = f"{base_url}/organizations/{org_id}/solutions/{solution_id}/content"
headers = {
  'Content-Type': 'application/json',
  'Authorization': api_key
}
res = requests.patch(patch_url, data=json.dumps(req_body), headers=headers)
print(res.json())