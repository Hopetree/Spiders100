# -*- coding: utf-8 -*-
import requests
import json
from urllib.parse import quote
from pymongo import MongoClient

"""
简书搜索爬虫
输入搜索关键词，将搜索到的所有文章爬取下来
数据保存到mongodb中
"""


class JianshuSearch(object):
    def __init__(self, db_name, coll_name, key, host='127.0.0.1', port=27017):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/57.0.2987.110 Safari/537.36"
        }
        self.url = 'http://www.jianshu.com/search/do?q={key}&type=note&page={page}&order_by=default'
        self.key = quote(key)
        self.start_page = 1
        self.host = host
        self.port = port
        self.db_name = db_name
        self.coll_name = coll_name

    def get_total_pages(self):
        '''提取总页码数'''
        url = self.url.format(key=self.key, page=self.start_page)
        html = requests.get(url, headers=self.headers).text
        data = json.loads(html)
        total_pages = data['total_pages']
        return total_pages

    def get_infos(self, page):
        '''提取单个页面的文章信息，格式为dict'''
        url = self.url.format(key=self.key, page=page)
        html = requests.get(url, headers=self.headers).text
        data = json.loads(html)
        entries = data['entries']
        for each in entries:
            self.save_infos(each)

    def save_infos(self, entry):
        '''保存一个文章的信息'''
        coon = MongoClient(host=self.host, port=self.port)
        coll = coon[self.db_name][self.coll_name]
        coll.insert(entry)

    def main(self):
        '''主函数，循环迭代进行翻页，提取所有页码的信息并保存到数据库'''
        total_pages = int(self.get_total_pages())
        for i in range(1, total_pages + 1):
            self.get_infos(i)
            print('总计{}页，已经爬完{}页'.format(total_pages, i))


if __name__ == '__main__':
    DB_NAME = 'jianshu'
    COLL_NAME = 'search_result'
    key = 'python'
    spider = JianshuSearch(key=key, db_name=DB_NAME, coll_name=COLL_NAME)
    spider.main()


