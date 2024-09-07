import sys
import time
import warnings
import pandas as pd
from seaspan_booking import book
from datetime import datetime
import requests
import pandas as pd
from io import BytesIO
from oauth import get_OAuth_token




def get_book():

    # Define constants
    search_query = f'{datetime.now().strftime('%b')}-Obws.xlsm'  # File name to search for
    print("authenticating")
    access_token = get_OAuth_token()
    # Define the API endpoint
    graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/root/search(q='{search_query}')"

    # Set up the request headers
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the request to search for the file
    print(f"Searching for file: {search_query}")
    response = requests.get(graph_api_url, headers=headers)

    if response.status_code == 200:
        results = response.json().get('value', [])
        if results:
            print(f"Found {len(results)} file(s).")
            for item in results:
                file_name = item['name']
                parent_reference = item.get('parentReference', {})
                file_path = parent_reference.get('path', 'Root Directory')
                print(f"Found file: {file_name} at {file_path}")
                # You can store the item ID or path for further operations
                file_id = item['id']
                full_path = f"{file_path}/{file_name}" if file_path != 'Root Directory' else file_name
                print(f"File ID: {file_id}, Full Path: {full_path}")

                # Fetch the file content
                file_content_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
                file_response = requests.get(file_content_url, headers=headers)
                if file_response.status_code == 200:
                    # Load the content into a DataFrame
                    file_content = BytesIO(file_response.content)
                    #df = pd.read_excel(file_content)

                    excel_book = pd.ExcelFile(file_content, engine='openpyxl')
                    todays_sheet = excel_book.sheet_names[0]

                    print(f"Retrieved file content for sheet: {todays_sheet}")
                    print(f"Today's book: {search_query}")
                    current_date = datetime.now().strftime('%b %d')

                    if current_date == todays_sheet.strip():
                        print("The Chan retrieved excel doc from oneDrive")
                        #interfaceExcel(file_content, todays_sheet)
                        return (file_content, todays_sheet)
                    else:
                        print(f"Today's sheet not found in the Excel book: {todays_sheet.strip()} - {current_date}")

                else:
                    print(f"Failed to fetch file content: {file_response.status_code}")
                    print(file_response.json())

        else:
            print("No files found.")
    else:
        print(f"Failed to search files: {response.status_code}")
        print(response.json())


def interface_excel():
    result = get_book()
    if result is None:
        print("Failed to retrieve the Excel book and sheet.")
        return

    bookname, sheetname = result

    print(f"Excel book: {bookname}")
    print(f"ExcelSheet: {sheetname}")
    time.sleep(2)
    print("retrieving bookings from surrey outbound")
    print("\n")

        #input trailer info fo booking
        #--------------------
        #using pandas access surrey outbound table

    warnings.filterwarnings("ignore", message="Data Validation extension is not supported")
    surrey_outbound_table = pd.read_excel(bookname, sheet_name=sheetname, usecols='x:AC', skiprows=12, nrows=11 )

        #print(surrey_outbound_table)
    surrey_outbound_table = surrey_outbound_table

    trailer_bookings = []

    #truncate the .0 from the float values in the dataframe
    def update_dict(row_dict):
        def convert_value(value):
            if pd.isna(value):
                return value
            elif isinstance(value, float):
            # Convert float to int then to string to remove the '.0'
                return str(int(value))
            else:
                return value

        return {k: convert_value(v) for k, v in row_dict.items()}

        #loop through surryoutbound, if bol is not present but trailer #
        #sailing time, contents and lh# add to trailer dictionary list
    for index, row in surrey_outbound_table.iterrows():
        if row.notna().any():
            print(row)
            if (pd.isna(row['Trailer']) ):
                #pd.isna(row['Contents']) or
                #pd.isna(row["LH#"])  or
                #pd.isna(row['Sailing']) or
                #pd.isna(row['Driver'])):
                    print(f"Trailer info incomplete - unable to make lineaul")
            elif pd.isna(row['LH#']):
                print("booking needed -- adding dataframe as dictionary to list")
                row_dict = row.to_dict()

                updated_dict = update_dict(row_dict)
                trailer_bookings.append(updated_dict)
            else:
                print(f"Booking exists with BOL: {row['BOL']}")
            print("\n")
        #----0
        #function param is row returns array with [trailer#, empty(bool),lh#,sailing time]

    print("\n")
    print(trailer_bookings)
    print("\n")
    print("Starting trailer Linehauls...\n")
    time.sleep(1)
    return trailer_bookings
   # book(trailer_bookings=trailer_bookings)

def update_surrey_outbound(trailer_booking):
    print("Updating surrey outbound")
    print(trailer_booking)



if __name__ == "__main__":
    interface_excel()