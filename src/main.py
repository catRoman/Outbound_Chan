import excel_interface
import msb_interface
import time
import sys
from threading import Thread, Event
import logging
from io import BytesIO
import seapspan_booking



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
cancel_linehaul = Event()

def print_concurrent_output():
    while True:
        sys.stdout.flush()


def Linehaul_Booking(gui_button, gui_root, access_token):
    from gui import show_confirmation_dialog

    def on_confirmation(result):
        if not result:
            logging.info("Chan got ran off again...USer cancelled linehaul booking")
            cancel_linehaul.set()
            gui_root.after(0, lambda:gui_button.config(text="Linehaul Bookings", state="normal"))
            return


        logging.info("Starting linehaul booking...")

        #msb driver
        msb_password = msb_interface.start_login()
        msb_interface.login_to_home(msb_password)
        msb_interface.home_to_dispatch()

        for booking in trailer_bookings:
            logging.info(f"Linehaul: {booking}")
            if booking['LH#'] == "nan":
                logging.info("Linehaul already exists, moving on")
                continue
            booking['LH#'] = msb_interface.create_new_linehaul(booking)
            time.sleep(1)
        
        seaspan_booking.book(trailer_bookings)
        logging.info(trailer_bookings)

        if not cancel_linehaul.is_set():
            logging.info("Linehaul booking complete, updating workbook")
            logging.info(trailer_bookings)
            excel_interface.update_surrey_outbound(trailer_bookings, access_token)

        gui_root.after(0, lambda:gui_button.config(state="normal"))


    trailer_bookings = []
    excel_data_cont = ["placeholder"]
    excel_interface.retrieve_surrey_outbound(trailer_bookings=trailer_bookings, excel_data_cont=excel_data_cont, access_token=access_token)

    gui_root.after(0, lambda: show_confirmation_dialog(gui_root, on_confirmation))



def main():

    from gui import start_gui
    logging.info("Starting logging thread")
    output_thread = Thread(target=print_concurrent_output, daemon=True)
    output_thread.start()
    start_gui()


if __name__ == "__main__":
    main()
