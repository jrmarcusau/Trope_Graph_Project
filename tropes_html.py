from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

from bs4 import BeautifulSoup
import codecs
import re
import requests
import pandas as pd
firefox_options = Options()




def scrape_index(driver, url):
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    twikilink_tags = soup.find_all('a', class_='twikilink')
    base_trope = "https://tvtropes.org"
    pdata = [{'text': tag.text.strip(), 'href': (base_trope + tag.get('href'))} for tag in twikilink_tags]
    return pdata



def main_1(start, end):
    data = []
    driver = webdriver.Firefox(options=firefox_options)
    url_base = "https://tvtropes.org/pmwiki/index_report.php?filter=&groupname=Main&page="

    for i in range(start, end):
        print("Page: " + str(i))
        data += scrape_index(driver, url_base + str(i))
    
    df = pd.DataFrame(data)
    print(df)
    df.to_csv("tropes_href.csv")



def scrape_page(driver, url):
    pdata = {}
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='headline'].entry-title")))
        pdata = {'source': driver.page_source}
        print("Good Page")
    except TimeoutException:
        print("Bad page")
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while scraping the page: {e}")
    
    return pdata



def main_2(start, end):
    old_data = pd.read_csv("tropes_href.csv")
    
    mdata = []
    driver = webdriver.Firefox(options=firefox_options)

    for index, row in old_data.iloc[start:end].iterrows():
        print("row: " + str(index) + ", " + str(row['text']))
        url = row['href']
        new_info = scrape_page(driver, url)

        all_info = row.to_dict()
        all_info.update(new_info)

        mdata.append(all_info)
        print(mdata)

        if ((index+1) % 200 == 0):
            df = pd.DataFrame(mdata)
            filename = "tropes_deepscrape_" + str(index+1) + ".csv"
            df.to_csv(filename, index=False)


#main_1(1, 113)
main_2(1, 2)
#1-112 inclusive