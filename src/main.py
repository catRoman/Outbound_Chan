import sys
import time
import warnings
import pandas as pd
from automation_test import bookseaspan

if __name__ == "__main__":
    if len(sys.argv) > 1:
        bookname = sys.argv[1]
        sheetname = sys.argv[2]
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


        trailer_bookings = []

       # time.sleep(10)

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
                    trailer_bookings.append(row_dict)
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
        #use values to fill in form, save
        #retrieve bol and put in row cell
        #make new booking
        #if page error, stop
        #on complete give pop up, close tab

    else:
        print("error: no arguments provided")