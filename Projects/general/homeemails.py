#!/usr/bin/env python3

# This scripts pulls a report from BambooHR, parses out the data, and updates an email group in Google Workspaces via the GAM tool.

import requests
import os
from variables import key
from colorama import Fore, Style

# Variables
api_key = key
domain = 'domain'
url = 'https://{0}:x@api.bamboohr.com/api/gateway.php/{1}/v1/reports/2727?format=csv'.format(api_key, domain)

print(Fore.CYAN + "\nRunning API request for custom report...")
# Does an API request to the above URL
r = requests.get(url)

# Checks to make sure the connection is successful (200 = success)
if r.status_code == 200:

    print(Fore.YELLOW + "\nDone!\n---------------------------------------------------")

else:

    # Prints error if anything other than successful connection.
    print(Fore.RED + "Connection error. Try again")
    exit()

print(Fore.CYAN + "\nWriting results to .csv...")
# Write results to .CSV
f = open('/tmp/homeemails.csv', "w")
f.write(r.text)
f.close()
print(Fore.YELLOW + "\nDone!\n---------------------------------------------------")

print(Fore.CYAN + "\nRunning GAM to update user list for Home Benefits Wiki group...\n")
# Runs a GAM command to update group members
os.system("gam update group homebenefitswiki@email.com sync member notsuspended csv /tmp/homeemails.csv:'Home Email'")
print(Fore.YELLOW + "\nDone!\n---------------------------------------------------")

print(Style.RESET_ALL)
