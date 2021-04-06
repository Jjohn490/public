#!/usr/bin/env python3

# This script goes and pull all the active users from our Github account and adds them by username and email to a
# dictionary that is passed through to 'upload.py' which will upload and update a Google Sheet that contains
# the list of all the usernames and their emails. Useful to know which username belongs to which person.

import time
import datetime
import requests
from variables import bearer
from queries import query_1, query_2
import upload as up
import logging
from logging.handlers import RotatingFileHandler

# Dictionary
user_dict = {}

# Variables
log = 'github_to_sheets.log'
column1 = 'Username'
column2 = 'Email'
sheet_key = 'sheetkey'
sheet_id = 0
sort_by = column2
dictionary = user_dict

# Starts requests in a Session
session = requests.Session()  # Use this to start a session instead of doing a HTTP call each time! Woot!
headers = {"Authorization": "Bearer " + bearer}


def logger_setup():  # Sets the log file and rotates logs if exceeds 1MB.

    logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%d-%b-%y %H:%M:%S',
            handlers=[RotatingFileHandler(log, maxBytes=100000, backupCount=10)])


class Github:

    def __init__(self):
        self.variables = None
        self.filtered = None
        self.end_cursor = None
        self.next_page = None
        self.request = None
        self.data = None
        self.start = time.time()

        # Starts a timer to know how long whole script takes to run
        self.start_time()

    def get_users(self):  # This method does the initial query to GitHub for first batch of users

        logging.info("Finding initial batch of users...")
        self.request = session.post('https://api.github.com/graphql', json={'query': query_1}, headers=headers)
        if self.request.status_code == 200:
            self.next_page_stuff()
            if self.next_page:
                self.data_extraction()
                self.more_users()
        else:
            logging.error(f"Query failed to run by returning code of {self.request.status_code}. {query_1}")

    def more_users(self):  # This method does additional queries to grab all users depending on if there are multiple pages

        logging.info("Finding more users...")
        while True:
            self.request = session.post('https://api.github.com/graphql', json={'query': query_2, 'variables': self.variables}, headers=headers)
            if self.request.status_code == 200:
                self.next_page_stuff()
                if self.next_page is False:
                    break
                else:
                    self.data_extraction()
            else:
                logging.error(f"Query failed to run by returning code of {self.request.status_code}. {query_1}")

    def next_page_stuff(self):  # This method just goes and grabs the 'hasNextPage' value

        self.data = self.request.json()
        self.next_page = self.data['data']['organization']['samlIdentityProvider']['externalIdentities']['pageInfo']['hasNextPage']

    def data_extraction(self):  # This method extracts the useful information from the results

        self.end_cursor = self.data['data']['organization']['samlIdentityProvider']['externalIdentities']['pageInfo']['endCursor']
        self.variables = {"cursor": self.end_cursor}
        self.filtered = self.data['data']['organization']['samlIdentityProvider']['externalIdentities']['edges']
        self.filtered_results()

    def filtered_results(self):  # This method further filters the results to grab just the username and emails

        for item in self.filtered:
            if item['node']['user']:
                email = item['node']['samlIdentity']['nameId']
                username = item['node']['user']['login']
                user_dict[username] = email
            else:
                username = 'N/A'
                email = item['node']['samlIdentity']['nameId']
                user_dict[username] = email

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
    logger_setup()
    run = Github()
    run.get_users()
    up.Upload(dictionary, column1, column2, sort_by, sheet_key, sheet_id)
    run.end_time()
