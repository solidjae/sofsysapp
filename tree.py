import time
from urllib.parse import unquote
import graphviz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
options = ChromeOptions()


# def get_sub_categories(cat_no):
    

#     sub_cat_dict = {}
#     options.add_argument("--headless=new")
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#     url = "https://sofsystem.cafe24.com/product/list.html?cate_no=" + str(cat_no)
    
#     driver.get(url)
    
#     time.sleep(1)
    
#     cats = driver.find_elements(By.XPATH, "//*[@id=\"contents\"]/div[1]/div[2]/ul/li/a")

#     for c in cats: 
#         links = c.get_attribute("href")
#         encoded = links.split("/")[4]
#         cat_no = links.split("/")[5]
#         decoded = unquote(encoded, encoding='utf-8')
#         print(decoded)
#         sub_cat_dict[decoded] = cat_no

#     print(sub_cat_dict)
#     return sub_cat_dict
        
#     driver.quit()


segments = {
    "Event": 52,
    "New": 198,
    "Best": 157,
    "책상": 368,
    "테이블식탁": 381,
    "모듈책장": 387,
    "책장선반": 392,
    "행거드레스룸": 397,
    "의자": 400
}
g = graphviz.Digraph(comment='hello')
converted = str()
for key in segments:
    converted += key + str(segments[key])
    g.edge(converted, "i")
    converted = str()
g.attr(fontname="NanumGothic", encoding='utf8')

g.render('hello', format='png', cleanup=True)


