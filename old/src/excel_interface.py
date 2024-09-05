import sys
import time
import warnings
import pandas as pd
from seaspan_booking import bookseaspan




def interfaceExcel(bookname, sheetname):
    
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
            if (pd.isna(row['Trailer']) or
                pd.isna(row['Contents']) or
                pd.isna(row["LH#"])  or
                pd.isna(row['Sailing']) or
                pd.isna(row['Driver'])):
                    print(f"Sailing info incomplete - unable to make booking")
            elif pd.isna(row['BOL']):
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
    print("Starting trailer bookings...\n")
    time.sleep(1)
    bookseaspan(trailer_bookings=trailer_bookings)
