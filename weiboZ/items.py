# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class WeibozItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mblogid = Field(serializer=str)  # 微博内容id
    created_at = Field(serializer=str)  # 说说时间
    comments_count = Field(serializer=int)  # 评论数
    reposts_count = Field(serializer=int)  # 转发数
    like_count = Field(serializer=int)  # 点赞数
    text = Field(serializer=str)  # 正文内容
    scheme = Field(serializer=str)  # 微博地址
    user = Field()  # 用户名\粉丝数\说说数
    #后期处理需要用到的字段
    admin=Field()
    price=Field()
    tag=Field()
