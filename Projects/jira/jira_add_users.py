#!/usr/bin/python3

import requests
from requests.auth import HTTPBasicAuth
import json
import variables

# This script adds specific user to specific group inside of Jira. Can easily be modified.

# Setting variables from the `variables` file
username = variables.username
api = variables.api
accountid = variables.accountid

url = "https://subdomain.atlassian.net/rest/api/3/group/user"

auth = HTTPBasicAuth(username, api)

headers = {
           "Accept": "application/json",
              "Content-Type": "application/json"
              }

query = {
           'groupname': 'sAPIen'
           }

payload = json.dumps({
      "accountId": accountid
      })

response = requests.request(
           "POST",
              url,
                 data=payload,
                    headers=headers,
                       params=query,
                          auth=auth
                          )

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

