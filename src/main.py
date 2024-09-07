import excel_interface
import msb_interface
import time
import sys
from treading import Thread




def print_concurrent_output():
    while True:
        print("This is concurrent output in the terminal")
        sys.stdout.flush()  # Force flush the output buffer to ensure it appears in real-time
        time.sleep(2)  # Simulate some ongoing terminal output

def Linehaul_Booking():
    print("Starting onedrive sync with workbook")
    trailer_bookings = excel_interface.interface_excel()

    print("Starting linehaul booking...")

    #driver
    print("Starting MSB login...")
    msb_password = msb_interface.start_login()
    print("MSB login successful")
    print("Moving to MSB home page...")
    msb_interface.login_to_home(msb_password)
    print("Moving to MSB dispatch page...")
    msb_interface.home_to_dispatch()
    print("Creating new linehaul...")

    for booking in trailer_bookings:
        print(f"Linehaul: {booking}")
        if booking['LH#'] == "nan":
            print("Linehaul already exists, moving on")
            continue
        booking['LH#'] = msb_interface.create_new_linehaul(booking)
        print("Linehaul created")
        time.sleep(1)

    print("Linehaul booking complete, updating workbook")
    excel_interface.update_surrey_outbound(trailer_bookings)


if __name__ == "__main__":
    from gui import start_gui
    output_thread = Thread(target=print_concurrent_output, daemon=True)
    output_thread.start()
    start_gui()