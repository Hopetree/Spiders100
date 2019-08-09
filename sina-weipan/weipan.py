# -*- coding:utf-8 -*-

'''
爬取新浪的微盘中歌曲（周杰伦的）
然后下载歌曲到本地
'''
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Weipan(object):

    def __init__(self, url):
        self.baseurl = url
        self.items = []
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.waiter = WebDriverWait(self.driver, 5)

    def search_info_by_url(self, url):
        self.driver.get(url)

        item_selectors = self.waiter.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="sort_name_intro"]/div/a'))
        )
        for item_selector in item_selectors:
            item_link = item_selector.get_attribute('href')
            item_title = item_selector.get_attribute('title')
            self.items.append((item_title, item_link))

        # 提取下一页的链接，并递归提取信息
        page_selectors = self.waiter.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="vd_page"]/a[@class="vd_bt_v2 vd_page_btn"]'))
        )
        for page_selector in page_selectors:
            next_text = page_selector.find_element_by_xpath('./span').text.strip()
            if next_text == '下一页':
                next_url = page_selector.get_attribute('href')
                self.search_info_by_url(next_url)

    def main(self):
        self.search_info_by_url(self.baseurl)
        self.driver.close()
        return self.items


class Load(object):

    def __init__(self, item):
        self.item = item
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.waiter = WebDriverWait(self.driver, 5)

    def run(self):
        title, url = self.item
        self.driver.get(url)
        load_button = self.waiter.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="download_big_btn"]'))
        )
        # 点击下载歌曲的按钮，自动下载到本地
        load_button.click()
        print('{} is loading, the url is {}'.format(title, url))
        time.sleep(20)

    def close(self):
        self.driver.close()


def run(item):
    L = Load(item)
    L.run()
    L.close()


def main(items):
    with ThreadPoolExecutor(max_workers=4) as pool:
        pool.map(run, items)


if __name__ == '__main__':
    url = 'https://vdisk.weibo.com/s/tg6IJ27yogat5'
    wp = Weipan(url)
    items = wp.main()
    main(items)
