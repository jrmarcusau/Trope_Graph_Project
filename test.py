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
import requests
import pandas as pd

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


print("here")
firefox_options = Options()
print("here2")
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)
print("here3")

url = "https://www.personality-database.com/profile/859/joy-inside-out-2015-mbti-personality-type"

driver.get(url)
wait = WebDriverWait(driver, 10)

source = driver.page_source
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.profile-name')))

soup = BeautifulSoup(driver.page_source, 'html.parser')

character = soup.find('h1', class_='profile-name').text
movie_div = soup.find('div', {'class': 'profile-category arrow'})
movie = movie_div.find('h1').text

personality = soup.find_all('div', 'rc-collapse personality-vote')

mbti_vote = ''
mbti_count = ''
big5_vote = ''
big5_count = ''
for per in personality:
    print(per.prettify())
    type = per.find('label', 'personality-vote-title').text
    count = per.find('label', 'personality-vote-count').text #fix the stripping
    vote = per.find('div', 'personality-vote-item').label.text

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

print("character: " + character)
print("tdata: ")
print(tdata)

# b'<!DOCTYPE html><html xmlns="http://www....
driver.quit()

print("hello world")
