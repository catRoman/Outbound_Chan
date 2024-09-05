from excel_interface import interfaceExcel
import pandas as pd
from datetime import datetime


if __name__ == '__main__':
    print("starting the chan")

    excel_path ="../Sep-Obws-testing.xlsm"
    excel_book = pd.ExcelFile(excel_path, engine='openpyxl')
    
    todays_sheet = excel_book.sheet_names[0]

    if datetime.now().strftime('%b %d') == todays_sheet.strip():
        print("The Chan is good to go retrieveing excel info")
        interfaceExcel(excel_path, todays_sheet)
    else:
        print(f"found {todays_sheet.strip()}, the chan needs you to do better.")
        
    
