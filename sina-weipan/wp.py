# -*- coding:utf-8 -*-
# Author: https://github.com/Hopetree
# Date: 2019/8/10

'''
新浪微盘资源下载，不需要模拟浏览器，完全使用接口调用
'''

import os
import re
import time
import json
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree


class Weipan(object):
    def __init__(self, url, output):
        self.baseurl = url
        self.items = []
        self.output = output

    def get_item_list(self, url):
        res = requests.get(url).text
        tree = etree.HTML(res)

        # 提取当前页所有资源，存入列表
        item_selectors = tree.xpath('//div[@class="sort_name_intro"]/div/a')
        for item_selector in item_selectors:
            link = item_selector.get('href')
            title = item_selector.get('title')
            self.items.append((link, title))

        # 提取下一页链接，进行递归爬取
        next_page_selectors = tree.xpath('//div[@class="vd_page"]/a[@class="vd_bt_v2 vd_page_btn"]')
        for next_page_selector in next_page_selectors:
            next_text = next_page_selector.xpath('./span')[0].text.strip()
            if next_text == "下一页":
                next_url = self.baseurl + next_page_selector.get('href')
                self.get_item_list(next_url)

    def get_callback_info_by_item(self, item):
        '''
        提取一个资源页面的有效信息，用来构造请求url
        '''
        url, title = item
        res = requests.get(url).text
        id = re.findall("CURRENT_URL = 'vdisk.weibo.com/s/(.*?)'", res)[0]
        sign = re.findall("SIGN = '(.*?)'", res)[0]
        url_temp = 'https://vdisk.weibo.com/api/weipan/fileopsStatCount?link={id}&ops=download&wpSign={sign}&_={timestr}'
        timestr = int(time.time() * 1000)
        callback = url_temp.format(id=id, sign=sign, timestr=timestr)
        return url, callback

    def get_load_info_by_callback_info(self, callback_info):
        '''
        请求回调地址，返回资源下载地址等信息
        '''
        url, callback = callback_info
        headers = {
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        res = requests.get(callback, headers=headers).text
        data = json.loads(res)
        name = data.get('name')
        load_url = data.get('url')
        return name, load_url

    def load(self, load_info):
        name, load_url = load_info
        content = requests.get(load_url).content
        savename = os.path.join(self.output, name)
        with open(savename, 'wb+') as f:
            f.write(content)
        print('{} load done'.format(name))

    def load_by_item(self, item):
        '''
        线程执行的函数
        '''
        callback_info = self.get_callback_info_by_item(item)
        load_info = self.get_load_info_by_callback_info(callback_info)
        self.load(load_info)

    def main(self):
        # 收集资源下载信息
        self.get_item_list(self.baseurl)
        # 多线程下载资源
        with ThreadPoolExecutor(max_workers=8) as pool:
            pool.map(self.load_by_item, self.items)


if __name__ == '__main__':
    URL = 'https://vdisk.weibo.com/s/tg6IJ27yogat5'
    OUTPUT = r'C:\Users\HP\Downloads\load'
    wp = Weipan(URL, OUTPUT)
    wp.main()
