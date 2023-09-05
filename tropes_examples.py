### [selenium] SCRIPT TO SCRAPE TROPE SPECIAL PAGES [in progress] ###
# Adapted from Deepscrape_6
# Project: Tropes
# Input: page source
# Output: list of movies

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
import ast
import re
import requests
import pandas as pd
firefox_options = Options()
#firefox_options.add_argument("--headless")


def get_li_data(film_node):
    data = []
    base_trope = "https://tvtropes.org"
    li_nodes = film_node.find_all('li')
    for l in li_nodes:
        example = {}
        a = l.find('a', class_='twikilink')
        if a:
            href = base_trope + a['href']
            if "Main" in href: 
                continue
            movie = href.split("/")[-1]
            movie = re.sub(r"(?<!^)(?=[A-Z])", " ", movie)
            example['movie'] = movie
            example['href'] = href
            example['text'] = l.text.strip()
            data.append(example)
    return data


def process_page(soup):
    cols = ['examples']
    tdata = dict.fromkeys(cols, [])

    main_article_div = soup.find('div', id='main-article')

    examples = get_li_data(main_article_div)
    tdata['examples'] = examples
    return tdata


def scrape_page(driver, url): #scrape ONE
    try: 
        wait = WebDriverWait(driver, 10)
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='headline'].entry-title")))
        return driver.page_source
    except TimeoutException:
        print("Bad Page")
        return ""

def get_overflow(soup, title):
    base_trope = "https://tvtropes.org"
    trope = title.replace(' ', '').strip()
    href_possible = re.compile(rf"/pmwiki/pmwiki.php/{trope}/(.*Animat.*|.*Film.*)", re.IGNORECASE)
    return list(set(base_trope + a['href'] for a in soup.find_all('a', href=href_possible)))

def main(start, end):
    
    example_df = pd.read_csv("tropes_examples_all.csv", nrows=50)
    source_df = pd.read_csv("tropes_deepscrape_all.csv", nrows=50)
    print("Done Loading-----")

    mdata = []
    driver = webdriver.Firefox(options=firefox_options)
    
    for index, row in example_df.iloc[start:end].iterrows():
        print("row: " + str(index) + ", " + row['text'])
        if ast.literal_eval(row['examples']) == []:
            mdata.append(row)
            print("empty")

        elif ast.literal_eval(row['examples'])[0]['movie'] == "OVERFLOW":
            print("OVERFLOW")
            all_info = row[['text', 'href']].to_dict()
            try: 
                source = source_df.loc[index, 'source']
                soup = BeautifulSoup(source, 'html.parser')
                advanced_urls = get_overflow(soup, all_info['text'])
                advanced_sources = [scrape_page(driver, u) for u in advanced_urls]
                advanced_soups = [BeautifulSoup(s, 'html.parser') for s in advanced_sources]
                new_infos = [process_page(s) for s in advanced_soups]
                new_info = {'examples': []}
                new_info['examples'].extend(n_i_example for n_i in new_infos if n_i for n_i_example in n_i['examples'])

                if (new_info['examples'] == []):
                    print("  Example: None")
                else:
                    print("  Example: " + new_info['examples'][0]['movie'] + ", ... , " + str(len(new_info['examples'])))

            except Exception as e:
                print(f"Skipping row {index} due to error: {e}")
                new_info = {'examples': []}
            
            all_info.update(new_info)
            mdata.append(all_info)
                
        else:
            mdata.append(row)
            print("normal")
        

        if ((index+1) % 200 == 0):
            df = pd.DataFrame(mdata)
            filename = "tropes_examples_v2_" + str(index+1) + ".csv"
            df.to_csv(filename, index=False)     
        
    return mdata

main(0, 40)
#main(0, 1000)
#main(1000, 2000)
#main(2000, 3000)
