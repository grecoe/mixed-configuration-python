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

# Use endpoints from INI and supplement with JSON values
legal_endpoint = config.LegalUri.format(config.PlatformName)
entitlements_endpoint = config.EntitlementsUri.format(config.PlatformName)

# Use SP information from keyvault
print(".....acquire token")
platform_cred = Credential(config.Client, config.Secret)
print("USER:", platform_cred.user_id)

print(".....prepare uris")
get_groups_uri = entitlements_endpoint + "/groups"
get_legal_uri = legal_endpoint + "/legaltags"

print(".....create generic headers")
headers = {
    "Authorization" : "Bearer {}".format(platform_cred.get_application_token()),
    "data-partition-id" : config.DataPartition
}

print(".....request legal tags")
response = requests.get(get_legal_uri, headers=headers)
print("Legal Tags Status: ", response.status_code)

if response.status_code == 200:
    print("....found legal tags, get something specific: *-Wellbore-Legal-Tag-*")
    data = response.json()
    if "legalTags" in data:
        if isinstance(data["legalTags"], list):
            for tag in data["legalTags"]:
                if "-Wellbore-Legal-Tag-" in tag["name"]:
                    print("Found usable legal tag: {}".format(tag["name"]))
                    break


print(".....request grouops")
response = requests.get(get_groups_uri, headers=headers)
print("Status: ", response.status_code)

print(".....get members of users.data.root")
if response.status_code == 200:
    groups = response.json()["groups"]
    for gp in groups:
        if gp["name"] == "users.data.root":
            gp_user_uri = entitlements_endpoint + "/groups/{}/members".format(gp["email"])
            headers["group-email"] = gp["email"]
            response = requests.get(gp_user_uri, headers = headers)
            print("Status: ", response.status_code)
            print(json.dumps(response.json(), indent=4))
            break