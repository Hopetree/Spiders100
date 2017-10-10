# -*- coding: utf-8 -*-

"""
汽车之家二手车爬虫
爬虫使用lxml解析器和Xpath选择器
数据存放到mongodb中
"""

import requests
from lxml import etree
from pymongo import MongoClient

class AutohomeSpider(object):
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                     " Chrome/57.0.2987.110 Safari/537.36"}

        self.coon = MongoClient('localhost',27017)
        self.coll = self.coon['autohome']['Oldcars']


    def get_items(self,url):
        html = requests.get(url,headers=self.headers).text
        selector = etree.HTML(html)
        next_page = selector.xpath('//*[@id="listpagination"]/a[last()]/@href')[0]
        next_text = selector.xpath('//*[@id="listpagination"]/a[last()]/text()')[0]
        url_list = selector.xpath('//*[@id="viewlist_ul"]/li/a/@href')
        for each in url_list:
            the_url = 'http://www.che168.com'+each
            self.get_infos(the_url)
        if next_text == '下一页':
            next_url = 'http://www.che168.com/china'+next_page
            self.get_items(next_url)

    def get_infos(self,page_url):
        dic = {}
        html = requests.get(page_url,headers=self.headers).text
        selector = etree.HTML(html)
        car_info = selector.xpath('//div[@class="car-info"]')
        if car_info:
            dic['title'] = car_info[0].xpath('//div[@class="car-title"]/h2/text()')[0]
            price = car_info[0].xpath('//div[@class="car-price"]/ins/text()')[0]
            dic['price'] = price.strip(' ').replace('￥','')
            dic['xslc'] = car_info[0].xpath('//div[@class="details"]/ul/li/span/text()')[0]
            dic['scsp'] = car_info[0].xpath('//div[@class="details"]/ul/li/span/text()')[1]
            dic['dwpl'] = car_info[0].xpath('//div[@class="details"]/ul/li/span/text()')[2]
            dic['city'] = car_info[0].xpath('//div[@class="details"]/ul/li/span/text()')[3]
            dic['call_num'] = car_info[0].xpath("//a[contains(@class,'btn') and contains(@class,'btn-iphone3')]/text()")[0]
            commitment_tag = car_info[0].xpath('//div[@class="commitment-tag"]/ul/li/span/text()')
            dic['commitment_tag'] = '/'.join(commitment_tag)
            dic['address'] = car_info[0].xpath('//div[@class="car-address"]/text()')[0].strip()
            dic['call_man'] = car_info[0].xpath('//div[@class="car-address"]/text()')[-1].strip()
            print(dic)
            self.coll.insert(dic)


if __name__ == '__main__':
    url = 'http://www.che168.com/china/list/'
    spider = AutohomeSpider()
    spider.get_items(url)

