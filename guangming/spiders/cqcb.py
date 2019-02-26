#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import re
import sys
import time
import traceback
import urllib
import urlparse
import codecs
import redis
import requests
import scrapy
from scrapy import Selector
from scrapy import signals
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.utils.response import get_base_url
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
# from scrapy.xlib.pydispatch import dispatcher
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Cqcb(scrapy.Spider):
    name = "cqcb"  # 上游新闻
    start_urls = [
        'http://www.cqcb.com/dianjing/ news',  # 电竞
        'http://www.cqcb.com/headline/ news',  # 头条
        'http://www.cqcb.com/highlights/ news',  # 要闻
        'http://www.cqcb.com/hot/ news',  # 重庆
        'http://www.cqcb.com/puguangtai/ news',  # 曝光台
        'http://www.cqcb.com/diaocha/ news',  # 调查
        'http://www.cqcb.com/manxinwen/ news',  # 慢新闻
        'http://www.cqcb.com/shipin/ news',  # 炫视频
        'http://www.cqcb.com/yxzx/video/ news',  # 视频
        'http://www.cqcb.com/personage/ news',  # 大咖
        'http://www.cqcb.com/wealth/ news',  # 财富
        'http://www.cqcb.com/dyh/ news',  # 上游号
        'http://www.cqcb.com/sports/ news',  # 体育
        'http://www.cqcb.com/yxzx/picture/ news',  # 图片
        'http://www.cqcb.com/shuju/ news',  # 数据
        'http://www.cqcb.com/shishi/ news',  # 时事
        'http://www.cqcb.com/yushang/ news',  # 渝商
        'http://www.cqcb.com/yuedu/ news',  # 悦读
        'http://www.cqcb.com/vision/ news',  # 智媒
        'http://www.cqcb.com/zhengquan/ news',  # 证券
        'http://www.cqcb.com/entertainment/ news',  # 娱乐
        'http://www.cqcb.com/science/ news',  # 科普
        'http://www.cqcb.com/xinjiaoyu/ news',  # 教育
        'http://www.cqcb.com/travel/ news',  # 旅游
        'http://www.cqcb.com/qiche/ news',  # 汽车
        'http://www.cqcb.com/housing-market/ news',  # 楼市
        'http://www.cqcb.com/meijia/ news',  # 美家
        'http://www.cqcb.com/shishang/ news',  # 时尚
        'http://www.cqcb.com/wenshi2/ news',  # 文史
        'http://www.cqcb.com/finance/ news',  # 金融
        'http://www.cqcb.com/dongman/ news',  # 游戏
        'http://www.cqcb.com/baoxiao/ news',  # 爆笑
        ### 'http://www.cqcb.com/convenience/ news',  # 便民 太旧
        ### 'http://www.cqcb.com/children/ news',  # 亲子 太旧
        'http://www.cqcb.com/housing-market/ news',  # 楼市
        'http://www.cqcb.com/health/ news',  # 健康
        'http://www.cqcb.com/topics/ news',  # 专题
        ### 'http://e.chinacqsb.com/html newspaper',  # 商报 域名变了
        ### 'http://epaper.cqwb.com.cn/html newspaper',  # 晚报 域名变了
        'http://epaper.cqcb.com/html newspaper',  # 晨报
        'http://rec.cqcb.com/api/getbyclass/1474?udid=861192942597231&appkey=dbb560ca4ba70d4fe7eb573eef737455 news',  # 生活
        'http://rec.cqcb.com/api/getbyclass/1507?udid=861192942597231&appkey=dbb560ca4ba70d4fe7eb573eef737455 news',  # 美食
        'http://source.cqcb.com/shangyouquan/ news',  # 爆料
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None,history=True):
        super(Cqcb, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            if channel['ba_type'] == 'newspaper':
                yield Request(url=url,method='get',meta={'ba_type':channel['ba_type'],'page_parse':True},callback=self.parse_newspaper_link)
            elif 'api' in url:
                 app_headers = {
                     'udid': '861192942597231',
                     'appkey': 'dbb560ca4ba70d4fe7eb573eef737455',
                     'User-Agent': 'com.shangyounews.news/2.0.8 (Linux; Android 5.1.1; Xiaomi Build/LMY48Z); HFWSH /SHANGYOU_UIWebView;version2.0',
                     'Host': 'rec.cqcb.com',
                 }
                 # 'Cookie': 'qnnqureturnurl=deleted; acw_tc=df6f181a15504644466826567e2d28c1754eabe37fc8a90cdf139cb92e; qnnquecookieinforecord=%252525252C537-232151%252525252C643-1443112%2525252C1178-1438775%25252C898-1442545%252C; SERVERID=aef89c288f7c23a3e222408d6cd216c1%7C1550473274%7C1550473274',
                 yield Request(url=url,headers=app_headers,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_app_link)
            else:
                yield Request(url=url,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        url_list = response.xpath('//div[@id="newslist"]//a')
        print response.url, ' 数量: ', len(url_list)
        for info in url_list:
            url = info.xpath('./@href').extract()[0]
            url = urlparse.urljoin(response.url, url)
            title = info.xpath('.//h1/text()').extract()[0]
            if 'cqcb' in url and 'topics' in url and not re.search(r'\d{4,6}-', url):
                # if self.doredis and self.expire_redis.exists(url):
                #    continue
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_topics_link)
            elif 'cqcb' in url and 'h5' not in url and 'vr' not in url and 'live' not in url:
                if 'shangyouquan' in url:
                    url = url.replace('_pc', '')
                    # if self.doredis and self.expire_redis.exists(url):
                    #    continue
                    url_id = re.search(r'/(\d+).html', url).group(1)
                    ajax_url = 'http://source.cqcb.com/api/baoliao_show.php?id={}&r='.format(url_id)
                    yield Request(url=ajax_url,method='get',meta={'ba_type':response.meta['ba_type'], 'url':url, 'title': title},callback=self.parse_preceding_item)
                else:
                    # if self.doredis and self.expire_redis.exists(url):
                    #    continue
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'], 'url':url, 'title': title},callback=self.parse_item)

    def parse_app_link(self, response):
        jsonDict = json.loads(response.body)['newslist']
        url = 'http://www.cqcb.com/'
        for news in jsonDict:
            # newstime = news['newstime']
            title_url = news['titleurl']
            url = urlparse.urljoin(url, title_url)
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_item)

    def parse_newspaper_link(self, response):
        url_list = response.xpath('//div[@class="newslist"]//a')
        print response.url, 'newspaer_link 数量: ', len(url_list)
        for info in url_list:
            url = info.xpath('./@href').extract()[0]
            url = urlparse.urljoin(response.url, url)
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_item)
        if response.meta['page_parse']:
            page_rule = response.xpath('//a/@href').extract()
            for page in page_rule:
                url = urlparse.urljoin(response.url, page)
                if url != response.url:
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},callback=self.parse_newspaper_link)

    def parse_topics_link(self, response):
        url_list = response.xpath('//div[@id="newslist"]//a')
        print response.url, ' 数量: ', len(url_list)
        for info in url_list:
            url = info.xpath('./@href').extract()[0]
            url = urlparse.urljoin(response.url, url)
            if 'topics' in url and not re.search(r'\d{4,6}-', url):
                # if self.doredis and self.expire_redis.exists(url):
                #    continue
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_topics_link)
            elif 'cqcb' in url and 'h5' not in url and 'vr' not in url:
                # if self.doredis and self.expire_redis.exists(url):
                #    continue
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_item)

    def parse_preceding_item(self, response):
        jsonDict = json.loads(response.body)['view']
        content = '<p class="content">{}</p>'.format(jsonDict['content'])
        imgs = jsonDict['images']
        reply = '<div class="report">{}</div>'.format(jsonDict['gfrepeat'])
        title = jsonDict['title']
        image = ''
        for img in imgs:
            image += '<img src="{}">\n'.format(img)
        final_content = content + '\n' + image + '\n' + reply
        yield Request(url=response.meta['url'],method='get',meta={'ba_type':response.meta['ba_type'], 'content': final_content, 'parse_content': True, 'title': title},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'重庆市'
        item['source'] = u"上游新闻"
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url

        medianame1 = response.xpath('//div[@class="post"]/text()').extract()
        medianame2 = response.xpath('//span[@class="label_nr"][1]/text()').extract()
        if len(medianame1) > 0:
            item['medianame'] = re.search(ur'来源[:：]\s?([^)\d]+)', medianame1[0].strip())
            if item['medianame']:
                item['medianame'] = item['medianame'].group(1).replace(' ', '')
                if not item['medianame']:
                    item['medianame'] = u'上游新闻'
            else:
                item['medianame'] = u'上游新闻'
        elif len(medianame2) > 0:
            item['medianame'] = medianame2[0].strip()
        else:
            item['medianame'] = u'上游新闻'

        pubtime = response.xpath('//div[@class="post"]/text()').extract() or \
                  response.xpath('//div[@class="post"]/span[last()]/text()').extract() or \
                  response.xpath('//*[@id="wenbenk"]/div[1]/div/span[4]/text()').extract() or \
                  response.xpath('//*[@id="ScroLeft"]/div[1]/p[3]/span[2]/text()').extract() or \
                  response.xpath('//span[@class="label_nr2"]/text()').extract()
        if re.search(r'\d{4}-\d{2}-\d{2}', response.url) and len(pubtime) == 0:
            pubtime = re.search(r'\d{4}-\d{2}-\d{2}', response.url).group()
            item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d").strftime('%Y-%m-%d %H:%M')
        else:
            final_pubtime1 = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
            final_pubtime2 = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\d{1,2}:\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
            final_pubtime3 = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
            final_pubtime4 = re.search(r'\d{2}-\d{2}\s\d{1,2}:\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
            if final_pubtime1:
                item['pubtime'] = datetime.datetime.strptime(final_pubtime1.group(), "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
            elif final_pubtime2:
                item['pubtime'] = datetime.datetime.strptime(final_pubtime2.group(), "%Y-%m-%d%H:%M").strftime('%Y-%m-%d %H:%M')
            elif final_pubtime3:
                item['pubtime'] = datetime.datetime.strptime(final_pubtime3.group(), "%Y-%m-%d").strftime('%Y-%m-%d %H:%M')
            elif final_pubtime4:
                year_time = re.search(r'(20\d{2})-', response.url).group(1)
                item['pubtime'] = datetime.datetime.strptime('{}-{}'.format(year_time,final_pubtime4.group()), "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')

        title = response.xpath('//div[@class="tile"]/text()').extract() or \
                response.xpath('//h1/text()').extract() or \
                response.xpath('//h3[@id="Title"]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()

        content = response.xpath('//div[@class="content"]').extract() or \
                  response.xpath('//div[@class="article_text"]').extract() or \
                  response.xpath('//div[@class="newsdetatext"]').extract()
        item['content'] = content[0]
        if response.meta.get('parse_content'):
            item['content'] = item['content'].replace('<p class="content"></p>', response.meta['content'])

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {} title:{}, pubtime:{}, {}'.format(item['url'],item['title'], item['pubtime'], item['content'])


