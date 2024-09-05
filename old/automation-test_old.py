from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



driver = webdriver.Chrome()

try:
  
    driver.get('https://www.google.com')
    
    driver.execute_script("window.open('');") 
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://sfctops.seaspan.com/')

    wait = WebDriverWait(driver, 10)

 
   # Locate elements
    customer_button = wait.until(EC.element_to_be_clickable((By.ID, 'ctl00_content_rblLoginAs_RB0_I_D')))
    name_field =wait.until(EC.element_to_be_clickable((By.ID, 'ctl00_content_txtUserName_I')))
    pass_field = driver.find_element(By.ID, 'ctl00_content_txtPassword_I')
    submit_button = driver.find_element(By.ID, 'ctl00_content_cmdLogin_I')


   

    # Click the radio button
    customer_button.click()


    # Input data
    name_field.send_keys('DIA125D')
    pass_field.send_keys('dv428664')

    # Submit the form
    submit_button.click()
    
    
finally:
    print("Test complete")
