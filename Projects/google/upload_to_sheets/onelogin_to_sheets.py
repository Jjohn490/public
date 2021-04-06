#!/usr/bin/env python3

# This script goes and pull all the active users from our OneLogin account and adds them by name and email to a
# dictionary that is passed through to 'upload.py' which will upload and update a Google Sheet that contains
# the list of all our active users.

import time
import datetime
import requests
from variables import client_id, secret
import upload as up
import logging
from logging.handlers import RotatingFileHandler

# Dictionary
user_data_dict = {}

# Variables
users_url = 'https://api.us.onelogin.com/api/1/users/'
log = 'onelogin_to_sheets.log'
column1 = 'Name'
column2 = 'Email'
sheet_key = 'sheetkey'
sheet_id = 1
sort_by = column1
dictionary = user_data_dict

# Starts requests in a Session
session = requests.Session()  # Use this to start a session instead of doing a HTTP call each time! Woot!


def logger_setup():  # Sets the log file and rotates logs if exceeds 1MB.

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        handlers=[RotatingFileHandler(log, maxBytes=100000, backupCount=10)])


class OneLogin:

    def __init__(self):

        self.token = None
        self.data = None
        self.start = time.time()

        # Starts a timer to know how long whole script takes to run
        self.start_time()

    def run_all(self):  # This functions run all the appropriate functions instead of having to call them one by one
        self.get_token()
        self.get_user_info()
        self.get_more_pages()

    def get_token(self):  # This function acquires a bearer token that gives us access to do API calls

        try:
            r = session.post('https://api.us.onelogin.com/auth/oauth2/v2/token', auth=(client_id, secret), json={"grant_type": "client_credentials"})
            response = r.json()
            self.token = response['access_token']
            logging.info("OneLogin token acquired")
        except requests.exceptions.RequestException as error:
            logging.error("Error: ", error)

    def get_user_info(self):  # This function goes and retrieves specific user info from OneLogin

        try:
            r = session.get(users_url + '?fields=email, firstname, lastname, status', headers={"Authorization": "Bearer " + self.token})
            self.data = r.json()
            logging.info("Finding initial batch of users...")
            self.dict_maker()
        except requests.exceptions.RequestException as error:
            logging.error("Error: ", error)

    def get_more_pages(self):  # This function will go and retrieve additional pages of users, if additional pages exist

        logging.info("Finding more users...")
        next_page = True
        while next_page:
            if self.data['pagination']['next_link'] is None:
                next_page = False
            else:
                next_user_url = users_url + '?after_cursor=' + self.data['pagination']['after_cursor'] + '?fields=email, firstname, lastname, status'
                try:
                    r = session.get(next_user_url, headers={"Authorization": "Bearer " + self.token})
                    self.data = r.json()
                    self.dict_maker()
                except requests.exceptions.RequestException as error:
                    logging.error("Error: ", error)

    def dict_maker(self):

        for item in self.data['data']:
            status = item['status']
            if status == 1:
                email = item['email']
                name = item['firstname'] + " " + item['lastname']
                user_data_dict[name] = email

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
    run = OneLogin()
    run.run_all()
    up.Upload(dictionary, column1, column2, sort_by, sheet_key, sheet_id)
    run.end_time()
