from tkinter import *
import sys


def main():
    root = Tk()
    root.title("The Chan")
   
    root.iconbitmap(r"C:\Users\catli\OneDrive\desktop\Chan_bot\gui_image\chan_gui\chan_img.ico")
    root.geometry("400x400")


    greeting = Label(root, text="Welcome The Chan")
    greeting.config(font=("Courier", 18))
    greeting.pack(pady=20)

    message = Label(root, text="The chan is here to help \nwith your outbound tasks.")
    message.config(font=("Courier", 12))
    message.pack(padx=40, pady=40)

    message_2 = Label(root, text="Automate:")
    message_2.config(font=("Courier", 14))
    message_2.pack(padx=10, pady=10)

    automate_booking = Button(root, text="Linehaul Bookings", command=quit)
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
    main()




