import pandas as pd
import sqlalchemy
import urllib
import re
import os
from datetime import datetime as dt
from dotenv import load_dotenv
load_dotenv() #loads environment variables from a .env file

def find_header(file_path, sheet_name):
    """Find where actual data starts in Excel sheet avoiding empty rows and columns"""
    try:
        # Read the first 10 rows and 5 columns
        df_subset = pd.read_excel(file_path, sheet_name=sheet_name, nrows=10, usecols="A:E")
        
        # Iterate over the indices of the rows in the DataFrame
        for row_index in range(len(df_subset)):
            # Retrieve the row as a list of values
            row_values = df_subset.iloc[row_index].tolist()
            
            # Check if all elements in the row are not empty or "null"
            if all(pd.notna(value) and value != "null" for value in row_values):
                return row_index

        # if header row is not found
        return  None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# # Example usage
# header_row_index = find_header('Streamlit_ClaimTool/ExcelTestFile.xlsx')
# print(f"Header row index: {header_row_index}")


def load_data(file_path, sheet_name):
    """Load data from an Excel or CSV file starting from the header row"""
    try:
        # Find the header row index
        header_row_index = find_header(file_path, sheet_name)
        
        if header_row_index is None:
            print("Header row not found.")
            return None
        
        # if 0 then do not skip any rows
        skiprows = header_row_index + 1 if header_row_index > 0 else None
        
        # Load the data starting from the header row
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)

        # Check if the DataFrame is empty
        if df.empty:
            print("The Excel file has no data.")
            return None
        
        
        # Convert all columns to string to avoid type conversion issues
        df = df.map(str)
        
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None


def load_to_azure_sql(df, table_name, server, database, username, password):
    """
    Load a DataFrame to Azure SQL Database.
    
    Parameters:
    df (DataFrame): The DataFrame to load.
    table_name (str): The name of the table to load the data into.
    server (str): The server name.
    database (str): The database name.
    username (str): The username.
    password (str): The password.
    """
    try:
        # Create the connection string
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        connection_uri = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"
        
        # Create the SQLAlchemy engine
        engine = sqlalchemy.create_engine(connection_uri)
        
        # Load the DataFrame to the SQL table
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print("Data loaded successfully to Azure SQL Database.")
    except Exception as e:
        print(f"Error loading data to Azure SQL Database: {e}")

# Example usage
if __name__ == "__main__":
    # Sample DataFrame
    data = {'Name': ['John', 'Anna', 'Peter'], 'Age': [28, 24, 35]}
    df = pd.DataFrame(data)
    
    # Azure SQL Database credentials
    server = os.getenv("az_sql_server") 
    database = os.getenv("az_database") 
    username = os.getenv("az_username") 
    password = os.getenv("az_password") 
    # Load the DataFrame to Azure SQL Database
    load_to_azure_sql(df, 'PythonTestTable', server, database, username, password)


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



# def clean_data(df):
#     """Clean and organize the DataFrame"""
#     df = df.dropna()  # Example: Drop rows with missing values
#     df = df.rename(columns=lambda x: x.strip())  # Strip whitespace from column names
#     return df

# def summarize_data(df):
#     """Return a summary of the DataFrame"""
#     return df.describe()
