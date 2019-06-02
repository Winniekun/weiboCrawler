"""
@Time : 2019/5/20 下午15:39
@Author : kongwiki
@File : redisInit.py
@Email : kongwiki@163.com
"""
import redis
import sys
import os
import datetime
sys.path.append(os.getcwd())
from WeiboCrawler.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT

r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT)
for key in r.scan_iter("weiboSpider*"):
    r.delete(key)
    print('删除成功')

url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime={}&endtime={}&sort=time&page=1"
# 搜索的关键词
keyword = "癌症"
# 搜索的起始日期 微博的创建日期是2009-08-16
date_start = datetime.datetime.strptime("2019-05-10", '%Y-%m-%d')
# 搜索的结束日期
date_end = datetime.datetime.strptime("2019-05-29", '%Y-%m-%d')
time_spread = datetime.timedelta(days=1)
while date_start < date_end:
    next_time = date_start + time_spread
    url = url_format.format(keyword, date_start.strftime("%Y%m%d"), next_time.strftime("%Y%m%d"))
    r.lpush('weiboSpider:start_urls', url)
    date_start = next_time
    print('添加{}成功'.format(url))