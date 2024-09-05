import pyautogui
import time
import os
from dotenv import load_dotenv

def startBot():
    cont = pyautogui.confirm(text='Wanna go full retard?', title='automate linehaul test', buttons=['ok', 'cancel'])

    if 'ok' not in cont:
        pyautogui.alert(text='ok', title='wow', button='ok')
        exit(1)

    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True
    load_dotenv()
    msb_password = os.getenv("MSB_PASSWORD")

    loginToHome(msb_password)
    time.sleep(1)
    homeToDispatch()

    cont = pyautogui.confirm(text='Are you sure you want the Chan to continue to make linehauls?', title='automate linehaul test', buttons=['ok', 'cancel'])

    if 'ok' not in cont:
        pyautogui.alert(text='ok', title='the chan needs to know', button='ok')
        exit(1)

def loginToHome(msb_password):

    pyautogui.alert(text="Here we go now...")
    #click icon
    makeMove('../gui_image/msb_img/msb_icon_1.png')
    #wait for load
    wait('../gui_image/msb_img/login_1.png')
    #click login
    makeMove('../gui_image/msb_img/login_1_btn.PNG')
    #wait login 2
    wait('../gui_image/msb_img/login_2.png')
    #type password
    pyautogui.typewrite(msb_password, interval=0.125)
    #click ok
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
#    makeMove('./gui_image/msb_img/login_2_submit_btn.png')

    #wait for printer screen
    wait('../gui_image/msb_img/printer_setup_1.png')
    #press enter
    time.sleep(1)
    pyautogui.press('enter')
    #wait for home page
    wait('../gui_image/msb_img/dispatch_btn.png')


def homeToDispatch():
    #click dispatch
    makeMove('../gui_image/msb_img/dispatch_btn.png', confid=0.95)
    #wait for dispatch page
    wait('../gui_image/msb_img/dispatch_linehaul_btn.png')
    #click linehaul
    makeMove('../gui_image/msb_img/dispatch_linehaul_btn.png', confid=0.95)




def makeMove(filepath, confid=0.78):
    try:
        imageToClick = pyautogui.locateCenterOnScreen(filepath, confidence=confid)
        if imageToClick is None:
            pyautogui.alert(text=f"{imageToClick} - Image not found on the screen. Bailing out...")
            exit()

        else:
            print(f"Image found at: {imageToClick}")
            pyautogui.moveTo(imageToClick.x, imageToClick.y, duration=0.5)
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

if __name__ == "__main__":
    startBot()
