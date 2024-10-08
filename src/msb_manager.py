import pyautogui
import time
import sys
import os
from dotenv import load_dotenv
import logging
from msb_scanner import MSBScanner

logging = logging.getLogger(__name__)

class MSBManagerException(Exception):
    def __init__(self, message="Issue using MSBManger"):
        self.message = message
        super().__init__(self.message)


class MSBManager:
    def __init__(self):
        self._pyauto_settings()
        self._load_dotenv()
        self.base_path = self._get_base_path()

    def _get_base_path(self):
        if getattr(sys, 'frozen', False):
            return sys._MEIPASS
        else:
            return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def _pyauto_settings(self):
        pyautogui.PAUSE = 0.5
        pyautogui.FAILSAFE = True

    def _load_dotenv(self):
        load_dotenv()
        self.msb_password = os.getenv("MSB_PASSWORD")

    def start_login(self):

        msb_icon_1 = os.path.join(self.base_path, 'assets', 'msb_img', 'msb_icon_1.png')
        try:
            locate_msb_icon = pyautogui.locateCenterOnScreen(msb_icon_1, confidence=0.85)
            if locate_msb_icon is None:
                pyautogui.alert("msb icon not found, sorry chans going home")
                sys.exit()
        except pyautogui.ImageNotFoundException:
            pyautogui.alert(text=f"Image not found issue. Chans going home...")
            sys.exit()
        except Exception as e:
                pyautogui.alert(text=f"Theres an issue. chans going home... \n {e}")
                sys.exit()


    def login_to_home(self):
        #location images
        msb_icon_1 = os.path.join(self.base_path, 'assets', 'msb_img', 'msb_icon_1.png')
        login_1 = os.path.join(self.base_path, 'assets', 'msb_img', 'login_1.png')
        login_1_btn= os.path.join(self.base_path, 'assets', 'msb_img', 'login_1_btn.png')
        login_2 = os.path.join(self.base_path, 'assets', 'msb_img', 'login_2.png')
        printer_setup_1 = os.path.join(self.base_path, 'assets', 'msb_img', 'printer_setup_1.png')
        dispatch_btn = os.path.join(self.base_path, 'assets', 'msb_img', 'dispatch_btn.png')

        logging.info("Starting MSB login...")
        #click icon
        self.make_move(msb_icon_1)
        #wait for load
        self.wait(login_1)
        #click login
        self.make_move(login_1_btn)
        #wait login 2
        self.wait(login_2)
        #type password
        pyautogui.typewrite(self.msb_password, interval=0.125)
        #click ok
        time.sleep(1)
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('enter')

        #wait for printer screen
        self.wait(printer_setup_1)
        #press enter
        time.sleep(1)
        pyautogui.press('enter')
        #wait for home page
        self.wait(dispatch_btn)
        logging.info("MSB login successful")


    def home_to_dispatch(self):
        #location images
        dispatch_btn = os.path.join(self.base_path, 'assets', 'msb_img', 'dispatch_btn.png')
        dispatch_linehaul_btn = os.path.join(self.base_path, 'assets', 'msb_img', 'dispatch_linehaul_btn.png')
        logging.info("Moving to MSB dispatch page...")
        #click dispatch:wq
        self.make_move(dispatch_btn, confid=0.95)
        #wait for dispatch page
        self.wait(dispatch_linehaul_btn)
        #click linehaul
        self.make_move(dispatch_linehaul_btn, confid=0.95)

    def create_new_linehaul(self, trailer_bookings):
        dispatch_linehaul_new_btn = os.path.join(self.base_path, 'assets', 'msb_img', 'dispatch_linehaul_new_btn.png')
        dispatch_empty_new_linehaul = os.path.join(self.base_path, 'assets', 'msb_img', 'dispatch_empty_new_linehaul.png')

        logging.info(f"Creating {trailer_bookings["Trailer"]} linehaul...")
        #click new box
        self.make_move(dispatch_linehaul_new_btn, confid=0.10, reg=(120,40,100,100))

        self.wait(dispatch_empty_new_linehaul)
        #2 tabs
        time.sleep(0.5)
        pyautogui.press('tab')
        pyautogui.press('tab')
        #send seaspan, tab
        pyautogui.typewrite("SEASPAN", interval=0.1)
        pyautogui.press('tab')
        #send trailer, tab
        pyautogui.typewrite(trailer_bookings["Trailer"], interval=0.1)
        pyautogui.press('tab')
        #send driver number
        pyautogui.typewrite("926", interval=0.1)
        pyautogui.press('tab')
        #send tab + 6 down strokes
        for _ in range(6):
            pyautogui.press('down')
        #send enter
        pyautogui.press('enter')

        #get line haul from number  via tesseract
        screenshot = pyautogui.screenshot()
        linehaul_num_scanner = MSBScanner(screenshot)
        linehaul_num = linehaul_num_scanner.scan_for_linehaul_number()

        logging.info(f"Linehaul created: {linehaul_num}")
        return  linehaul_num

    def make_move(self, filepath, confid=0.78, reg=(0,0, *pyautogui.size())):
        try:
            imageToClick = pyautogui.locateCenterOnScreen(filepath, region=reg, confidence=confid)
            if imageToClick is None:
                logging.critical("%s - Image not found on the screen. Bailing out...", imageToClick)
                sys.exit(1)

            else:
                logging.debug("Image found at: %s",imageToClick)
                pyautogui.moveTo(imageToClick.x, imageToClick.y, duration=0.4)
                pyautogui.leftClick()

        except pyautogui.ImageNotFoundException:
            logging.critical("%s - Image not found exception.Bailing out...", imageToClick)
            raise MSBManagerException("Image not found exception.Bailing out...")
        except Exception as e:
            logging.critical("An error occurred: %",e)
            raise MSBManagerException("An error occurred in MSB Manager: %",e)

    def wait(self, image_path, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
        # Try to locate the image on the screen
            try:
                location = pyautogui.locateCenterOnScreen(image_path, confidence=0.78)  # confidence is optional and used for image accuracy
                if location is not None:
                    logging.debug("Found image at %s",location)
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            except Exception as e:
                logging.critical("An error occurred: %s",e)
                raise MSBManagerException("An error occurred: %s",e)

            time.sleep(1)
        logging.critical("Timed out waiting for %s",image_path)
        sys.exit(1)




if __name__ == "__main__":
    msb = MSBManager()
    msb.start_login()
