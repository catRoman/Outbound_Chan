import excel_interface
import msb_interface
import time
import sys
from threading import Thread
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def print_concurrent_output():
    while True:
        sys.stdout.flush()


def Linehaul_Booking():
    logging.info("Starting oneDrive sync with workbook")
    trailer_bookings = excel_interface.interface_excel()

    logging.info("Starting linehaul booking...")

    #driver
    msb_password = msb_interface.start_login()
    msb_interface.login_to_home(msb_password)
    msb_interface.home_to_dispatch()

    for booking in trailer_bookings:
        logging.info(f"Linehaul: {booking}")
        if booking['LH#'] == "nan":
            logging.info("Linehaul already exists, moving on")
            continue
        booking['LH#'] = msb_interface.create_new_linehaul(booking)
        logging.info("Linehaul created")
        time.sleep(1)

    logging.info("Linehaul booking complete, updating workbook")
    logging.info(trailer_bookings)
    excel_interface.update_surrey_outbound(trailer_bookings)

def main():

    from gui import start_gui
    logging.info("Starting logging thread")
    output_thread = Thread(target=print_concurrent_output, daemon=True)
    output_thread.start()
    start_gui()


if __name__ == "__main__":
    main()