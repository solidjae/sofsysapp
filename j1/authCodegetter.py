import urllib.request
from pip._vendor import requests
import re
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

gecko_driver_path = r'C:\Users\user\geckodriver.exe'
firefox_service = FirefoxService(executable_path=gecko_driver_path)

firefox_options = FirefoxOptions()
firefox_options.headless = True

driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

id = "sofsystem"
pw = "Bestsof2755!"


def getting_auth_code():

    url = 'https://sofsystem.cafe24api.com/api/v2/oauth/authorize?response_type=code&client_id=iCNM1P8VOBIkwUfhvyZAdC&redirect_uri=https://www.sofsys.co.kr/&'
    url += 'scope=mall.read_product,mall.write_product&mall.read_category'
    driver.get(url)

    driver.implicitly_wait(10)

    driver.find_element("id", "mall_id").send_keys(id)
    driver.find_element("id", "userpasswd").send_keys(pw)
    driver.find_element(By.CLASS_NAME, "mButton").click()

    driver.implicitly_wait(4)

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

if __name__ == "__main__":
    getting_auth_code()
