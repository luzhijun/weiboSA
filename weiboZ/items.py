# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class WeibozItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mblogid = Field()  # 微博内容id
    created_at = Field()  # 说说时间
    comments_count = Field(serializer=int)  # 评论数
    reposts_count = Field(serializer=int)  # 转发数
    like_count = Field(serializer=int)  # 点赞数
    text = Field()  # 正文内容
    scheme = Field()  # 微博地址
    user = Field()  # 用户名\粉丝数\说说数
    #后期处理需要用到的字段
    admin=Field()
    price=Field()
    tag=Field()

class DoubanItem(Item):
    scheme=Field()  #信息地址
    user=Field()  #发帖作者
    created_at=Field()  # 发布时间
    title=Field() #发布标题
    text=Field() #正文内容
    like_count = Field(serializer=int)  # 点赞数
    #后期处理需要用到的字段
    mblogid = Field()
    admin=Field()
    price=Field()
    tag=Field()