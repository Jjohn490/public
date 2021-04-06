#!/usr/bin/env python3

# This script goes and pulls all the users from Google and compares them to the list pulled from BambooHR report.
# It takes all users and adds their managers to a dictionary and then uses that dictionary to do a 'patch' to
# each user in Google Workspace, updating their manager to the appropriate person.

import time
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from bhr_managers import *

# Some required Google variables
scopes = ['https://www.googleapis.com/auth/admin.directory.user']
creds = 'oauth2service.json'

delegate = 'email@email.com'  # Service account will impersonate this user. Must have proper admin privileges in G Suite.
target = 'email.com'  # Service account wants to access data from this domain.


class Google:

    def __init__(self):

        self.service = None
        self.next_page = None
        self.manager_dict = None
        self.users = None
        self.google_users = []
        self.manager_dict = {}
        self.start = time.time()

        # Starts a timer to know how long whole script takes to run
        self.start_time()

        # Authenticates to Google and builds the service using the assing Google variables
        credentials = service_account.Credentials.from_service_account_file(creds, scopes=scopes)
        credentials_delegated = credentials.with_subject(delegate)
        self.service = build('admin', 'directory_v1', credentials=credentials_delegated, cache_discovery=False)

    def find_users(self):  # Does an initial search for users and assigns 'nextPageToken' to be used in further requests

        logging.info("Finding initial batch of users...")
        request = self.service.users().list(domain=target, orderBy='email').execute()
        self.users = request.get('users', [])
        self.next_page = request.get('nextPageToken', {})
        self.append_to_dict()
        self.more_users()

    def more_users(self):  # Uses that 'nextPageToken' to find the remainder of the users until it no longer returns 'nextPageToken'

        logging.info("Finding more users...")
        looper = True
        while looper:
            if self.next_page:
                request = self.service.users().list(domain=target, pageToken=self.next_page, orderBy='email').execute()
                self.users = request.get('users', [])
                self.append_to_dict()
                self.next_page = request.get('nextPageToken', {})
            else:
                looper = False

    def append_to_dict(self):  # Creates a list of all the users retrieved from Google

        if not self.users:
            logging.error("No users is the domain")
        else:
            for user in self.users:
                email = user['primaryEmail']
                self.google_users.append(email)

    def dict_maker(self):  # Creates a dictionary matching user from Google with their user in the BambooHR report and puts manager as value

        logging.info("Making dictionary of user and manager emails")
        for key in bamboo_supervisor_email_dict.keys():
            for item in self.google_users:
                if key in item:
                    self.manager_dict[item] = bamboo_supervisor_email_dict[key]

        logging.info(str(len(self.google_users)) + " total Google users found.")
        logging.info(str(len(self.manager_dict)) + " users from BambooHR will be updated with manager emails.")

    def update(self):  # This goes and updates everyone in the dictionary (user and manager) in Google

        logging.info("Updating manager emails in Google Workspace")
        for k, v in list(self.manager_dict.items()):
            email = k
            supervisor = v
            body = {'relations': [{'type': 'manager', 'value': supervisor}]}
            self.service.users().patch(userKey=email, body=body).execute()
            logging.info(email + " --> " + supervisor)

    def start_time(self):

        self.start = time.time()
        mst_time = datetime.datetime.fromtimestamp(self.start)
        logging.info("Started at: " + str(mst_time))

    def end_time(self):

        end = time.time()
        mst_time = datetime.datetime.fromtimestamp(end)
        logging.info("Ended at: " + str(mst_time))
        elapsed_time = (time.time() - self.start)
        converted_time = str(datetime.timedelta(seconds=elapsed_time))
        logging.info("It took " + converted_time + " to complete.")


if __name__ == '__main__':
    run = Google()
    run.find_users()
    run.dict_maker()
    run.update()
    run.end_time()
