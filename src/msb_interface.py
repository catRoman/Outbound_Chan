import pyautogui
import time
import sys
import os
from dotenv import load_dotenv

def start_login():
    #confirm its in chans hand now
    cont = pyautogui.confirm(text='Wanna go full Chan on this?', title='automate linehaul test', buttons=['ok', 'cancel'])

    if 'ok' not in cont:
        pyautogui.alert(text='ok', title='wow', button='ok')
        exit(1)

    base_path = get_base_path()
    msb_icon_1 = os.path.join(base_path, 'assets', 'msb_img', 'msb_icon_1.png')
    try:
        locate_msb_icon = pyautogui.locateCenterOnScreen(msb_icon_1, confidence=0.85)
        if locate_msb_icon is None:
            pyautogui.alert("msb icon not found, sorry chans going home")
            exit()
    except pyautogui.ImageNotFoundException:
        pyautogui.alert(text=f"Image not found issue. Chans going home...")
        exit()
    except Exception as e:
            pyautogui.alert(text=f"Theres an issue. chans going home... \n {e}")
            exit()



    #setup
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True
    load_dotenv()
    return os.getenv("MSB_PASSWORD")



def login_to_home(msb_password):
    #location images
    base_path = get_base_path()
    msb_icon_1 = os.path.join(base_path, 'assets', 'msb_img', 'msb_icon_1.png')
    login_1 = os.path.join(base_path, 'assets', 'msb_img', 'login_1.png')
    login_1_btn= os.path.join(base_path, 'assets', 'msb_img', 'login_1_btn.png')
    login_2 = os.path.join(base_path, 'assets', 'msb_img', 'login_2.png')
    printer_setup_1 = os.path.join(base_path, 'assets', 'msb_img', 'printer_setup_1.png')
    dispatch_btn = os.path.join(base_path, 'assets', 'msb_img', 'dispatch_btn.png')


    #click icon
    make_move(msb_icon_1)
    #wait for load
    wait(login_1)
    #click login
    make_move(login_1_btn)
    #wait login 2
    wait(login_2)
    #type password
    pyautogui.typewrite(msb_password, interval=0.125)
    #click ok
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')

    #wait for printer screen
    wait(printer_setup_1)
    #press enter
    time.sleep(1)
    pyautogui.press('enter')
    #wait for home page
    wait(dispatch_btn)


def home_to_dispatch():
    #location images
    base_path = get_base_path()
    dispatch_btn = os.path.join(base_path, 'assets', 'msb_img', 'dispatch_btn.png')
    dispatch_linehaul_btn = os.path.join(base_path, 'assets', 'msb_img', 'dispatch_linehaul_btn.png')

    #click dispatch
    make_move(dispatch_btn, confid=0.95)
    #wait for dispatch page
    wait(dispatch_linehaul_btn)
    #click linehaul
    make_move(dispatch_linehaul_btn, confid=0.95)

def create_new_linehaul(trailer_bookings):
    base_path = get_base_path()
    dispatch_linehaul_new_btn = os.path.join(base_path, 'assets', 'msb_img', 'dispatch_linehaul_new_btn.png')
    dispatch_empty_new_linehaul = os.path.join(base_path, 'assets', 'msb_img', 'disptach_empyt_new_linehaul.png')

    #click new box
    make_move(dispatch_linehaul_new_btn, confid=0.95)

    wait(dispatch_empty_new_linehaul)
    #2 tabs
    time.sleep(0.5)
    pyautogui.press('tab')
    pyautogui.press('tab')
    #send seaspan, tab
    pyautogui.typewrite("SEASPAN", interval=0.5)
    pyautogui.press('tab')
    #send trailer, tab
    pyautogui.typewrite(trailer_bookings["Trailer"], interval=0.5)
    pyautogui.press('tab')
    #send driver number
    pyautogui.typewrite("926", interval=0.5)
    pyautogui.press('tab')
    #send tab + 6 down strokes
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    #send enter
    pyautogui.press('enter')

    #get line haul from number opencv
    linehaul = "123456"
    return  linehaul





def make_move(filepath, confid=0.78):
    try:
        imageToClick = pyautogui.locateCenterOnScreen(filepath, confidence=confid)
        if imageToClick is None:
            pyautogui.alert(text=f"{imageToClick} - Image not found on the screen. Bailing out...")
            exit()

        else:
            print(f"Image found at: {imageToClick}")
            pyautogui.moveTo(imageToClick.x, imageToClick.y, duration=0.4)
            pyautogui.leftClick()

    except pyautogui.ImageNotFoundException:
        pyautogui.alert(text=f"{imageToClick} - Image not found exception.Bailing out...")
        exit()
    except Exception as e:
        pyautogui.alert(text=f"An error occurred: {e}")
        exit()

def wait(image_path, timeout=30) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
    # Try to locate the image on the screen

        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.78)  # confidence is optional and used for image accuracy
            if location is not None:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            pyautogui.alert(text=f"An error occurred: {e}")
            exit()

        time.sleep(1)


    raise TimeoutError(f"Timed out waiting for {image_path}")

# Wit for the image to appear and get its location
    try:
        location = wait(image_path)
        print(f"Found image at {location}")
# Click on the found location
        return True
    except TimeoutError as e:
        pyautogui.alert(text=f"Timed out waiting for image {image_path}\n Bailing out...")
        exit()

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


if __name__ == "__main__":
    start_login()
