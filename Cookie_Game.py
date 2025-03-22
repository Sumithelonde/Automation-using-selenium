from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

edge_options = Options()
edge_options.add_argument("--headless")  
edge_options.add_argument("--disable-gpu")  
edge_options.add_argument("--log-level=3")  
edge_options.add_argument("--disable-logging")  
edge_options.add_experimental_option("detach", True)  

service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'langSelect-EN'))
    )

input_element = driver.find_element(By.ID, "langSelect-EN")
input_element.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "bigCookie"))
    )

cookie = driver.find_element(By.ID, "bigCookie")
cookie_count = driver.find_element(By.ID, "cookies")

while True:
    cookie.click()
    cookie_count = driver.find_element(By.ID, "cookies").text.split("\n")[0]
    numeric_cookie = int(cookie_count.split(" ")[0].replace(",", ""))

    print(numeric_cookie)

    for i in range(4):
        product_elements = driver.find_elements(By.ID, f"productPrice{i}")
        if product_elements:
            product_price_text = product_elements[0].text.replace(",", "").strip()

            if product_price_text.isdigit():
                product_price_value = int(product_price_text)

                if numeric_cookie >= product_price_value:
                    buy_button = driver.find_element(By.ID, f"product{i}")
                    if buy_button.is_enabled():
                        buy_button.click()
                        print(f"Purchased product {i+1} for {product_price_value} cookies.")
