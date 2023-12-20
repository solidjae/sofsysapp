import time
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
options = ChromeOptions()
options.headless = True

def get_sub_categories(cat_no):
    
    sub_cat_dict = {}

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    
    url = "https://sofsystem.cafe24.com/product/list.html?cate_no=" + str(cat_no)
    
    driver.get(url)
    
    time.sleep(1)
    
    cats = driver.find_elements(By.XPATH, "//*[@id=\"contents\"]/div[1]/div[4]/ul/li/a")

    for c in cats: 
        links = c.get_attribute("href")
        encoded = links.split("/")[4]
        cat_no = links.split("/")[5]
        decoded = unquote(encoded, encoding='utf-8')
        print(decoded)
        sub_cat_dict[decoded] = cat_no

    print(sub_cat_dict)
    return sub_cat_dict
        
    driver.quit()
    
if __name__ == "__main__": 
    get_sub_categories()
    
    