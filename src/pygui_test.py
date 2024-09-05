import pyautogui
import time

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


def startBot():
    cont = pyautogui.confirm(text='Wanna go full retard?', title='automate linehaul test', buttons=['ok', 'cancel'])

    if 'ok' not in cont:
        pyautogui.alert(text='ok', title='wow', button='ok')
        exit(1)

    pyautogui.alert("Here we go now...")
    #click icon
    makeMove('../gui_image/msb_img/msb_icon.png') #click icon
    #wait for load
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
    
    pyautogui.typewrite('8675309', interval=0.25) 



def makeMove(filepath):
    try:
        imageToClick = pyautogui.locateCenterOnScreen(filepath, confidence=0.78)
        if imageToClick is None:
            pyautogui.alert(f"{imageToClick} - Image not found on the screen. Bailing out...")
            exit()

        else:
            pyautogui.alert("Image found at:", imageToClick)
            pyautogui.moveTo(imageToClick.x, imageToClick.y, duration=0.25)
            pyautogui.leftClick()

    except pyautogui.ImageNotFoundException:
        pyautogui.alert(f"{imageToClick} - Image not found exception.Bailing out...")
        exit()
    except Exception as e:
        pyautogui.alert(f"An error occurred: {e}")
        exit()


if __name__ == "__main__":
    startBot()
