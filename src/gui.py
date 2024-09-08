import tkinter as tk
from tkinter import ttk, Button, Label, Frame, Toplevel, LEFT, RIGHT, CENTER, scrolledtext, PhotoImage
import sys
import os
from main import Linehaul_Booking, cancel_linehaul
import logging
from threading import Thread, Event
import oauth
import time
import sv_ttk
import threading



logging = logging.getLogger(__name__)
access_token = None


def start_gui():
    global access_token
    logging.info("Starting GUI")
    root = tk.Tk()
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
    root.geometry("400x450")
    root.resizable(False, False)


    sv_ttk.set_theme("dark")
    style =ttk.Style()
    style.configure('Title.TLabel', font=("Arial",14))
    style.configure('SubTitle.TLabel', font=("Arial",12))
    style.configure('Text.TLabel', font=("Arial",10))
    style.configure('TButton', font=("Arial",10))
    
    # Load and display the image
    image_path = os.path.join(os.path.dirname(__file__),'..', 'assets', 'chan_gui', 'chan_img-3.png')
    image = PhotoImage(file=image_path)
    image_label = Label(root, image=image)
    image_label.image = image  
    image_label.pack(pady=10)
    image_label.place(relx=0.5, rely=0.38, anchor=CENTER)

    logging.info("authenticating")
    auth_label = ttk.Label(root, text="Authenticating...", style="Title.TLabel")
    auth_label.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.update()

    access_token = oauth.get_OAuth_token()
    auth_label.destroy()
    image_label.destroy()
    #access_token = oauth.get_oauth_token(root)
    logging.info("authenticated")

    greeting = ttk.Label(root, text="Welcome The Chan", style="Title.TLabel")
    greeting.pack(pady=20)

    image_label2 = Label(root, image=image)
    image_label2.image = image 
    image_label2.pack(pady=40)
    
    message_2 = ttk.Label(root, text="Automate:", style="SubTitle.TLabel")
    message_2.pack(padx=10, pady=10)

    automate_booking = ttk.Button(root, text="Linehaul Bookings",padding=(10,5), command=lambda: start_linehaul(gui_button=automate_booking, gui_root=root))
    automate_booking.pack(pady=5)

    update_queue = ttk.Button(root, text="Update Queue",padding=(10,5), command=lambda: sys.exit(0))
    update_queue.pack(pady=5)


    print_labels = ttk.Button(root, text="Quit",padding=(10,5), command=lambda: sys.exit(0))
    print_labels.pack(pady=5)

    message = ttk.Label(root, text="The chan is here to help with your outbound tasks.", style="Text.TLabel")
    message.pack(padx=0, pady=15)
    root.mainloop()

def start_linehaul(gui_button, gui_root):
    cancel_linehaul.clear()
    gui_button.config(text="Loading..", state="disabled")
    thread = Thread(target=Linehaul_Booking, args=(gui_button, gui_root, access_token))
    thread.start()

def show_confirmation_dialog(root, callback):

    def on_confirm():
        callback(True)  # User confirmed
        dialog.destroy()

    def on_cancel():
        callback(False)  # User canceled
        dialog.destroy()

    dialog = Toplevel(root)
    dialog.title("Confirmation for the Chan")
    dialog.geometry("500x150")
    dialog.resizable(False, False)

    sv_ttk.set_theme("dark")

    style =ttk.Style()
    
    style.configure('SubTitle.TLabel', font=("Arial",12))
 
    style.configure('TButton', font=("Arial",10))

  # Center the dialog on the root window
    root.update_idletasks()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    dialog_width = 500
    dialog_height = 150

    dialog_x = root_x + (root_width // 2) - (dialog_width // 2)
    dialog_y = root_y + (root_height // 2) - (dialog_height // 2)

    dialog.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")


    label = ttk.Label(dialog, text="Do you want to go full Chan?", style="SubTitle.TLabel").pack(padx=20, pady=20)
    button_frame = ttk.Frame(dialog)
    button_frame.pack(pady=20)
    confirm_btn = ttk.Button(button_frame, text="Yes", style="TButton",command=on_confirm, padding=(10,5)).pack(side=LEFT, padx=20)
    cancel_btn = ttk.Button(button_frame, text="No",style="TButton", command=on_cancel, padding=(10,5)).pack(side=RIGHT, padx=20)

    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)


if __name__ == "__main__":
    start_gui()




