# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def get_urls():
    url = 'https://docs.djangoproject.com/en/1.11/'
    html =  requests.get(url).text
    soup = BeautifulSoup(html,'lxml')
    # print(soup)
    urls = soup.select('#s-django-documentation a.reference')
    for each in urls:
        print(each)
if __name__ == '__main__':
    get_urls()
