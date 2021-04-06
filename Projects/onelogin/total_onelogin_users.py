# This script goes and grabs information from OneLogin about each user and assigns it to a dict

import json
import csv
from colorama import Fore, Style
from variables import client_id, secret
import requests
import pprint
import datetime
import time

# Variables
users_url = 'https://api.us.onelogin.com/api/1/users/'

# Acquiring of the token
r = requests.post('https://api.us.onelogin.com/auth/oauth2/v2/token', auth=(client_id, secret), json={"grant_type": "client_credentials"})

response = r.json()

token = response['access_token']

print(Fore.MAGENTA + "############################################\nSuper-Awesome OneLogin User Manipulator 5000\n"
                     "############################################" + Fore.RESET)
# Retrieving user info
user_data_dict = {}

session = requests.Session()  # Use this to start a session instead of doing a HTTP call each time! Woot!

r = session.get(users_url + '?fields=email, firstname, lastname, status', headers={"Authorization": "Bearer " + token})
data = r.json()
for item in data['data']:
    status = item['status']
    if status == 1:
        email = item['email']
        name = item['firstname'] + " " + item['lastname']
        user_data_dict[name] = email

next_page = True
while next_page:
    if data['pagination']['next_link'] is None:
        next_page = False

    else:
        next_user_url = users_url + '?after_cursor=' + data['pagination']['after_cursor'] + '?fields=email, firstname, lastname, status'
        r = session.get(next_user_url, headers={"Authorization": "Bearer " + token})
        data = r.json()

        for item in data['data']:
            status = item['status']
            if status == 1:
                email = item['email']
                name = item['firstname'] + " " + item['lastname']
                user_data_dict[name] = email

pprint.pprint(user_data_dict)
