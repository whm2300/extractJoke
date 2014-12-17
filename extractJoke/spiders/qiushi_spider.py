#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time

import scrapy
from scrapy.http.request import Request

from extractJoke.save_to_mongo import SaveToMongo

#from extractJoke.items import QiuShiItem

#热门
hot_base_url = 'http://www.qiushibaike.com/8hr/page/%d'
hot_max_page = 35 #热门最大页码

#24小时精华
day_base_url = 'http://www.qiushibaike.com/hot/page/%d'
day_max_page = 150

#周精华
week_base_url = 'http://www.qiushibaike.com/week/page/%d'
week_max_page = 280

#月精华
month_base_url = 'http://www.qiushibaike.com/month/page/%d'
month_max_page = 1000

#真相--硬菜
fact_base_url = 'http://www.qiushibaike.com/imgrank/page/%d'
fact_max_page = 25

#真相-时令
season_base_url = 'http://www.qiushibaike.com/pic/page/%d'
season_max_page = 350

#最新
late_base_url = 'http://www.qiushibaike.com/late/page/%d'
late_max_page = 2000

name_type = {'8hr':1, 'hot':2, 'week':3, 'month':4, 'imgrank':5, 'pic':6, 'late':7}

def make_start_urls():
    urls = []
    add_urls(urls, hot_base_url, hot_max_page)
    add_urls(urls, day_base_url, day_max_page)
    add_urls(urls, week_base_url, week_max_page)
    add_urls(urls, month_base_url, month_max_page)
    add_urls(urls, fact_base_url, fact_max_page)
    add_urls(urls, season_base_url, season_max_page)
    add_urls(urls, late_base_url, late_max_page)

    return urls

def add_urls(urls, base_url, max_page):
    for i in range(max_page):
        urls.append(base_url % (i+1))

class Qiushi(scrapy.Spider):
    name = "qiushi"
    allowed_domains = ["qiushibaike.com"]
    start_urls = make_start_urls()
    download_delay = 1

    def __init__(self):
        self._db = SaveToMongo()
        self._db.clear_data()

    def parse(self, response):
        if response.status != 200:
            self.log("get fail , url:" + response.url)
            return

        patter = re.compile(r'<div class="content"(\s*.*?\s*)*>(\s*.*?\s*)*</div>|<div class="thumb"(\s*.*?\s*)*>(\s*.*?\s*)*</div>') #提取内容和图片部分div
        content_patter = re.compile(r'\n\s*.*\n\s*') #提取div中的内容
        picurl_patter = re.compile(r'http://.*" alt') #提取图片url 

        #当前页码
        cur_page = int(response.url.split('/')[-1])
        index = (cur_page - 1)*50
        #当前分类
        cur_type_name = response.url.split('/')[3]
        cur_type = name_type[cur_type_name]

        page_content = []
        for m in patter.finditer(response.body):
            s = m.group()
            data = {}
            if s.find('class="content"') != -1: #内容数据
                match = content_patter.search(s)
                if match:
                    a = match.group().strip(' \n')
                    index += 1
                    data["content"] = a.replace('<br/>', '')
                    data["index"] = index
                    data["type"] = cur_type
                    page_content.append(data)
            else: #图片数据
                match = picurl_patter.search(s)
                if match: #将图片数据保存到上一个内容
                    page_content[-1]["pic_url"] = match.group().rstrip('" alt')
        self._db.save_data(page_content)

    def make_requests_from_url(self, url):
        #模拟浏览器请求
        headers = {
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
                }
        request = Request(url, headers=headers)
        return request

    def closed(self, reason):
        pass
