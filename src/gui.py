from tkinter import *
import sys
import os
import main


def start_gui():
    root = Tk()
    root.title("The Chan")
    if getattr(sys, 'frozen', False):
    # Running as a bundled executable
        base_path = sys._MEIPASS
    else:
    # Running as a script
        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, '..'))

    icon_path = os.path.join(base_path, 'assets', 'chan_gui', 'chan_img.ico')

    root.iconbitmap(icon_path)
    root.geometry("400x400")


    greeting = Label(root, text="Welcome The Chan")
    greeting.config(font=("Courier", 18))
    greeting.pack(pady=20)

    message = Label(root, text="The chan is here to help \nwith your outbound tasks.")
    message.config(font=("Courier", 12))
    message.pack(padx=40, pady=20)

    message_2 = Label(root, text="Automate:")
    message_2.config(font=("Courier", 14))
    message_2.pack(padx=10, pady=10)

    automate_booking = Button(root, text="Linehaul Bookings", command=main.Linehaul_Booking)
    automate_booking.config(font=("Courier", 12))
    automate_booking.pack(pady=5)

    update_queue = Button(root, text="Update Queue", command=quit)
    update_queue.config(font=("Courier", 12))
    update_queue.pack(pady=5)


    print_labels = Button(root, text="Print Labels", command=quit)
    print_labels.config(font=("Courier", 12))
    print_labels.pack(pady=5)

    root.mainloop()


def quit():
    sys.exit()

if __name__ == "__main__":
    start_gui()




