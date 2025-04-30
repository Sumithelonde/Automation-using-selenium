from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time

edge_options = Options()
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--log-level=3")
edge_options.add_argument("--disable-logging")
edge_options.add_experimental_option("detach", True)

service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service, options=edge_options)

driver.get("https://www.boat-lifestyle.com/collections/smart-watches")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "position-relative"))
)

Names = driver.find_elements(By.CLASS_NAME, "position-relative")

for Name in Names:
    print(Name.text)

time.sleep(10)
driver.quit()
