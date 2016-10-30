#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 14:40:56 2016

@author: Trucy
"""

import random
#import logging

class RandomUserAgent(object):
    def __init__(self, agents):
        self.agents = agents
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
        
    def process_request(self, request, spider):
        #随机选个agent
        agent=random.choice(self.agents)
        #logging.warning('Agent:%s'%agent)
        request.headers.setdefault('User-Agent', agent)

  
class ProxyMiddleware(object):
    def __init__(self, proxies):
        self.proxies = proxies

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('PROXIES'))
        
    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy

            

