import sqlalchemy 
import urllib
import pandas as pd
import re
from datetime import datetime as dt
import os
from dotenv import load_dotenv
load_dotenv() #loads environment variables from a .env file


def remove_extension(filename):
    """Remove the file extension from the filename."""
    return re.sub(r'\.[^.]+$', '', filename)

def extract_name_date(stringname):
    '''
    The function returns two values: name (file or folder), and date.
    These values are returned as elements of a tuple, but we don't explicitly create a tuple. 
    Python automatically packs them into a tuple because of the comma-separated values.
    When calling the function, we can unpack the returned tuple into separate variables file_name and file_date.

    Example usage:
    filename = "JohnEastern 08152024"
    file_name, file_date = extract_name_date(filename)
    print(f"File Name: {file_name}, File Date: {file_date}")
    '''

    # Remove extension if exists
    string_no_extension = remove_extension(filename=stringname)

    # Define regex patterns to extract dates
    date_patterns = [
        r'(\d{1,2}\.\d{1,2}\.\d{4})',   # MM.DD.YYYY pattern
        r'(\d{1,2}-\d{1,2}-\d{4})',     # MM-DD-YYYY pattern
        r'(\d{1,2}\d{1,2}\d{4})',       # MMDDYYYY pattern
        r'(\d{4}\d{2}\d{2})',           # YYYYMMDD pattern
        r'(\d{4}-\d{2}-\d{2})',         # YYYY-MM-DD pattern
    ]

    # Define the desired date format
    desired_date_format = "%m-%d-%Y"

    # Extract the date from the filename using different patterns
    date = None
    for pattern in date_patterns:
        date_match = re.search(pattern, string_no_extension)
        if date_match:
            # extract the date string that matches the regex pattern from the filename
            date = date_match.group(0)  
            # Cut off the matched date from the remaining file name
            string_no_extension = string_no_extension.replace(date, '').strip()
            break

    if date:
        try:
            if '-' in date:
                if len(date) == 10:  # Check if the date is in YYYY-MM-DD format
                    date_obj = dt.strptime(date, "%Y-%m-%d")
                else:
                    date_obj = dt.strptime(date, "%m-%d-%Y")
            elif '.' in date:
                date_obj = dt.strptime(date, "%m.%d.%Y")
            elif len(date) == 8 and date.isdigit():
                if int(date[:2]) <= 12:  # Check if the first two digits are a valid month
                    date_obj = dt.strptime(date, "%m%d%Y")
                else:
                    date_obj = dt.strptime(date, "%Y%m%d")
            else:
                date_obj = dt.strptime(date, "%m%d%Y")
            string_date = date_obj.strftime(desired_date_format)
        except ValueError:
            string_date = dt.now().strftime(desired_date_format)
    else:
        string_date = dt.now().strftime(desired_date_format)

    return string_no_extension, string_date
# #'''
# # Example usage
# filename = "JohnEastern 2023-01-01.xlsx"
# file_name, file_date = extract_name_date(filename)
# print(f"File Name: {file_name}, File Date: {file_date}")
# #'''
