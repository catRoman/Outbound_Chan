import logging
import time
import os
import sys

from datetime import datetime, timedelta
from selenium import webdriver
from dotenv import load_dotenv

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException



class SeaspanBooking:

    def __init__(self, trailer_booking):
        self.trailer_booking = trailer_booking
        self._load_dotenv()
        self._setup_driver()
        self._set_screen_dimensions()



    def _load_dotenv(self):
        logging.info("accessing user credentials")
        load_dotenv()
        self.seaspan_username = os.getenv("SEASPAN_USERNAME")
        self.seaspan_password = os.getenv("SEASPAN_PASSWORD")


    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--log-level=3')  # 3 = ERROR
        self.driver = webdriver.Chrome(options=chrome_options)


    def _set_screen_dimensions(self):
        screen_width = self.driver.execute_script("return window.screen.availWidth;")
        screen_height = self.driver.execute_script("return window.screen.availHeight;")
        self.driver.set_window_rect(
            x=0,  # X position (left edge of the screen)
            y=0,  # Y position (top edge of the screen)
            width=int(screen_width * 0.5),  # Width 50% of screen width
            height=int(screen_height)  # Height 50% of screen height
        )

    def login_seaspan(self):
        self.driver.get("https://sfctops.seaspan.com/")
        time.sleep(2)
        #login
        customer_radio = self.driver.find_element(By.ID, "ctl00_content_rblLoginAs_RB0_I_D")
        username = self.driver.find_element(By.ID, "ctl00_content_txtUserName_I")
        passwords = self.driver.find_element(By.ID, "ctl00_content_txtPassword_I")
        login_btn = self.driver.find_element(By.ID, "ctl00_content_cmdLogin_CD")
        logging.info("attempting logging in to seaspan...")

        try:
            customer_radio.click()
            username.send_keys(self.seaspan_username)
            passwords.send_keys(self.seaspan_password)
            time.sleep(1)
            login_btn.click()
        except Exception as e:
            logging.error("failed to login:  %s",e)
            self.driver.quit()
            return
        logging.info("successfully logged in...")
    time.sleep(2)

    def add_new_job(self):
        jobs_menu = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ctl00_menuMain_DXI0_")),)
        hover_jobs_menu = ActionChains(self.driver)
        hover_jobs_menu.move_to_element(jobs_menu).perform()
        add_new_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ctl00_menuMain_DXI0i1_T")))
        logging.info("adding new job...")
        add_new_btn.click()
    time.sleep(1)

    def switch_to_new_job_tab(self):
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])

    def _modal_close(self, modal_window_id, modal_close_btn_id):
        try:
            modal = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, modal_window_id)))
            close_btn = modal.find_element(By.ID, modal_close_btn_id)
            close_btn.click()
            logging.debug("Modal closed, continuing booking")
        except TimeoutException:
            logging.debug("Modal not present, continuing booking")

    def make_new_booking(self, booking):
        unit_number = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_txtUnitNumber_I")))
        unit_type = self.driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_cmbContainerType_I")
        length = self.driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_seLength_I")
        route = self.driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_cmbRoute_I")
        po_number = self.driver.find_element(By.ID, "ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_txtPONumber_I")
        pickup_date = self.driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_deShipmentDate_I")
        pickup_time = self.driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_teShipmentTime_I")
        loaded_radio_btn = self.driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_rbLoaded_S_D")
        empty_radio_btn = self.driver.find_element(By.ID, "ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_rbEmpty_S_D")
        contents = self.driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_cmbContents_I")
        destination = self.driver.find_element(By.ID, "ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_cmbDestination_I")
        remarks = self.driver.find_element(By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_txtConsignmentComments_I")

        try:
            logging.info("Booking trailer: %s",booking['Trailer'])
            unit_number.send_keys(booking['Trailer'])

            unit_type.send_keys("Van");
            self._modal_close("ctl00_content_puUnitSearch_PopupControlSFCUnitSearch_PW-1", "ctl00_content_puUnitSearch_PopupControlSFCUnitSearch_HCB-1")
            length.send_keys("53")
            route.send_keys("Swartz Bay > Tilbury")
            po_number.send_keys(booking['LH#'])
            #tomorrows dat unless friday then monday
            adjusted_date = self.get_adjusted_date()
            pickup_date.send_keys(adjusted_date.strftime('%m/%d/%Y'))
            time.sleep(1)
            #driver.execute_script("arguments[0].value = '09:00';", pickup_time)
            pickup_time_input = ActionChains(self.driver)
            pickup_time_input.move_to_element(pickup_time).click().send_keys('09').perform()
            time.sleep(1)
            if "empty" in booking['Contents'].lower():
                empty_radio_btn.click()
            else:
                loaded_radio_btn.click()
                contents.send_keys("Consumer- Commercial")
            destination.send_keys("BC-Mainland - Lower Mainland")
            remarks.send_keys(booking['Sailing'])

            self.save_booking_for_bol()

            self._modal_close("ctl00_content_puConfirm_PopupControlConfirmationBox_PWC-1", "ctl00_content_puConfirm_PopupControlConfirmationBox_cmdOK_CD")

            booking['BOL'] = self.retrieve_bol_number()
            logging.info("Booking Successful trailer %s",booking['Trailer'])
            time.sleep(1)
        except SeaspanBookingException as e:
            logging.error(   ",e)
            self.driver.quit()
            return

        logging.info("trailer info successfully input...")
        time.sleep(1)


    def fill_new_job_fields(self):

        #loop through booking list and populate
        time.sleep(1)
        logging.info("attempting bookings....")
        for index, booking in enumerate(self.trailer_bookings):
            self.make_new_booking(booking)

            if index == len(self.trailer_bookings)-1:
                break
            else:
                self.save_and_continue_booking()

        logging.info("seaspan bookings complete...")
        logging.info("Assigning reservations")
        self.driver.quit()

    def save_booking_for_bol(driver):
        save_btn = driver.find_element(By.ID, "ctl00_content_menuMain_DXI2_T")
        logging.info("attempting to save booking...")
        try:
            logging.info("hovering over save button")
            save_btn_hover = ActionChains(driver)
            time.sleep(3)
            save_btn_hover.move_to_element(save_btn).click().perform()
            logging.info("clicking save button, wait 30 seconds")
            save_btn.click()
            time.sleep(10)
        except Exception as e:
            logging.error("failed to save booking: %s",e)
            driver.quit()
            sys.exit(1)


    def retrieve_bol_number(driver):
        bol_number = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID,"ctl00_content_ctlCallbackJobSCF_ASPxFormLayout_txtJobNumber_I")))
        logging.info("bol#: %s", bol_number.get_attribute('value'))
        return bol_number.get_attribute('value')

    def save_and_continue_booking(driver):
        save_new_btn = driver.find_element(By.ID, "ctl00_content_menuMain_DXI4_T")
        try:
            logging.info("attempting next booking...")
            save_new_btn_hover = ActionChains(driver)
            logging.info("hover")
            time.sleep(3)
            save_new_btn_hover.move_to_element(save_new_btn).perform()
            logging.info("preform")
            time.sleep(3)
            save_new_btn.click()
            logging.info("click")
            time.sleep(3)
        except Exception as e:
            logging.error("failed to continue booking: %s", e )
            driver.quit()
            sys.exit(1)

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

    def book(trailer_bookings):
        driver, seaspan_username, seaspan_password = setup_driver()
        login_seaspan(driver, seaspan_username, seaspan_password)
        add_new_job(driver)
        switch_to_new_job_tab(driver)
        fill_new_job_fields(driver, trailer_bookings)
        logging.info(trailer_bookings)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    book([

    {'Trailer': '53H354', 'Contents': 'Empty ??', 'LH#': '112497', 'BOL': 'nan', 'Sailing': '1:55 p1', 'Driver': '926'}])
else:
    logging = logging.getLogger(__name__)


#box -> ctl00_content_puConfirm_PopupControlConfirmationBox_PWC-1
#ok_btn -> ctl00_content_puConfirm_PopupControlConfirmationBox_cmdOK_CD
class SeaspanBookingException(Exception):
    def __init__(self, trailer, message="Issue booking trailer on seaspan"):
        self.value = trailer
        self.message = message
        super().__init__(self.message)