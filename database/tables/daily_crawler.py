import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import re
import time
from dateutil import parser
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd

import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
#https://www.reuters.com/search/news?blob=


# class ArticleGetter:
#     def __init__(self, base_url, query=""):
#         self.base_url = base_url
#         self.search_url = base_url + query + '&sortBy=date&dateRange=all'
#     def get_daily_news(self, query):
#         # get our search webpage
#         search_url = self.base_url + query + '&sortBy=date&dateRange=all'


class ArticleGetter:
    def __init__(self, query):
        self.url = 'https://www.reuters.com/search/news?blob='
        self.query = query
        
    def get_daily_news(self):

        # script = 'which Chrome'
        # a = os.system(script)
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe', options=chrome_options)

        #driver = webdriver.Chrome('/Users/samhsia/intelligent-asset-allocation/database/tables/chromedriver')
        driver.get(self.url)

        input_field = driver.find_element_by_id('newsSearchField')
        input_field.send_keys(self.query)
        input_button = driver.find_element_by_class_name('search-button')
        input_button.click()

        # Getting current URL
        print("Current Search keyword: ", self.query)
        curr_url = driver.current_url 
        driver.get(curr_url)
        try:
            name = driver.find_element_by_class_name('search-stock-ticker').text
            sub_name = name[name.find("(")+1:name.find(")")] 
            # driver.close()

            base = 'https://www.reuters.com/companies/'
            news_url = "{}{}/news".format(base, sub_name)
            driver.get(news_url)

            origin_soup = BeautifulSoup(driver.page_source, 'html.parser')
            divs = origin_soup.find_all('div', class_='item')
            
            urls = []
            for div in divs:
                time = div.find('div', class_='MarketStoryItem-footer-1SCZA').text
                if "days" in time or "1 month ago" in time: 
                    print(time)
                    link = div.find('a', class_='TextLabel__text-label___3oCVw TextLabel__black-to-orange___23uc0 TextLabel__medium___t9PWg MarketStoryItem-headline-2cgfz')['href']
                    urls.append(link)
            
            # Get the info for each news
            all_time = []
            all_title = []

            for url in urls:
                try:
                    resp = requests.get(url)
                    resp.encoding = 'utf-8'
                    current_page = resp.text
                    soup = BeautifulSoup(current_page, 'html.parser')

                    time = soup.find('div', class_='ArticleHeader_date').text
                    time = str(time).split('/')[0].rstrip()
                    time = parser.parse(time)
                    title = soup.find('h1', class_='ArticleHeader_headline').text

                    all_time.append(time)
                    all_title.append(title)

                except:
                    pass

            query = [self.query] * len(all_time)

            article_df = pd.DataFrame({
                'title': all_title,
                'time': all_time,
                'query': query,
                'url': urls
            })
        except:
            article_df = pd.DataFrame({
                'title': [],
                'time': [],
                'query': [],
                'url': []
            })
        driver.close()
        return article_df


if __name__ == "__main__":
    base_url = 'https://www.reuters.com/search/news?blob='
    query = 'Google'

    article_getter = ArticleGetter('Google')
    article_getter.get_daily_news()