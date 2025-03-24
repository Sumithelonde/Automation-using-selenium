from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time

Email = input("ENTER YOUR USERNAME OR EMAIL-ID : ")
login_pass = input("ENTER YOUR PASSWORD : ")


edge_options = Options()
edge_options.add_argument("--headless")  
edge_options.add_argument("--disable-gpu")  
edge_options.add_argument("--log-level=3")  
edge_options.add_argument("--disable-logging")  
edge_options.add_experimental_option("detach", True)  

service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)

driver.get("https://www.facebook.com/")

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "email"))
)

input_credential = driver.find_element(By.ID, "email")
input_credential.send_keys(Email)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "pass"))
)


password = driver.find_element(By.ID, "pass")
password.send_keys(login_pass)

WebDriverWait(driver, 3).until(
    EC.presence_of_all_elements_located((By.NAME, "login"))
)

button = driver.find_element(By.NAME, "login")
button.click()

time.sleep(15)

# After this step we need to solve a captcha 