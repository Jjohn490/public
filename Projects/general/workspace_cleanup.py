#!/usr/bin/env python3

# This script goes and removes old Amazon Workspaces if they haven't been used since a set amount of days

import boto3
import json
from datetime import date, timedelta
from colorama import Fore

# Tells boto3 what profile and region to use
session = boto3.Session(profile_name='corp', region_name='eu-west-1')

# Users the 'workspaces' boto3 module
client = session.client('workspaces')

# Since we're limited on how many results spit out, a paginator is needed to iterate through all the pages
details_paginator = client.get_paginator('describe_workspaces')

details_iterator = details_paginator.paginate()

connection_paginator = client.get_paginator('describe_workspaces_connection_status')

connection_iterator = connection_paginator.paginate()

# Creates a list that details_stuff() will append to which will be used later by connection_stuff()
detail_list = []

# Creates a list that connection_stuff() will append to that contains old workspace IDs
old_workspaces_list = []


# This function takes user input on how many days they want to subtract and check against)
def initial():
    global string_date
    while True:
        try:
            days_to_subtract = int(input("How many days prior do you want to check against from today's date? "))
            # This takes today's today and subtracts the number of days we defined above
            start_date = date.today() - timedelta(days_to_subtract)
            # This converts the "datetime" to a usable string
            string_date = start_date.strftime('%Y-%m-%d')
            break

        except ValueError:
            print("Please enter a valid number.")


# This function is grabbing the workspace details ('describe_workspace')
def details_stuff():
    while True:
        try:
            for page in details_iterator:
                details_data = json.dumps(page, indent=4, default=str)
                details_data = json.loads(details_data)

                for item in details_data['Workspaces']:
                    workspace_id = item['WorkspaceId']
                    username = item['UserName']
                    identity = workspace_id + " (" + username + ")"
                    detail_list.append(identity)
                    # print(Fore.YELLOW + username + Fore.RESET + " " + Fore.BLUE + workspace_id)
            break

        except Exception as e:
            print(e)


# This function grabbing the connection details of the workspaces ('describe_workspaces_connection_status')
def connection_stuff():
    while True:
        try:
            for connection in connection_iterator:
                connection_data = json.dumps(connection, indent=4, default=str)
                connection_data = json.loads(connection_data)

                for stamp in connection_data['WorkspacesConnectionStatus']:
                    if 'LastKnownUserConnectionTimestamp' in stamp:
                        old_date = stamp['LastKnownUserConnectionTimestamp'][0:10]

                        if old_date <= string_date:

                            old_workspace = stamp['WorkspaceId']

                            for identifier in detail_list:
                                if old_workspace in identifier:
                                    print(Fore.YELLOW + identifier + Fore.RESET + " hasn't accessed been accessed since " + Fore.RED + old_date + Fore.RESET)
                                    old_workspaces_list.append(identifier)
            break

        except Exception as e:
            print(e)


# This will delete the workspaces identified to be older than days_to_subtract
def delete_stuff():
    while True:
        try:
            for each in old_workspaces_list:
                first_id = each.split()[0]
                print("\n" + Fore.YELLOW + each + Fore.RESET)
                confirm = input("\nDo you want to delete the above workspaces? (y/N): ")
                if confirm == "Yes" or confirm == "yes" or confirm == "y" or confirm == "Y":

                    try:
                        # Uncomment if you actually want to delete stuff! AHHH!
                        # termination = client.terminate_workspaces(TerminateWorkspaceRequests=[{'WorkspaceId': first_id}])
                        if termination['FailedRequests']:
                            print('Failed to terminate: ' + termination['FailedRequests'])
                            print(Fore.YELLOW + each + Fore.RESET + Fore.GREEN + " has been deleted." + Fore.RESET)
                        else:
                            print(termination)
                            print(Fore.YELLOW + each + Fore.RESET + Fore.GREEN + " has been deleted." + Fore.RESET)
                    except Exception as e:
                        print("Error: " + e)

                else:
                    print(Fore.YELLOW + each + Fore.RESET + Fore.RED + " not deleted.\n" + Fore.RESET)
                    continue

            print("That's all of em! Bye!")
            break

        except Exception as e:
            print(e)


if __name__ == '__main__':
    initial()
    details_stuff()
    connection_stuff()
    details_stuff()
