from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os



def book(trailer_bookings):

    #setup
    load_dotenv()
    seaspan_username = os.getenv("SEASPAN_USERNAME")
    seaspan_password = os.getenv("SEASPAN_PASSWORD")
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')  # 3 = ERROR
    driver = webdriver.Chrome(options=chrome_options)

    screen_width = driver.execute_script("return window.screen.availWidth;")
    screen_height = driver.execute_script("return window.screen.availHeight;")

    driver.set_window_rect(
        x=0,  # X position (left edge of the screen)
        y=0,  # Y position (top edge of the screen)
        width=int(screen_width * 0.5),  # Width 50% of screen width
        height=int(screen_height)  # Height 50% of screen height
    )

    driver.get("https://sfctops.seaspan.com/")

    time.sleep(2)

    #login
    customer_radio = driver.find_element(By.ID, "ctl00_content_rblLoginAs_RB0_I_D")
    username = driver.find_element(By.ID, "ctl00_content_txtUserName_I")
    passwords = driver.find_element(By.ID, "ctl00_content_txtPassword_I")
    login_btn = driver.find_element(By.ID, "ctl00_content_cmdLogin_CD")

    customer_radio.click()
    username.send_keys(seaspan_username)
    passwords.send_keys(seaspan_password)
    time.sleep(1)
    login_btn.click()
    #make a new job
    jobs_menu = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "ctl00_menuMain_DXI0_")),)

    hover_jobs_menu = ActionChains(driver)
    hover_jobs_menu.move_to_element(jobs_menu).perform()
    add_new_btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "ctl00_menuMain_DXI0i1_T")))

    add_new_btn.click()

    time.sleep(1)
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])

    #new job fields
    unit_number = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_txtUnitNumber_I")))
    unit_type = driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_cmbContainerType_I")
    length = driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_seLength_I")
    route = driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_cmbRoute_I")
    po_number = driver.find_element(By.ID, "ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_txtPONumber_I")
    pickup_date = driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_deShipmentDate_I")
    pickup_time = driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_teShipmentTime_I")
    loaded_radio_btn = driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_rbLoaded_S_D")
    empty_radio_btn = driver.find_element(By.ID, "ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_rbEmpty_S_D")
    contents = driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_cmbContents_I")
    destination = driver.find_element(By.ID, "ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_cmbDestination_I")
    remarks = driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_txtConsignmentComments_I")

    save_btn = driver.find_element(By.ID, "ctl00_content_menuMain_DXI2_T")
    save_new_btn = driver.find_element(By.ID, "ctl00_content_menuMain_DXI4_T")
    #loop through booking list and populate
    time.sleep(1)
    for index, booking in enumerate(trailer_bookings):
        print(f"Booking trailer: {booking['Trailer']}")
        unit_number.send_keys(booking['Trailer'])
        try:
            unit_type.send_keys("Van");
            modal = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'ctl00_content_puUnitSearch_PopupControlSFCUnitSearch_PW-1')))

            close_btn = modal.find_element(By.ID, 'ctl00_content_puUnitSearch_PopupControlSFCUnitSearch_HCB-1')
            close_btn.click()
            print(f"Modal closed, continuing booking")
        except Exception as e:
            print(f"Modal not present, continuing booking")
        length.send_keys("53")
        route.send_keys("Swartz Bay > Tilbury")
        po_number.send_keys(str(int(booking['LH#'])))

        #tomorrows dat unless friday then monday
        adjusted_date = get_adjusted_date()
        pickup_date.send_keys(adjusted_date.strftime('%m/%d/%Y'))


        time.sleep(1)
        #driver.execute_script("arguments[0].value = '09:00';", pickup_time)
        pickup_time_input = ActionChains(driver)
        pickup_time_input.move_to_element(pickup_time).click().send_keys('9').perform()
        time.sleep(1)
        if "empty" in booking['Contents'].lower():
            empty_radio_btn.click()
        else:
            loaded_radio_btn.click()
            contents.send_keys("Consumer- Commercial")

        destination.send_keys("BC-Mainland - Lower Mainland")
        remarks.send_keys(booking['Sailing'])
        time.sleep(1)
         #save for bol


        save_btn_hover = ActionChains(driver)
        save_btn_hover.move_to_element(save_btn).click().perform()

        save_btn.click()

        time.sleep(5)

        bol_number = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_txtJobNumber_I")))

        print(f"bol#: {bol_number.get_attribute('value')}")

        if index == len(trailer_bookings)-1:
            break
        else:
            save_new_btn_hover = ActionChains(driver)
            save_new_btn_hover.move_to_element(save_new_btn).perform()
            save_new_btn.click()

        time.sleep(2)


    print("bookings finished ending script...")

    driver.quit()


def get_adjusted_date():
    # Get today's date
    today = datetime.now()

    # Calculate tomorrow's date
    tomorrow = today + timedelta(days=1)

    # Check if tomorrow is Friday
    if tomorrow.weekday() == 4:  # 4 corresponds to Friday
        # Calculate next Monday's date
        days_until_monday = (7 - tomorrow.weekday()) % 7
        next_monday = tomorrow + timedelta(days=days_until_monday)
        return next_monday
    else:
        return tomorrow


