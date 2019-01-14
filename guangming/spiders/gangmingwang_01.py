#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
__author__ = ''
import re
import time
import sys
import scrapy
import json
import redis
import urllib
import requests
import urlparse
from scrapy.http import Request
import traceback
import datetime
# from scrapy import Selector
from scrapy.http import FormRequest
# from scrapy.utils.response import get_base_url
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame

# from bidTest.bidTest.items import DataItem
from ..items import DataItem


reload(sys)
sys.setdefaultencoding('utf-8')


class guangmingwang_news(scrapy.Spider):
    name = "guangmingwang_news"
    start_urls = [
        # 特殊类型还没处理，最后再看
        # 地方频道一大堆
        # "http://difang.gmw.cn/node_29677.htm news",  # 地方要闻
        # "http://difang.gmw.cn/node_29670.htm news",  # 教育
        # "http://difang.gmw.cn/node_24074.htm news",  # 科学
        # "http://difang.gmw.cn/node_24073.htm news",  # 文化
        # "http://difang.gmw.cn/node_24072.htm news",  # 卫生
        # "http://difang.gmw.cn/node_24071.htm news",  # 经济
        # "http://difang.gmw.cn/node_24070.htm news",  # 社会
        # "http://difang.gmw.cn/node_29671.htm news",  # 地方政情
        # ### "http://difang.gmw.cn/node_29675.htm news",  # 地方专题
        # "http://difang.gmw.cn/node_29669.htm news",  # 华夏纵览

        # "http://difang.gmw.cn/hb/node_12827.htm news",  # 湖北要闻
        # "http://difang.gmw.cn/hb/node_21279.htm news", #湖北图片新闻
        # "http://difang.gmw.cn/roll2/node_10045083.htm news", # 湖北当地新闻
        # "http://difang.gmw.cn/ah/node_12871.htm news", # 安徽要闻
        # "http://difang.gmw.cn/ah/node_21276.htm news", # 安徽图片新闻
        # "http://difang.gmw.cn/roll2/node_10045082.htm news", # 安徽当地新闻
        # "http://difang.gmw.cn/roll2/node_10045087.htm news", # 北京地方频道
        "http://difang.gmw.cn/bj/node_21282.htm news", # 北京图片新闻
        # "http://difang.gmw.cn/bj/node_12792.htm news", # 北京要闻
        # "http://difang.gmw.cn/qd/node_13146.htm news", # 青岛要闻
        # "http://difang.gmw.cn/cq/node_12898.htm news",  # 重庆要闻
        # "http://difang.gmw.cn/cq/node_12897.htm news",  # 重庆时政
        # "http://difang.gmw.cn/cq/node_12896.htm news",  # 重庆教育
        # "http://difang.gmw.cn/cq/node_12890.htm news",  # 重庆人物
        # "http://difang.gmw.cn/cq/node_12895.htm news",  # 重庆科技
        # "http://difang.gmw.cn/cq/node_12894.htm news",  # 重庆经济
        # "http://difang.gmw.cn/cq/node_12891.htm news",  # 重庆旅游
        # "http://difang.gmw.cn/cq/node_12893.htm news",  # 重庆文化
        # "http://difang.gmw.cn/cq/node_12892.htm news",  # 重庆社会

        # 除了重庆的地方子频道如下：
        # "http://difang.gmw.cn/hb/node_12827.htm news",
        # "http://difang.gmw.cn/hb/node_21279.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045083.htm news",
        # "http://difang.gmw.cn/ah/node_12871.htm news",
        # "http://difang.gmw.cn/ah/node_21276.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045082.htm news",
        # "http://difang.gmw.cn/bj/node_12792.htm news",
        # "http://difang.gmw.cn/bj/node_21282.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045087.htm news",
        # "http://difang.gmw.cn/dl/node_13119.htm news",
        # "http://difang.gmw.cn/dl/node_21278.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045105.htm news",
        # "http://difang.gmw.cn/fj/node_12907.htm news",
        # "http://difang.gmw.cn/fj/node_21312.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045085.htm news",
        # "http://difang.gmw.cn/gd/node_12934.htm news",
        # "http://difang.gmw.cn/gd/node_21330.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045101.htm news",
        # "http://difang.gmw.cn/gs/node_12916.htm news",
        # "http://difang.gmw.cn/gs/node_21314.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045094.htm news",
        # "http://difang.gmw.cn/gx/node_12944.htm news",
        # "http://difang.gmw.cn/gx/node_21313.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045097.htm news",
        # "http://difang.gmw.cn/gz/node_12925.htm news",
        # "http://difang.gmw.cn/gz/node_21315.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045109.htm news",
        # "http://difang.gmw.cn/ha/node_12962.htm news",
        # "http://difang.gmw.cn/ha/node_21316.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045111.htm news",
        # "http://difang.gmw.cn/he/node_12853.htm news",
        # "http://difang.gmw.cn/he/node_21280.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045091.htm news",
        # "http://difang.gmw.cn/hi/node_13056.htm news",
        # "http://difang.gmw.cn/hi/node_21299.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045110.htm news",
        # "http://difang.gmw.cn/hlj/node_12836.htm news",
        # "http://difang.gmw.cn/hlj/node_21281.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045114.htm news",
        # "http://difang.gmw.cn/hn/node_12971.htm news",
        # "http://difang.gmw.cn/hn/node_21317.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045100.htm news",
        # "http://difang.gmw.cn/jl/node_12998.htm news",
        # "http://difang.gmw.cn/jl/node_21292.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045086.htm news",
        # "http://difang.gmw.cn/js/node_12980.htm news",
        # "http://difang.gmw.cn/js/node_21319.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045113.htm news",
        # "http://difang.gmw.cn/jx/node_12953.htm news",
        # "http://difang.gmw.cn/jx/node_21318.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045099.htm news",
        # "http://difang.gmw.cn/ln/node_13020.htm news",
        # "http://difang.gmw.cn/ln/node_21294.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045084.htm news",
        # "http://difang.gmw.cn/nb/node_13137.htm news",
        # "http://difang.gmw.cn/nb/node_21283.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045102.htm news",
        # "http://difang.gmw.cn/nx/node_13029.htm news",
        # "http://difang.gmw.cn/nx/node_21295.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045095.htm news",
        # "http://difang.gmw.cn/qd/node_13146.htm news",
        # "http://difang.gmw.cn/qd/node_21284.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045122.htm news",
        # "http://difang.gmw.cn/qh/node_26918.htm news",
        # "http://difang.gmw.cn/qh/node_26917.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045096.htm news",
        # "http://difang.gmw.cn/sc/node_13030.htm news",
        # "http://difang.gmw.cn/sc/node_21296.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045098.htm news",
        # "http://difang.gmw.cn/sd/node_12862.htm news",
        # "http://difang.gmw.cn/sd/node_21288.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045112.htm news",
        # "http://difang.gmw.cn/sh/node_12880.htm news",
        # "http://difang.gmw.cn/sh/node_21377.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045093.htm news",
        # "http://difang.gmw.cn/sn/node_20914.htm news",
        # "http://difang.gmw.cn/sn/node_21286.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045107.htm news",
        # "http://difang.gmw.cn/sx/node_12818.htm news",
        # "http://difang.gmw.cn/sx/node_21285.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045090.htm news",
        # "http://difang.gmw.cn/sz/node_13083.htm news",
        # "http://difang.gmw.cn/sz/node_21550.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045103.htm news",
        # "http://difang.gmw.cn/tj/node_12889.htm news",
        # "http://difang.gmw.cn/tj/node_21289.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045088.htm news",
        # "http://difang.gmw.cn/xiamen/node_13128.htm news",
        # "http://difang.gmw.cn/xiamen/node_21290.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045104.htm news",
        # "http://difang.gmw.cn/nmg/node_13007.htm news",
        # "http://difang.gmw.cn/nmg/node_21293.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045106.htm news",
        # "http://difang.gmw.cn/yn/node_13047.htm news",
        # "http://difang.gmw.cn/yn/node_21297.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045108.htm news",
        # "http://difang.gmw.cn/zj/node_12989.htm news",
        # "http://difang.gmw.cn/zj/node_21291.htm news",
        # "http://difang.gmw.cn/node_29669.htm news",
        # "http://difang.gmw.cn/roll2/node_10045089.htm news",
        #
        "http://topics.gmw.cn/node_118186.htm news", # 乐跑要闻
        #
        # "https://news.gmw.cn/node_4108.htm news", # 光明日报
        # "http://www.gmw.cn/index/node_4322.htm news", # 光明时评

        # "https://news.gmw.cn/node_115159.htm news", # E视线-观察
        # "https://news.gmw.cn/node_115160.htm news", # E视线-会客厅
        # "https://news.gmw.cn/node_115156.htm news", # E视线-融媒多一点
        # "https://news.gmw.cn/node_115158.htm news", # E视线-网事风云

        # "http://news.gmw.cn/node_4108.htm news", #光明推荐
        # "http://news.gmw.cn/node_46432.htm news", #光明网一周重点访谈要目   存在视频
        # ## "http://news.gmw.cn/node_65373.htm news" ,#读图解意                         舍弃 太旧了 2016年
        # ## "http://topics.gmw.cn/node_98645.htm news",#新媒体策划 这个频道比较特殊 稍后再研究
        # "http://news.gmw.cn/node_4705.htm news",#新闻热评
        # "http://news.gmw.cn/node_4703.htm news",#世相漫说
        # "http://world.gmw.cn/node_8858.htm news" ,#滚动大图
        #
        # ## 这些频道可能要降低一下爬取速度
        # "http://world.gmw.cn/node_24178.htm news" ,#图片新闻
        # "http://world.gmw.cn/node_4660.htm news" ,#大千世界
        # "http://world.gmw.cn/node_9663.htm news" ,#滚动播报
        #
        # ## "http://politics.gmw.cn/node_9833.htm news" ,#时政专题      #特殊类型

        # "http://politics.gmw.cn/node_9832.htm news" ,#领导人活动集   #特殊类型
        # "http://politics.gmw.cn/node_9826.htm news" ,#人事任免
        # "http://politics.gmw.cn/node_10495.htm news" ,#滚动播报
        # "http://politics.gmw.cn/node_9840.htm news" ,#国内要闻
        # "http://politics.gmw.cn/node_9843.htm news" ,#滚动图片
        # "http://politics.gmw.cn/node_6405.htm news" ,#新闻图片
        # "http://politics.gmw.cn/node_9831.htm news" ,#政务信息
        # "http://politics.gmw.cn/node_9830.htm news" ,#部委声音
        # "http://politics.gmw.cn/node_9847.htm news" ,#人大·政协
        # "http://politics.gmw.cn/node_9828.htm news" ,#发布·解读
        # "http://politics.gmw.cn/node_9822.htm news" ,#纪实
        # "http://politics.gmw.cn/node_9844.htm news" ,#要闻
        # "http://politics.gmw.cn/node_9836.htm news" ,#观察
        # "http://politics.gmw.cn/node_9838.htm news" ,#港澳热点
        # "http://politics.gmw.cn/node_9837.htm news" ,#台海直播
        # "http://politics.gmw.cn/node_9835.htm news" ,#人物楷模
        # "http://politics.gmw.cn/node_9842.htm news" ,#视频

        # "http://world.gmw.cn/node_4661.htm news" ,#国际要闻
        # "http://world.gmw.cn/node_4485.htm news" ,#国际观察
        # "http://world.gmw.cn/node_4696.htm news" ,#外媒聚焦
        # "http://world.gmw.cn/node_24176.htm news" ,#世界博览
        # "http://world.gmw.cn/node_24177.htm news" ,#光明推荐
        # "http://mil.gmw.cn/node_8986.htm news" ,#军事要闻
        # "http://mil.gmw.cn/node_8988.htm news" ,#滚动大图
        # "http://mil.gmw.cn/node_8981.htm news" ,#军事视点
        # "http://mil.gmw.cn/node_8984.htm news" ,#中国军情
        # "http://mil.gmw.cn/node_11179.htm news" ,#台海聚焦
        # "http://mil.gmw.cn/node_11178.htm news" ,#军营文化
        # "http://mil.gmw.cn/node_11176.htm news" ,#军旅人生
        # "http://mil.gmw.cn/node_8982.htm news" ,#国际军情
        # "http://mil.gmw.cn/node_11177.htm news" ,#邻邦扫描
        # "http://mil.gmw.cn/node_8977.htm news" ,#军情集锦
        # "http://mil.gmw.cn/node_8978.htm news" ,#武器装备
        # "http://mil.gmw.cn/node_8979.htm news" ,#军史揭秘
        # "http://mil.gmw.cn/node_8972.htm news" ,#军事图库
        # "http://mil.gmw.cn/node_11175.htm news" ,#视频新闻
        # ## "http://topics.gmw.cn/node_4979.htm news" ,#军事专题   特殊类型
        # "http://mil.gmw.cn/node_9664.htm news" ,#滚动播报
        # "http://legal.gmw.cn/node_9021.htm news" ,#焦点大图
        # "http://legal.gmw.cn/node_9020.htm news" ,#法治要闻
        # "http://legal.gmw.cn/node_9015.htm news" ,#法眼观察
        # "http://legal.gmw.cn/node_9668.htm news" ,#滚动播报
        # "http://legal.gmw.cn/node_9018.htm news" ,#反腐倡廉
        # "http://legal.gmw.cn/node_9017.htm news" ,#案件快递
        # "http://legal.gmw.cn/node_9014.htm news" ,#法治人物
        # "http://legal.gmw.cn/node_12330.htm news" ,#社会万象
        # "http://legal.gmw.cn/node_12328.htm news" ,#平安中国
        # "http://legal.gmw.cn/node_12332.htm news" ,#图片新闻
        # ## "http://legal.gmw.cn/node_22489.htm news" ,#法治专题   #特殊类型
        # "http://sports.gmw.cn/node_9642.htm news" ,#热点荟萃
        # "http://sports.gmw.cn/node_9641.htm news" ,#要点新闻
        # "http://sports.gmw.cn/node_9644.htm news" ,#滚动大图
        # "http://sports.gmw.cn/node_10674.htm news" ,#滚动播报
        # "http://sports.gmw.cn/node_9631.htm news" ,#风云人物
        # ##"http://sports.gmw.cn/node_9640.htm news" ,#热点·专题  #特殊类型
        # "http://sports.gmw.cn/node_9632.htm news" ,#视频
        # "http://sports.gmw.cn/node_9636.htm news" ,#篮球
        # "http://sports.gmw.cn/node_9638.htm news" ,#足球
        # "http://sports.gmw.cn/node_9633.htm news" ,#综合体育
        # "http://sports.gmw.cn/node_9629.htm news" ,#光明机器人
        # "http://photo.gmw.cn/node_10890.htm news" ,#焦点
        # "http://photo.gmw.cn/node_10444.htm news" ,#环球
        # "http://photo.gmw.cn/node_21034.htm news" ,#社会
        # "http://photo.gmw.cn/node_10442.htm news" ,#最新图片
        # "http://photo.gmw.cn/node_10443.htm news" ,#美图
        # "http://photo.gmw.cn/node_79388.htm news" ,#光明图刊
        # "http://photo.gmw.cn/node_10990.htm news" ,#奇闻趣图
        # "http://photo.gmw.cn/node_109914.htm news" ,#漫画
        #
        # ## "http://topics.gmw.cn/node_4296.htm news" ,#时政专题   #特殊类型
        # ## "http://topics.gmw.cn/node_4511.htm news" ,#国内专题   #特殊类型
        # ## "http://topics.gmw.cn/node_4870.htm news" ,#国际专题  #特殊类型
        # ## "http://topics.gmw.cn/node_4670.htm news" ,#教育专题
        # ## "http://topics.gmw.cn/node_4782.htm news" ,#科技专题
        # ## "http://topics.gmw.cn/node_4920.htm news" ,#文化专题
        # ## "http://topics.gmw.cn/node_6047.htm news" ,#卫生专题
        # ## "http://topics.gmw.cn/node_4979.htm news" ,#军事专题
        # ## "http://topics.gmw.cn/node_5578.htm news" ,#人物专题
        # ## "http://topics.gmw.cn/node_5360.htm news" ,#经济专题
        # ## "http://topics.gmw.cn/node_4825.htm news" ,#体育专题
        # ## "http://economy.gmw.cn/node_8970.htm news" ,#专题  #特殊类型
        # ## "http://travel.gmw.cn/node_39033.htm news" ,#专题  #特殊类型
        # ##"http://travel.gmw.cn/node_98574.htm news" ,#VR看中国   #特殊类型
        # ###"http://shipin.gmw.cn/node_35781.htm news" ,#专题   #特殊类型
        #
        # "http://economy.gmw.cn/node_12470.htm news" ,#焦点
        # "http://economy.gmw.cn/node_8969.htm news" ,#滚动大图
        # "http://economy.gmw.cn/node_8971.htm news" ,#经济要闻
        # "http://economy.gmw.cn/node_59269.htm news" ,#光明独家
        # "http://economy.gmw.cn/node_21787.htm news" ,#产经
        # "http://economy.gmw.cn/node_12466.htm news" ,#民生热点
        # "http://economy.gmw.cn/node_8992.htm news" ,#人物
        # "http://economy.gmw.cn/node_9141.htm news" ,#财经眼
        # "http://economy.gmw.cn/node_12468.htm news" ,#经营快讯
        # ### "http://economy.gmw.cn/newspaper/ news" ,#滚动读报 404 可能是被舍弃了
        # "http://finance.gmw.cn/node_42533.htm news" ,#滚动图
        # "http://finance.gmw.cn/node_42534.htm news" ,#今日头版
        # ##"http://finance.gmw.cn/node_42535.htm news" ,#专题    #特殊类型 #太旧了　舍弃
        # "http://finance.gmw.cn/node_42539.htm news" ,#银行
        # "http://finance.gmw.cn/node_42538.htm news" ,#证券
        # "http://finance.gmw.cn/node_42551.htm news" ,#投资/理财
        # "http://finance.gmw.cn/node_42554.htm news" ,#基金
        # "http://finance.gmw.cn/node_42555.htm news" ,#保险
        # "http://finance.gmw.cn/node_70075.htm news" ,#滚动读报
        # "http://travel.gmw.cn/node_9167.htm news" ,#焦点图
        # "http://travel.gmw.cn/node_21604.htm news" ,#今日头条
        # "http://travel.gmw.cn/node_9126.htm news" ,#国内游
        # "http://travel.gmw.cn/node_9130.htm news" ,#国际游
        # "http://travel.gmw.cn/node_23658.htm news" ,#行业动态
        # "http://travel.gmw.cn/node_23732.htm news" ,#大千世界
        # "http://travel.gmw.cn/node_9123.htm news" ,#曝光台
        # "http://travel.gmw.cn/node_39035.htm news" ,#滚动读报
        # "http://life.gmw.cn/node_9268.htm news" ,#今日关注
        # "http://life.gmw.cn/node_9265.htm news" ,#衣
        # "http://life.gmw.cn/node_9252.htm news" ,#食
        # "http://life.gmw.cn/node_9251.htm news" ,#住
        # "http://life.gmw.cn/node_9261.htm news" ,#行
        # "http://shipin.gmw.cn/node_82718.htm news" ,#食品安全大咖谈
        # "http://shipin.gmw.cn/node_82717.htm news" ,#吃货公开课
        # "http://shipin.gmw.cn/node_36162.htm news" ,#焦点
        # "http://shipin.gmw.cn/node_35758.htm news" ,#食品安全“沃”知道
        # "http://shipin.gmw.cn/node_35759.htm news" ,#今日头条
        # "http://shipin.gmw.cn/node_35757.htm news" ,#曝光台
        # "http://shipin.gmw.cn/node_35779.htm news" ,#光明述评
        # "http://shipin.gmw.cn/node_35755.htm news" ,#行业资讯
        # "http://shipin.gmw.cn/node_35753.htm news" ,#秀色可餐
        # "http://shipin.gmw.cn/node_36082.htm news" ,#滚动播报
        # "http://shipin.gmw.cn/node_35753.htm news" ,#权威发声
        # "http://shipin.gmw.cn/node_35783.htm news" ,#专家视角
        # "http://shipin.gmw.cn/node_35780.htm news" ,#光明独家
        # "http://culture.gmw.cn/node_10570.htm news" ,#文化要闻
        # "http://culture.gmw.cn/node_10572.htm news" ,#光明文化
        # "http://culture.gmw.cn/node_4369.htm news" ,#文化观察
        # ##"http://culture.gmw.cn/node_10561.htm news" ,#文化专题  #特殊类型
        # "http://culture.gmw.cn/node_10559.htm news" ,#非物质文化遗产
        # "http://culture.gmw.cn/node_10565.htm news" ,#文化产业
        # "http://culture.gmw.cn/node_10575.htm news" ,#视觉大观
        # "http://culture.gmw.cn/node_10250.htm news" ,#艺术
        # "http://culture.gmw.cn/node_11507.htm news" ,#人文百科
        # "http://e.gmw.cn/node_7511.htm news" ,#要闻
        # "http://e.gmw.cn/node_8758.htm news" ,#明星
        # "http://e.gmw.cn/node_8756.htm news" ,#影视电影动态
        # "http://e.gmw.cn/node_7512.htm news" ,#光明V影评
        # "http://e.gmw.cn/node_10563.htm news" ,#影视综艺看点
        # "http://e.gmw.cn/node_24942.htm news" ,#演出资讯
        # "http://e.gmw.cn/node_8763.htm news" ,#音乐资讯
        #
        # ##"http://e.gmw.cn/node_10045.htm news" ,#影视独家策划  #特殊类型
        # "http://reader.gmw.cn/node_9139.htm news" ,#书业要闻
        # "http://reader.gmw.cn/node_5547.htm news" ,#资讯
        # "http://reader.gmw.cn/node_4244.htm news" ,#阅读
        # "http://reader.gmw.cn/node_12024.htm news" ,#新书
        # "http://reader.gmw.cn/node_4252.htm news" ,#光明日报
        # "http://reader.gmw.cn/node_9138.htm news" ,#书评
        # "http://reader.gmw.cn/node_8636.htm news" ,#悦读会
        # ##"http://reader.gmw.cn/node_4300.htm news" ,#图书专题   #特殊类型 #废弃
        # "http://reader.gmw.cn/node_4256.htm news" ,#读图
        # "http://shuhua.gmw.cn/node_10673.htm news" ,#热点
        # "http://shuhua.gmw.cn/node_11584.htm news" ,#展讯
        # ##"http://reader.gmw.cn/node_11586.htm news" ,#收藏  #已经废弃了
        # ##"http://reader.gmw.cn/node_11585.htm news" ,#轶闻  #已经废弃了
        # ##"http://reader.gmw.cn/node_11592.htm news" ,#艺评  #已经废弃了
        # ### "http://reader.gmw.cn/node_9011.htm news" ,#拍卖  #已经废弃了
        # ### "http://reader.gmw.cn/node_11595.htm news" ,#视觉秀  #已经废弃了
        # ## "http://reader.gmw.cn/node_9661.htm news" ,#艺术▪人物  #已经废弃了
        # ## "http://reader.gmw.cn/node_115738.htm news" ,#视频▪访谈  #已经废弃了
        # "http://tech.gmw.cn/node_4360.htm news" ,#评论+
        # "http://tech.gmw.cn/node_5557.htm news" ,#科博会
        # "http://tech.gmw.cn/node_10609.htm news" ,#网事
        # "http://tech.gmw.cn/node_4359.htm news" ,#赛先生
        # "http://tech.gmw.cn/node_10617.htm news" ,#创业者说
        # "http://tech.gmw.cn/node_4394.htm news" ,#言商
        # "http://tech.gmw.cn/node_10606.htm news" ,#知了
        # "http://tech.gmw.cn/node_5555.htm news" ,#探索者
        #
        # ##"http://tech.gmw.cn/topics_73960.htm news" ,#中国数字科技馆  #特殊结构
        # ##"http://tech.gmw.cn/iscience/ news" ,#i科学 #特殊结构
        # ##"http://tech.gmw.cn/scientist/index.htm news" ,#科技名家风采录  #特殊结构
        # ##"http://tech.gmw.cn/mil/ news" ,#军事科技前沿  #特殊结构
        # "http://tech.gmw.cn/node_9671.htm news" ,#滚动新闻
        # "http://kepu.gmw.cn/node_86782.htm news" ,#科普头条
        # "http://kepu.gmw.cn/node_86783.htm news" ,#光明微科普
        # "http://kepu.gmw.cn/node_86784.htm news" ,#唠科
        # "http://kepu.gmw.cn/node_86786.htm news" ,#图个明白
        # "http://kepu.gmw.cn/node_86790.htm news" ,#食品健康
        # "http://kepu.gmw.cn/node_86791.htm news" ,#农业军事
        # "http://kepu.gmw.cn/node_86792.htm news" ,#天文地理
        # "http://kepu.gmw.cn/node_86787.htm news" ,#科学人
        # "http://kepu.gmw.cn/node_86785.htm news" ,#生活一点通
        # "http://kepu.gmw.cn/node_87638.htm news" ,#知识分子
        # "http://kepu.gmw.cn/node_86788.htm news" ,#科普影视
        # "http://kepu.gmw.cn/node_86789.htm news" ,#科普阅读
        # "http://kepu.gmw.cn/node_87685.htm news" ,#滚动新闻
        # "http://www.gmw.cn/ny/node_22814.htm news" ,#能源要闻
        # "http://www.gmw.cn/ny/node_22809.htm news" ,#能源财经
        # "http://www.gmw.cn/ny/node_23440.htm news" ,#新能源
        # "http://www.gmw.cn/ny/node_23450.htm news" ,#生态环保
        # ## "http://www.gmw.cn/ny/node_23446.htm news" ,#能直播   #这个居然是直播间
        # "http://www.gmw.cn/ny/node_22807.htm news" ,#能源人物
        # "http://www.gmw.cn/ny/node_22808.htm news" ,#企业观察
        # "http://www.gmw.cn/ny/node_23434.htm news" ,#图说能源
        # "http://www.gmw.cn/ny/node_22806.htm news" ,#滚动新闻
        # "http://tech.gmw.cn/jd/node_39857.htm news" ,#家电要闻
        # "http://tech.gmw.cn/jd/node_39858.htm news" ,#HOME见
        # "http://tech.gmw.cn/jd/node_39856.htm news" ,#家电人物
        # "http://tech.gmw.cn/jd/node_43398.htm news" ,#产品资讯
        # "http://tech.gmw.cn/jd/node_39855.htm news" ,#行业+
        # "http://tech.gmw.cn/jd/node_40051.htm news" ,#滚动新闻
        # "http://it.gmw.cn/node_6060.htm news" ,#互联网
        # "http://it.gmw.cn/node_29401.htm news" ,#移动互联网
        # "http://it.gmw.cn/node_29400.htm news" ,#电信
        # "http://it.gmw.cn/node_5972.htm news" ,#业界|3C
        # "http://it.gmw.cn/node_29411.htm news" ,#IT时评
        # "http://it.gmw.cn/node_29413.htm news" ,#原创
        # "http://it.gmw.cn/node_4487.htm news" ,#产业|公司
        # "http://it.gmw.cn/node_29396.htm news" ,#网络|安全
        # "http://it.gmw.cn/node_29390.htm news" ,#手机
        # "http://it.gmw.cn/node_29395.htm news" ,#曝光台
        # ##"http://it.gmw.cn/node_29408.htm news" ,#专题     #特殊结构
        # "http://it.gmw.cn/node_29394.htm news" ,#新品评测
        # "http://it.gmw.cn/node_6061.htm news" ,#滚动新闻
        # "http://theory.gmw.cn/node_10133.htm news" ,#理论首发
        # "http://theory.gmw.cn/node_4332.htm news" ,#理论热点
        # "http://theory.gmw.cn/node_10129.htm news" ,#理论讲堂
        # "http://theory.gmw.cn/node_6088.htm news" ,#会议快讯
        # "http://theory.gmw.cn/node_6092.htm news" ,#深化改革
        # "http://theory.gmw.cn/node_10141.htm news" ,#教育公平
        # ###"http://theory.gmw.cn/node_10128.htm news" ,#理论专题   #特殊结构
        # "http://theory.gmw.cn/node_10148.htm news" ,#新著评论
        # "http://theory.gmw.cn/node_10122.htm news" ,#主编推荐
        # "http://theory.gmw.cn/node_10145.htm news" ,#经济生态
        # "http://theory.gmw.cn/node_10149.htm news" ,#文化科技
        # "http://theory.gmw.cn/node_10142.htm news" ,#低碳发展
        # "http://wenyi.gmw.cn/node_84179.htm news" ,#文艺观察
        # "http://wenyi.gmw.cn/node_84178.htm news" ,#看客
        # "http://wenyi.gmw.cn/node_84177.htm news" ,#听说
        # "http://wenyi.gmw.cn/node_84176.htm news" ,#书虫
        # "http://wenyi.gmw.cn/node_84175.htm news" ,#玩艺
        #
        # ## "http://wenyi.gmw.cn/node_84174.htm news" ,#大家   #特殊结构
        # ##"http://theory.gmw.cn/node_4331.htm news" ,#理论头条  #已经废弃
        # "http://wenyi.gmw.cn/node_84173.htm news" ,#线下沙龙
        # ## "http://www.gmw.cn/sixiang/node_22899.htm news" ,#重磅推荐  #已经废弃
        # ## "http://www.gmw.cn/sixiang/node_22890.htm news" ,#国是论衡  #已经废弃
        # ## "http://www.gmw.cn/sixiang/node_22896.htm news" ,#学习与实践  #已经废弃
        # ## "http://www.gmw.cn/sixiang/node_22884.htm news" ,#热点面对面  #已经废弃
        # ## "http://www.gmw.cn/sixiang/node_22893.htm news" ,#干部讲堂  #已经废弃
        # ## "http://www.gmw.cn/sixiang/node_22900.htm news" ,#政策解读  #已经废弃
        # ## "http://www.gmw.cn/sixiang/node_22892.htm news" ,#华夏文明  #已经废弃
        # ## "http://www.gmw.cn/sixiang/node_22891.htm news" ,#域外采风  #已经废弃
        # ## "http://www.gmw.cn/sixiang/node_22882.htm news" ,#热点专题  #已经废弃
        # ## "http://www.gmw.cn/sixiang/node_22883.htm news" ,#最新思想书目  #已经废弃
        # "http://dangjian.gmw.cn/node_11941.htm news" ,#党建要闻
        # "http://dangjian.gmw.cn/node_11940.htm news" ,#党建动态
        # "http://dangjian.gmw.cn/node_11938.htm news" ,#党建专家
        # "http://dangjian.gmw.cn/node_11939.htm news" ,#党员风采
        # "http://dangjian.gmw.cn/node_11937.htm news" ,#党建理论
        # ### "http://dangjian.gmw.cn/node_11935.htm news" ,#党建专题   #特殊结构
        # "http://dangjian.gmw.cn/node_11928.htm news" ,#党建纵横
        # "http://dangjian.gmw.cn/node_11925.htm news" ,#高校党建
        # "http://dangjian.gmw.cn/node_11936.htm news" ,#基层党建
        # "http://dangjian.gmw.cn/node_22417.htm news" ,#企业党建
        # "http://dangjian.gmw.cn/node_11933.htm news" ,#组织建设
        # "http://dangjian.gmw.cn/node_11930.htm news" ,#反腐倡廉
        # "http://dangjian.gmw.cn/node_11929.htm news" ,#思政工作
        # "http://dangjian.gmw.cn/node_11927.htm news" ,#机关党建
        # "http://dangjian.gmw.cn/node_11924.htm news" ,#党建论坛
        # "http://dangjian.gmw.cn/node_11922.htm news" ,#学习园地
        # "http://dangjian.gmw.cn/node_11934.htm news" ,#思想建设
        # "http://dangjian.gmw.cn/node_11932.htm news" ,#军队党建
        # "http://dangjian.gmw.cn/node_11931.htm news" ,#制度建设
        # "http://dangjian.gmw.cn/node_9823.htm news" ,#党报解读
        # "http://dangjian.gmw.cn/node_9825.htm news" ,#廉政报道
        # "http://dangjian.gmw.cn/node_11923.htm news" ,#党建文献
        # "http://dangjian.gmw.cn/node_10207.htm news" ,#党情博览
        # "http://dangjian.gmw.cn/node_10206.htm news" ,#文摘
        # "http://dangjian.gmw.cn/node_10208.htm news" ,#知识
        # "http://www.gmw.cn/xueshu/node_23642.htm news" ,#学术要闻 已废弃
        # "http://www.gmw.cn/xueshu/node_23641.htm news" ,#学界热议 已废弃
        # "http://www.gmw.cn/xueshu/node_23640.htm news" ,#学术讲堂 已废弃
        # "http://www.gmw.cn/xueshu/node_23639.htm news" ,#学术争鸣
        # "http://www.gmw.cn/xueshu/node_23638.htm news" ,#学术会议
        # "http://www.gmw.cn/xueshu/node_23637.htm news" ,#学科建设 废弃
        # "http://www.gmw.cn/xueshu/node_23636.htm news" ,#学术机构巡礼 废弃
        # "http://www.gmw.cn/xueshu/node_23635.htm news" ,#学术打假
        # "http://www.gmw.cn/xueshu/node_23634.htm news" ,#学刊荐文 废弃
        # "http://www.gmw.cn/xueshu/node_23633.htm news" ,#学人风采
        # "http://www.gmw.cn/xueshu/node_23632.htm news" ,#学术文摘 废弃
        # "http://www.gmw.cn/xueshu/node_23631.htm news" ,#图书推荐
        # ##"http://www.gmw.cn/xueshu/node_23630.htm news" ,#光明网学术论文库  #已经废弃
        # ##"http://www.gmw.cn/xueshu/node_23627.htm news" ,#光明日报学术版  #详细页废弃
        # ##"http://www.gmw.cn/xueshu/node_23626.htm news" ,#学术机构  #无用 特殊结构
        # "http://www.gmw.cn/xueshu/node_23625.htm news" ,#学术网站  #无用
        # ### "http://123.gmw.cn/ news" ,#学术导航   #舍弃

        # ###"http://view.gmw.cn/ news" ,#光明网评论员  #舍弃 已转向另一个新频道
        # "http://guancha.gmw.cn/node_11273.htm news", # 光明评论员 比较特殊
        # "http://guancha.gmw.cn/node_12014.htm news", # 漫说图解

        # "http://guancha.gmw.cn/node_40479.htm news", # 光明网-专栏 就是没有来源的
        # "http://guancha.gmw.cn/node_26275.htm news" ,#光明观察．原创
        # "http://guancha.gmw.cn/node_10056.htm news" ,#今日推荐
        # "http://guancha.gmw.cn/node_5992.htm news" ,#光明时评
        # "http://guancha.gmw.cn/node_11104.htm news" ,#犀论榜
        # "http://guancha.gmw.cn/node_26276.htm news" ,#媒体观点撷英
        # "http://guancha.gmw.cn/node_26274.htm news" ,#光明言论
        # "http://guancha.gmw.cn/node_7292.htm news" ,#百家争鸣
        # ## "http://guancha.gmw.cn/node_36652.htm news" ,#时评专题 专题类 特殊结构
        # "http://guancha.gmw.cn/node_11097.htm news" ,#漫画天下
        # "http://guancha.gmw.cn/node_11098.htm news" ,#编读互动
        # "http://guancha.gmw.cn/node_11096.htm news" ,#光明日报·观点 废弃

        # "http://history.gmw.cn/node_5613.htm news",#轶闻秘史
        # "http://history.gmw.cn/node_38754.htm news",#古今中国
        # "http://history.gmw.cn/node_33005.htm news",#历史映像
        # "http://history.gmw.cn/node_5990.htm news",#历史映像
        # "http://history.gmw.cn/node_4323.htm news",#军史探秘
        # "http://history.gmw.cn/node_4324.htm news",#焦点图
        # "http://history.gmw.cn/node_4427.htm news",#历史人物
        # "http://history.gmw.cn/node_4426.htm news",#口述•迷云
        # ##"http://history.gmw.cn/node_5613.htm news",#轶闻秘史   #这条重复了
        # "http://history.gmw.cn/node_5615.htm news",#考古•发现
        # "http://history.gmw.cn/node_4348.htm news",#环球风云
        # ##"http://history.gmw.cn/node_5613.htm news",#轶闻秘史  #这条还是重复了
        # ##"http://history.gmw.cn/node_38754.htm news",#古今中国 #这条仍旧重复了
        # ##"http://history.gmw.cn/node_33005.htm news",#历史映像  #这条重复了
        # ##"http://history.gmw.cn/node_5990.htm news",#民间往事  #这条重复了

        # "http://www.gmw.cn/guoxue/node_23032.htm news" ,#温故
        # "http://www.gmw.cn/guoxue/node_23031.htm news" ,#艺述
        # ##"http://www.gmw.cn/guoxue/node_73496.htm news" ,#节日读书  #特殊结构
        # ## "http://topics.gmw.cn/node_59788.htm news" ,#国学与社会主义核心价值观   #特殊结构
        # "http://www.gmw.cn/guoxue/node_23029.htm news" ,#光明推荐
        # "http://edu.gmw.cn/node_9737.htm news" ,#评论
        # "http://edu.gmw.cn/node_9717.htm news" ,#教育人物
        # "http://edu.gmw.cn/node_9757.htm news" ,#高校
        # "http://edu.gmw.cn/node_9729.htm news" ,#中小学
        # "http://edu.gmw.cn/node_9746.htm news" ,#留学
        # "http://edu.gmw.cn/node_9749.htm news" ,#招生信息
        # "http://edu.gmw.cn/node_9722.htm news" ,#职教
        # "http://edu.gmw.cn/node_10602.htm news" ,#要闻
        # "http://edu.gmw.cn/node_10810.htm news" ,#光明教育
        # "http://edu.gmw.cn/node_9758.htm news" ,#高招信息
        # "http://edu.gmw.cn/node_10809.htm news" ,#专题策划
        # "http://edu.gmw.cn/node_9743.htm news" ,#学前
        # "http://edu.gmw.cn/node_9725.htm news" ,#权威发布
        # "http://en.gmw.cn/node_32061.htm news" ,#GMW Insights
        # "http://en.gmw.cn/node_23654.htm news" ,#Culture Express
        # ##"http://en.gmw.cn/node_32064.htm news" ,#Figures  #特殊结构 404
        # "http://en.gmw.cn/node_32065.htm news" ,#Calligraphy & Painting 404
        # "http://en.gmw.cn/node_29530.htm news" ,#Books Recommended 404
        # "http://en.gmw.cn/node_32066.htm news" ,#Amazing China
        # "http://en.gmw.cn/node_32067.htm news" ,#China
        # "http://en.gmw.cn/node_32068.htm news" ,#World
        # "http://en.gmw.cn/node_32069.htm news" ,#Broad View  请求太快会 502 503 404 各种错误
        # "http://en.gmw.cn/node_28366.htm news" ,#Photo Gallery
        # "http://en.gmw.cn/node_32063.htm news" ,#China Anecdote  404
        # "http://en.gmw.cn/node_32062.htm news" ,#GMW Encyclopedia
        # "http://en.gmw.cn/node_29528.htm news" ,#Special Report 特殊结构
        # "http://en.gmw.cn/node_23652.htm news" ,#Opinion
        # "http://en.gmw.cn/node_32070.htm news" ,#Bilingual Zone
        # "http://en.gmw.cn/node_23648.htm news" ,#Culture Report 这个频道就是没有来源的
        # "http://en.gmw.cn/node_23647.htm news" ,#China Think Tank 404
        # "http://health.gmw.cn/node_9583.htm news" ,#要闻时评
        # ##"http://interview.gmw.cn/node_74196.htm news" ,#健康视点   #特殊结构
        # "http://health.gmw.cn/node_9222.htm news" ,#资讯速递
        # "http://health.gmw.cn/node_9214.htm news" ,#健康科普
        # "http://health.gmw.cn/node_9215.htm news" ,#名医名院
        # "http://health.gmw.cn/node_9201.htm news" ,#医疗专家 此频道比较旧　只能爬到前面的　后面的13年　14年的全部404
        # "http://health.gmw.cn/node_24189.htm news" ,#疾病护理
        # "http://health.gmw.cn/node_9592.htm news" ,#健康情报局
        # "http://health.gmw.cn/node_9224.htm news" ,#医疗前沿
        # "http://health.gmw.cn/node_9223.htm news" ,#品牌活动 专题类　特殊结构
        # "http://yangsheng.gmw.cn/node_12215.htm news" ,#要闻
        # "http://yangsheng.gmw.cn/node_12206.htm news" ,#健康常识
        # "http://yangsheng.gmw.cn/node_12212.htm news" ,#美容美体
        # "http://yangsheng.gmw.cn/node_12207.htm news" ,#营养保健
        # "http://yangsheng.gmw.cn/node_12202.htm news" ,#养生名人堂
        # "http://yangsheng.gmw.cn/node_12211.htm news" ,#品牌活动   #特殊结构 舍弃
        #
        # ## "http://cm.health.gmw.cn/node_21861.htm news" ,#中医资讯  #这些全都指向中医频道首页
        # ## "http://cm.health.gmw.cn/node_6926.htm news" ,#特色诊疗
        # ## "http://cm.health.gmw.cn/node_4372.htm news" ,#药膳饮食
        # ## "http://cm.health.gmw.cn/node_5522.htm news" ,#中医药文化
        # ## "http://cm.health.gmw.cn/node_21857.htm news" ,#中医讲堂
        # ## "http://cm.health.gmw.cn/node_28939.htm news" ,#中医百科
        # ## "http://cm.health.gmw.cn/node_21852.htm news" ,#知名中医
        #
        # "http://zhongyi.gmw.cn/node_118363.htm news" , #　中医新时代
        # "http://zhongyi.gmw.cn/node_21861.htm news" , # 中医要闻　
        # "http://zhongyi.gmw.cn/node_21857.htm news" , # 医患情深　
        # "http://zhongyi.gmw.cn/node_118413.htm news" , # 药技致富人
        # "http://zhongyi.gmw.cn/node_118362.htm news" , # 校园新中医　
        #
        # ##"http://cm.health.gmw.cn/node_21855.htm news" ,#品牌活动   #特殊结构 舍弃
        # ##"http://v.gmw.cn/node_11395.htm news" ,#新闻视野 #特殊结构 视频为主
        # ##"http://v.gmw.cn/node_10813.htm news" ,#第一观察  #特殊结构
        # ##"http://v.gmw.cn/node_11394.htm news" ,#文化娱乐 #特殊结构 视频为主
        # ##"http://v.gmw.cn/node_8401.htm news" ,#人文历史 #特殊结构 视频为主
        # ##"http://v.gmw.cn/node_41025.htm news" ,#光明讲坛 #特殊结构 视频为主
        # ##"http://v.gmw.cn/node_45701.htm news" ,#电影短片 #特殊结构 视频为主
        # "http://interview.gmw.cn/node_8811.htm news" ,#高端对话
        # "http://interview.gmw.cn/node_22804.htm news" ,#智慧思想
        # "http://interview.gmw.cn/node_22802.htm news" ,#热点解读
        # "http://interview.gmw.cn/node_22803.htm news" ,#文化艺术
        # "http://interview.gmw.cn/node_22798.htm news" ,#精彩观点
        # "http://interview.gmw.cn/node_8803.htm news" ,#往期回顾
        # "http://lady.gmw.cn/node_33738.htm news" ,#焦点图
        # "http://lady.gmw.cn/node_33671.htm news" ,#精选
        # "http://lady.gmw.cn/node_33670.htm news" ,#风尚标
        # "http://lady.gmw.cn/node_33667.htm news" ,#明星爱大牌
        # "http://lady.gmw.cn/node_33665.htm news" ,#美容彩妆
        # ##"http://interview.gmw.cn/index.htm news" ,#她对话   #特殊结构
        # "http://lady.gmw.cn/node_33721.htm news" ,#婚嫁亲子
        # "http://lady.gmw.cn/node_33726.htm news" ,#街拍秀
        #
        # # #pic频道需要登录
        # ## "http://pic.gmw.cn/channel_6100.html news" ,#突发事件
        # ## "http://pic.gmw.cn/channel_6103.html news" ,#自然环境
        # ## "http://pic.gmw.cn/channel_6200.html news" ,#社会
        # ## "http://pic.gmw.cn/channel_9100.html news" ,#军事
        # ## "http://pic.gmw.cn/channel_10050.html news" ,#人物
        # ## "http://pic.gmw.cn/channel_6050.html news" ,#体育
        # ## "http://pic.gmw.cn/channel_6104.html news" ,#文化
        # ## "http://pic.gmw.cn/channel_12054.html news" ,#环保
        # ## "http://pic.gmw.cn/channel_6105.html news" ,#科技
        # ## "http://pic.gmw.cn/channel_23050.html news" ,#两会
        # ## "http://pic.gmw.cn/channel_12056.html news" ,#城市人文
        # ## "http://pic.gmw.cn/channel_12057.html news" ,#乡土人文
        # ## "http://pic.gmw.cn/channel_12058.html news" ,#建筑装饰
        # ## "http://pic.gmw.cn/channel_12060.html news" ,#人物肖像
        # ## "http://pic.gmw.cn/channel_12059.html news" ,#静物
        # ## "http://pic.gmw.cn/channel_12061.html news" ,#食物
        # ## "http://pic.gmw.cn/channel_12062.html news" ,#风光
        # ## "http://pic.gmw.cn/channel_18050.html news" ,#其他图片
        # ## "http://pic.gmw.cn/channel_17050.html news" ,#图片分享
        #
        # ### "http://pic.gmw.cn/channel_14100.html news" ,#中华新闻图片库   #特殊结构
        # ### "http://photo.gmw.cn/ news" ,#图片论坛   #特殊结构
        # "http://meiwen.gmw.cn/node_24064.htm news" ,#光明文荟
        # "http://meiwen.gmw.cn/node_24065.htm news" ,#光明掠影
        # "http://meiwen.gmw.cn/node_24075.htm news" ,#今日推荐
        # "http://meiwen.gmw.cn/node_24059.htm news" ,#文学品读
        # "http://meiwen.gmw.cn/node_23777.htm news" ,#书人茶座
        # "http://meiwen.gmw.cn/node_23769.htm news" ,#读者天地
        # "http://meiwen.gmw.cn/node_23766.htm news" ,#影像故事
        # "http://gongyi.gmw.cn/node_37842.htm news" ,#要闻
        # "http://gongyi.gmw.cn/node_37846.htm news" ,#热点关注
        # "http://gongyi.gmw.cn/node_37854.htm news" ,#公益影像
        # "http://gongyi.gmw.cn/node_59613.htm news" ,#企业社会责任
        # "http://gongyi.gmw.cn/node_59614.htm news" ,#慈善家
        # "http://gongyi.gmw.cn/node_37847.htm news" ,#公益短片   #特殊结构
        #
        # ### "http://gongyi.gmw.cn/node_108121.htm news" ,#品牌活动  #特殊结构
        # ### "http://interview.gmw.cn/ news" ,#焦点对话  #特殊结构
        # ### "http://cloud.gmw.cn/ news" ,#光明云媒  #特殊结构 #这个页面手机app安装页面　
        # ### "http://yd.gmw.cn/ news" ,#云端读报  #特殊结构 #　打不开页面
        # ### "http://wap.gmw.cn/v2.html news" ,#光明网手机版  #特殊结构
        # ### "http://epaper.gmw.cn/gmrb/ news" ,#光明日报电子版  #特殊结构
        # ### "http://epaper.gmw.cn/zhdsb/ news" ,#中华读书报电子版     #这个是电子版 需要另外做
        # ### "http://www.gmw.cn/01wzb/ news" ,#文摘报 404
        # ### "http://epaper.gmw.cn/sz/ news" ,#书摘 特殊结构
        # ### "http://epaper.gmw.cn/blqs/ news" ,#博览群书 特殊结构
        #
        # ### "http://jyj.gmw.cn/ news" ,#教育家 是个首页　以下是子频道
        # "http://jyj.gmw.cn/node_77695.htm news" , # 教育家_信息联播
        # "http://jyj.gmw.cn/node_77694.htm news" , # 教育家_聚焦
        # "http://jyj.gmw.cn/node_77691.htm news" , # 教育家_实践者说
        # "http://jyj.gmw.cn/node_77693.htm news" , # 教育家_环球
        # "http://jyj.gmw.cn/node_77697.htm news" , # 教育家_治教
        # "http://jyj.gmw.cn/node_77692.htm news" , # 教育家_新锐
        # "http://jyj.gmw.cn/node_77689.htm news" , # 教育家_名家
        #
        # ### "http://feiyi.gmw.cn/node_115939.htm/ news" ,#名人坊 404
        # ### "http://feiyi.gmw.cn/node_115940.htm/ news" ,#今日热点 404
        # ### "http://feiyi.gmw.cn/node_115937.htm/ news" ,#非遗集萃 404
        # ### "http://feiyi.gmw.cn/node_115938.htm/ news" ,#传承动态 404
        # ### "http://museum.gmw.cn/node_115786.htm/ news" ,#镇馆之宝 404
        # ### "http://museum.gmw.cn/node_115785.htm/ news" ,#数字博物馆 404
        # ### "http://museum.gmw.cn/node_115787.htm/ news" ,#行业动态 404
        #
        # "http://shuhua.gmw.cn/node_10673.htm news", #书画热点
        # "http://shuhua.gmw.cn/node_9661.htm news", # 艺术人物
        # "http://www.gmw.cn/xueshu/node_23642.htm news", #学术要闻　废弃
    ]
    Debug = True
    doredis = False
    source = u"光明网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"DOWNLOAD_TIMEOUT": 120.0, "DOWNLOAD_DELAY": 0.25, "ROBOTSTXT_OBEY": False}
    sta = {"eff": 0, "inv": 0, "warn": 0, "all": 0, "inv2": 0}

    def print_info(self, info, flag="success", count=True):
        if flag == "error":
            color = "31"
            self.sta["inv"] += [0, 1][count]
        elif flag == "error2":
            color = "35"
            self.sta["inv2"] += [0, 1][count]
        elif flag == "warn":
            color = "33"
            self.sta["warn"] += [0, 1][count]
        else:
            self.sta["eff"] += [0, 1][count]
            color = "32"
        print('\033[0;'+color+';0m')
        print('*' * 100)
        if color == "31":
            print "抛出异常: ", info
        elif color == "33":
            print "警告： ", info
        else:
            print "信息: ", info
        print "统计: ",
        print "有效:", self.sta["eff"], " 无效: ", self.sta["inv"], " 警告: ", self.sta["warn"]," 人为失效:", self.sta["inv2"], \
            " 乐观总计:", self.sta["all"], " 采集率:", "%.2f%%" % (float(self.sta["eff"])/float(self.sta["all"] - self.sta["warn"]-self.sta["inv"])*100)
        print('*' * 100)
        print('\033[0m')

    def __init__(self, start_url=None):
        super(guangmingwang_news, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url": job.split()[0], "ba_type": job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            yield Request(url=channel["url"], method='get', meta={"ba_type": channel["ba_type"]}, callback=self.parse_link)

    def get_parse_link_urls(self, response, url):  #有改良方案，再说吧
        # 专题类的还没处理，　思路是　url中含topics和node_后跟的数字大于5位　认为是专题页面　然后需要找“更多”这个text()的a/@href
        # 进入列表页　然后抽取列表页的详情页
        urls_list = [
            "//div[@class='main_list']//h1/a/@href",   #1科技板块
            "//ul[@class='channel-newsGroup']/li/a/@href",  #2普通列表
            "//span[@class='channel-newsTitle']/a[last()]/@href", #图片列表
            "//div[@class='news_box']/a/@href", #图片列表2
            "//a[@target='_parent ']/text()/../@href", #普通列表种类2
            "//div[@class='area']//p[@class='black14']/a/@href", #6焦点
            "//div[@class='imglist1']/div[@class='list']/a/@href", #7光明图刊
            "//div[@class='black12']/a/@href", #阅读-读图
            "//span[@class='pic_title']/a/@href",#9科普
            "//div[@class='each_news']//h1/a/@href", #能源频道
            "//td[@class='picbd']/span/a/@href",   #picbd 图片频道
            "//ul[@class='list newPoint']/li/a/@href", # 领导人活动报道集
            "//ul[@class='title_list']/li/a/@href", # 教育家频道
            "//div[@class='each_news']/h3/a/@href", # 地方频道
            "//div[@class='content_left']//a[contains(@href, 'content')]/@href", # 光明评论员
            # "//div/div/div[2]/a/@href"  #法制新闻图片共同
        ]
        for url_xpath in urls_list:
            urls = response.xpath(url_xpath).extract()
            if len(urls) > 0:
                urls = set(urls)
                print url, " 本次套用:", url_xpath," 条目数:", len(urls)
                return url_xpath

    def parse_link(self, response):
        xpath = self.get_parse_link_urls(response, response.url)
        # print "xpath: ", xpath
        urls = set(response.xpath(xpath).extract())
        self.sta["all"] += len(urls)
        print "看看数量吧, 总量: ",self.sta["all"]
        for index, url in enumerate(urls):
            if '../' in url:
                url = url.replace('../', '')
            # print response.url, url
            final = urlparse.urljoin(response.url, url)
            print 'final_url is %s'%final
            # if index>0:
            #     break
            # if self.doredis and self.expire_redis.exists(final):
            #    continue

            yield Request(url=final, method='get',
                          meta={"ba_type": response.meta["ba_type"], "parse_for_content": True},
                          callback=self.parse_item, errback=self.parse_err_detail)

    def parse_err_detail(self, failure):
        response = failure.value.response
        self.print_info("页面异常: " + response.url + "  状态：" + str(response.status), "error")

    def parse_item(self, response):
        try:
            if response.meta["parse_for_content"]:
                item = DataItem()

                pubtime1 = response.xpath("//*[@id='pubTime']/text()").extract() or \
                           response.xpath("//div[@class='tips']/p[4]/span/text()").extract()
                if len(pubtime1) > 0:
                    item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", pubtime1[0]).group(0)

                pubtime2 = response.xpath("//div[@id='qihao']/text()").extract()
                if len(pubtime2) > 0 and len(pubtime1) == 0:
                    item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", pubtime2[0].replace(".", "-")).group(0) + " 00:00"

                if len(pubtime2) == 0 and len(pubtime1) == 0:
                    if response.headers.has_key('Date'):
                        item['pubtime'] = datetime.datetime.strptime(response.headers["Date"], '%a, %d %b %Y %H:%M:%S GMT').strftime("%Y-%m-%d %H:%M")

                item["type"] = response.meta["ba_type"]
                if "//world.gmw" in response.url:
                    item['area'] = u'国际'
                else:
                    item['area'] = u'全国'
                item['source'] = self.source
                item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
                item['url'] = response.url

                #4 理论-五老评热点
                title1 = response.xpath("//*[@id='articleTitle']") or \
                         response.xpath("//p[@class='p_title']") or \
                         response.xpath("//*[@class='picContentHeading']") or \
                         response.xpath("//*[@id='toptitle']") or \
                         response.xpath("//div[@class='img_showbox']/h1")        #图片频道的内容描述固定，所以不需要翻页

                if len(title1) > 0:
                    item['title'] = title1[0].xpath('string(.)').extract()[0].strip()

                title2 = response.xpath("//title/text()").extract()
                if len(title2) > 0:
                    item['title'] = title2[0]

                #1 普通   2 视频类  3组图类  4五老评热点
                content = response.xpath("//div[@id='contentMain']").extract() or \
                          response.xpath("//div[@class='con_text']").extract() or \
                          response.xpath("//div[@class='u-mainText']").extract() or \
                          response.xpath("//div[@class='video_zy']").extract() or \
                          response.xpath("//div[@id='ContentMain']").extract() or \
                          response.xpath("//div[@id='cont_left']").extract() or \
                          response.xpath("//div[@id='ArticleContent']").extract() or \
                          response.xpath("//div[@class='content']").extract() or \
                          response.xpath("//div[@class='layer1']/..").extract()   #最后2个英文版
                if len(content) > 0:
                    item['content'] = content[0]
                #视频类
                content2 = response.xpath("//div[contains(@class,'black14')]").extract() or \
                           response.xpath("//span[contains(@class,'black14')]").extract() or \
                           response.xpath("//div[@class='abstract']").extract()
                if len(content2) > 0 and len(content) == 0:
                    item['content'] = content2[0]
                #图片类 -图片频道
                content3 = response.xpath("//div[@class='bd']").extract() or \
                           response.xpath("//div[@class='h-contentMain']").extract()
                if len(content3) > 0 and len(content2) == 0 and len(content) == 0:
                    item['content'] = content3[0]
                # print 'content: ', content, content2, content3

                medianame1 = response.xpath("//*[@id='source']")
                medianame2 = response.xpath("//div[@class='tips']/p[3]/span[2]/text()").extract()
                medianame3 = response.xpath("//div[@class='share_right']/span[2]/a[last()]/text()").extract()    #适配英文版
                medianame4 = response.xpath("//div[@class='small_title']/text()[2]").extract()
                medianame5 = response.xpath("//span[@class='m-con-source']/a/text()").extract()
                medianame6 = response.xpath("//div[@class='g-tips']/span[3]/a/text()").extract()
                medianame7 = response.xpath("//div[@class='share_right']/span[2]/text()").extract()
                medianame8 = response.xpath("//div[@class='m-con-info']/span[2]/text()").extract()
                medianame9 = response.xpath("//div[@class='xinxi']/span[3]/text()").extract()
                # medianame4 = response.xpath("//span[@class='source']/a/text()").extract()   #图片为主类
                # print 'medianame1', medianame1,
                # print 'medianame2', medianame2,
                # print 'medianame3', medianame3,
                # print 'medianame4', medianame4,
                # print 'medianame5', medianame5,
                # print 'medianame6', medianame6

                item['medianame'] = ""
                if len(medianame1) > 0:
                    medianame1 = medianame1.xpath('string(.)').extract()[0].strip()
                    if len(re.findall(ur"(来源|出处|来自|稿源|出自|来源于)",medianame1))>0:
                        item["medianame"] = re.search(u'.*?(来源|出处|来自|稿源|出自|来源于)\s*[：:]\s*(\S*)', medianame1).group(2)
                    else:
                        item["medianame"] = medianame1
                if len(medianame2) > 0:
                    item["medianame"] = medianame2[0]
                if len(medianame3) > 0 and len(medianame2) == 0 and len(medianame1) == 0:
                    item["medianame"] = medianame3[0].strip()
                if len(medianame4) > 0 and len(medianame3) == 0 and len(medianame2) == 0 and len(medianame1) == 0:
                    item["medianame"] = medianame4[0].strip()
                if len(medianame5) > 0 and len(medianame4) == 0 and len(medianame3) == 0 and len(medianame2) == 0 and len(medianame1) == 0:
                    item["medianame"] = medianame5[0].strip()
                if len(medianame6) > 0 and len(medianame5) == 0 and len(medianame4) == 0 and len(medianame3) == 0 and len(medianame2) == 0 and len(medianame1) == 0:
                    item["medianame"] = medianame6[0].strip()
                if len(medianame7) > 0 and len(medianame6) == 0 and len(medianame5) == 0 and len(medianame4) == 0 and len(medianame3) == 0 and len(medianame2) == 0 and len(medianame1) == 0:
                    item["medianame"] = medianame7[0].strip()
                if len(medianame8) > 0 and len(medianame7) == 0 and len(medianame6) == 0 and len(medianame5) == 0 and len(medianame4) == 0 and len(medianame3) == 0 and len(medianame2) == 0 and len(medianame1) == 0:
                    item['medianame'] = medianame8[0].split(':')[-1].strip()
                    if "：" in item['medianame']:
                        item['medianame'] = item['medianame'].split('：')[-1].strip()
                if len(medianame9) > 0 and len(medianame8) == 0 and len(medianame7) == 0 and len(medianame6) == 0 and len(medianame5) == 0 and len(medianame4) == 0 and len(medianame3) == 0 and len(medianame2) == 0 and len(medianame1) == 0:
                    item['medianame'] = medianame9[0]
                if item["medianame"] == "":
                    self.print_info(item['title'] + " " + response.url + "  这个详细页无来源！！！", "warn", False)
                    item["medianame"] = u"光明日报"

                total_pages = response.xpath("//a[@class='ptfontpic'][2]/@href").extract() or \
                              response.xpath("//a[@class='ptfontcon'][2]/@href").extract()
                if len(total_pages) > 0:
                    total_pages = re.search(ur"_(\d+).htm", total_pages[0]).group(1)
                else:
                    total_pages = 1 #图片类
                if total_pages > 1:
                    url = response.url.replace(".htm","_2.htm")
                    yield Request(url=url,method='get',
                                  meta={"ba_type": response.meta["ba_type"],"item": item,
                                        "parse_for_content": False,"total_pages": total_pages,"current_page": 2},
                                  callback=self.parse_item,errback=self.parse_err_detail)
                else:
                    if len(response.xpath("//*[@id='gmweqxiu']").extract()) > 0:
                        self.print_info("被主动舍弃的详细页: " + response.url + " 原因: 无content",  "warn")
                        pass
                    else:
                        if item['pubtime'] and item['title'] and item['content']:
                            self.print_info("发布时间: " + item['pubtime'] + " 标题: " + item["title"] + " 发布源: " + item['medianame'] + " url: " + response.url + "  共1页")
                            yield item
            else:
                item = response.meta["item"]
                content = response.xpath("//div[@id='ContentMain']").extract() or \
                          response.xpath("//div[@id='contentMain']").extract() or \
                          response.xpath("//div[@id='ArticleContent']").extract() or \
                          response.xpath("//div[@class='content']").extract() or \
                          response.xpath("//div[@class='layer1']/..").extract() #最后2个英文版
                content = content[0]
                item["content"] += "/n" + content
                if int(response.meta["current_page"]) == int(response.meta["total_pages"]):
                    if item['pubtime'] and item['title'] and item['content']:
                        self.print_info("发布时间: " + item['pubtime'] + " 标题: "+item["title"] + " 发布源: " + item['medianame'] + " url: " + response.url + "  共" + str(response.meta["current_page"]) + "页")
                        yield item
                else:
                    url = response.url.replace("_"+ str(response.meta["current_page"]) + ".htm","_" + str(response.meta["current_page"] + 1 ) +".htm")
                    yield Request(url=url,method='get',
                                  meta={"ba_type":response.meta["ba_type"],"item":item,
                                        "parse_for_content":False,"total_pages":response.meta["total_pages"],"current_page": response.meta["current_page"] + 1},
                                  callback=self.parse_item,errback=self.parse_err_detail)
        except Exception:
            if len(response.xpath("//title/text()").extract()) > 0 and \
                    (u"页面没有找到" in response.xpath("//title/text()").extract()[0] or u"出错啦" in response.xpath("//title/text()").extract()[0]):
                self.print_info(traceback.format_exc() + "url:" + response.url + "  status: "+str(response.status), "error")
            else:
                self.print_info(traceback.format_exc() + "url:" + response.url + "  status: "+str(response.status), "error2")
