import pyautogui
import time

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


def startBot():
    cont = pyautogui.confirm(text='Wanna go full retard?', title='automate linehaul test', buttons=['ok', 'cancel'])

    if 'ok' not in cont:
        pyautogui.alert(text='ok', title='wow', button='ok')
        exit(1)

    pyautogui.alert(text="Here we go now...")
    #click icon
    makeMove('../gui_image/msb_img/msb_icon_1.png')
    #wait for load
    if wait('../gui_image/msb_img/login_1.png'):
        makeMove('../gui_image/msb_img/login_1_btn.PNG')
        
        
    
    #click login
    #makeMove('./gui_test_img/four_btn.png') #click four
    #type password
    #click ok
    #@makeMove("./gui_test_img/multi_btn.png") #click X
    #wait for printer screen
    #press enter
    #wait for home page
    #click dispatch
    #makeMove("./gui_test_img/nine_btn.png") #click nine
    #wait for dispatch page
    #click linehaul
    #makeMove("./gui_test_img/equal_btn.png") #click equal
    #wait for linehauls page
    #click new
    #makeMove("./gui_test_img/menu_btn.png") #click menu
    #click tab then type, seaspan tab trailer# tab #driver tab 4 down clicks and enter
    # press back
   # makeMove("./gui_test_img/scientific_btn.png") #click scientific
    
    #pyautogui.typewrite('8675309', interval=0.25) 



def makeMove(filepath):
    try:
        imageToClick = pyautogui.locateCenterOnScreen(filepath, confidence=0.78)
        if imageToClick is None:
            pyautogui.alert(text=f"{imageToClick} - Image not found on the screen. Bailing out...")
            exit()

        else:
            pyautogui.alert(text=f"Image found at: {imageToClick}")
            pyautogui.moveTo(imageToClick.x, imageToClick.y, duration=2)
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
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.78)  # confidence is optional and used for image accuracy
        if location:
            return location
        time.sleep(1)  # Wait for 1 second before trying again
        raise TimeoutError(f"Timed out waiting for {image_path}")

# Wit for the image to appear and get its location
    try:
        location = wait(image_path)
        pyautogui.alert(text=f"Found image at {location}")
# Click on the found location
        return True
    except TimeoutError as e:
        pyautogui.alert(text=f"Timed out waiting for image {image_path}\n Bailing out...")
        exit()

if __name__ == "__main__":
    startBot()
