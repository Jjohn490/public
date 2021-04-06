#!/usr/bin/env python3

# A Python script that goes and removes old TeamViewer computers

# A few required modules
import requests
from datetime import date, timedelta

# Optional. Delete if you don't want colors. Make sure to remove any code that show "Fore." or "Style."
from colorama import Fore, Style

# Change this to however many days prior you want to check against from today's date
days_to_subtract = 10

# This takes today's today and subtracts the number of days we defined above
start_date = date.today() - timedelta(days_to_subtract)

# This converts the "datetime" to a usable string
string_date = start_date.strftime('%Y-%m-%d')

print("Searching for old devices...\n------------------------------")

# TeamViewer API Endpoint
url = "https://webapi.teamviewer.com/api/v1/devices"

# Searches online for devices that are offline
querystring = {"online_state": "offline"}

# This is where you will add your token from TeamViewer, just after "Bearer"
headers = {
    'Authorization': "Bearer <toke>",
    }

# The actual API GET request
response = requests.get(url, headers=headers, params=querystring)

# Checks to make sure the connection is successful (200 = success)
if not response.status_code == 200:

    # Prints error if anything other than successful connection.
    print(Fore.RED + "Connection error. Try again. Error code " + str(response.status_code))
    print(Style.RESET_ALL)
    exit()

# Adds the results of the GET request to JSON
results = response.json()

# This for loop will look for devices that have "last_seen" in the fields, it will then cut the date out in the format of "2019-01-31".
# It will then check that 'old_date' against the 'string_date' and if it's less than or equal to, it prints out the device and last online date.
# If no devices were found that matched, it will print out "No devices were found"
try:
    found_device = False
    for item in results['devices']:

        if 'last_seen' in item:

            date = (item['last_seen'].split('T'))

            old_date = date[0]

            if old_date <= string_date:
                found_device = True
                print(Fore.BLUE + "Device" + Fore.RESET + " -- " + Fore.YELLOW + item['alias'] + Fore.RESET + " -- (Last Online: " + Fore.BLUE + old_date + Fore.RESET + ")")

    if not found_device:
        print(Fore.BLUE + "No devices were found")
        exit()

except Exception:

    print("Error")

# Prompts the user if they want to delete the above devices from TeamViewer
confirm = input("\nDo you want to delete the above devices? (y/N): ")

# If "Yes", it will run a new API call and delete the above devices matching on the same criteria as above.
if confirm == "Yes" or confirm == "yes" or confirm == "y" or confirm == "Y":

    print()

    try:
        for item in results['devices']:

            if 'last_seen' in item:

                date = (item['last_seen'].split('T'))

                old_date = date[0]

                if old_date <= string_date:

                    device_id = (item['device_id'])

                    delete_url = "https://webapi.teamviewer.com/api/v1/devices/" + device_id

                    # Make sure to uncomment out the line below if you want to actually delete devices.
                    # requests.delete(delete_url, headers=headers)

                    print(Fore.RED + "Device deleted" + Fore.RESET + " -- " + Fore.YELLOW + item[
                        'alias'] + Fore.RESET)

    except Exception:

        print("Error")

else:

    print(Fore.RED + "\nNo files deleted." + Style.RESET_ALL)

exit()
