#!/usr/bin/env python3

# This script goes and calls BambooHR API and pull and specific custom report that has been made on my (Jesse's)
# BambooHR account. The report contains everyone who is a manager/supervisor by the "Is Supervisor?" field. It also
# holds all the manager's emails for each individual person. The extract_data function pulls out the necessary
# information and appends it to a list and a dictionary that are called in 'onelogin_user_modifier.py' script.

import requests
import logging
import variables
from logging.handlers import RotatingFileHandler

# Variables
api_key = variables.api_key
domain = 'domain'
url = f'https://{api_key}:x@api.bamboohr.com/api/gateway.php/{domain}/v1/reports/3113?format=json'
log = 'google_user_modifier.log'


def logger_setup():  # Sets the log file and rotates logs if exceeds 1MB.

    logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%d-%b-%y %H:%M:%S',
            handlers=[RotatingFileHandler(log, maxBytes=100000, backupCount=10)])


def report_request():  # Grabs the custom report from BambooHR

    logging.info("Running API request for custom report...")
    r = requests.get(url)
    if r.status_code == 200:
        logging.info("Connection established to BambooHR")
    else:
        logging.error("Connection error. Try again" + str(r.status_code))
        exit()
    data = r.json()
    return data


bamboo_supervisor_list = []
bamboo_supervisor_email_dict = {}


def extract_data():  # Extracts necessary data from the custom report.

    data = report_request()
    for item in data['employees']:
        user_email = item['workEmail']
        supervisor_email = item['supervisorEmail']
        is_supervisor = item['-44']
        if user_email is not None:
            if is_supervisor is not None:
                bamboo_supervisor_list.append(user_email)
            if supervisor_email is not None:
                bamboo_supervisor_email_dict[user_email] = supervisor_email

    logging.info("Supervisor list updated and appended")
    logging.info("Supervisor email addresses updated")


logger_setup()
extract_data()
