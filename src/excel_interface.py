import sys
import time
import warnings
import pandas as pd
#from seaspan_booking import book
from datetime import datetime
import requests
import pandas as pd
from io import BytesIO
import logging
from gui import access_token

logger = logging.getLogger(__name__)


class OutboundWorkBook:
    def __init__(self):
        self.excel_data = None
        self.access_token = None
        self.search_query = self.get_this_months_book()

    def get_this_months_book(self):
        return f'{datetime.now().strftime('%b')}-Obws.xlsm'  # File name to search for
    
    def get_book(access_token):
        # Define constants

        # Define the API endpoint
        graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/root/search(q='{search_query}')"

        # Set up the request headers
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Make the request to search for the file
        logging.info(f"Searching for file: {search_query}")
        response = requests.get(graph_api_url, headers=headers)

        if response.status_code == 200:
            results = response.json().get('value', [])
            if results:
                logging.info("Found %d files(s)", len(results))
                for item in results:
                    file_name = item['name']
                    parent_reference = item.get('parentReference', {})
                    file_path = parent_reference.get('path', 'Root Directory')
                    logging.info("Found file: %s at %s",file_name, file_path)
                    # You can store the item ID or path for further operations
                    file_id = item['id']
                    full_path = f"{file_path}/{file_name}" if file_path != 'Root Directory' else file_name
                    logging.info("File ID: %s, Full Path: %s ",file_id, full_path)

                    # Fetch the file content
                    file_content_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
                    file_response = requests.get(file_content_url, headers=headers)
                    if file_response.status_code == 200:
                        # Load the content into a DataFrame
                        file_content = BytesIO(file_response.content)
                        #df = pd.read_excel(file_content)

                        excel_book = pd.ExcelFile(file_content, engine='openpyxl')
                        todays_sheet = excel_book.sheet_names[0]

                        logging.info("Retrieved file content for sheet: %s",todays_sheet)
                        logging.info("Today's book: %s",search_query)
                        current_date = datetime.now().strftime('%b %d')

                        if current_date == todays_sheet.strip():
                            logging.info("The Chan retrieved excel doc from oneDrive")
                            #interfaceExcel(file_content, todays_sheet)
                            return (file_content, todays_sheet)
                        else:
                            logging.error("Today's sheet not found in the Excel book: %s",todays_sheet.strip() - current_date)

                    else:
                        logging.error("Failed to fetch file content: %s",file_response.status_code)
                        logging.error(file_response.json())

            else:
                logging.error("No files found.")
        else:
            logging.error("Failed to search files: %s",response.status_code)
            logging.error(response.json())


    def retrieve_surrey_outbound(trailer_bookings, excel_data_cont, access_token):
        logging.info("Starting oneDrive sync with excel workbook")
        excel_data = get_book(access_token)
        if excel_data is None:
            logging.critical("Failed to retrieve the Excel book and sheet.")
            sys.exit(1)

        bookname, sheetname = excel_data
        excel_data_cont[0] = excel_data

        logging.info("Excel book: %s",bookname)
        logging.info("ExcelSheet: %s",sheetname)
        time.sleep(2)
        logging.info("retrieving bookings from surrey outbound")

            #input trailer info fo booking
            #--------------------
            #using pandas access surrey outbound table

        warnings.filterwarnings("ignore", message="Data Validation extension is not supported")
        surrey_outbound_table = pd.read_excel(bookname, sheet_name=sheetname, usecols='x:AC', skiprows=12, nrows=11 )



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
                logging.info(f"\n{row}")
                if (pd.isna(row['Trailer']) ):
                    #pd.isna(row['Contents']) or
                    #pd.isna(row["LH#"])  or
                    #pd.isna(row['Sailing']) or
                    #pd.isna(row['Driver'])):
                    logging.warning("Trailer info incomplete - unable to make linehaul\n")
                elif pd.isna(row['LH#']):
                    logging.info("booking needed -- adding dataframe as dictionary to list\n")
                    row_dict = row.to_dict()

                    updated_dict = update_dict(row_dict)
                    trailer_bookings.append(updated_dict)
                else:
                    logging.warning("Booking exists with BOL: %s\n",row['BOL'])
            #----0
            #function param is row returns array with [trailer#, empty(bool),lh#,sailing time]

        logging.debug(trailer_bookings)
        logging.info("Starting trailer Linehauls...\n")
        time.sleep(1)
        return excel_data
       # book(trailer_bookings=trailer_bookings)

    def update_surrey_outbound(trailer_booking, access_token):
        logging.info("Updating surrey outbound")
        logging.debug(trailer_booking)
        # Suppose `byte_stream` is your byte stream of the Excel file
        byte_stream = ...  # Replace this with your byte stream source

        # Load the byte stream into a pandas DataFrame
        excel_data = pd.read_excel(BytesIO(byte_stream), sheet_name=None)  # Load all sheets

        # Process the DataFrame
        sheet_name = 'Sheet1'
        df = excel_data[sheet_name]  # Load a specific sheet into DataFrame

        # Modify the DataFrame (e.g., add a new column)
        df['NewColumn'] = 'SomeValue'

        # Save the modified DataFrame back into a byte stream
        output_stream = BytesIO()

        with pd.ExcelWriter(output_stream, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Get the bytes from the output stream
        modified_bytes = output_stream.getvalue()


if __name__ == "__main__":
    retrieve_surrey_outbound()
