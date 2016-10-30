#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 18:01:55 2016
日期转换 from 微博 to mongoDB
@author: Trucy
"""
import datetime
import hashlib

def convert_in_an_hour(fr):
    now=datetime.datetime.now()
    if len(fr)==4 :
        if ord(fr[1])>100: #m分钟
            delta=datetime.timedelta(minutes=int(fr[0]))
        else: #ss秒
            delta=datetime.timedelta(seconds=int(fr[:2]))
    else: #mm分钟
        delta=datetime.timedelta(minutes=int(fr[:2]))
    return now-delta
    
def convert(fr):
    '''
    微博时间形式:
        wblog日期形式:[10,20,30,40,50]秒前,[1-59]分钟前，今天hh:mm，MM月DD日 hh:mm, yyyy-MM-dd hh:mm
    豆瓣时间格式: yyyy-MM-dd hh:mm:ss
    返回USC时间
    '''
    delta=datetime.timedelta(hours=8)
    minute=fr[-2:] if fr[-2]!='0' else fr[-1]
    hour=fr[-5:-3] if fr[-5:]!='0' else fr[-2]
    td=datetime.date.today()-delta
    if len(fr)<6:
        return convert_in_an_hour(fr)-delta
    if len(fr)==8:
        return datetime.datetime(td.year,td.month,td.day,int(hour),int(minute))-delta
    if len(fr)==11: 
        mon=fr[1] if fr[0]=='0' else fr[:2]
        day=fr[4] if fr[3]=='0' else fr[3:5] 
        return datetime.datetime(td.year,int(mon),int(day),int(hour),int(minute))-delta
    if len(fr)==16:
        dt=fr.split('-')
        if len(dt[1])==1:
            dt[1]='0'+dt[1]
        if len(dt[2])==1:
            dt[2]='0'+dt[2]
        fr=''.join(dt)
        return datetime.datetime.strptime(fr,"%Y%m%d %H:%M")-delta
    else: ##豆瓣时间格式
        return datetime.datetime.strptime(fr,"%Y-%m-%d %H:%M:%S")-delta

def calc_md5(s):
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest()