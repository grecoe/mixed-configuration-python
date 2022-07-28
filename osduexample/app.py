"""
Simple application that uses the json, ini and a key vault to acquire information
about an OSDU instance. 

Generates a bearer token for a service principal (non user so no refresh token needed), 
and then retrieves the legal tags. 
"""

import sys
import os
import requests
import json
  
# Fix path to get configuration
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from configuration.config import Config
from auth import Credential

print(".....load configuration")
config = Config("./config.json")

legal_endpoint = config.LegalUri.format(config.PlatformName)

print(".....acquire token")
platform_cred = Credential(config.Client, config.Secret)

print(".....request legal tags")
get_legal_uri = legal_endpoint + "/legaltags"
headers = {
    "Authorization" : "Bearer {}".format(platform_cred.get_application_token()),
    "data-partition-id" : config.DataPartition
}

response = requests.get(get_legal_uri, headers=headers)
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))