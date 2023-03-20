#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

class ScienceDotOrgScraper():
    def __init__(self):
        self.base_url = 'https://www.science.org/topic/category/physics?'

    def get_soup(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            return f"Error: HTTP Code: {response.status_code}"
    
    def get_h2_text_from_page(self, url):
        soup = self.get_soup(url)
        title=soup.find_all('h2', class_='article-title sans-serif text-deep-gray mb-1')
        h2_tag_text_list = [ tag.text for tag in title ]
        return h2_tag_text_list


    def get_max_start_page(self):
        
        """
        This sends a web request with pageSize set to the highest value the web UI allows for. 100.
        we will grab the text value in the navigation bar at the bottom of the page to compute a way to retrieve
        all of the data
        """
        params = 'startPage=0&pageSize=100'
        url = self.base_url + params

        soup = self.get_soup(url)

        # get the page size from the bottom navbar
        page_size_bar = soup.find('ul', class_='pagination justify-content-center text-darker-gray')
        page_size_list_item_tags = page_size_bar.find_all('li', class_='page-item')
        page_size_bar_len = len(page_size_list_item_tags)
        max_page_ele = page_size_bar_len - 2
        max_start_page = page_size_list_item_tags[max_page_ele].text

        return int(max_start_page)

    def perform(self):
        h2_text_data = []
        # first do base request so we can get the startPage size that we need.
        # we will use this in the startPage param
        max_start_page_size = self.get_max_start_page()
        start_page_range = range(0, max_start_page_size + 1)
        for start_page in start_page_range:
            url = f'https://www.science.org/topic/category/physics?startPage={start_page}&pageSize=100'
            print(f"Sending Request to: {url}")
            h2_text = self.get_h2_text_from_page(url)
            h2_text_data.append(h2_text)

        # flatten the list 
        h2_text = [item for sublist in h2_text_data for item in sublist]

        return h2_text
    
# instantiate a new ScienceDotOrgScraper() object and run its perform() method call.
my_scraper = ScienceDotOrgScraper()
text_data = my_scraper.perform()
for item in text_data:
    print(item)