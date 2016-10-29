# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from weiboZ import DateUtil
import pickle
import logging
import os
import datetime


class JsonPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        logging.warning('生成文件:items.json')
        self.file.close()

    def process_item(self, item, spider):
        try:
            line = json.dumps(dict(item), ensure_ascii=False, indent=2) + ',\n'
            self.file.write(line)
            return item
        except Exception:
            self.file.close()


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_col):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col
        cwd = os.getcwd()
        with open(os.path.join(cwd, 'weiboZ/data.pl'), 'rb') as f:
            data = pickle.load(f)
        self.tAdmin = data['admin']
        self.tPrice = data['price']
        self.tTag = data['tag']
        self.recent = datetime.datetime(2006, 1, 1, 0, 0)  # 最老数据

    @classmethod
    def from_crawler(cls, crawler):
        logging.warning('生成MongoPipeline对象')
        return cls(
            crawler.settings.get('MONGO_URI'),
            crawler.settings.get('MONGO_DATABASE')['db'],
            crawler.settings.get('MONGO_DATABASE')['col']
        )

    def open_spider(self, spider):
        logging.warning('开始spider')
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
        except ValueError:
            logging.error('数据库连接错误')
        # 表是否存在，若不存在建立对应的索引
        if self.mongo_col not in self.db.collection_names():
            self.db[self.mongo_col].create_index(
                [('created_at', pymongo.DESCENDING)])
            self.db[self.mongo_col].create_index(
                [('admin', pymongo.ASCENDING)], sparse=True)
            self.db[self.mongo_col].create_index(
                [('price', pymongo.ASCENDING)], sparse=True)
            self.db[self.mongo_col].create_index(
                [('mblogid', pymongo.ASCENDING)], unique=True)
        else:
            # 找到当前表中最新插入的数据，方便过滤
            recent_row = list(self.db[self.mongo_col].find(projection=['created_at', '_id'],
                                                           limit=1, sort=[('created_at', pymongo.DESCENDING)]))
            self.recent = recent_row[0]['created_at']  # 最新时间
            logging.warning("允许插入数据的时间大于%s"%(self.recent+datetime.timedelta(hours=8)).__str__())

    def close_spider(self, spider):
        logging.warning('结束spider')
        self.client.close()

    def process_item(self, item, spider):
        #collection_name = item.__class__.__name__
        # logging.warning('开始插入表%s'%self.mongo_col)
        try:
            dt = DateUtil.convert(item["created_at"])  # 时间格式化
            if dt <= self.recent:  # 数据库中已经有或者太老，不再插入
                return item
            item["created_at"] = dt
            admin, price, tag = self.extract(
                item['text'], self.tAdmin, self.tPrice, self.tTag)
            item["admin"] = admin
            item["price"] = price
            item["tag"] = tag

            self.db[self.mongo_col].insert(dict(item))
            return item
        except Exception:
            logging.error('编号为:%s的数据插入异常' % item['mblogid'])
            #logging.error(item['text'])

    def extract(self, text, tAdmin, tPrice, tTag):
        i = 0
        location = []  # 存储行政区
        price = []  # 存储价格
        rent = True  # 默认为出租信息
        while i < len(text):
            if tPrice.has_keys_with_prefix(text[i]):  # 优先匹配价格
                j = i
                i += 1
                # 正向最大匹配
                while i < len(text) and tPrice.has_keys_with_prefix(text[j:i + 1]):
                    i += 1
                if text[j:i] in tPrice.keys(text[j:i]):  # 价格转换成数字
                    if ord(text[j]) > 60:
                        price.append(tPrice[text[j:i]])
                    else:
                        price.append(int(text[j:i]))
                    continue
                else:  # 未匹配，去尝试匹配地点
                    i = j
            if tAdmin.has_keys_with_prefix(text[i]):  # 匹配地点
                j = i
                i += 1
                # 正向最大匹配
                while i < len(text) and tAdmin.has_keys_with_prefix(text[j:i + 1]):
                    i += 1
                if text[j:i] in tAdmin.keys(text[j:i]):
                    location.append(text[j:i])
                    continue
                else:  # 未匹配，去尝试匹配租房还是求房
                    i = j
            if rent and tTag.has_keys_with_prefix(text[i]):  # 未匹配过的情况下匹配租房还是求房
                j = i
                i += 1
                # 正向最大匹配
                while i < len(text) and tTag.has_keys_with_prefix(text[j:i + 1]):
                    i += 1
                if text[j:i] in tTag.keys(text[j:i]):
                    rent = False
                else:  # 未匹配，去尝试匹配租房还是求房
                    i = j + 1
            else:
                i += 1
        return location, price, rent
