# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import datetime
import base64
import json
import redis
import random
import urllib
import requests
import urlparse
from scrapy import Selector
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url
from scrapy import signals
from urlparse import urljoin
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Yysggzygov(scrapy.Spider):
    name = "yysggzygov"  # 岳阳市公共资源交易网
    start_urls = [
        # 'http://ggzy.yueyang.gov.cn/004/004001/004001001/about-gcjs.html PN',  # 工程建设-招标
        # 'http://ggzy.yueyang.gov.cn/004/004001/004001002/about-gcjs.html CN',  # 变更公告
        # 'http://ggzy.yueyang.gov.cn/004/004001/004001003/about-gcjs.html RN',  # 中标公告
        # 'http://ggzy.yueyang.gov.cn/004/004001/004001004/about-gcjs.html RN',  # 其他公告 有废标 有答疑 要处理一下
        # 'http://ggzy.yueyang.gov.cn/004/004002/004002001/about-zfcg.html PN',  # 政府采购-招标公告
        # 'http://ggzy.yueyang.gov.cn/004/004002/004002002/about-zfcg.html CN',  # 变更公告
        # 'http://ggzy.yueyang.gov.cn/004/004002/004002003/about-zfcg.html RN',  # 中标公告
        # 'http://ggzy.yueyang.gov.cn/004/004002/004002004/about-zfcg.html PN',  # 其他公告 杂乱的 要处理
        'http://ggzy.yueyang.gov.cn/004/004003/004003001/about03.html PN',  # 国土资源-出让公告  比较特殊
        # 'http://ggzy.yueyang.gov.cn/004/004003/004003002/about03.html RN',  # 成交公告
        # 'http://ggzy.yueyang.gov.cn/004/004003/004003005/about03.html RN',  # 其他公告
        # 'http://ggzy.yueyang.gov.cn/004/004004/004004001/about03.html PN',  # 产权交易-转让公告
        # 'http://ggzy.yueyang.gov.cn/004/004004/004004002/about03.html RN',  # 成交公告
        # 'http://ggzy.yueyang.gov.cn/004/004005/004005001/about03.html PN',  # 医疗-招标公告
        # 'http://ggzy.yueyang.gov.cn/004/004005/004005002/about03.html CN',  # 变更公告
        # 'http://ggzy.yueyang.gov.cn/004/004005/004005003/about03.html RN',  # 中标公告
        # 'http://ggzy.yueyang.gov.cn/004/004005/004005004/about03.html RN',  # 其他公告 这个全是废标
        # 'http://ggzy.yueyang.gov.cn/004/004006/004006001/about03.html RN',  # 排污权交易-其他公告 有RN 有PN
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":10,}

    def __init__(self,start_url=None,history=True):
        super(Yysggzygov, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//ul/li[@class="news-list-item"]')
        for each in data_list:
            url = each.xpath('./a/@href').extract()[0]
            title = each.xpath('./a/@title').extract()[0]
            pubtime = each.xpath('./span/text()').extract()[0]
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime)
            url = urljoin(response.url, url)
            if pubtime:
                pubtime = pubtime.group()
            if '004003001' in url:
                url_id = url.rpartition('/')[-1].split('.')[0]
                get_url = 'http://ggzy.yueyang.gov.cn:90/TPFrame/tdjyztbmis/pages/hy_toubiaobaoming/DiKuai_Detail'
                get_params = {'GongGaoGuid': url_id}
                get_url += '?{}'.format(urllib.urlencode(get_params))
                print '特殊处理1'
                yield Request(url=get_url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,'pubtime':pubtime,
                                                             "url":url},
                              callback=self.parse_another_item)
            else:
                yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,'pubtime':pubtime},
                              callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath('//li[contains(@class, "page-item")][last()]/a/@href').extract()
            if len(page_rule) > 0:
                total_page = re.search(r'/(\d+).html', page_rule[0]).group(1)
                for i in range(2, int(total_page)+1):
                    final = response.url.rpartition('/')[0] + '/{}.html'.format(i)
                    yield Request(url=final,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},
                                  callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//div[@class="xiangxidate"]/text()').extract()
        title = response.xpath('//div[@class="xiangxiyebiaoti"]/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime[0].replace('/', '-').strip())
            if item['pubtime']:
                item['pubtime'] = item['pubtime'].group().strip() + ' 00:00'
            else:
                item['pubtime'] = response.meta['pubtime'].strip() + ' 00:00'
        else:
            item['pubtime'] = response.meta['pubtime'].strip() + ' 00:00'
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        if u'成交' in item['title'] or u'结果' in item['title'] or u'中标' in item['title'] or \
                u'未入围' in item['title'] or u'失败' in item['title'] or u'废标' in item['title'] or \
                u'流拍' in item['title'] or u'流标' in item['title'] or \
                u'终止' in item['title']:
            item['type'] = 'RN'
        elif u'变更' in item['title'] or u'澄清' in item['title'] or u'答疑' in item['title'] or \
                u'更正' in item['title'] or u'更改' in item['title'] or u'暂停' in item['title']:
            item['type'] = 'CN'
        elif u'招标公' in item['title'] or u'磋商' in item['title'] or u'采购公' in item['title'] or \
                u'出让公告' in item['title'] or u'恢复' in item['title'] or u'单一来源' in item['title'] or \
                u'竞争性谈判' in item['title']:
            item['type'] = 'PN'
        elif u'预告' in item['title']:
            item['type'] = 'PF'
        item["type"] = response.meta["ba_type"]
        item['area'] = u'湖南省岳阳市'
        item['source'] = u'岳阳市公共资源交易网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@class="xiangxiyekuang"]').extract()
        if len(content) > 0:
            item['content'] = content[0]
        else:
            print '{} content 有问题'.format(response.url)
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item['pubtime'], item['title'], response.url
            raise Exception('{} 字段缺失!!! pubtime:{}, title:{}'.format(response.url,item['pubtime'],item['title']))

    def parse_another_item(self, response):
        # 国土资源的出让公告 需要post
        print '特殊处理2'
        post_url = 'http://ggzy.yueyang.gov.cn:90/TPFrame/tdjyztbmis/pages/hy_toubiaobaoming/yydikuaiDetailAction.action'
        url_id = response.meta['url'].rpartition('/')[-1].split('.')[0]
        post_url_params = {'cmd': 'page_Load', 'GongGaoGuid': url_id, 'isCommondto': 'true'}
        post_url = post_url + '?' + urllib.urlencode(post_url_params)
        # formdata = 'commonDto=[{"id":"biaoduanno","bind":"dataBean.biaoduanno","type":"outputtext"},{"id":"guapaifromdate","bind":"dataBeanbd.guapaifromdate","type":"outputtext","format":"yyyy-MM-dd+HH:mm:ss","dataOptions":"{format:\"yyyy-MM-dd+HH:mm:ss\"}"},{"id":"biaoduanname","bind":"dataBean.biaoduanname","type":"outputtext"},{"id":"lblBZJDaoZhangDate","bind":"dataBean2.bzjshoudate","type":"outputtext","format":"yyyy-MM-dd+HH:mm:ss","dataOptions":"{format:\"yyyy-MM-dd+HH:mm:ss\"}"},{"id":"guapaitodate","bind":"dataBeanbd.guapaitodate","type":"outputtext","format":"yyyy-MM-dd+HH:mm:ss","dataOptions":"{format:\"yyyy-MM-dd+HH:mm:ss\"}"},{"id":"biaoduanbelongs","bind":"dataBean2.biaoduanbelongs","type":"outputtext"},{"id":"biaoduanplace","bind":"dataBean2.biaoduanplace","type":"outputtext"},{"id":"tenurearea","bind":"dataBean2.tenurearea","type":"outputtext"},{"id":"landuse","bind":"dataBean2.landuse","type":"outputtext"},{"id":"volumeratio","bind":"dataBean2.volumeratio","type":"outputtext"},{"id":"ziyuancunchu","bind":"dataBean2.ziyuancunchu","type":"outputtext"},{"id":"kuangqumj","bind":"dataBean2.kuangqumj","type":"outputtext"},{"id":"kuangzhong","bind":"dataBean2.kuangzhong","type":"outputtext"},{"id":"caikuangfs","bind":"dataBean2.caikuangfs","type":"outputtext"},{"id":"gongqi","bind":"dataBean2.gongqi","type":"outputtext"},{"id":"StartPrice","bind":"dataBean2.StartPrice","type":"outputtext","format":"#0.0000","dataOptions":"{format:\"#0.0000\"}"},{"id":"bzjmoney","bind":"dataBean2.bzjmoney","type":"outputtext","format":"#0.0000","dataOptions":"{format:\"#0.0000\"}"},{"id":"increaseRate","bind":"dataBean2.increaseRate","type":"outputtext","format":"#0.0000","dataOptions":"{format:\"#0.0000\"}"},{"id":"dingbiaodate","bind":"dataBeanbd.dingbiaodate","type":"outputtext","format":"yyyy-MM-dd+HH:mm:ss","dataOptions":"{format:\"yyyy-MM-dd+HH:mm:ss\"}"},{"id":"zhongbiaoprice","bind":"dataBeanbd.zhongbiaoprice","type":"outputtext","format":"#0.0000","dataOptions":"{format:\"#0.0000\"}"},{"id":"mini-21","bind":"dataBeanbd.Zhongbiaodanweiname","type":"outputtext"},{"id":"otherterms","bind":"dataBean2.otherterms","type":"outputtext"},{"id":"ywscanfilelist1","type":"UserControl","action":"ywscanfileValue","value":""},{"id":"_common_hidden_viewdata","type":"hidden","value":""}]'
        formdata = 'commonDto=%5B%7B%22id%22%3A%22biaoduanno%22%2C%22bind%22%3A%22dataBean.biaoduanno%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22guapaifromdate%22%2C%22bind%22%3A%22dataBeanbd.guapaifromdate%22%2C%22type%22%3A%22outputtext%22%2C%22format%22%3A%22yyyy-MM-dd+HH%3Amm%3Ass%22%2C%22dataOptions%22%3A%22%7Bformat%3A%5C%22yyyy-MM-dd+HH%3Amm%3Ass%5C%22%7D%22%7D%2C%7B%22id%22%3A%22biaoduanname%22%2C%22bind%22%3A%22dataBean.biaoduanname%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22lblBZJDaoZhangDate%22%2C%22bind%22%3A%22dataBean2.bzjshoudate%22%2C%22type%22%3A%22outputtext%22%2C%22format%22%3A%22yyyy-MM-dd+HH%3Amm%3Ass%22%2C%22dataOptions%22%3A%22%7Bformat%3A%5C%22yyyy-MM-dd+HH%3Amm%3Ass%5C%22%7D%22%7D%2C%7B%22id%22%3A%22guapaitodate%22%2C%22bind%22%3A%22dataBeanbd.guapaitodate%22%2C%22type%22%3A%22outputtext%22%2C%22format%22%3A%22yyyy-MM-dd+HH%3Amm%3Ass%22%2C%22dataOptions%22%3A%22%7Bformat%3A%5C%22yyyy-MM-dd+HH%3Amm%3Ass%5C%22%7D%22%7D%2C%7B%22id%22%3A%22biaoduanbelongs%22%2C%22bind%22%3A%22dataBean2.biaoduanbelongs%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22biaoduanplace%22%2C%22bind%22%3A%22dataBean2.biaoduanplace%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22tenurearea%22%2C%22bind%22%3A%22dataBean2.tenurearea%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22landuse%22%2C%22bind%22%3A%22dataBean2.landuse%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22volumeratio%22%2C%22bind%22%3A%22dataBean2.volumeratio%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22ziyuancunchu%22%2C%22bind%22%3A%22dataBean2.ziyuancunchu%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22kuangqumj%22%2C%22bind%22%3A%22dataBean2.kuangqumj%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22kuangzhong%22%2C%22bind%22%3A%22dataBean2.kuangzhong%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22caikuangfs%22%2C%22bind%22%3A%22dataBean2.caikuangfs%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22gongqi%22%2C%22bind%22%3A%22dataBean2.gongqi%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22StartPrice%22%2C%22bind%22%3A%22dataBean2.StartPrice%22%2C%22type%22%3A%22outputtext%22%2C%22format%22%3A%22%230.0000%22%2C%22dataOptions%22%3A%22%7Bformat%3A%5C%22%230.0000%5C%22%7D%22%7D%2C%7B%22id%22%3A%22bzjmoney%22%2C%22bind%22%3A%22dataBean2.bzjmoney%22%2C%22type%22%3A%22outputtext%22%2C%22format%22%3A%22%230.0000%22%2C%22dataOptions%22%3A%22%7Bformat%3A%5C%22%230.0000%5C%22%7D%22%7D%2C%7B%22id%22%3A%22increaseRate%22%2C%22bind%22%3A%22dataBean2.increaseRate%22%2C%22type%22%3A%22outputtext%22%2C%22format%22%3A%22%230.0000%22%2C%22dataOptions%22%3A%22%7Bformat%3A%5C%22%230.0000%5C%22%7D%22%7D%2C%7B%22id%22%3A%22dingbiaodate%22%2C%22bind%22%3A%22dataBeanbd.dingbiaodate%22%2C%22type%22%3A%22outputtext%22%2C%22format%22%3A%22yyyy-MM-dd+HH%3Amm%3Ass%22%2C%22dataOptions%22%3A%22%7Bformat%3A%5C%22yyyy-MM-dd+HH%3Amm%3Ass%5C%22%7D%22%7D%2C%7B%22id%22%3A%22zhongbiaoprice%22%2C%22bind%22%3A%22dataBeanbd.zhongbiaoprice%22%2C%22type%22%3A%22outputtext%22%2C%22format%22%3A%22%230.0000%22%2C%22dataOptions%22%3A%22%7Bformat%3A%5C%22%230.0000%5C%22%7D%22%7D%2C%7B%22id%22%3A%22mini-21%22%2C%22bind%22%3A%22dataBeanbd.Zhongbiaodanweiname%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22otherterms%22%2C%22bind%22%3A%22dataBean2.otherterms%22%2C%22type%22%3A%22outputtext%22%7D%2C%7B%22id%22%3A%22ywscanfilelist1%22%2C%22type%22%3A%22UserControl%22%2C%22action%22%3A%22ywscanfileValue%22%2C%22value%22%3A%22%22%7D%2C%7B%22id%22%3A%22_common_hidden_viewdata%22%2C%22type%22%3A%22hidden%22%2C%22value%22%3A%22%22%7D%5D'
        headers = {
            'Host': 'ggzy.yueyang.gov.cn:90',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': response.url,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Cache-Control': 'max-age=0, no-cache',
            'Pragma': 'no-cache',
        }
        # print post_url
        yield Request(url=post_url,method='post',body=formdata,headers=headers,
                          meta={"ba_type":response.meta["ba_type"],"pubtime":response.meta['pubtime'],"title":response.meta['title'],"response_body":response, "url":response.meta['url']},
                          callback=self.parse_content_item)

    def parse_content_item(self, response):
        item = DataItem()
        print '特殊处理3'
        response_body = response.meta['response_body']
        jsonDict = json.loads(response.body_as_unicode())
        content = jsonDict['controls']
        item['pubtime'] = response.meta['pubtime'].strip() + ' 00:00'
        item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'湖南省岳阳市'
        item['source'] = u'岳阳市公共资源交易网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.meta['url']
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")

        id_dict = {'biaoduanno': u'挂牌编号', 'guapaifromdate': u'挂牌开始时间', 'biaoduanname': u'地块名称',
                   'lblBZJDaoZhangDate': u'保证金缴纳截止时间', 'guapaitodate': u'挂牌截止时间',
                   'biaoduanbelongs': u'土地权属单位', 'biaoduanplace': u'土地位置', 'tenurearea': u'使用权面积',
                   'landuse': u'土地用途', 'volumeratio': u'规划容积率',
                   'ziyuancunchu': u'资源储量', 'kuangqumj': u'设计规模', 'kuangzhong': u'开采矿种',
                   'caikuangfs': u'采矿方法', 'gongqi': u'出让年限', 'StartPrice': u'起始价(万元)',
                   'bzjmoney': u'竞买保证金(万元)', 'increaseRate': u'加价幅度(万元)', 'dingbiaodate': u'成交时间',
                   'zhongbiaoprice': u'成交价(万元)', 'mini-21': '', 'otherterms': u'其他交易条件',
                   'ywscanfilelist1': u'相关附件', '_common_hidden_viewdata': '_common_hidden_viewdata'}
        final_content_list = []
        for each in content:
            if 'data' in each.keys():
                final = '{}: {} {}'.format(id_dict[each['id']], each['data'], each['value'])
            else:
                final = '{}: {}'.format(id_dict[each['id']], each['value'])
            final_content_list.append(final)
        final_content = '; '.join(final_content_list)
        item['content'] = final_content
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item['pubtime'], item['title'], item['url']

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

