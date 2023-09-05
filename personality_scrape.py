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

#chrome_options = Options()
#chrome_options.add_argument("--log-level=3")


def process_page(driver):
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print("start parsing soup")
    info_cards = soup.find_all('a', class_='profile-card-link')
    print("NumChars: " + str(len(info_cards)))
    tdata = []
    for card in info_cards:
        character = card.find('h2', class_='info-name').text
        movie = card.find('div', class_='info-subcategory').label.text
        mbti = card.find('div', class_='personality').text
        href = "https://www.personality-database.com" + card['href']

        dic = {'character': character,
            'movie': movie,
            'mbti' : mbti,
            'href': href}

        tdata.append(dic)
    
    print("done parsing soup")
    return tdata


def loop_pages_by_all(driver):
    pdata = []
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
    for i in range(210):
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.info-name')))
            time.sleep(2)
            pdata += process_page(driver)
            time.sleep(2)
            print("page: " + str(i))
            #next_button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "rc-pagination-next", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "rc-pagination-item-link", " " ))]')
            next_button = driver.find_element(By.CSS_SELECTOR, '.rc-pagination-next .rc-pagination-item-link')
            print("about to click")
            next_button.click()
            time.sleep(2)
        except TimeoutException:
            print("Bad Page")
            break
    print("soupy done")
    return pdata

def loop_pages_by_mbti(driver):
    pdata = []
    print("initial wait, sleep 10")
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
    for i in range(3, 17):
        print("MBTI start: " + str(i) + " -----------------")
        mdata = []
        url_mbti = "https://www.personality-database.com/profile?pid=2&cid=3&sub_cat_id=0&type1=" + str(i)
        driver.get(url_mbti)
        print("loading page, sleep 20")
        time.sleep(20)
               
        for j in range(210):
            print("loading next, sleep 15")
            time.sleep(15)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.info-name')))
                print("Good Page: " + str(j))
                mdata += process_page(driver)
                next_button = driver.find_element(By.CSS_SELECTOR, '.rc-pagination-next .rc-pagination-item-link')
                next_button.click()
                print("clicked next page")
            except TimeoutException:
                print("Bad Page")
                break
        print("MBTI end: n=" + str(len(mdata)))
        df = pd.DataFrame(mdata)
        filename = "page" + str(i) + ".csv"
        df.to_csv(filename, index=False)

    return pdata

    
def main():
    data = []
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    url = "https://www.personality-database.com/profile?pid=2&cid=3"
    
    driver.get(url)


    #data = loop_pages_by_mbti(driver)
    data = loop_pages_by_mbti(driver)
    print("my data made it here!")




#__main__

main()