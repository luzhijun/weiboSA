# -*- coding: utf-8 -*-
import scrapy
import json
from w3lib.html import remove_tags,replace_escape_chars
from weiboZ.items import WeibozItem
import logging


class SearchspiderSpider(scrapy.Spider):

    name = "mblogSpider"
    #allowed_domains = ["http://m.weibo.cn/page/"]
    url_temp = 'http://m.weibo.cn/page/pageJson?containerid=&containerid=100103type%3D1%26q%3D%40%E4%B8%8A%E6%B5%B7%E7%A7%9F%E6%88%BF&type=all&queryVal=%40%E4%B8%8A%E6%B5%B7%E7%A7%9F%E6%88%BF&featurecode=20000180&oid=4035270175262125&luicode=20000061&lfid=4035270175262125&title=%40%E4%B8%8A%E6%B5%B7%E7%A7%9F%E6%88%BF&v_p=11&ext=&fid=100103type%3D1%26q%3D%40%E4%B8%8A%E6%B5%B7%E7%A7%9F%E6%88%BF&uicode=10000011&next_cursor=&page='
    start_urls = [
        url_temp + '1'
    ]
    # 移动版最多允许查看100页
    maxPage = 100

    def __init__(self, num=100, new_url='', *args, **kwargs):
        super(SearchspiderSpider, self).__init__(*args, **kwargs)
        self.num = int(num)
        self.new_url = new_url
        if len(self.new_url) != 0:
            self.url_temp = self.new_url

    def etl(self, d, k, keys):
        return d[k] if k in keys and d[k] != None else 0

    def parseFunc(self, response, N):
        js = json.loads(response.text, encoding='utf-8')
        cardN = len(js['cards'])
        for i in range(N, cardN):
            cgN = len(js['cards'][i]['card_group'])
            for j in range(cgN):
                it = js['cards'][i]['card_group'][j]
                #logging.warning('i:%d,j:%d' % (i, j))
                if 'mblog' in it.keys():
                    mblog = it['mblog']
                    keys = mblog.keys()
                    item = WeibozItem()
                    item['mblogid'] = mblog['mblogid']
                    item['created_at'] = mblog['created_at']
                    item['comments_count'] = self.etl(
                        mblog, 'comments_count', keys)
                    item['like_count'] = self.etl(mblog, 'like_count', keys)
                    item['reposts_count'] = self.etl(
                        mblog, 'reposts_count', keys)
                    item['text'] = replace_escape_chars(remove_tags(mblog['text']),
                        which_ones=('\n', '\t', '\r',' '))
                    item['scheme'] = it['scheme']
                    item['user'] = {
                        'name': mblog['user']['screen_name'],
                        'fansNum': mblog['user']['fansNum'],
                        'statuses_count': mblog['user']['statuses_count']
                    }
                    yield item

    def parse(self, response):
        # 处理第一页
        logging.warning('do page1.')
        items = self.parseFunc(response, 2)
        for item in items:
            yield item
        # 处理其余页
        for i in range(2, min(self.maxPage, self.num) + 1):
            #logging.warning('do page%d' % i)
            yield scrapy.Request(self.url_temp + str(i), self.parse_other)

    def parse_other(self, response):
        items = self.parseFunc(response, 0)
        for item in items:
            yield item
