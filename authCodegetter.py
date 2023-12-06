import urllib.request
from pip._vendor import requests
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
options = ChromeOptions()
options.add_argument("--headless=new")

id = "sofsystem"
pw = "Bestsof2755!"


def getting_auth_code():
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    url = 'https://sofsystem.cafe24api.com/api/v2/oauth/authorize?response_type=code&client_id=iCNM1P8VOBIkwUfhvyZAdC&redirect_uri=https://www.sofsys.co.kr/&'
    url += 'scope=mall.read_product,mall.write_product&mall.read_category'
    driver.get(url)
    

    time.sleep(1)

    driver.find_element("id", "mall_id").send_keys(id)
    time.sleep(1)
    driver.find_element("id", "userpasswd").send_keys(pw)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "mButton").click()

    time.sleep(10)

    current_url = driver.current_url
    print("URL with the code: ", current_url)
    driver.quit()

    # Search for patterns and extract the auth code

    pattern = re.compile(r"=(.*?)&")
    match = pattern.search(current_url)

    if match:
        extracted_string = match.group(1)
        print("Authcode:", extracted_string)
        return extracted_string
    else:
        print("Substring not found.")

# ssh jjung2945@20.196.216.221
# plotly_express12
#scp
if __name__ == "__main__":
    getting_auth_code()
