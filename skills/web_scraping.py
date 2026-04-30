import requests
from bs4 import BeautifulSoup

def scrape(url):
    """Generic extraction logic."""
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser').title.text
