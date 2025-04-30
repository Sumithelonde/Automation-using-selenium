from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time


input_email = "SUMITHELONDE2005@GMAIL.COM"
input_pass = "sUMIT@2005"


service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)

driver.get("https://www.google.co.in/")

WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'gb_Ua gb_zd gb_qd gb_hd')]"))
)

signin_button = driver.find_element(By.XPATH, "//a[contains(@class, 'gb_Ua gb_zd gb_qd gb_hd')]")
signin_button.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.ID, "identifierId"))
)

Email = driver.find_element(By.ID, "identifierId")
Email.send_keys(input_email) 

next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/parent::button"))
)
next_button.click()



time.sleep(120)