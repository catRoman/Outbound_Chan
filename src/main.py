from excel_interface import interface_excel
import excel_interface
import time


if __name__ == "__main__":
    from gui import start_gui
    start_gui()

def Linehaul_Booking():
    print("Starting onedrive sync with workbook")
    trailer_bookings = interface_excel()

    print("Starting linehaul booking...")

    #driver
    print("Starting MSB login...")
    msb_password = excel_interface.start_login()
    print("MSB login successful")
    print("Moving to MSB home page...")
    excel_interface.login_to_home(msb_password)
    print("Moving to MSB dispatch page...")
    excel_interface.home_to_dispatch()
    print("Creating new linehaul...")

    for booking in trailer_bookings:
        print(f"Linehaul: {booking}")
        if booking['LH#'] is not None:
            print("Linehaul already exists, moving on")
            continue
        booking['LH#'] = excel_interface.create_new_linehaul(booking)
        print("Linehaul created")
        time.sleep(1)

    print("Linehaul booking complete, updating workbook")
    excel_interface.update_surrey_outbound(trailer_bookings)
