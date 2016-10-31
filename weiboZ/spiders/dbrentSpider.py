# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags, replace_escape_chars
from weiboZ.items import DoubanItem
from scrapy.selector import Selector


class dbrentSpider(CrawlSpider):

    name = "dbSpider"
    url_temp = 'https://www.douban.com/group/shanghaizufang/discussion?start='
    #allowed_domains = ['douban.com']
    maxPage = 10000
    start_urls = [
        url_temp + '0'
    ]
    rules = (
        Rule(LinkExtractor(allow=(r'https://www.douban.com/group/topic/.*'),
                           deny=(r'https://www.douban.com/group/topic/.*/\?.*')),
             callback='parse_item', follow=True),
    )

    def __init__(self, num=100, new_url='', *args, **kwargs):
        super(dbrentSpider, self).__init__(*args, **kwargs)
        self.num = int(num)
        self.new_url = new_url
        if len(self.new_url) != 0:
            self.url_temp = self.new_url
        self.start_urls = [self.url_temp +
                           str(i * 25) for i in range(0, min(int(num), self.maxPage))]

    def parse_item(self, response):
        DI = DoubanItem()
        DI['scheme'] = response.url
        sel = Selector(response, type='html')
        context = sel.css(
            '#content > div > div.article > div.topic-content.clearfix > div.topic-doc')
        # 发布人
        DI['user'] = context.css("h3 > span.from > a::text").extract()[0]
        # 时间
        DI['created_at'] = context.css(
            ' h3 > span.color-green::text').extract()[0]
        # 标题，可能两种匹配，优先选择正文中的
        title = context.css(
            'table > tbody > tr:nth-child(2) > td.tablecc').extract()
        if not title:
            title = sel.css('#content > h1').extract()[0]
        else:
            title = title[0]
        DI['title'] = remove_tags(title).strip()
        # 正文文本
        DI['text'] = replace_escape_chars(
            '。'.join(sel.css('#link-report > div >p ::text').extract()),
            which_ones=('\n', '\t', '\r', ' '))

        # 点赞数，不存在就是0
        lc = sel.css('#sep > div.sns-bar-fav > span > a::text').extract()
        if not lc:
            lc = 0
        else:
            lc = lc[0][:-1]
        DI['like_count'] = lc
        return DI
