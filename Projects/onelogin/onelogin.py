#!/usr/local/bin/python3

# This script can go and change the role of a user in OneLogin

import requests
import csv
from colorama import Fore, Style
from variables import client_id, secret

# Variables
roles_url = 'https://api.us.onelogin.com/api/1/roles'
users_url = 'https://api.us.onelogin.com/api/1/users/?email=%s&fields=id, email'
add_roles_url = 'https://api.us.onelogin.com/api/1/users/%s/add_roles'
remove_roles_url = 'https://api.us.onelogin.com/api/1/users/%s/remove_roles'


# Acquiring of the token
r = requests.post('https://api.us.onelogin.com/auth/oauth2/v2/token', auth=(client_id, secret), json={"grant_type": "client_credentials"})

response = r.json()

token = response['access_token']

print(Fore.MAGENTA + "############################################\nSuper-Awesome OneLogin Role Manipulator 5000\n"
                     "############################################")

while True:
    while True:
        # This asks for user input and then goes and gathers the different roles in OneLogin
        request_roles = input(Fore.CYAN + "Do you need a list of role IDs? (Y/n) " + Style.RESET_ALL)
        request_roles = request_roles[0].lower()
        if request_roles == '' or request_roles not in ['y', 'n']:
            print(Fore.RED + "Please answer with a 'yes' or 'no'!" + Style.RESET_ALL)
        else:
            break

    if request_roles == 'y':
        print(Fore.CYAN + "Here is a list of all the roles and their IDs:\n-----------------------------------------------" + Style.RESET_ALL)
        next_page = True
        while next_page:
            r = requests.get(roles_url, headers={"Authorization": "Bearer " + token})

            response = r.json()

            for role_data in response['data']:
                role_id = str((role_data.get('id')))
                name = (role_data.get('name'))
                print(Fore.YELLOW + role_id + Style.RESET_ALL + " " + name)

            if r.json()['pagination']['next_link'] is None:
                next_page = False
            else:
                new_roles_url = roles_url + '?after_cursor=' + r.json()['pagination']['after_cursor']
                r = requests.get(new_roles_url, headers={"Authorization": "Bearer " + token})
                response = r.json()

                if r.json()['pagination']['next_link'] is None:
                    next_page = False

                response = r.json()
                for role_data in response['data']:
                    role_id = str((role_data.get('id')))
                    name = (role_data.get('name'))
                    print(Fore.YELLOW + role_id + Style.RESET_ALL + " " + name)

    if request_roles == 'n':
        while True:
            custom_role_id = input(
                Fore.CYAN + "Please enter the role ID you wish to use: " + Style.RESET_ALL)
            if len(custom_role_id) != 6:
                print(
                    Fore.RED + 'Role ID must be six digits in length. Try again.' + Style.RESET_ALL)
            else:
                custom_role_id = int(custom_role_id)
                break

    else:
        while True:
            custom_role_id = input(Fore.CYAN + "Please enter the role ID you wish to use: " + Style.RESET_ALL)
            if len(custom_role_id) != 6:
                print(Fore.RED + 'Role ID must be six digits in length. Try again.' + Style.RESET_ALL)
            else:
                custom_role_id = int(custom_role_id)
                break

    while True:
        add_remove = input(Fore.CYAN + "To add users to role, press " + Fore.YELLOW + "`1`" + Style.RESET_ALL + Fore.CYAN + ", to remove, press " + Fore.YELLOW + "`2`" + Style.RESET_ALL + ": " + Style.RESET_ALL)
        if add_remove == '' or add_remove not in ['1', '2']:
            print(Fore.RED + "Please enter a '1' or '2'." + Style.RESET_ALL)
        else:
            add_remove = int(add_remove)
            break

    if add_remove == 1:

        # This reads an emails.csv file and takes those email addresses and adds the selected role to the users
        with open('emails.csv', 'r') as f:
            file = csv.reader(f)
            for row in file:
                email = (row[0])

                r = requests.get(users_url % email, headers={"Authorization": "Bearer:" + token})

                data = r.json()

                for id_number in data['data']:
                    user_id = str((id_number.get('id')))
                    # print(user_id + " " + email)
                    payload = {
                        'role_id_array': [custom_role_id]
                    }
                    r = requests.put(add_roles_url % user_id, headers={"Authorization": "Bearer:" + token, 'Content-Type': 'application/json'}, json=payload)
                    response = r.json()
                    if r.status_code == 200:
                        print(Fore.GREEN + email + " added successfully." + Style.RESET_ALL)
                    else:
                        error_code = response.get('status').get('message')
                        if "included" in error_code:
                            print(Fore.RED + email + " is already a member of the role" + Style.RESET_ALL)
                        else:
                            print(r.content)

    # This reads an emails.csv file and takes those email addresses and removes the selected role from the users
    elif add_remove == 2:

        with open('emails.csv', 'r') as f:
            file = csv.reader(f)
            for row in file:
                email = (row[0])

                r = requests.get(users_url % email, headers={"Authorization": "Bearer:" + token})

                data = r.json()

                for id_number in data['data']:
                    user_id = str((id_number.get('id')))
                    # print(user_id + " " + email)
                    payload = {
                        'role_id_array': [custom_role_id]
                    }
                    r = requests.put(remove_roles_url % user_id,
                                     headers={"Authorization": "Bearer:" + token, 'Content-Type': 'application/json'},
                                     json=payload)
                    response = r.json()
                    if r.status_code == 200:
                        print(Fore.GREEN + email + " removed successfully." + Style.RESET_ALL)
                    else:
                        error_code = response.get('status').get('message')
                        if "not included" in error_code:
                            print(Fore.RED + email + " isn't a member of the role" + Style.RESET_ALL)
                        else:
                            print(r.content)

    # This asks if user wants to run through the script again
    while True:
        carry_on = input(Fore.CYAN + "Do you want to add users to another role? (Y/n) " + Style.RESET_ALL)
        carry_on = carry_on[0].lower()

        if carry_on == '' or carry_on not in ['y', 'n']:
            print(Fore.RED + "Please answer with a 'yes' or 'no'." + Style.RESET_ALL)
        else:
            break

    if carry_on == 'y':
        continue
    else:
        print(Fore.RED + "Ending script" + Style.RESET_ALL)
        exit()
