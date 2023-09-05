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

def process_page(soup):
    
    print("start parsing soup")
    
    character = soup.find('h1', class_='profile-name').text
    movie_div = soup.find('div', {'class': 'profile-category arrow'})
    movie = movie_div.find('h1').text

    personality = soup.find_all('div', 'rc-collapse personality-vote')

    mbti_vote = ''
    mbti_count = ''
    big5_vote = ''
    big5_count = ''
    for per in personality:
        type = per.find('label', 'personality-vote-title').text
        count = per.find('label', 'personality-vote-count').text #fix the stripping
        vote = per.find('label', 'personality-vote-item').find('label').text

        if (type == 'Four Letter'):
            mbti_vote = vote
            mbti_count = count
        elif (type == 'Big 5 (SLOAN)'):
            big5_vote = vote
            big5_count = count

    tdata = {'character': character,
        'movie': movie,
        'mbti_vote' : mbti_vote,
        'mbti_count' : mbti_count,
        'big5_vote' : big5_vote,
        'big5_count' : big5_count}

    
    print("done parsing soup")
    return tdata

def scrape_page(driver, url):
    pdata = []
    print("initial wait, sleep 10")
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    print("secondary wait, sleep 10")
    time.sleep(10)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.profile-name')))
        print("Good Page")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #MAJOR CHANGE
        #pdata = soup

        #pdata = process_page(soup)
    except TimeoutException:
        print("Bad Page")
    except AttributeError:
        print("Bad Page")

    return pdata



def main():
    data = []
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    url = "https://www.personality-database.com/profile/859/joy-inside-out-2015-mbti-personality-type"
    
    driver.get(url)

    data += scrape_page(driver, url)
    
    print("final data: " + data)

    #df = pd.DataFrame(data)
    #filename = ""
    #df.to_csv(filename, index=False)




#__main__

main()