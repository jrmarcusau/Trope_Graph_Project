from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

with open('imdbids.txt', 'r') as f:
    content_list = f.readlines()

# If you want to remove trailing newline characters, you can use list comprehension
content_list = [line.strip() for line in content_list]

data = []
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

for i in range(1801, 2660):
    id = content_list[i]
    url = "https://www.imdb.com/title/tt" + str(id)
    driver.get(url)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-afe43def-1.fDTGTb')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try: 
            name = soup.find('span', class_='sc-afe43def-1 fDTGTb').text   
        except AttributeError:
            print("missing name")
            name = None
        try: 
            ul = soup.find('ul', class_='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt')
            year = ul.find_all('li')[0].find('a').text
        except AttributeError:
            print("missing year")
            year = None
        dic = {'name' : name, 'year' : year, 'id' : id}
        print(dic)
        data.append(dic)
    except TimeoutException:
        print("fucked name")

    if (i % 100 == 0):
        df = pd.DataFrame(data)
        filename = "movie_names" + str(i / 100) + ".csv"
        df.to_csv(filename, index=False)
        print("saved file " + str(i / 100))

df = pd.DataFrame(data)
df.to_csv("movie_names_fin.csv", index=False)
print("done")

