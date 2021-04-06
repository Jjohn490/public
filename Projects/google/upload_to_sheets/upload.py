#!/usr/bin/env python3

# This script creates a dataframe using Pandas from the data in `github_to_sheets.py' and 'onelogin_to_sheets.py'.
# It then goes and uploads that to a specific Google Sheets document and a specific sheet inside of that document,
# clearing out the old data and uploading the new stuff.

import pygsheets
import pandas as pd
import logging


class Upload:

    def __init__(self, dictionary, column1, column2, sort_by, sheet_key, sheet_id):
        #  The next six variables are sent through from the other scripts
        self.dictionary = dictionary  # 1
        self.column1 = column1  # 2
        self.column2 = column2  # 3
        self.sort_by = sort_by  # 4
        self.sheet_key = sheet_key  # 5
        self.sheet_id = sheet_id  # 6
        self.sorted_df = None  # Sets this to None as it's assigned in pandas method

        self.pandas()  # Calls the pandas method
        self.uploader()  # Calls the uploader method

    def pandas(self):  # This method creates the pandas dataframe that is then passed to the Google Sheets uploader

        df = pd.DataFrame(list(self.dictionary.items()), columns=[self.column1, self.column2])
        logging.info("Pandas dataframe created.")
        self.sorted_df = df.sort_values(by=[self.sort_by], ignore_index=True)  # Sorts the values based on 'sort_by' variable in ascending mode

    def uploader(self):  # This method uploads the data to the specified Google Sheets document

        gc = pygsheets.authorize(service_file='client_secret.json')  # Authorizes Pygsheets to grants access to Google Sheets
        sheet = gc.open_by_key(self.sheet_key)  # Opens the Google Sheet by its key value
        wks = sheet[self.sheet_id]  # Sets the current sheet inside of the spreadsheet
        wks.clear(start='A', end='B')  # Clears old data from Column A and B in the sheet
        wks.set_dataframe(self.sorted_df, (1, 1))  # Sets the new data based on the Pandas dataframe
        logging.info("Data written to spreadsheet.")
