# -*- coding: utf-8 -*-

import requests
import json
import re

class Tools(object):
    def __init__(self,site,token):
        self.site = site
        self.token = token
        self.headers = {
            'User-Agent': 'curl/7.12.1',
            'Host': 'data.zz.baidu.com',
            'Content - Type': 'text / plain',
            'Content - Length': '83'
        }
        self.base_url = 'http://data.zz.baidu.com/urls?site={site}&token={token}'

    def get_json(self,url_list):
        data = '\n'.join(url_list)
        url = self.base_url.format(site=self.site,token=self.token)
        html = requests.post(url,headers=self.headers,data=data).text
        info = json.loads(html)
        print(info)

    def get_urls(self,sitemap):
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/57.0.2987.110 Safari/537.36'
        }
        html = requests.get(sitemap,headers=headers).text
        urls = re.findall('<loc>http://(.*?)</loc>',html)
        urls = ['www.'+url for url in urls]
        # print(urls)
        return urls

if __name__ == '__main__':
    site = 'www.stopfollow.com'
    token = 'NpU01TxKEtTQAlBV'
    # urls = ['www.stopfollow.com/article/django-study-notes/','www.stopfollow.com/article/selenium-crawler-get-tmall-information/']
    tool = Tools(site,token)
    urls = tool.get_urls('http://www.stopfollow.com/sitemap.xml')
    tool.get_json(urls)

