#! python3
# -*- coding: utf-8 -*-

import re, json
from urllib import request, parse
from pandas import DataFrame, Series
import pandas as pd

__author__ = '放养的小爬虫'

# 计算总共页数
def SearchPageCount(position, city):
    url = 'http://www.lagou.com/jobs/positionAjax.json?'
    params = {'city': city, 'kd': position}
    url += parse.urlencode(params)
    with request.urlopen(url) as f:
        data = f.read()
        content = json.loads(str(data, encoding='utf-8', errors='ignore'))['content']
        count = int(content['totalPageCount'])
        totalCount = int(content['totalCount'])
        print('本次搜索到{0}个职位'.format(totalCount))
    return count

def LaGouSpiderWithKeyWord(position, city):
    # 获取总共页数
    pageCount = SearchPageCount(position, city)
    if pageCount == 0:
        print('抱歉！在您搜索的城市中没有您要找的职位')
        return

    for i in range(0, pageCount):
        url = 'http://www.lagou.com/jobs/positionAjax.json?'
        params = {'city': city, 'kd': position, 'pn': i+1}
        url += parse.urlencode(params)
        data = request.urlopen(url).read()
    #     读取Json数据
        jsondata = json.loads(str(data, encoding='utf-8', errors='ignore'))['content']['result']
        for t in list(range(len(jsondata))):
            jsondata[t]['companyLabelListTotal'] = '-'.join(jsondata[t]['companyLabelList'])
            jsondata[t].pop('companyLabelList')
            if t == 0:
                rdata = DataFrame(Series(data=jsondata[t])).T
            else:
                rdata = pd.concat([rdata,DataFrame(Series(data=jsondata[t])).T])
        totaldata = pd.concat([totaldata, rdata])
        print('正在解析第{0}页...'.format(i+1))
    totaldata.to_excel('lagou.xls', sheet_name='sheet1')

if __name__ == "__main__":
    position = input('请输入你要爬取的职位')
    city = input('请输入你要爬取的城市')
    LaGouSpiderWithKeyWord(position, city)
