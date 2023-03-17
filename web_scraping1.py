#!/usr/bin/env python3

#Python web scraping with BeautifulSoup

import requests
import re
from bs4 import BeautifulSoup

healthy_recipes_url = 'https://www.allrecipes.com/recipes/84/healthy-recipes/'

def do_request(url):
    r = requests.get(url)
    if r.status_code == 200:
        html = r.text
        return html 
    else:
        return f"Error: {r.status_code}"
    
html = do_request(healthy_recipes_url)
soup = BeautifulSoup(html, 'html.parser')
a_tags = soup.find_all('a',href=True )
healthy_recipe_url_re = 'https://www.allrecipes.com/recipes/\d.*/healthy-recipes/.*'

print(f"Title: {soup.title.text}")

for a in a_tags:
    href = a['href']
    if re.match(healthy_recipe_url_re, href):
        print(href)
    else:
        continue

