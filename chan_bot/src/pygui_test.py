import pyautogui
import time

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


def startBot():
    cont = pyautogui.confirm(text='Wanna go full retard?', title='automate life', buttons=['ok', 'cancel'])

    if 'ok' not in cont:
        pyautogui.alert(text='ok', title='wow', button='ok')
        exit(1)

    print("continuing")
    makeMove('./gui_test_img/calc_icon.png') #click icon
    makeMove('./gui_test_img/four_btn.png') #click four
    makeMove("./gui_test_img/multi_btn.png") #click X
    makeMove("./gui_test_img/nine_btn.png") #click nine
    makeMove("./gui_test_img/equal_btn.png") #click equal
    makeMove("./gui_test_img/menu_btn.png") #click menu
    makeMove("./gui_test_img/scientific_btn.png") #click scientific
    pyautogui.typewrite('8675309', interval=0.25) 



def makeMove(filepath):
    try:
        imageToClick = pyautogui.locateCenterOnScreen(filepath, confidence=0.78)
        if imageToClick is None:
            print("Image not found on the screen.")
        else:
            print("Image found at:", imageToClick)
            pyautogui.moveTo(imageToClick.x, imageToClick.y, duration=0.25)
            pyautogui.leftClick()

    except pyautogui.ImageNotFoundException:
        print("Image not found. Make sure the image is correct and visible on the screen.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    startBot()
