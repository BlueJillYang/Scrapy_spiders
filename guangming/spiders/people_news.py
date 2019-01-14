﻿#!/usr/bin/python
# -*- coding: utf-8 -*-import sys
__author__ = 'cwq'
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
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
from scrapy import Selector
from scrapy import signals
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.utils.response import get_base_url
# from scrapy.xlib.pydispatch import dispatcher
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class people_news(scrapy.Spider):
    name = "people_news"
    start_urls = [
        # "http://news.people.com.cn/ news 中国,"  # 滚动新闻 这个ajax加载的 有算法处理
        # "http://politics.people.com.cn/GB/70731/index.html news 中国,"  # 时政_滚动新闻
        # "http://politics.people.com.cn/GB/99014/index.html news 中国,"  # 时政_原创
        # "http://politics.people.com.cn/GB/1024/index.html news 中国,"  # 时政_高层动态
        # "http://politics.people.com.cn/GB/1027/index.html news 中国,"  # 时政_中央部委
        # "http://politics.people.com.cn/GB/369059/index.html news 中国,"  # 时政_反腐倡廉
        # "http://politics.people.com.cn/GB/389979/index.html news 中国,"  # 时政_时事解读
        # "http://world.people.com.cn/GB/157278/index.html news 中国,"  # 国际_滚动新闻
        # "http://world.people.com.cn/GB/1030/index.html news 中国,"  # 国际_国际观察
        # "http://world.people.com.cn/GB/1029/index.html news 中国,"  # 国际_时事快报
        # "http://world.people.com.cn/GB/1029/42354/index.html news 中国,"  # 国际_时事快报_亚太
        # "http://world.people.com.cn/GB/1029/42355/index.html news 中国,"  # 国际_时事快报_美洲
        # "http://world.people.com.cn/GB/1029/42356/index.html news 中国,"  # 国际_时事快报_欧洲
        # "http://world.people.com.cn/GB/1029/42361/index.html news 中国,"  # 国际_时事快报_中东
        # "http://world.people.com.cn/GB/1029/42359/index.html news 中国,"  # 国际_时事快报_非洲
        # "http://world.people.com.cn/GB/1029/42408/index.html news 中国,"  # 国际_时事快报_其他
        # "http://world.people.com.cn/GB/57507/index.html news 中国,"  # 国际_独家稿库
        # "http://world.people.com.cn/GB/107182/395377/index.html news 中国,"  # 国际_外媒_社会
        # "http://world.people.com.cn/GB/107182/395378/index.html news 中国,"  # 国际_外媒_科技
        # "http://world.people.com.cn/GB/107182/395380/index.html news 中国,"  # 国际_外媒_健康
        # "http://world.people.com.cn/GB/57506/index.html news 中国,"  # 国际_关注中国
        # "http://world.people.com.cn/GB/57506/211302/211438/index.html news 中国,"  # 国际_关注中国_国际政治
        # "http://world.people.com.cn/GB/57506/211302/211439/index.html news 中国,"  # 国际_关注中国_世界军事
        # "http://world.people.com.cn/GB/57506/211302/211440/index.html news 中国,"  # 国际_关注中国_世界经济
        # "http://world.people.com.cn/GB/57506/211302/211534/index.html news 中国,"  # 国际_关注中国_中国对外关系
        # "http://world.people.com.cn/GB/57506/211302/211539/index.html news 中国,"  # 国际_关注中国_中国人在海外
        # "http://world.people.com.cn/GB/57506/190965/190967/index.html news 中国,"  # 国际_关注中国_中国经济
        # "http://world.people.com.cn/GB/57506/190965/190968/index.html news 中国,"  # 国际_关注中国_中国外交
        # "http://world.people.com.cn/GB/57506/190965/190969/index.html news 中国,"  # 国际_关注中国_中国军事
        # "http://world.people.com.cn/GB/57506/190965/190970/index.html news 中国,"  # 国际_关注中国_中国社会
        # "http://world.people.com.cn/GB/57506/190965/190972/index.html news 中国,"  # 国际_关注中国_中国地位
        # "http://world.people.com.cn/GB/57506/190965/190973/index.html news 中国,"  # 国际_关注中国_中国人
        # "http://world.people.com.cn/GB/57506/190965/190974/index.html news 中国,"  # 国际_关注中国_中国商品
        # "http://world.people.com.cn/GB/57506/190965/197902/index.html news 中国,"  # 国际_关注中国_中国科技
        # "http://world.people.com.cn/GB/57506/190965/205394/index.html news 中国,"  # 国际_关注中国_聚焦人民币
        # "http://world.people.com.cn/GB/57506/190965/351428/index.html news 中国,"  # 国际_关注中国_中国政治
        # "http://world.people.com.cn/GB/57506/190965/351610/index.html news 中国,"  # 国际_关注中国_中国文化
        # "http://world.people.com.cn/GB/57506/190965/360030/index.html news 中国,"  # 国际_关注中国_中国投资
        # "http://chinese.people.com.cn/GB/420164/index.html news 中国,"  # 华侨华人_滚动新闻
        # "http://chinese.people.com.cn/GB/207230/index.html news 中国,"  # 华侨华人_原创
        # "http://chinese.people.com.cn/GB/420181/index.html news 中国,"  # 华侨华人_创业投资
        # "http://chinese.people.com.cn/GB/42314/index.html news 中国,"  # 华侨华人_华侨华人
        # "http://chinese.people.com.cn/GB/42315/index.html news 中国,"  # 华侨华人_侨务动态
        # "http://chinese.people.com.cn/GB/155405/index.html news 中国,"  # 华侨华人_留学移民
        # "http://japan.people.com.cn/GB/368232/index.html news 日本,"  # 日本_滚动新闻
        # "http://japan.people.com.cn/GB/35469/index.html news 日本,"  # 日本_时政
        # "http://japan.people.com.cn/GB/35463/index.html news 日本,"  # 日本_财经
        # "http://japan.people.com.cn/GB/35467/index.html news 日本,"  # 日本_社会
        # "http://japan.people.com.cn/GB/35465/index.html news 日本,"  # 日本_文化
        # "http://japan.people.com.cn/GB/35466/index.html news 日本,"  # 日本_数码
        # "http://usa.people.com.cn/GB/351373/index.html news 美国,"  # 美国_滚动新闻
        # "http://usa.people.com.cn/GB/242806/index.html news 美国,"  # 美国_文化
        # "http://usa.people.com.cn/GB/241411/index.html news 美国,"  # 美国_聚焦美国
        # "http://usa.people.com.cn/GB/242805/index.html news 美国,"  # 美国_观点
        # "http://usa.people.com.cn/GB/242804/index.html news 美国,"  # 美国_科技
        # "http://usa.people.com.cn/GB/242807/index.html news 美国,"  # 美国_留学移民
        # "http://usa.people.com.cn/GB/406587/index.html news 美国,"  # 美国_中美关系
        # "http://usa.people.com.cn/GB/406812/index.html news 美国,"  # 美国_美媒看中国
        # "http://usa.people.com.cn/GB/242328/index.html news 美国,"  # 美国_使领馆信息
        # "http://uk.people.com.cn/GB/352858/index.html news 英国,"  # 英国_经济
        # "http://uk.people.com.cn/GB/352867/index.html news 英国,"  # 英国_文化
        # "http://uk.people.com.cn/GB/352926/index.html news 英国,"  # 英国_体育
        # "http://uk.people.com.cn/GB/352930/index.html news 英国,"  # 英国_华人
        # "http://uk.people.com.cn/GB/356559/index.html news 英国,"  # 英国_UK NEWS
        # "http://ru.people.com.cn/GB/408061/index.html news 俄罗斯,"  # 俄罗斯_滚动新闻
        # "http://ru.people.com.cn/GB/408052/index.html news 俄罗斯,"  # 俄罗斯_时政
        # "http://ru.people.com.cn/GB/408053/index.html news 俄罗斯,"  # 俄罗斯_军事
        # "http://ru.people.com.cn/GB/408054/index.html news 俄罗斯,"  # 俄罗斯_经济
        # "http://ru.people.com.cn/GB/408055/index.html news 俄罗斯,"  # 俄罗斯_社会
        # "http://ru.people.com.cn/GB/408056/index.html news 俄罗斯,"  # 俄罗斯_科技
        # "http://ru.people.com.cn/GB/408057/index.html news 俄罗斯,"  # 俄罗斯_文化
        # "http://ru.people.com.cn/GB/408058/index.html news 俄罗斯,"  # 俄罗斯_教育
        # "http://korea.people.com.cn/GB/407862/index.html news 韩国,"  # 韩国_滚动新闻
        # "http://korea.people.com.cn/GB/407881/index.html news 韩国,"  # 韩国_时政
        # "http://korea.people.com.cn/GB/407882/index.html news 韩国,"  # 韩国_经济
        # "http://korea.people.com.cn/GB/407864/index.html news 韩国,"  # 韩国_社会
        # "http://korea.people.com.cn/GB/407889/index.html news 韩国,"  # 韩国_企业
        # "http://korea.people.com.cn/GB/407883/index.html news 韩国,"  # 韩国_文体
        # "http://korea.people.com.cn/GB/407887/index.html news 韩国,"  # 韩国_留学
        # "http://australia.people.com.cn/GB/408098/index.html news 澳新,"  # 澳新_滚动新闻
        # "http://australia.people.com.cn/GB/408082/index.html news 澳新,"  # 澳新_时政|经济
        # "http://australia.people.com.cn/GB/408094/index.html news 澳新,"  # 澳新_资讯
        # "http://australia.people.com.cn/GB/408084/index.html news 澳新,"  # 澳新_社会
        # "http://australia.people.com.cn/GB/408092/index.html news 澳新,"  # 澳新_华人
        # "http://australia.people.com.cn/GB/408086/index.html news 澳新,"  # 澳新_文化
        # "http://australia.people.com.cn/GB/408088/index.html news 澳新,"  # 澳新_教育
        # "http://australia.people.com.cn/GB/408096/index.html news 澳新,"  # 澳新_南太
        # "http://money.people.com.cn/GB/399292/index.html news 中国,"  # 金融_原创新闻
        # "http://money.people.com.cn/bank/GB/index.html news 中国,"  # 金融_银行
        # "http://money.people.com.cn/fund/GB/index.html news 中国,"  # 金融_基金
        # "http://money.people.com.cn/GB/392426/index.html news 中国,"  # 金融_互联网金融
        # "http://money.people.com.cn/GB/397730/index.html news 中国,"  # 金融_新三板
        # "http://money.people.com.cn/GB/67605/index.html news 中国,"  # 金融_债券
        # "http://money.people.com.cn/forex/GB/index.html news 中国,"  # 金融_外汇
        # "http://money.people.com.cn/GB/67604/index.html news 中国,"  # 金融_期货
        # "http://rmfp.people.com.cn/GB/406732/index.html news 中国,"  # 扶贫_政策解读
        # "http://rmfp.people.com.cn/GB/406733/index.html news 中国,"  # 扶贫_部委扶贫举措
        # "http://rmfp.people.com.cn/GB/406734/index.html news 中国,"  # 扶贫_地方要闻
        # "http://rmfp.people.com.cn/GB/406737/index.html news 中国,"  # 扶贫_观察思考
        # "http://rmfp.people.com.cn/GB/406736/index.html news 中国,"  # 扶贫_致富项目
        # "http://rmfp.people.com.cn/GB/406735/index.html news 中国,"  # 扶贫_县域动态
        # "http://ccnews.people.com.cn/GB/142052/index.html news 中国,"  # 央企_新闻
        # "http://ccnews.people.com.cn/GB/355691/index.html news 中国,"  # 央企_人事
        # "http://ccnews.people.com.cn/GB/354509/index.html news 中国,"  # 央企_广角
        # "http://ccnews.people.com.cn/GB/242789/index.html news 中国,"  # 央企_企业舆情
        # "http://ccnews.people.com.cn/GB/142036/index.html news 中国,"  # 央企_独家新闻
        # "http://finance.people.com.cn/GB/70846/index.html news 中国,"  # 财经_滚动新闻
        # "http://finance.people.com.cn/GB/153179/153180/index.html news 中国,"  # 财经_宏观
        # "http://finance.people.com.cn/GB/1045/index.html news 中国,"  # 财经_观察
        # "http://finance.people.com.cn/GB/153179/153522/index.html news 中国,"  # 财经_部委快讯
        # "http://finance.people.com.cn/GB/153179/153480/index.html news 中国,"  # 财经_人物
        # "http://finance.people.com.cn/GB/414330/index.html news 中国,"  # 财经_原创
        # "http://finance.people.com.cn/GB/226375/402602/index.html news 中国,"  # 财经_人民财评
        # "http://tw.people.com.cn/GB/104510/index.html news 中国,"  # 台湾_滚动
        # "http://tw.people.com.cn/GB/14812/14875/index.html news 中国,"  # 台湾_要闻
        # "http://tw.people.com.cn/GB/14812/14874/index.html news 中国,"  # 台湾_万象
        # "http://tw.people.com.cn/GB/14810/index.html news 中国,"  # 台湾_涉台新闻
        # "http://tw.people.com.cn/GB/14813/index.html news 中国,"  # 台湾_两岸交流
        # "http://tw.people.com.cn/GB/88649/index.html news 中国,"  # 台湾_台海军情
        # "http://tw.people.com.cn/GB/157509/index.html news 中国,"  # 台湾_史海珍闻
        # "http://military.people.com.cn/GB/172467/index.html news 中国,"  # 军事_滚动
        # "http://military.people.com.cn/GB/52963/index.html news 中国,"  # 军事_中央部委
        # "http://military.people.com.cn/GB/115150/index.html news 中国,"  # 军事_国防部
        # "http://military.people.com.cn/GB/52936/index.html news 中国,"  # 军事_原创
        # "http://military.people.com.cn/GB/367527/index.html news 中国,"  # 军事_中国军情
        # "http://military.people.com.cn/GB/1077/index.html news 中国,"  # 军事_国际军情
        # "http://military.people.com.cn/GB/42969/index.html news 中国,"  # 军事_评论
        # "http://military.people.com.cn/GB/367540/index.html news 中国,"  # 军事_名家论剑
        # "http://opinion.people.com.cn/GB/223228/index.html news 中国,"  # 观点_人民网评
        # "http://opinion.people.com.cn/GB/8213/420650/index.html news 中国,"  # 观点_三评
        # "http://opinion.people.com.cn/GB/364597/index.html news 中国,"  # 观点_原创快评
        # "http://opinion.people.com.cn/GB/1036/index.html news 中国,"  # 观点_网友来论
        # "http://opinion.people.com.cn/GB/40604/index.html news 中国,"  # 观点_报系言论
        # "http://opinion.people.com.cn/GB/159301/index.html news 中国,"  # 观点_每日新评
        # "http://opinion.people.com.cn/GB/8213/119388/index.html news 中国,"  # 观点_观点1+1
        # "http://leaders.people.com.cn/GB/70117/index.html news 中国,"  # 领导_各地人事任免
        # "http://leaders.people.com.cn/GB/70149/index.html news 中国,"  # 领导_执政新举
        # "http://leaders.people.com.cn/GB/70118/index.html news 中国,"  # 领导_贪腐曝光
        # "http://leaders.people.com.cn/GB/70120/index.html news 中国,"  # 领导_热评官场
        # "http://leaders.people.com.cn/GB/70116/index.html news 中国,"  # 领导_理论文章
        # "http://cpc.people.com.cn/GB/64093/64094/index.html news 中国,"  # 人事_高层动态
        # "http://cpc.people.com.cn/GB/64093/64102/index.html news 中国,"  # 人事_干部论坛
        # "http://theory.people.com.cn/GB/409499/ news 中国,"  # 理论_重要评论
        # "http://theory.people.com.cn/GB/409497/409507/index.html news 中国,"  # 理论_文章列表
        # "http://legal.people.com.cn/GB/188502/index.html news 中国,"  # 法治_滚动
        # "http://legal.people.com.cn/GB/42729/index.html news 中国,"  # 法治_动态
        # "http://legal.people.com.cn/GB/204446/index.html news 中国,"  # 法治_司法关注
        # "http://legal.people.com.cn/GB/204445/index.html news 中国,"  # 法治_行政执法
        # "http://legal.people.com.cn/GB/204447/index.html news 中国,"  # 法治_法治监督
        # "http://society.people.com.cn/GB/136657/index.html news 中国,"  # 社会_滚动新闻
        # "http://society.people.com.cn/GB/86800/index.html news 中国,"  # 社会_原创
        # "http://society.people.com.cn/GB/41158/index.html news 中国,"  # 社会_百姓民生
        # "http://society.people.com.cn/GB/1062/index.html news 中国,"  # 社会_万象
        # "http://edu.people.com.cn/GB/1053/index.html news 中国,"  # 教育_滚动
        # "http://edu.people.com.cn/GB/367001/index.html news 中国,"  # 教育_原创
        # "http://sports.people.com.cn/GB/22176/index.html news 中国,"  # 体育_滚动新闻
        # "http://sports.people.com.cn/GB/35862/index.html news 中国,"  # 体育_原创
        # "http://sports.people.com.cn/GB/22155/index.html news 中国,"  # 体育_综合
        # "http://sports.people.com.cn/GB/22172/index.html news 中国,"  # 体育_评论
        # "http://sports.people.com.cn/GB/401891/401892/index.html news 中国,"  # 体育_跑步资讯
        # "http://sports.people.com.cn/GB/401891/401893/index.html news 中国,"  # 体育_跑步跑者
        # "http://sports.people.com.cn/GB/401891/401894/index.html news 中国,"  # 体育_跑步知识
        # "http://sports.people.com.cn/GB/407727/408077/index.html news 中国,"  # 体育_冰雪_竞技动态
        # "http://sports.people.com.cn/GB/407727/408078/index.html news 中国,"  # 体育_冰雪_大众冰雪
        # "http://sports.people.com.cn/GB/407727/408080/index.html news 中国,"  # 体育_冰雪_冰雪产业
        # "http://sports.people.com.cn/jianshen/ news 中国,"  # 体育_全民健身
        # "http://sports.people.com.cn/GB/22134/index.html news 中国,"  # 体育_国内足球
        # "http://sports.people.com.cn/GB/22141/index.html news 中国,"  # 体育_国际足球
        # "http://sports.people.com.cn/GB/22149/index.html news 中国,"  # 体育_篮球
        # "http://qipai.people.com.cn/GB/47625/index.html news 中国,"  # 棋牌_围棋
        # "http://qipai.people.com.cn/GB/47627/index.html news 中国,"  # 棋牌_象棋
        # "http://qipai.people.com.cn/GB/47626/index.html news 中国,"  # 棋牌_国际象棋
        # "http://qipai.people.com.cn/GB/408735/index.html news 中国,"  # 棋牌_综合棋牌
        # "http://qipai.people.com.cn/GB/408691/index.html news 中国,"  # 棋牌_滚动新闻
        # "http://qipai.people.com.cn/GB/408695/index.html news 中国,"  # 棋牌_原创
        # "http://culture.people.com.cn/GB/172318/index.html news 中国,"  # 文化_滚动
        # "http://culture.people.com.cn/GB/87423/index.html news 中国,"  # 文化_原创
        # "http://culture.people.com.cn/GB/27296/index.html news 中国,"  # 文化_媒体评弹
        # "http://culture.people.com.cn/GB/22219/index.html news 中国,"  # 文化_媒体联播
        # "http://art.people.com.cn/GB/226026/index.html news 中国,"  # 书画_滚动资讯
        # "http://art.people.com.cn/GB/206244/356129/index.html news 中国,"  # 书画_绘画资讯
        # "http://art.people.com.cn/GB/206244/356132/index.html news 中国,"  # 书画_书法资讯
        # "http://art.people.com.cn/GB/206254/206256/index.html news 中国,"  # 书画_瓷器
        # "http://art.people.com.cn/GB/206254/206255/index.html news 中国,"  # 书画_玉石
        # "http://art.people.com.cn/GB/206246/408046/index.html news 中国,"  # 书画_人民艺评
        # "http://art.people.com.cn/GB/206246/408047/index.html news 中国,"  # 书画_美术论谈
        # "http://art.people.com.cn/GB/206261/index.html news 中国,"  # 书画_艺海钩沉
        # "http://auto.people.com.cn/GB/1052/98358/98363/index.html news 中国,"  # 汽车_人民车评
        # "http://auto.people.com.cn/GB/1049/index.html news 中国,"  # 汽车_国内新闻
        # "http://auto.people.com.cn/GB/173005/index.html news 中国,"  # 汽车_国际新闻
        # "http://auto.people.com.cn/GB/1051/index.html news 中国,"  # 汽车_政策法规
        # "http://auto.people.com.cn/GB/14555/index.html news 中国,"  # 汽车_行业动态
        # "http://auto.people.com.cn/GB/1052/25089/index.html news 中国,"  # 汽车_汽车价格
        # "http://health.people.com.cn/GB/408564/index.html news 中国,"  # 健康_政策声音
        # "http://health.people.com.cn/GB/408565/index.html news 中国,"  # 健康_行业热点
        # "http://health.people.com.cn/GB/408567/index.html news 中国,"  # 健康_医学前沿
        # "http://health.people.com.cn/GB/408568/index.html news 中国,"  # 健康_观察评论
        # "http://health.people.com.cn/GB/26466/401878/404200/404225/index.html news 中国,"  # 健康_人民营养家_营养学堂
        # "http://health.people.com.cn/GB/415859/index.html news 中国,"  # 健康_滚动新闻
        # "http://health.people.com.cn/GB/405407/index.html news 中国,"  # 健康_中医中药
        # "http://health.people.com.cn/GB/408569/index.html news 中国,"  # 健康_食品
        # "http://health.people.com.cn/GB/408573/index.html news 中国,"  # 健康_母婴
        # "http://health.people.com.cn/GB/408572/index.html news 中国,"  # 健康_养生
        # "http://health.people.com.cn/GB/408575/index.html news 中国,"  # 健康_美容
        # "http://health.people.com.cn/GB/408571/index.html news 中国,"  # 健康_健身
        # "http://scitech.people.com.cn/GB/1057/index.html news 中国,"  # 科技_滚动新闻
        # "http://scitech.people.com.cn/GB/59405/index.html news 中国,"  # 科技_独家
        # "http://scitech.people.com.cn/GB/41163/index.html news 中国,"  # 科技_产业动态
        # "http://scitech.people.com.cn/GB/1056/index.html news 中国,"  # 科技_科学界
        # "http://scitech.people.com.cn/GB/53752/index.html news 中国,"  # 科技_发明创新
        # "http://scitech.people.com.cn/GB/25895/index.html news 中国,"  # 科技_探索发现
        # "http://scitech.people.com.cn/GB/25893/index.html news 中国,"  # 科技_医学健康
        # "http://scitech.people.com.cn/GB/25892/index.html news 中国,"  # 科技_航空航天
        # "http://scitech.people.com.cn/GB/53753/index.html news 中国,"  # 科技_评论
        # "http://dangjian.people.com.cn/GB/394443/index.html news 中国,"  # 党建_中央精神
        # "http://dangjian.people.com.cn/GB/219967/index.html news 中国,"  # 党建_各地动态
        # "http://dangjian.people.com.cn/GB/132289/index.html news 中国,"  # 党建_干部谈党建
        # "http://dangjian.people.com.cn/GB/394444/index.html news 中国,"  # 党建_评论观点
        # "http://dangjian.people.com.cn/GB/359559/index.html news 中国,"  # 党建_独家报道
        # "http://dangjian.people.com.cn/GB/117103/index.html news 中国,"  # 党建_综合报道
        # "http://dangjian.people.com.cn/GB/394323/index.html news 中国,"  # 党建_专家辅导
        # "dangjian.people.com.cn/GB/117104/index.html news 中国,"  # 党建_交流体会
        # "http://fanfu.people.com.cn/GB/64372/index.html news 中国,"  # 反腐_中央精神
        # "http://fanfu.people.com.cn/GB/64379/index.html news 中国,"  # 反腐_部委信息
        # "http://fanfu.people.com.cn/GB/403580/index.html news 中国,"  # 反腐_一周反腐
        # "http://fanfu.people.com.cn/GB/64376/index.html news 中国,"  # 反腐_廉政时评
        # "http://fanfu.people.com.cn/GB/64375/index.html news 中国,"  # 反腐_干部论述
        # "http://fanfu.people.com.cn/GB/64378/index.html news 中国,"  # 反腐_地方动态
        # "http://fanfu.people.com.cn/GB/140194/index.html news 中国,"  # 反腐_案件播报
        # "http://fanfu.people.com.cn/GB/64374/index.html news 中国,"  # 反腐_案情追踪
        # "http://fanfu.people.com.cn/GB/350251/index.html news 中国,"  # 反腐_综合报道
        # "http://fanfu.people.com.cn/GB/140331/index.html news 中国,"  # 反腐_警钟长鸣
        # "http://hm.people.com.cn/GB/230533/index.html news 中国,"  # 港澳_滚动新闻
        # "http://hm.people.com.cn/GB/42273/index.html news 中国,"  # 港澳_时政新闻
        # "http://hm.people.com.cn/GB/85423/index.html news 中国,"  # 港澳_港澳内地
        # "http://hm.people.com.cn/GB/85418/index.html news 中国,"  # 港澳_科教文卫
        # "http://hm.people.com.cn/GB/42275/index.html news 中国,"  # 港澳_社会万象
        # "http://media.people.com.cn/GB/40606/index.html news 中国,"  # 传媒_资讯
        # "http://media.people.com.cn/GB/40628/index.html news 中国,"  # 传媒_研究
        # "http://media.people.com.cn/GB/40710/index.html news 中国,"  # 传媒_报刊
        # "http://media.people.com.cn/GB/40757/index.html news 中国,"  # 传媒_出版
        # "http://media.people.com.cn/GB/40724/index.html news 中国,"  # 传媒_电视
        # "http://media.people.com.cn/GB/138367/index.html news 中国,"  # 传媒_电影
        # "http://media.people.com.cn/GB/40728/index.html news 中国,"  # 传媒_网络
        # "http://media.people.com.cn/GB/408724/index.html news 中国,"  # 传媒_社交媒体
        # "http://media.people.com.cn/GB/40641/index.html news 中国,"  # 传媒_产业新闻
        # "http://media.people.com.cn/GB/408725/index.html news 中国,"  # 传媒_新技术
        # "http://media.people.com.cn/GB/408721/index.html news 中国,"  # 传媒_媒介素养
        # "http://media.people.com.cn/GB/40698/index.html news 中国,"  # 传媒_媒介批评
        # "http://media.people.com.cn/GB/40701/index.html news 中国,"  # 传媒_传媒人物
        # "http://media.people.com.cn/GB/408709/index.html news 中国,"  # 传媒_传媒教育
        # "http://tc.people.com.cn/GB/183206/index.html news 中国,"  # 通信_原创
        # "http://tc.people.com.cn/GB/183760/index.html news 中国,"  # 通信_运营商
        # "http://tc.people.com.cn/GB/183784/index.html news 中国,"  # 通信_手机评测
        # "http://it.people.com.cn/GB/243510/index.html news 中国,"  # IT_滚动新闻
        # "http://it.people.com.cn/GB/114490/index.html news 中国,"  # IT_原创
        # "http://homea.people.com.cn/GB/41392/index.html news 中国,"  # 家电_企业视点
        # "http://homea.people.com.cn/GB/41391/index.html news 中国,"  # 家电_行业焦点
        # "http://yuqing.people.com.cn/GB/405625/index.html news 中国,"  # 舆情_数读舆情
        # "http://blockchain.people.com.cn/GB/421538/421539/index.html news 中国,"  # 区块链_原创
        # "http://blockchain.people.com.cn/GB/421538/421540/index.html news 中国,"  # 区块链_资讯
        # "http://blockchain.people.com.cn/GB/421538/421541/index.html news 中国,"  # 区块链_深度
        # "http://blockchain.people.com.cn/GB/421538/421542/index.html news 中国,"  # 区块链_专访
        # "http://blockchain.people.com.cn/GB/421538/421543/index.html news 中国,"  # 区块链_活动
        # "http://blockchain.people.com.cn/GB/421538/421546/index.html news 中国,"  # 区块链_滚动新闻
        # "http://money.people.com.cn/stock/GB/68055/index1.html news 中国,"  # 股票_上市公司
        # "http://money.people.com.cn/stock/GB/220477/index.html news 中国,"  # 股票_新股聚焦
        # "http://money.people.com.cn/stock/GB/68059/index.html news 中国,"  # 股票_股市直播
        # "http://money.people.com.cn/stock/GB/220485/index.html news 中国,"  # 股票_监管新闻
        # "http://money.people.com.cn/stock/GB/222900/index.html news 中国,"  # 股票_券商投行
        # "http://energy.people.com.cn/GB/71890/index.html news 中国,"  # 能源_滚动
        # "http://energy.people.com.cn/GB/133190/index.html news 中国,"  # 能源_能源经济
        # "http://energy.people.com.cn/GB/140056/index.html news 中国,"  # 能源_原创
        # "http://energy.people.com.cn/GB/71894/index.html news 中国,"  # 能源_评论
        # "http://energy.people.com.cn/GB/71891/index.html news 中国,"  # 能源_国际
        # "http://energy.people.com.cn/GB/71895/index.html news 中国,"  # 能源_企业
        # "http://energy.people.com.cn/GB/71897/index.html news 中国,"  # 能源_石油
        # "http://energy.people.com.cn/GB/71900/index.html news 中国,"  # 能源_天然气
        # "http://energy.people.com.cn/power/ news 中国,"  # 能源_电力
        # "http://energy.people.com.cn/GB/71898/index.html news 中国,"  # 能源_煤炭
        # "http://energy.people.com.cn/GB/71896/index.html news 中国,"  # 能源_新能源
        # "http://energy.people.com.cn/GB/133184/index.html news 中国,"  # 能源_人物
        # "http://energy.people.com.cn/GB/396326/index.html news 中国,"  # 能源_部委消息
        # "http://industry.people.com.cn/GB/413885/index.html news 中国,"  # 产经_产业
        # "http://industry.people.com.cn/GB/413887/index.html news 中国,"  # 产经_公司
        # "http://industry.people.com.cn/GB/413890/index.html news 中国,"  # 产经_理财
        # "http://industry.people.com.cn/GB/413888/index.html news 中国,"  # 产经_消费
        # "http://gongyi.people.com.cn/GB/151650/index.html news 中国,"  # 公益_滚动新闻
        # "http://gongyi.people.com.cn/GB/419333/index.html news 中国,"  # 公益_原创
        # "http://gongyi.people.com.cn/GB/151650/152516/index.html news 中国,"  # 公益_政策法规
        # "http://gongyi.people.com.cn/GB/151650/152542/index.html news 中国,"  # 公益_助学成长
        # "http://gongyi.people.com.cn/GB/151650/152544/index.html news 中国,"  # 公益_医疗救助
        # "http://gongyi.people.com.cn/GB/151650/152511/index.html news 中国,"  # 公益_观点
        # "http://gongyi.people.com.cn/GB/151662/index.html news 中国,"  # 公益_公益人物
        # "http://gongyi.people.com.cn/GB/191114/index.html news 中国,"  # 公益_社会组织
        # "http://gongyi.people.com.cn/GB/151658/153096/index.html news 中国,"  # 公益_公益曝光
        # "http://gongyi.people.com.cn/GB/151658/186202/index.html news 中国,"  # 公益_公益活动
        # "http://gongyi.people.com.cn/GB/413802/index.html news 中国,"  # 公益_社会责任
        # "http://env.people.com.cn/GB/74877/index.html news 中国,"  # 环保_滚动新闻
        # "http://env.people.com.cn/GB/359626/index.html news 中国,"  # 环保_原创
        # "http://env.people.com.cn/GB/217507/index.html news 中国,"  # 环保_天气新闻速递
        # "http://env.people.com.cn/GB/219130/index.html news 中国,"  # 环保_曝光台
        # "http://env.people.com.cn/GB/193224/index.html news 中国,"  # 环保_部委信息
        # "http://env.people.com.cn/GB/1075/index.html news 中国,"  # 环保_绿色生活
        # "http://env.people.com.cn/GB/1074/index.html news 中国,"  # 环保_自然生态
        # "http://env.people.com.cn/GB/36686/index.html news 中国,"  # 环保_环保产业
        # "http://env.people.com.cn/GB/1073/index.html news 中国,"  # 环保_污染防治
        # "http://env.people.com.cn/GB/35525/index.html news 中国,"  # 环保_人民环评
        # "http://hongmu.people.com.cn/GB/392170/index.html news 中国,"  # 红木_资讯
        # "http://hongmu.people.com.cn/GB/392173/index.html news 中国,"  # 红木_特色产区
        # "http://hongmu.people.com.cn/GB/392174/index.html news 中国,"  # 红木_名企动态
        # "http://jiaju.people.com.cn/GB/151419/index.html news 中国,"  # 家居_人民出品
        # "http://jiaju.people.com.cn/GB/151426/index.html news 中国,"  # 家居_资讯
        # "http://jiaju.people.com.cn/GB/155381/index.html news 中国,"  # 家居_潮流饰家
        # "http://dengshi.people.com.cn/GB/402720/index.html news 中国,"  # 灯饰_灯都要闻
        # "http://dengshi.people.com.cn/GB/402719/index.html news 中国,"  # 灯饰_行业资讯
        # "http://dengshi.people.com.cn/GB/402715/index.html news 中国,"  # 灯饰_专利展示
        # "http://dengshi.people.com.cn/GB/402707/index.html news 中国,"  # 灯饰_灯都论坛
        # "http://dengshi.people.com.cn/GB/402606/index.html news 中国,"  # 灯饰_高端访谈
        # "http://shipin.people.com.cn/GB/395905/index.html news 中国,"  # 食品_行业24小时
        # "http://shipin.people.com.cn/GB/115280/index.html news 中国,"  # 食品_本网原创
        # "http://shipin.people.com.cn/GB/395906/index.html news 中国,"  # 食品_吃喝百宝袋
        # "http://shipin.people.com.cn/GB/86117/index.html news 中国,"  # 食品_曝光台
        # "http://shipin.people.com.cn/GB/215731/index.html news 中国,"  # 食品_滚动新闻
        # "http://shipin.people.com.cn/GB/418903/index.html news 中国,"  # 食品_原创
        # "http://jiu.people.cn/GB/407854/index.html news 中国,"  # 酒业_政策解读
        # "http://jiu.people.cn/GB/407855/index.html news 中国,"  # 酒业_行业资讯
        # "http://jiu.people.cn/GB/407856/index.html news 中国,"  # 酒业_品牌传播
        # "http://jiu.people.cn/GB/407857/index.html news 中国,"  # 酒业_饮酒新文化
        # "http://jiu.people.cn/GB/407858/index.html news 中国,"  # 酒业_互动交流
        # "http://jiu.people.cn/GB/407859/index.html news 中国,"  # 酒业_舆情分析
        # "http://country.people.com.cn/GB/419851/index.html news 中国,"  # 美丽乡村_滚动新闻
        # "http://country.people.com.cn/GB/419856/index.html news 中国,"  # 美丽乡村_权威发布
        # "http://country.people.com.cn/GB/419859/index.html news 中国,"  # 美丽乡村_生态环境
        # "http://country.people.com.cn/GB/419861/index.html news 中国,"  # 美丽乡村_质量兴农
        # "http://country.people.com.cn/GB/419863/index.html news 中国,"  # 美丽乡村_魅力村镇
        # "http://country.people.com.cn/GB/419864/index.html news 中国,"  # 美丽乡村_我是村官
        # "http://country.people.com.cn/GB/419857/index.html news 中国,"  # 美丽乡村_乡村振兴
        # "http://country.people.com.cn/GB/422187/index.html news 中国,"  # 美丽乡村_乡村文明
        # "http://ip.people.com.cn/GB/179663/index.html news 中国,"  # 知识产权_综合资讯
        # "http://ip.people.com.cn/GB/417806/index.html news 中国,"  # 知识产权_地方动态
        # "http://ip.people.com.cn/GB/192430/index.html news 中国,"  # 知识产权_本网原创
        # "http://ip.people.com.cn/GB/417807/index.html news 中国,"  # 知识产权_发明视界
        # "http://ip.people.com.cn/GB/192427/index.html news 中国,"  # 知识产权_法律法规
        # "http://bj.people.com.cn/GB/233088/index.html news 北京市,"  # 北京_原创
        # "http://bj.people.com.cn/GB/82837/index.html news 北京市,"  # 北京_时政
        # "http://bj.people.com.cn/GB/82840/index.html news 北京市,"  # 北京_社会
        # "http://bj.people.com.cn/GB/82838/index.html news 北京市,"  # 北京_十六区动态
        # "http://bj.people.com.cn/GB/233092/index.html news 北京市,"  # 北京_人事任免
        # "http://bj.people.com.cn/GB/14545/index.html news 北京市,"  # 北京_观察
        # "http://bj.people.com.cn/GB/233086/index.html news 北京市,"  # 北京_国内
        # "http://bj.people.com.cn/GB/233087/index.html news 北京市,"  # 北京_国际
        # "http://bj.people.com.cn/GB/82839/index.html news 北京市,"  # 北京_财经
        # "http://bj.people.com.cn/GB/349239/index.html news 北京市,"  # 北京_科技
        # "http://bj.people.com.cn/GB/82846/index.html news 北京市,"  # 北京_文化
        # "http://bj.people.com.cn/GB/339781/index.html news 北京市,"  # 北京_体育
        # "http://bj.people.com.cn/GB/82841/index.html news 北京市,"  # 北京_教育
        # "http://bj.people.com.cn/GB/233081/index.html news 北京市,"  # 北京_健康
        # "http://bj.people.com.cn/GB/25527/358528/358529/index.html news 北京市,"  # 北京_十六区动态_朝阳要闻
        # "http://bj.people.com.cn/GB/25527/358528/358533/index.html news 北京市,"  # 北京_十六区动态_朝阳区城市建设
        # "http://bj.people.com.cn/GB/25527/358528/358532/index.html news 北京市,"  # 北京_十六区动态_朝阳区社会民生
        # "http://bj.people.com.cn/GB/25527/358528/358530/index.html news 北京市,"  # 北京_十六区动态_朝阳区产业发展
        # "http://bj.people.com.cn/GB/25527/358528/371472/index.html news 北京市,"  # 北京_十六区动态_朝阳区基层亮点
        # "http://bj.people.com.cn/GB/25527/361124/361133/index.html news 北京市,"  # 北京_十六区动态_顺义要闻
        # "http://bj.people.com.cn/GB/82838/337124/index.html news 北京市,"  # 北京_十六区动态_海淀要闻
        # "http://bj.people.com.cn/GB/25527/384629/384630/index.html news 北京市,"  # 北京_十六区动态_丰台要闻
        # "http://bj.people.com.cn/GB/82838/337132/index.html news 北京市,"  # 北京_十六区动态_昌平要闻
        # "http://bj.people.com.cn/GB/25527/360761/360771/index.html news 北京市,"  # 北京_农业要闻
        # "http://bj.people.com.cn/GB/25527/376731/376732/index.html news 北京市,"  # 北京_城市副中心动态
        # "http://tj.people.com.cn/GB/375547/index.html news 天津市,"  # 天津_今日天津
        # "http://tj.people.com.cn/GB/378596/index.html news 天津市,"  # 天津_国内要闻
        # "http://tj.people.com.cn/GB/375887/index.html news 天津市,"  # 天津_本网原创
        # "http://tj.people.com.cn/GB/375555/index.html news 天津市,"  # 天津_天津要闻
        # "http://tj.people.com.cn/GB/375548/index.html news 天津市,"  # 天津_高层动态
        # "http://tj.people.com.cn/GB/375550/index.html news 天津市,"  # 天津_区县新闻
        # "http://tj.people.com.cn/GB/375551/index.html news 天津市,"  # 天津_财经动态
        # "http://tj.people.com.cn/GB/375549/index.html news 天津市,"  # 天津_民生舆情
        # "http://tj.people.com.cn/GB/375557/index.html news 天津市,"  # 天津_生态环保
        # "http://tj.people.com.cn/GB/375799/index.html news 天津市,"  # 天津_法治天津
        # "http://tj.people.com.cn/GB/375552/index.html news 天津市,"  # 天津_教科文
        # "http://tj.people.com.cn/GB/378595/index.html news 天津市,"  # 天津_体育
        # "http://tj.people.com.cn/GB/375800/index.html news 天津市,"  # 天津_医疗卫生
        # "http://tj.people.com.cn/GB/375787/index.html news 天津市,"  # 天津_观点评论
        # "http://he.people.com.cn/GB/200202/index.html news 河北省,"  # 河北_原创新闻
        # "http://he.people.com.cn/GB/197034/index.html news 河北省,"  # 河北_时政
        # "http://he.people.com.cn/GB/197037/index.html news 河北省,"  # 河北_经济
        # "http://he.people.com.cn/GB/338616/index.html news 河北省,"  # 河北_国际
        # "http://he.people.com.cn/GB/197039/index.html news 河北省,"  # 河北_社会
        # "http://he.people.com.cn/GB/197043/index.html news 河北省,"  # 河北_法治
        # "http://he.people.com.cn/GB/338626/index.html news 河北省,"  # 河北_地方动态
        # "http://he.people.com.cn/GB/197046/index.html news 河北省,"  # 河北_科教
        # "http://he.people.com.cn/GB/197355/index.html news 河北省,"  # 河北_健康
        # "http://he.people.com.cn/GB/197051/379525/index.html news 河北省,"  # 河北_交通
        # "http://he.people.com.cn/GB/199852/index.html news 河北省石家庄市,"  # 河北_石家庄
        # "http://he.people.com.cn/GB/197049/382163/index.html news 河北省正定县,"  # 河北_正定新闻
        # "http://he.people.com.cn/GB/197089/384749/386569/386757/index.html news 河北省石家庄市,"  # 河北_石家庄_鹿泉新闻
        # "http://he.people.com.cn/GB/200201/index.html news 河北省,"  # 河北_本网专稿
        # "http://he.people.com.cn/GB/197051/379555/index.html news 河北省,"  # 河北_京津冀
        # "http://he.people.com.cn/GB/197051/379528/index.html news 河北省,"  # 河北_精准扶贫
        # "http://he.people.com.cn/GB/197051/379529/index.html news 河北省,"  # 河北_数据新闻
        # "http://he.people.com.cn/GB/338628/index.html news 河北省,"  # 河北_企业
        # "http://he.people.com.cn/GB/197047/index.html news 河北省,"  # 河北_网评
        # "http://he.people.com.cn/GB/197051/379531/index.html news 河北省,"  # 河北_环保
        # "http://he.people.com.cn/GB/197051/379530/index.html news 河北省,"  # 河北_能源
        # "http://sx.people.com.cn/GB/189130/index.html news 山西省,"  # 山西_山西要闻
        # "http://sx.people.com.cn/GB/189132/index.html news 山西省,"  # 山西_本网关注
        # "http://sx.people.com.cn/GB/352664/index.html news 山西省,"  # 山西_国际国内
        # "http://sx.people.com.cn/GB/189133/index.html news 山西省,"  # 山西_地市链接
        # "http://sx.people.com.cn/GB/189150/index.html news 山西省,"  # 山西_产业经济
        # "http://sx.people.com.cn/GB/189151/index.html news 山西省,"  # 山西_金融
        # "http://sx.people.com.cn/GB/352662/index.html news 山西省,"  # 山西_健康
        # "http://sx.people.com.cn/GB/352650/index.html news 山西省,"  # 山西_教育
        # "http://sx.people.com.cn/GB/353623/index.html news 山西省,"  # 山西_反腐
        # "http://sx.people.com.cn/GB/189139/388656/index.html news 山西省,"  # 山西_融媒体
        # "http://nm.people.com.cn/GB/196667/index.html news 内蒙古自治区,"  # 内蒙古_要闻
        # "http://nm.people.com.cn/GB/196820/index.html news 内蒙古自治区,"  # 内蒙古_人民日报看内蒙古
        # "http://nm.people.com.cn/GB/196689/index.html news 内蒙古自治区,"  # 内蒙古_本网专稿
        # "http://nm.people.com.cn/GB/196693/index.html news 内蒙古自治区,"  # 内蒙古_时政
        # "http://nm.people.com.cn/GB/196688/347185/378036/index.html news 内蒙古自治区呼和浩特市,"  # 内蒙古_呼和浩特要闻
        # "http://nm.people.com.cn/GB/196688/347185/378037/index.html news 内蒙古自治区呼和浩特市,"  # 内蒙古_呼和浩特_人民网看首府
        # "http://nm.people.com.cn/GB/196688/347185/378038/index.html news 内蒙古自治区呼和浩特市,"  # 内蒙古_呼和浩特_两点扫描
        # "http://nm.people.com.cn/GB/196688/347185/378108/index.html news 内蒙古自治区呼和浩特市,"  # 内蒙古_呼和浩特_时政要闻
        # "http://nm.people.com.cn/GB/196702/index.html news 内蒙古自治区,"  # 内蒙古_舆论监督
        # "http://nm.people.com.cn/GB/196688/347185/378043/index.html news 内蒙古自治区呼和浩特市,"  # 内蒙古_呼和浩特_产业经济
        # "http://nm.people.com.cn/GB/196678/index.html news 内蒙古自治区,"  # 内蒙古_社会
        # "http://nm.people.com.cn/GB/346104/346107/index.html news 内蒙古自治区,"  # 内蒙古_热点
        # "http://nm.people.com.cn/GB/196688/347186/index.html news 内蒙古自治区包头市,"  # 内蒙古_包头
        # "http://nm.people.com.cn/GB/196688/347188/index.html news 内蒙古自治区兴安盟市,"  # 内蒙古_兴安盟
        # "http://nm.people.com.cn/GB/196688/347193/index.html news 内蒙古自治区通辽市,"  # 内蒙古_通辽
        # "http://nm.people.com.cn/GB/196688/347190/index.html news 内蒙古自治区赤峰市,"  # 内蒙古_赤峰
        # "http://nm.people.com.cn/GB/196688/347191/index.html news 内蒙古自治区锡林郭勒市,"  # 内蒙古_锡林郭勒
        # "http://nm.people.com.cn/GB/196688/347192/index.html news 内蒙古自治区乌兰察布市,"  # 内蒙古_乌兰察布
        # "http://nm.people.com.cn/GB/196688/347194/index.html news 内蒙古自治区鄂尔多斯市,"  # 内蒙古_鄂尔多斯
        # "http://nm.people.com.cn/GB/196688/347196/index.html news 内蒙古自治区巴彦淖尔市,"  # 内蒙古_巴彦淖尔
        # "http://nm.people.com.cn/GB/196688/347197/index.html news 内蒙古自治区乌海市,"  # 内蒙古_乌海
        # "http://nm.people.com.cn/GB/196688/347198/index.html news 内蒙古自治区阿拉善市,"  # 内蒙古_阿拉善
        # "http://nm.people.com.cn/GB/196688/347199/index.html news 内蒙古自治区满洲里市,"  # 内蒙古_满洲里
        # "http://nm.people.com.cn/GB/196688/347200/index.html news 内蒙古自治区二连浩特市,"  # 内蒙古_二连浩特
        # "http://ln.people.com.cn/GB/378322/index.html news 辽宁省,"  # 辽宁_人民日报看辽宁
        # "http://ln.people.com.cn/GB/378317/index.html news 辽宁省,"  # 辽宁_要闻
        # "http://ln.people.com.cn/GB/378320/index.html news 辽宁省,"  # 辽宁_原创
        # "http://ln.people.com.cn/GB/378326/index.html news 辽宁省,"  # 辽宁_国内时政
        # "http://ln.people.com.cn/GB/378327/index.html news 辽宁省,"  # 辽宁_社会民生
        # "http://ln.people.com.cn/GB/378329/index.html news 辽宁省,"  # 辽宁_国际军事
        # "http://ln.people.com.cn/GB/378330/index.html news 辽宁省,"  # 辽宁_教育健康
        # "http://ln.people.com.cn/GB/378331/index.html news 辽宁省,"  # 辽宁_文娱体育
        # "http://jl.people.com.cn/GB/351793/index.html news 吉林省,"  # 吉林_要闻
        # "http://jl.people.com.cn/GB/351542/index.html news 吉林省,"  # 吉林_人民日报看吉林
        # "http://jl.people.com.cn/GB/351549/index.html news 吉林省,"  # 吉林_专稿
        # "http://jl.people.com.cn/GB/351113/index.html news 吉林省,"  # 吉林_地方新闻
        # "http://jl.people.com.cn/GB/351109/index.html news 吉林省,"  # 吉林_时政
        # "http://jl.people.com.cn/GB/351120/index.html news 吉林省,"  # 吉林_产经
        # "http://jl.people.com.cn/GB/351118/index.html news 吉林省,"  # 吉林_社会
        # "http://jl.people.com.cn/GB/351119/index.html news 吉林省,"  # 吉林_民生
        # "http://jl.people.com.cn/GB/351122/index.html news 吉林省,"  # 吉林_科教
        # "http://jl.people.com.cn/GB/351125/index.html news 吉林省,"  # 吉林_健康
        # "http://hlj.people.com.cn/GB/220024/index.html news 黑龙江省,"  # 黑龙江_专稿
        # "http://hlj.people.com.cn/GB/220027/ news 黑龙江省,"  # 黑龙江_省内要闻
        # "http://hlj.people.com.cn/GB/220075/index.html news 黑龙江省,"  # 黑龙江_地方视窗
        # "http://hlj.people.com.cn/GB/369794/index.html news 黑龙江省,"  # 黑龙江_国际新闻
        # "http://hlj.people.com.cn/GB/369793/index.html news 黑龙江省,"  # 黑龙江_国内新闻
        # "http://hlj.people.com.cn/GB/338553/index.html news 黑龙江省,"  # 黑龙江_社会政法
        # "http://hlj.people.com.cn/GB/220037/ news 黑龙江省,"  # 黑龙江_体育
        # "http://hlj.people.com.cn/GB/338579/358416/358691/index.html news 黑龙江省,"  # 黑龙江_企业资讯
        # "http://hlj.people.com.cn/GB/222646/index.html news 黑龙江省,"  # 黑龙江_热点关注
        # "http://hlj.people.com.cn/GB/338505/index.html news 黑龙江省,"  # 黑龙江_舆情监督
        # "http://hlj.people.com.cn/GB/220026/index.html news 黑龙江省,"  # 黑龙江_人民时评
        # "http://hlj.people.com.cn/GB/220075/220077/351370/index.html news 黑龙江省齐齐哈尔市,"  # 黑龙江_齐齐哈尔_时政
        # "http://hlj.people.com.cn/GB/220075/220077/351369/index.html news 黑龙江省齐齐哈尔市,"  # 黑龙江_齐齐哈尔_领导动态
        # "http://hlj.people.com.cn/GB/220075/220077/351377/index.html news 黑龙江省齐齐哈尔市,"  # 黑龙江_齐齐哈尔_大项目建设
        # "http://hlj.people.com.cn/GB/220075/220077/351379/351380/index.html news 黑龙江省齐齐哈尔市,"  # 黑龙江_齐齐哈尔_地方视窗
        # "http://hlj.people.com.cn/GB/220075/220077/351384/index.html news 黑龙江省齐齐哈尔市,"  # 黑龙江_齐齐哈尔_行业动态
        # "http://hlj.people.com.cn/GB/220075/361643/361644/index.html news 黑龙江省牡丹江市,"  # 黑龙江_牡丹江_时政
        # "http://hlj.people.com.cn/GB/220075/361643/361656/index.html news 黑龙江省牡丹江市,"  # 黑龙江_牡丹江_百姓关注
        # "http://hlj.people.com.cn/GB/220075/361643/361658/index.html news 黑龙江省牡丹江市,"  # 黑龙江_牡丹江_地方视窗
        # "http://hlj.people.com.cn/GB/220075/361643/361648/index.html news 黑龙江省牡丹江市,"  # 黑龙江_牡丹江_项目建设
        # "http://sh.people.com.cn/GB/138654/index.html news 上海市,"  # 上海_要闻
        # "http://sh.people.com.cn/GB/346252/index.html news 上海市,"  # 上海_原创
        # "http://sh.people.com.cn/GB/138656/index.html news 上海市,"  # 上海_看上海
        # "http://sh.people.com.cn/GB/134829/index.html news 上海市,"  # 上海_区县新闻
        # "http://sh.people.com.cn/GB/176738/index.html news 上海市,"  # 上海_经济中心
        # "http://sh.people.com.cn/GB/139965/index.html news 上海市,"  # 上海_金融
        # "http://sh.people.com.cn/GB/176737/index.html news 上海市,"  # 上海_社会|法治
        # "http://sh.people.com.cn/GB/176739/index.html news 上海市,"  # 上海_教育|科技
        # "http://sh.people.com.cn/GB/134819/index.html news 上海市,"  # 上海_美食|健康
        # "http://js.people.com.cn/GB/360297/index.html news 江苏省,"  # 江苏_江苏要闻
        # "http://js.people.com.cn/GB/359574/index.html news 江苏省,"  # 江苏_国内国际
        # "http://js.people.com.cn/GB/360298/index.html news 江苏省,"  # 江苏_评论
        # "http://js.people.com.cn/GB/360300/index.html news 江苏省,"  # 江苏_政治
        # "http://js.people.com.cn/GB/360299/index.html news 江苏省,"  # 江苏_舆情
        # "http://js.people.com.cn/GB/360301/index.html news 江苏省,"  # 江苏_经济
        # "http://js.people.com.cn/GB/360302/index.html news 江苏省,"  # 江苏_民生
        # "http://js.people.com.cn/GB/360303/index.html news 江苏省,"  # 江苏_社会
        # "http://js.people.com.cn/GB/360307/index.html news 江苏省,"  # 江苏_教育
        # "http://js.people.com.cn/GB/361417/359575/index.html news 江苏省南京市,"  # 江苏_南京
        # "http://js.people.com.cn/GB/361417/359575/359601/359604/index.html news 江苏省南京市,"  # 江苏_南京_玄武
        # "http://js.people.com.cn/GB/361417/359575/359601/359607/index.html news 江苏省南京市,"  # 江苏_南京_鼓楼
        # "http://js.people.com.cn/GB/361417/359575/359601/359606/380871/index.html news 江苏省南京市,"  # 江苏_南京_建邺要闻
        # "http://js.people.com.cn/GB/361417/359575/359601/359606/380870/index.html news 江苏省南京市,"  # 江苏_南京_建邺专稿报道
        # "http://js.people.com.cn/GB/361417/359575/359601/359606/380873/index.html news 江苏省南京市,"  # 江苏_南京_建邺民生福祉
        # "http://js.people.com.cn/GB/361417/359575/359601/359606/380874/index.html news 江苏省南京市,"  # 江苏_南京_建邺产经
        # "http://js.people.com.cn/GB/361417/359575/359601/359609/382526/index.html news 江苏省南京市,"  # 江苏_南京_栖霞要闻
        # "http://js.people.com.cn/GB/361417/359575/359601/359609/382527/index.html news 江苏省南京市,"  # 江苏_南京_栖霞城市发展
        # "http://js.people.com.cn/GB/361417/359575/359601/359609/382528/index.html news 江苏省南京市,"  # 江苏_南京_栖霞民生福祉
        # "http://js.people.com.cn/GB/361417/359575/359601/359609/382529/index.html news 江苏省南京市,"  # 江苏_南京_栖霞科教文卫
        # "http://js.people.com.cn/GB/361417/359575/359601/359608/index.html news 江苏省南京市,"  # 江苏_南京_雨花台
        # "http://js.people.com.cn/GB/361417/359575/359601/359605/index.html news 江苏省南京市,"  # 江苏_南京_秦淮
        # "http://js.people.com.cn/GB/361417/359575/359601/359614/371870/index.html news 江苏省南京市,"  # 江苏_南京_溧水要闻
        # "http://js.people.com.cn/GB/361417/359575/359601/359614/372149/index.html news 江苏省南京市,"  # 江苏_南京_溧水社会民生
        # "http://js.people.com.cn/GB/361417/359575/359601/359613/index.html news 江苏省南京市,"  # 江苏_南京_六合
        # "http://js.people.com.cn/GB/361417/359575/359601/359610/index.html news 江苏省南京市,"  # 江苏_南京_浦口
        # "http://js.people.com.cn/GB/361417/359575/359601/359612/index.html news 江苏省南京市,"  # 江苏_南京_江宁
        # "http://js.people.com.cn/GB/361417/359575/359601/359615/index.html news 江苏省南京市,"  # 江苏_南京_高淳
        # "http://js.people.com.cn/GB/361417/359576/index.html news 江苏省苏州市,"  # 江苏_苏州
        # "http://js.people.com.cn/GB/361417/359576/359764/359765/index.html news 江苏省苏州市,"  # 江苏_苏州_张家港
        # "http://js.people.com.cn/GB/361417/359576/359764/359766/index.html news 江苏省苏州市,"  # 江苏_苏州_常熟
        # "http://js.people.com.cn/GB/361417/359576/359764/359770/index.html news 江苏省苏州市,"  # 江苏_苏州_相城
        # "http://js.people.com.cn/GB/361417/359576/359764/359773/index.html news 江苏省苏州市,"  # 江苏_苏州_吴中
        # "http://js.people.com.cn/GB/361417/359576/359764/359769/index.html news 江苏省苏州市,"  # 江苏_苏州_吴江
        # "http://js.people.com.cn/GB/361417/359576/359764/359768/index.html news 江苏省苏州市,"  # 江苏_苏州_昆山
        # "http://js.people.com.cn/GB/361417/359576/359764/359767/index.html news 江苏省苏州市,"  # 江苏_苏州_太仓
        # "http://js.people.com.cn/GB/361417/359576/359764/359772/index.html news 江苏省苏州市,"  # 江苏_苏州_虎丘
        # "http://js.people.com.cn/GB/361417/359576/359764/359771/index.html news 江苏省苏州市,"  # 江苏_苏州_姑苏
        # "http://wuxi.people.com.cn/GB/359628/index.html news 江苏省无锡市,"  # 江苏_无锡要闻
        # "http://wuxi.people.com.cn/GB/359629/index.html news 江苏省无锡市,"  # 江苏_无锡经济
        # "http://wuxi.people.com.cn/GB/359630/index.html news 江苏省无锡市,"  # 江苏_无锡社会民生
        # "http://wuxi.people.com.cn/GB/359632/index.html news 江苏省无锡市,"  # 江苏_无锡科教文卫
        # "http://wuxi.people.com.cn/GB/359645/375151/384623/index.html news 江苏省无锡市,"  # 江苏_无锡_新吴要闻
        # "http://wuxi.people.com.cn/GB/359645/359780/index.html news 江苏省无锡市,"  # 江苏_无锡_梁溪
        # "http://wuxi.people.com.cn/GB/359645/359778/index.html news 江苏省无锡市,"  # 江苏_无锡_滨湖
        # "http://wuxi.people.com.cn/GB/359645/359777/index.html news 江苏省无锡市,"  # 江苏_无锡_惠山
        # "http://wuxi.people.com.cn/GB/359645/359776/index.html news 江苏省无锡市,"  # 江苏_无锡_锡山
        # "http://wuxi.people.com.cn/GB/359645/359775/index.html news 江苏省无锡市,"  # 江苏_无锡_宜兴
        # "http://wuxi.people.com.cn/GB/359645/359774/index.html news 江苏省无锡市,"  # 江苏_无锡_江阴
        # "http://js.people.com.cn/GB/361417/359578/index.html news 江苏省常州市,"  # 江苏_常州
        # "http://js.people.com.cn/GB/361417/359578/359644/359783/index.html news 江苏省常州市,"  # 江苏_常州_金坛
        # "http://js.people.com.cn/GB/361417/359578/359644/359784/index.html news 江苏省常州市,"  # 江苏_常州_溧阳
        # "http://js.people.com.cn/GB/361417/359578/359644/359785/index.html news 江苏省常州市,"  # 江苏_常州_武进
        # "http://js.people.com.cn/GB/361417/359578/359644/359786/index.html news 江苏省常州市,"  # 江苏_常州_新北
        # "http://js.people.com.cn/GB/361417/359578/359644/359787/index.html news 江苏省常州市,"  # 江苏_常州_天宁
        # "http://js.people.com.cn/GB/361417/359578/359644/359788/index.html news 江苏省常州市,"  # 江苏_常州_钟楼
        # "http://js.people.com.cn/GB/361417/359579/index.html news 江苏省镇江市,"  # 江苏_镇江
        # "http://js.people.com.cn/GB/361417/359579/359655/359790/index.html news 江苏省镇江市,"  # 江苏_镇江_丹阳
        # "http://js.people.com.cn/GB/361417/359579/359655/359791/index.html news 江苏省镇江市,"  # 江苏_镇江_句容
        # "http://js.people.com.cn/GB/361417/359579/359655/359792/index.html news 江苏省镇江市,"  # 江苏_镇江_扬中
        # "http://js.people.com.cn/GB/361417/359579/359655/359793/index.html news 江苏省镇江市,"  # 江苏_镇江_丹徒
        # "http://js.people.com.cn/GB/361417/359579/359655/359794/index.html news 江苏省镇江市,"  # 江苏_镇江_京口
        # "http://js.people.com.cn/GB/361417/359579/359655/359795/index.html news 江苏省镇江市,"  # 江苏_镇江_润口
        # "http://js.people.com.cn/GB/361417/359580/index.html news 江苏省扬州市,"  # 江苏_扬州
        # "http://js.people.com.cn/GB/361417/359580/359665/359796/index.html news 江苏省扬州市,"  # 江苏_扬州_宝应
        # "http://js.people.com.cn/GB/361417/359580/359665/359797/index.html news 江苏省扬州市,"  # 江苏_扬州_高邮
        # "http://js.people.com.cn/GB/361417/359580/359665/359798/index.html news 江苏省扬州市,"  # 江苏_扬州_江都
        # "http://js.people.com.cn/GB/361417/359580/359665/359799/index.html news 江苏省扬州市,"  # 江苏_扬州_仪征
        # "http://js.people.com.cn/GB/361417/359580/359665/359800/index.html news 江苏省扬州市,"  # 江苏_扬州_刊江
        # "http://js.people.com.cn/GB/361417/359580/359665/359801/index.html news 江苏省扬州市,"  # 江苏_扬州_广陵
        # "http://js.people.com.cn/GB/361417/359580/359657/index.html news 江苏省扬州市,"  # 江苏_扬州_滚动新闻
        # "http://js.people.com.cn/GB/361417/359581/index.html news 江苏省泰州市,"  # 江苏_泰州
        # "http://js.people.com.cn/GB/361417/359581/359675/359802/388347/index.html news 江苏省泰州市,"  # 江苏_泰州_靖江
        # "http://js.people.com.cn/GB/361417/359581/359675/359802/388330/index.html news 江苏省泰州市,"  # 江苏_泰州_实业靖江
        # "http://js.people.com.cn/GB/361417/359581/359675/359802/388331/index.html news 江苏省泰州市,"  # 江苏_泰州_民生靖江
        # "http://js.people.com.cn/GB/361417/359581/359675/359803/index.html news 江苏省泰州市,"  # 江苏_泰州_泰兴
        # "http://js.people.com.cn/GB/361417/359581/359675/359804/index.html news 江苏省泰州市,"  # 江苏_泰州_姜堰
        # "http://js.people.com.cn/GB/361417/359581/359675/359805/index.html news 江苏省泰州市,"  # 江苏_泰州_高港
        # "http://js.people.com.cn/GB/361417/359581/359675/359806/index.html news 江苏省泰州市,"  # 江苏_泰州_海陵
        # "http://js.people.com.cn/GB/361417/359581/359675/359807/index.html news 江苏省泰州市,"  # 江苏_泰州_兴化
        # "http://js.people.com.cn/GB/361417/359581/359667/index.html news 江苏省泰州市,"  # 江苏_泰州_滚动新闻
        # "http://nantong.people.com.cn/GB/384475/index.html news 江苏省南通市,"  # 江苏_南通_聚焦南通
        # "http://nantong.people.com.cn/GB/384477/index.html news 江苏省南通市,"  # 江苏_南通_专稿报道
        # "http://nantong.people.com.cn/GB/384478/index.html news 江苏省南通市,"  # 江苏_南通_经济
        # "http://nantong.people.com.cn/GB/384479/index.html news 江苏省南通市,"  # 江苏_南通_社会民生
        # "http://nantong.people.com.cn/GB/384480/index.html news 江苏省南通市,"  # 江苏_南通_科教文卫
        # "http://nantong.people.com.cn/GB/359685/359809/364763/index.html news 江苏省南通市,"  # 江苏_南通_海门要闻
        # "http://nantong.people.com.cn/GB/359685/359809/364765/index.html news 江苏省南通市,"  # 江苏_南通_海门社会民生
        # "http://nantong.people.com.cn/GB/359685/359809/364764/index.html news 江苏省南通市,"  # 江苏_南通_海门经济
        # "http://nantong.people.com.cn/GB/359685/359810/index.html news 江苏省南通市,"  # 江苏_南通_通州
        # "http://nantong.people.com.cn/GB/359685/359808/index.html news 江苏省南通市,"  # 江苏_南通_启东
        # "http://nantong.people.com.cn/GB/359685/359811/index.html news 江苏省南通市,"  # 江苏_南通_如皋
        # "http://nantong.people.com.cn/GB/359685/359812/index.html news 江苏省南通市,"  # 江苏_南通_如东
        # "http://nantong.people.com.cn/GB/359685/359813/index.html news 江苏省南通市,"  # 江苏_南通_海安
        # "http://nantong.people.com.cn/GB/359685/359814/index.html news 江苏省南通市,"  # 江苏_南通_崇川
        # "http://nantong.people.com.cn/GB/359685/359815/index.html news 江苏省南通市,"  # 江苏_南通_港闸
        # "http://nantong.people.com.cn/GB/359685/373076/373091/index.html news 江苏省南通市,"  # 江苏_南通_海门桑石桥要闻
        # "http://nantong.people.com.cn/GB/359677/index.html news 江苏省南通市,"  # 江苏_南通_滚动新闻
        # "http://js.people.com.cn/GB/361417/359583/index.html news 江苏省盐城市,"  # 江苏_盐城
        # "http://js.people.com.cn/GB/361417/359583/359695/359816/index.html news 江苏省盐城市,"  # 江苏_盐城_东台
        # "http://js.people.com.cn/GB/361417/359583/359695/359817/370641/index.html news 江苏省盐城市,"  # 江苏_盐城_大丰要闻
        # "http://js.people.com.cn/GB/361417/359583/359695/359818/index.html news 江苏省盐城市,"  # 江苏_盐城_射阳
        # "http://js.people.com.cn/GB/361417/359583/359695/359819/index.html news 江苏省盐城市,"  # 江苏_盐城_建湖
        # "http://js.people.com.cn/GB/361417/359583/359695/359820/index.html news 江苏省盐城市,"  # 江苏_盐城_阜宁
        # "http://js.people.com.cn/GB/361417/359583/359695/359821/index.html news 江苏省盐城市,"  # 江苏_盐城_滨海
        # "http://js.people.com.cn/GB/361417/359583/359695/359822/index.html news 江苏省盐城市,"  # 江苏_盐城_响水
        # "http://js.people.com.cn/GB/361417/359583/359695/359823/374596/index.html news 江苏省盐城市,"  # 江苏_盐城_盐都
        # "http://js.people.com.cn/GB/361417/359583/359695/359823/374599/index.html news 江苏省盐城市,"  # 江苏_盐城_盐都经济
        # "http://js.people.com.cn/GB/361417/359583/359695/359823/374600/index.html news 江苏省盐城市,"  # 江苏_盐城_社会民生
        # "http://js.people.com.cn/GB/361417/359583/359695/359823/374601/index.html news 江苏省盐城市,"  # 江苏_盐城_综合新闻
        # "http://js.people.com.cn/GB/361417/359583/359695/359824/index.html news 江苏省盐城市,"  # 江苏_盐城_亭湖
        # "http://xuzhou.people.com.cn/GB/384674/index.html news 江苏省徐州市,"  # 江苏_徐州_徐州要闻
        # "http://xuzhou.people.com.cn/GB/384676/index.html news 江苏省徐州市,"  # 江苏_徐州_本网专稿
        # "http://xuzhou.people.com.cn/GB/384677/index.html news 江苏省徐州市,"  # 江苏_徐州_政治经济
        # "http://xuzhou.people.com.cn/GB/384678/index.html news 江苏省徐州市,"  # 江苏_徐州_社会民生
        # "http://xuzhou.people.com.cn/GB/384679/index.html news 江苏省徐州市,"  # 江苏_徐州_科教文卫
        # "http://xuzhou.people.com.cn/GB/359715/359825/index.html news 江苏省徐州市,"  # 江苏_徐州_丰县
        # "http://xuzhou.people.com.cn/GB/359715/359827/index.html news 江苏省徐州市,"  # 江苏_徐州_铜山
        # "http://xuzhou.people.com.cn/GB/359715/359828/index.html news 江苏省徐州市,"  # 江苏_徐州_睢宁
        # "http://xuzhou.people.com.cn/GB/359715/359829/index.html news 江苏省徐州市,"  # 江苏_徐州_邳州
        # "http://xuzhou.people.com.cn/GB/359715/359830/index.html news 江苏省徐州市,"  # 江苏_徐州_新沂
        # "http://xuzhou.people.com.cn/GB/359715/359831/index.html news 江苏省徐州市,"  # 江苏_徐州_鼓楼
        # "http://xuzhou.people.com.cn/GB/359715/359832/index.html news 江苏省徐州市,"  # 江苏_徐州_云龙
        # "http://xuzhou.people.com.cn/GB/359715/359833/index.html news 江苏省徐州市,"  # 江苏_徐州_泉山
        # "xuzhou.people.com.cn/GB/359715/359834/index.html news 江苏省徐州市,"  # 江苏_徐州_贾汪
        # "http://js.people.com.cn/GB/361417/359585/index.html news 江苏省连云港市,"  # 江苏_连云港
        # "http://js.people.com.cn/GB/361417/359585/359725/359835/index.html news 江苏省连云港市,"  # 江苏_连云港_赣榆
        # "http://js.people.com.cn/GB/361417/359585/359725/359836/index.html news 江苏省连云港市,"  # 江苏_连云港_东海
        # "http://js.people.com.cn/GB/361417/359585/359725/359837/index.html news 江苏省连云港市,"  # 江苏_连云港_灌云
        # "http://js.people.com.cn/GB/361417/359585/359725/359838/index.html news 江苏省连云港市,"  # 江苏_连云港_灌南
        # "http://js.people.com.cn/GB/361417/359585/359725/359840/index.html news 江苏省连云港市,"  # 江苏_连云港_连云
        # "http://js.people.com.cn/GB/361417/359585/359725/359841/index.html news 江苏省连云港市,"  # 江苏_连云港_海州
        # "http://js.people.com.cn/GB/361417/359585/359717/index.html news 江苏省连云港市,"  # 江苏_连云港_滚动新闻
        # "http://js.people.com.cn/GB/361417/359586/index.html news 江苏省宿迁市,"  # 江苏_宿迁
        # "http://js.people.com.cn/GB/361417/359586/359738/361489/index.html news 江苏省宿迁市,"  # 江苏_宿迁_泗阳
        # "http://js.people.com.cn/GB/361417/359586/359738/359843/index.html news 江苏省宿迁市,"  # 江苏_宿迁_宿豫
        # "http://js.people.com.cn/GB/361417/359586/359738/359844/index.html news 江苏省宿迁市,"  # 江苏_宿迁_沭阳
        # "http://js.people.com.cn/GB/361417/359586/359738/359845/385272/index.html news 江苏省宿迁市,"  # 江苏_宿迁_泗洪要闻
        # "http://js.people.com.cn/GB/361417/359586/359738/359845/385273/index.html news 江苏省宿迁市,"  # 江苏_宿迁_泗洪专稿
        # "http://js.people.com.cn/GB/361417/359586/359738/359845/385275/index.html news 江苏省宿迁市,"  # 江苏_宿迁_泗洪社会民生
        # "http://js.people.com.cn/GB/361417/359586/359738/359846/index.html news 江苏省宿迁市,"  # 江苏_宿迁_宿城
        # "http://huaian.people.com.cn/GB/384956/index.html news 江苏省淮安市,"  # 江苏_淮安要闻
        # "http://huaian.people.com.cn/GB/384957/index.html news 江苏省淮安市,"  # 江苏_淮安专稿
        # "http://huaian.people.com.cn/GB/384958/index.html news 江苏省淮安市,"  # 江苏_淮安经济
        # "http://huaian.people.com.cn/GB/384959/index.html news 江苏省淮安市,"  # 江苏_淮安社会民生
        # "http://huaian.people.com.cn/GB/384960/index.html news 江苏省淮安市,"  # 江苏_淮安科教文卫
        # "http://huaian.people.com.cn/GB/359748/359847/index.html news 江苏省淮安市,"  # 江苏_淮安_清江浦
        # "http://huaian.people.com.cn/GB/359748/359849/380491/index.html news 江苏省淮安市,"  # 江苏_淮安_淮安区要闻
        # "http://huaian.people.com.cn/GB/359748/359849/380494/index.html news 江苏省淮安市,"  # 江苏_淮安_淮安区经济
        # "http://huaian.people.com.cn/GB/359748/359849/380495/index.html news 江苏省淮安市,"  # 江苏_淮安_淮安区社会民生
        # "http://huaian.people.com.cn/GB/359748/359849/380602/index.html news 江苏省淮安市,"  # 江苏_淮安_淮安区科教文卫
        # "http://huaian.people.com.cn/GB/359748/359850/index.html news 江苏省淮安市,"  # 江苏_淮安_江阴
        # "http://huaian.people.com.cn/GB/359748/359851/388006/index.html news 江苏省淮安市,"  # 江苏_淮安_荷都要闻
        # "http://huaian.people.com.cn/GB/359748/359852/index.html news 江苏省淮安市,"  # 江苏_淮安_盱眙
        # "http://huaian.people.com.cn/GB/359748/359853/379032/index.html news 江苏省淮安市,"  # 江苏_淮安_聚焦洪泽
        # "http://huaian.people.com.cn/GB/359748/359854/index.html news 江苏省淮安市,"  # 江苏_淮安_涟水
        # "http://zj.people.com.cn/GB/186938/186949/index.html news 浙江省杭州市,"  # 浙江_杭州
        # "http://zj.people.com.cn/GB/186929/186995/index.html news 浙江省,"  # 浙江_浙江新闻
        # "http://zj.people.com.cn/GB/186935/index.html news 浙江省,"  # 浙江_社会
        # "http://zj.people.com.cn/GB/186943/index.html news 浙江省,"  # 浙江_消费
        # "http://zj.people.com.cn/GB/189773/index.html news 浙江省,"  # 浙江_体育
        # "http://zj.people.com.cn/GB/187005/index.html news 浙江省,"  # 浙江_网摘
        # "http://zj.people.com.cn/GB/186938/186950/index.html news 浙江省宁波市,"  # 浙江_宁波
        # "http://zj.people.com.cn/GB/186938/186951/index.html news 浙江省温州市,"  # 浙江_温州
        # "http://zj.people.com.cn/GB/186938/186952/index.html news 浙江省嘉兴市,"  # 浙江_嘉兴
        # "http://zj.people.com.cn/GB/186938/186953/index.html news 浙江省湖州市,"  # 浙江_湖州
        # "http://zj.people.com.cn/GB/186938/186954/index.html news 浙江省绍兴,"  # 浙江_绍兴
        # "http://zj.people.com.cn/GB/186938/186955/index.html news 浙江省金华,"  # 浙江_金华
        # "http://zj.people.com.cn/GB/186938/186956/index.html news 浙江省衢州,"  # 浙江_衢州
        # "http://zj.people.com.cn/GB/186938/186957/index.html news 浙江省舟山,"  # 浙江_舟山
        # "http://zj.people.com.cn/GB/186938/186958/index.html news 浙江省台州,"  # 浙江_台州
        # "http://zj.people.com.cn/GB/186938/186959/index.html news 浙江省丽水,"  # 浙江_丽水
        # "http://ah.people.com.cn/GB/226938/371897/index.html news 安徽省,"  # 安徽_人民日报看安徽1
        # "http://ah.people.com.cn/GB/226938/380305/index.html news 安徽省,"  # 安徽_人民日报看安徽2
        # "http://ah.people.com.cn/GB/226938/373325/index.html news 安徽省,"  # 安徽_人民日报看安徽3
        # "http://ah.people.com.cn/GB/226938/378917/index.html news 安徽省,"  # 安徽_人民日报看安徽4
        # "http://ah.people.com.cn/GB/358073/358321/index.html news 安徽省,"  # 安徽_有话网上说
        # "http://ah.people.com.cn/GB/358073/358428/index.html news 安徽省,"  # 安徽_要闻
        # "http://ah.people.com.cn/GB/358073/358266/index.html news 安徽省,"  # 安徽_本网特稿
        # "http://ah.people.com.cn/GB/358073/365328/index.html news 安徽省,"  # 安徽_舆情焦点
        # "http://ah.people.com.cn/GB/366345/366711/index.html news 安徽省,"  # 安徽_舆情事件
        # "http://ah.people.com.cn/GB/358073/374164/index.html news 安徽省,"  # 安徽_县区动态
        # "http://ah.people.com.cn/GB/227130/358317/index.html news 安徽省,"  # 安徽_热评网评
        # "http://ah.people.com.cn/GB/227767/index.html news 安徽省,"  # 安徽_名企动态
        # "http://ah.people.com.cn/GB/358073/358338/358339/index.html news 安徽省合肥,"  # 安徽_合肥
        # "http://ah.people.com.cn/GB/358073/358338/358340/index.html news 安徽省芜湖,"  # 安徽_芜湖
        # "http://ah.people.com.cn/GB/358073/358338/358341/index.html news 安徽省安庆,"  # 安徽_安庆
        # "http://ah.people.com.cn/GB/358073/358338/358342/index.html news 安徽省马鞍山,"  # 安徽_马鞍山
        # "http://ah.people.com.cn/GB/358073/358338/358343/index.html news 安徽省阜阳,"  # 安徽_阜阳
        # "http://ah.people.com.cn/GB/358073/358338/358344/index.html news 安徽省滁州,"  # 安徽_滁州
        # "http://ah.people.com.cn/GB/358073/358338/358345/index.html news 安徽省六安,"  # 安徽_六安
        # "http://ah.people.com.cn/GB/358073/358338/358346/index.html news 安徽省宿州,"  # 安徽_宿州
        # "http://ah.people.com.cn/GB/358073/358338/358347/index.html news 安徽省蚌埠,"  # 安徽_蚌埠
        # "http://ah.people.com.cn/GB/358073/358338/358348/index.html news 安徽省淮南,"  # 安徽_淮南
        # "http://ah.people.com.cn/GB/358073/358338/358349/index.html news 安徽省宣城,"  # 安徽_宣城
        # "http://ah.people.com.cn/GB/358073/358338/358350/index.html news 安徽省亳州,"  # 安徽_亳州
        # "http://ah.people.com.cn/GB/358073/358338/358351/index.html news 安徽省淮北,"  # 安徽_淮北
        # "http://ah.people.com.cn/GB/358073/358338/358352/index.html news 安徽省铜陵,"  # 安徽_铜陵
        # "http://ah.people.com.cn/GB/358073/358338/358353/index.html news 安徽省池州,"  # 安徽_池州
        # "http://fj.people.com.cn/GB/234469/index.html news 福建省,"  # 福建_头条
        # "http://fj.people.com.cn/GB/350390/350391/index.html news 福建省,"  # 福建_要闻
        # "http://fj.people.com.cn/GB/234949/index.html news 福建省,"  # 福建_综合
        # "http://fj.people.com.cn/GB/339483/index.html news 福建省,"  # 福建_人民日报看福建
        # "http://fj.people.com.cn/GB/384193/index.html news 福建省,"  # 福建_驻闽央企
        # "http://fj.people.com.cn/GB/373331/373335/index.html news 福建省,"  # 福建_卫健新闻
        # "http://fj.people.com.cn/GB/373331/373344/index.html news 福建省,"  # 福建_健康福建
        # "http://fj.people.com.cn/GB/339045/385327/387971/index.html news 福建省,"  # 福建_闽检之窗
        # "http://fj.people.com.cn/GB/339045/385327/386436/index.html news 福建省,"  # 福建_产业中心
        # "http://jx.people.com.cn/GB/190181/index.html news 江西省,"  # 江西_要闻
        # "http://jx.people.com.cn/GB/190260/index.html news 江西省,"  # 江西_本网专稿
        # "http://jx.people.com.cn/GB/190316/index.html news 江西省,"  # 江西_国内国际
        # "http://jx.people.com.cn/GB/190268/index.html news 江西省,"  # 江西_人事任免
        # "http://jx.people.com.cn/GB/357314/357731/index.html news 江西省南昌市,"  # 江西_南昌经济发展
        # "http://jx.people.com.cn/GB/357314/357729/index.html news 江西省南昌市,"  # 江西_南昌党建工作
        # "http://jx.people.com.cn/GB/357314/357734/index.html news 江西省南昌市,"  # 江西_南昌城市建设
        # "http://jx.people.com.cn/GB/357314/357727/index.html news 江西省南昌市,"  # 江西_南昌要闻
        # "http://jx.people.com.cn/GB/190259/index.html news 江西省,"  # 江西_强赣评论
        # "http://jx.people.com.cn/GB/359142/359151/index.html news 江西省九江市,"  # 江西_中央媒体看九江
        # "http://jx.people.com.cn/GB/359142/359147/index.html news 江西省,"  # 江西_社会
        # "http://jx.people.com.cn/GB/359142/360846/index.html news 江西省,"  # 江西_人事任免
        # "http://jx.people.com.cn/GB/359068/359085/index.html news 江西省景德镇市,"  # 江西_景德镇资讯
        # "http://jx.people.com.cn/GB/359068/359093/index.html news 江西省景德镇市,"  # 江西_中央媒体看瓷都
        # "http://jx.people.com.cn/GB/359071/360836/index.html news 江西省萍乡市,"  # 江西_萍乡新闻
        # "http://jx.people.com.cn/GB/359071/359136/index.html news 江西省萍乡市,"  # 江西_中央媒体看萍乡
        # "http://jx.people.com.cn/GB/359071/359133/index.html news 江西省萍乡市,"  # 江西_萍乡城市建设
        # "http://jx.people.com.cn/GB/359071/359153/index.html news 江西省萍乡市,"  # 江西_萍乡舆情
        # "http://jx.people.com.cn/GB/359071/359134/index.html news 江西省萍乡市,"  # 江西_萍乡民生
        # "http://jx.people.com.cn/GB/359072/359201/index.html news 江西省新余市,"  # 江西_新余要闻
        # "http://jx.people.com.cn/GB/359072/359232/index.html news 江西省新余市,"  # 江西_中央媒体看新余
        # "http://jx.people.com.cn/GB/359072/359202/index.html news 江西省新余市,"  # 江西_新余舆情
        # "http://jx.people.com.cn/GB/359073/359195/index.html news 江西省鹰潭市,"  # 江西_鹰潭要闻
        # "http://jx.people.com.cn/GB/359073/359210/index.html news 江西省鹰潭市,"  # 江西_中央媒体看鹰潭
        # "http://jx.people.com.cn/GB/359073/359213/index.html news 江西省鹰潭市,"  # 江西_鹰潭民生
        # "http://jx.people.com.cn/GB/359073/359214/index.html news 江西省鹰潭市,"  # 江西_鹰潭_社会
        # "http://jx.people.com.cn/GB/190800/338175/338249/index.html news 江西省赣州市,"  # 江西_赣州新闻
        # "http://jx.people.com.cn/GB/190800/338175/338255/index.html news 江西省赣州市,"  # 江西_赣州经济发展
        # "http://jx.people.com.cn/GB/190800/338175/338305/index.html news 江西省赣州市,"  # 江西_赣州_赣南苏区
        # "http://jx.people.com.cn/GB/190800/338175/338253/index.html news 江西省赣州市,"  # 江西_中央媒体看赣州
        # "http://jx.people.com.cn/GB/190800/338175/338307/index.html news 江西省赣州市,"  # 江西_赣州聚焦三农
        # "http://jx.people.com.cn/GB/190800/338175/338311/index.html news 江西省赣州市,"  # 江西_赣州民生舆情
        # "http://jx.people.com.cn/GB/190800/338202/338273/index.html news 江西省宜春市,"  # 江西_宜春要闻
        # "http://jx.people.com.cn/GB/190800/338202/338276/index.html news 江西省宜春市,"  # 江西_中央媒体看宜春
        # "http://jx.people.com.cn/GB/190800/338202/338277/index.html news 江西省宜春市,"  # 江西_宜春_社会法制
        # "http://jx.people.com.cn/GB/190800/338202/338282/index.html news 江西省宜春市,"  # 江西_宜春_医疗健康
        # "http://jx.people.com.cn/GB/190800/338202/338281/index.html news 江西省宜春市,"  # 江西_宜春_聚焦三农
        # "http://jx.people.com.cn/GB/190800/337939/337959/index.html news 江西省上饶市,"  # 江西_上饶要闻
        # "http://jx.people.com.cn/GB/190800/337939/337962/index.html news 江西省上饶市,"  # 江西_中央媒体看上饶
        # "http://jx.people.com.cn/GB/359067/359075/index.html news 江西省吉安市,"  # 江西_吉安要闻
        # "http://jx.people.com.cn/GB/359067/359084/index.html news 江西省吉安市,"  # 江西_中央媒体看吉安
        # "http://jx.people.com.cn/GB/359217/359218/index.html news 江西省抚州市,"  # 江西_抚州要闻
        # "http://jx.people.com.cn/GB/359217/359219/index.html news 江西省抚州市,"  # 江西_中央媒体看抚州
        # "http://jx.people.com.cn/GB/359217/359223/index.html news 江西省抚州市,"  # 江西_抚州民生
        # "http://jx.people.com.cn/GB/369404/369405/index.html news 江西省崇川市,"  # 江西_崇川资讯
        # "http://jx.people.com.cn/GB/369404/369409/index.html news 江西省崇川市,"  # 江西_人民网看崇川
        # "http://jx.people.com.cn/GB/369404/369406/index.html news 江西省崇川市,"  # 江西_崇川社会民生
        # "http://jx.people.com.cn/GB/361980/361981/index.html news 江西省南丰市,"  # 江西_南丰新闻
        # "http://jx.people.com.cn/GB/361980/361982/index.html news 江西省南丰市,"  # 江西_人民网看南丰
        # "http://jx.people.com.cn/GB/361980/361985/index.html news 江西省南丰市,"  # 江西_南丰民生聚焦
        # "http://jx.people.com.cn/GB/379279/379282/index.html news 江西省宜黄市,"  # 江西_宜黄新闻
        # "http://jx.people.com.cn/GB/379279/379283/index.html news 江西省宜黄市,"  # 江西_中央媒体看宜黄
        # "http://jx.people.com.cn/GB/366551/366630/index.html news 江西省上高市,"  # 江西_上高新闻
        # "http://jx.people.com.cn/GB/375315/375322/index.html news 江西省南昌市,"  # 江西_南昌青山湖区新闻
        # "http://jx.people.com.cn/GB/347363/index.html news 江西省,"  # 江西_安全
        # "http://jx.people.com.cn/GB/190800/346776/346907/index.html news 江西省,"  # 江西_国企动态
        # "http://jx.people.com.cn/GB/190800/346776/347862/index.html news 江西省,"  # 江西_国资要闻
        # "http://jx.people.com.cn/GB/190800/346776/346914/index.html news 江西省,"  # 江西_党建工作
        # "http://sd.people.com.cn/GB/166192/index.html news 山东省,"  # 山东_要闻
        # "http://sd.people.com.cn/GB/364532/index.html news 山东省,"  # 山东_本网原创
        # "http://sd.people.com.cn/GB/386905/index.html news 山东省,"  # 山东_产经财经
        # "http://sd.people.com.cn/GB/386903/index.html news 山东省,"  # 山东_文化教育
        # "http://sd.people.com.cn/GB/386907/index.html news 山东省,"  # 山东_能源环保
        # "http://sd.people.com.cn/GB/386900/index.html news 山东省,"  # 山东_社会法治
        # "http://sd.people.com.cn/GB/386901/index.html news 山东省,"  # 山东_军事天地
        # "http://sd.people.com.cn/GB/166202/373025/index.html news 山东省,"  # 山东_时政舆情
        # "http://sd.people.com.cn/GB/386910/index.html news 山东省,"  # 山东_山东各地
        # "http://sd.people.com.cn/GB/386785/index.html news 山东省,"  # 山东_长波短讯
        # "http://sd.people.com.cn/GB/362710/index.html news 山东省,"  # 山东_今日时评
        # "http://sd.people.com.cn/GB/166194/index.html news 山东省,"  # 山东_人民日报看山东
        # "http://henan.people.com.cn/GB/363904/index.html news 河南省,"  # 河南_要闻
        # "http://henan.people.com.cn/GB/356896/index.html news 河南省,"  # 河南_本网专稿
        # "http://henan.people.com.cn/GB/378395/index.html news 河南省,"  # 河南_网络舆情
        # "http://henan.people.com.cn/GB/357261/index.html news 河南省,"  # 河南_时评
        # "http://henan.people.com.cn/GB/378397/index.html news 河南省,"  # 河南_河南各地
        # "http://henan.people.com.cn/GB/356900/index.html news 河南省,"  # 河南_社会
        # "http://henan.people.com.cn/GB/356897/index.html news 河南省,"  # 河南_人民网看河南
        # "http://henan.people.com.cn/GB/356906/index.html news 河南省,"  # 河南_国内
        # "http://henan.people.com.cn/GB/356905/index.html news 河南省,"  # 河南_国际
        # "http://henan.people.com.cn/GB/378399/index.html news 河南省,"  # 河南_民生
        # "http://henan.people.com.cn/GB/378405/index.html news 河南省,"  # 河南_健康
        # "http://hb.people.com.cn/GB/194146/194147/index.html news 湖北省,"  # 湖北_要闻
        # "http://hb.people.com.cn/GB/337099/index.html news 湖北省,"  # 湖北_本网原创
        # "http://hb.people.com.cn/GB/194083/355457/index.html news 湖北省,"  # 湖北_舆情速递
        # "http://hb.people.com.cn/GB/194083/194172/index.html news 湖北省,"  # 湖北_廉政
        # "http://hb.people.com.cn/GB/194084/365909/index.html news 湖北省,"  # 湖北_国内
        # "http://hb.people.com.cn/GB/194084/355474/index.html news 湖北省,"  # 湖北_国际
        # "http://hb.people.com.cn/GB/195932/343732/index.html news 湖北省,"  # 湖北_法制
        # "http://hb.people.com.cn/GB/194087/194097/index.html news 湖北省,"  # 湖北_健康
        # "http://hb.people.com.cn/GB/194086/index.html news 湖北省,"  # 湖北_产经
        # "http://hb.people.com.cn/GB/194083/index.html news 湖北省,"  # 湖北_舆情
        # "http://hb.people.com.cn/GB/194146/index.html news 湖北省,"  # 湖北_湖北各地
        # "http://hb.people.com.cn/GB/194334/index.html news 湖北省,"  # 湖北_人民网看湖北
        # "http://hn.people.com.cn/GB/195194/index.html news 湖南省,"  # 湖南_湖南要闻
        # "http://hn.people.com.cn/GB/337651/index.html news 湖南省,"  # 湖南_本网专稿
        # "http://hn.people.com.cn/GB/208814/index.html news 湖南省,"  # 湖南_人民网看湖南
        # "http://hn.people.com.cn/GB/356376/index.html news 湖南省,"  # 湖南_人事任免
        # "http://hn.people.com.cn/GB/356887/index.html news 湖南省,"  # 湖南_市州在线
        # "http://hn.people.com.cn/GB/338398/index.html news 湖南省,"  # 湖南_国内要闻
        # "http://hn.people.com.cn/GB/338399/index.html news 湖南省,"  # 湖南_国际要闻
        # "http://hn.people.com.cn/GB/356883/index.html news 湖南省,"  # 湖南_社会
        # "http://hn.people.com.cn/GB/356890/index.html news 湖南省,"  # 湖南_法治
        # "http://hn.people.com.cn/GB/195196/index.html news 湖南省,"  # 湖南_网评
        # "http://hn.people.com.cn/GB/356337/index.html news 湖南省,"  # 湖南_卫生
        # "http://hn.people.com.cn/GB/371273/index.html news 湖南省,"  # 湖南_健康
        # "http://gd.people.com.cn/GB/218365/index.html news 广东省,"  # 广东_原创
        # "http://gd.people.com.cn/GB/378386/index.html news 广东省,"  # 广东_要闻
        # "http://gd.people.com.cn/GB/378375/index.html news 广东省,"  # 广东_地市
        # "http://gd.people.com.cn/GB/378376/index.html news 广东省,"  # 广东_社会
        # "http://gd.people.com.cn/GB/378373/index.html news 广东省,"  # 广东_教育
        # "http://gd.people.com.cn/GB/378377/index.html news 广东省,"  # 广东_科技
        # "http://gd.people.com.cn/GB/378378/index.html news 广东省,"  # 广东_财经
        # "http://gd.people.com.cn/GB/378379/index.html news 广东省,"  # 广东_法治
        # "http://gd.people.com.cn/GB/378380/index.html news 广东省,"  # 广东_生态
        # "http://gx.people.com.cn/GB/179430/index.html news 广西省,"  # 广西_广西要闻
        # "http://gx.people.com.cn/GB/179464/index.html news 广西省,"  # 广西_原创新闻
        # "http://gx.people.com.cn/cpc/GB/179666/index.html news 广西省,"  # 广西_党网要闻
        # "http://gx.people.com.cn/GB/179435/index.html news 广西省,"  # 广西_人民日报看壮乡
        # "http://gx.people.com.cn/GB/229247/index.html news 广西省,"  # 广西_国内新闻
        # "http://gx.people.com.cn/GB/229256/index.html news 广西省,"  # 广西_国际新闻
        # "http://gx.people.com.cn/GB/229260/index.html news 广西省,"  # 广西_市县
        # "http://gx.people.com.cn/GB/347802/index.html news 广西省,"  # 广西_行业
        # "http://gx.people.com.cn/GB/179461/index.html news 广西省,"  # 广西_社会法制
        # "http://hi.people.com.cn/GB/231207/index.html news 海南省,"  # 海南_本网原创
        # "http://hi.people.com.cn/GB/231190/ news 海南省,"  # 海南_海南要闻
        # "http://hi.people.com.cn/GB/231187/index.html news 海南省,"  # 海南_时事财经
        # "http://hi.people.com.cn/GB/231186/index.html news 海南省,"  # 海南_社会法治
        # "http://hi.people.com.cn/GB/370012/index.html news 海南省,"  # 海南_海口动态
        # "http://hi.people.com.cn/GB/231190/index.html news 海南省,"  # 海南_海南新闻
        # "http://hi.people.com.cn/GB/231217/336437/index.html news 海南省,"  # 海南_三沙新闻
        # "http://hi.people.com.cn/GB/231217/231233/index.html news 海南省,"  # 海南_儋州
        # "http://hi.people.com.cn/GB/231217/231234/index.html news 海南省,"  # 海南_琼海
        # "http://hi.people.com.cn/GB/231217/231235/index.html news 海南省,"  # 海南_文昌
        # "http://hi.people.com.cn/GB/231217/231230/index.html news 海南省,"  # 海南_东方
        # "http://hi.people.com.cn/GB/231217/231231/index.html news 海南省,"  # 海南_五指山
        # "http://hi.people.com.cn/GB/231217/231232/377823/index.html news 海南省,"  # 海南_万宁要闻
        # "http://hi.people.com.cn/GB/231217/231229/index.html news 海南省,"  # 海南_定安
        # "http://hi.people.com.cn/GB/231217/231228/index.html news 海南省,"  # 海南_屯昌
        # "http://hi.people.com.cn/GB/231217/231227/index.html news 海南省,"  # 海南_澄迈
        # "http://hi.people.com.cn/GB/231217/231226/index.html news 海南省,"  # 海南_临高
        # "http://hi.people.com.cn/GB/231217/231225/index.html news 海南省,"  # 海南_昌江
        # "http://hi.people.com.cn/GB/231217/231224/index.html news 海南省,"  # 海南_乐东
        # "http://hi.people.com.cn/GB/231217/231223/index.html news 海南省,"  # 海南_陵水
        # "http://hi.people.com.cn/GB/231217/231222/index.html news 海南省,"  # 海南_白沙
        # "http://hi.people.com.cn/GB/231217/231221/index.html news 海南省,"  # 海南_保亭
        # "http://hi.people.com.cn/GB/231217/231220/index.html news 海南省,"  # 海南_琼中
        # "http://hi.people.com.cn/GB/231217/231219/index.html news 海南省,"  # 海南_洋浦
        # "http://cq.people.com.cn/GB/365401/367673/index.html news 重庆市,"  # 重庆_原创
        # "http://cq.people.com.cn/GB/365402/ news 重庆市,"  # 重庆_新闻
        # "http://cq.people.com.cn/GB/365411/ news 重庆市,"  # 重庆_区县
        # "http://mcq.people.com.cn/jkpd/class1/ news 重庆市,"  # 重庆_健康要闻
        # "http://mcq.people.com.cn/jkpd/class4/ news 重庆市,"  # 重庆_名医视界
        # "http://mcq.people.com.cn/gy/class1/ news 重庆市,"  # 重庆_公益新闻快报
        # "http://mcq.people.com.cn/gy/class2/ news 重庆市,"  # 重庆_公益发布
        # "http://cq.people.com.cn/GB/365403/ news 重庆市,"  # 重庆_国内新闻
        # "http://cq.people.com.cn/GB/365405/ news 重庆市,"  # 重庆_社会
        # "http://cq.people.com.cn/GB/365408/ news 重庆市,"  # 重庆_评论
        # "http://sc.people.com.cn/GB/345452/345453/index.html news 四川省,"  # 四川_人民日报看四川
        # "http://sc.people.com.cn/GB/387373/388810/index.html news 四川省,"  # 四川_人民日报记者看神州
        # "http://sc.people.com.cn/GB/345452/345509/index.html news 四川省,"  # 四川_新闻资讯
        # "http://sc.people.com.cn/GB/345452/345510/index.html news 四川省,"  # 四川_记者调查
        # "http://sc.people.com.cn/GB/345452/379469/index.html news 四川省,"  # 四川_政商动态
        # "http://sc.people.com.cn/GB/345452/346033/index.html news 四川省,"  # 四川_一周热点
        # "http://sc.people.com.cn/GB/345452/379470/index.html news 四川省,"  # 四川_四川新闻
        # "http://sc.people.com.cn/GB/345452/379471/index.html news 四川省,"  # 四川_成都资讯
        # "http://sc.people.com.cn/GB/345452/345458/index.html news 四川省,"  # 四川_市州资讯
        # "http://sc.people.com.cn/GB/345452/387095/index.html news 四川省,"  # 四川_蓉平资讯
        # "http://sc.people.com.cn/GB/345452/345460/index.html news 四川省,"  # 四川_国内新闻
        # "http://sc.people.com.cn/GB/345452/345462/index.html news 四川省,"  # 四川_港澳台
        # "http://sc.people.com.cn/GB/345452/345461/index.html news 四川省,"  # 四川_海外
        # "http://sc.people.com.cn/GB/345527/index.html news 四川省,"  # 四川_军事
        # "http://sc.people.com.cn/GB/345452/345459/index.html news 四川省,"  # 四川_社会
        # "http://sc.people.com.cn/GB/345529/index.html news 四川省,"  # 四川_科技
        # "http://sc.people.com.cn/GB/345515/index.html news 四川省,"  # 四川_教育
        # "http://sc.people.com.cn/GB/345528/index.html news 四川省,"  # 四川_文化
        # "http://sc.people.com.cn/GB/346399/index.html news 四川省,"  # 四川_卫生
        # "http://gz.people.com.cn/GB/344124/index.html news 贵州省,"  # 贵州_头条
        # "http://gz.people.com.cn/GB/194827/index.html news 贵州省,"  # 贵州_要闻
        # "http://gz.people.com.cn/GB/222152/index.html news 贵州省,"  # 贵州_原创
        # "http://gz.people.com.cn/GB/222174/index.html news 贵州省,"  # 贵州_时评
        # "http://gz.people.com.cn/GB/369574/index.html news 贵州省,"  # 贵州_纪委
        # "http://gz.people.com.cn/GB/194849/index.html news 贵州省,"  # 贵州_地方联播
        # "http://gz.people.com.cn/GB/344103/index.html news 贵州省,"  # 贵州_国际要闻
        # "http://gz.people.com.cn/GB/344102/index.html news 贵州省,"  # 贵州_国内要闻
        # "http://gz.people.com.cn/GB/194831/361177/index.html news 贵州省,"  # 贵州_人民日报看贵州1
        # "http://gz.people.com.cn/GB/194831/361178/index.html news 贵州省,"  # 贵州_人民日报看贵州2
        # "http://gz.people.com.cn/GB/194831/361179/index.html news 贵州省,"  # 贵州_人民日报看贵州3
        # "http://gz.people.com.cn/GB/194831/385620/index.html news 贵州省,"  # 贵州_人民日报看贵州4
        # "http://gz.people.com.cn/GB/222173/index.html news 贵州省,"  # 贵州_党建
        # "http://gz.people.com.cn/GB/361324/index.html news 贵州省,"  # 贵州_社会民生
        # "http://gz.people.com.cn/GB/358160/index.html news 贵州省,"  # 贵州_教育
        # "http://gz.people.com.cn/GB/194864/index.html news 贵州省,"  # 贵州_IT科技
        # "http://gz.people.com.cn/GB/200190/205620/357463/index.html news 贵州省,"  # 贵州_聚焦贵阳
        # "http://gz.people.com.cn/GB/200190/205620/206282/index.html news 贵州省,"  # 贵州_贵阳时政
        # "http://gz.people.com.cn/GB/200190/205620/357464/index.html news 贵州省,"  # 贵州_贵阳社会民生
        # "http://gz.people.com.cn/GB/200190/375231/375236/index.html news 贵州省,"  # 贵州_铜仁时政
        # "http://qxn.people.com.cn/GB/362626/index.html news 贵州省,"  # 贵州_黔西南州头条
        # "http://gz.people.com.cn/GB/200190/371778/371796/index.html news 贵州省,"  # 贵州_贵安动态
        # "http://gz.people.com.cn/GB/200190/381077/389084/index.html news 贵州省,"  # 贵州_毕节动态
        # "http://gz.people.com.cn/GB/200190/383886/383899/index.html news 贵州省,"  # 贵州_黔东南州新闻
        # "http://gz.people.com.cn/GB/200190/386204/index.html news 贵州省,"  # 贵州_安顺
        # "http://gz.people.com.cn/GB/200190/388758/388766/index.html news 贵州省,"  # 贵州_聚焦遵义
        # "http://gz.people.com.cn/GB/200190/388758/388761/index.html news 贵州省,"  # 贵州_遵义时政
        # "http://gz.people.com.cn/GB/200190/217573/217641/index.html news 贵州省,"  # 贵州_习水时政
        # "http://gz.people.com.cn/GB/200190/205621/205813/index.html news 贵州省,"  # 贵州_桐梓时政
        # "http://gz.people.com.cn/GB/200190/374443/374448/index.html news 贵州省,"  # 贵州_水城政务动态
        # "http://gz.people.com.cn/GB/200190/368775/368833/index.html news 贵州省,"  # 贵州_德江时政
        # "http://gz.people.com.cn/GB/200190/369966/369967/index.html news 贵州省,"  # 贵州_新蒲要闻
        # "http://gz.people.com.cn/GB/200190/366762/index.html news 贵州省,"  # 贵州_务川新闻资讯
        # "http://gz.people.com.cn/GB/200190/370430/370433/index.html news 贵州省,"  # 贵州_钟山时政
        # "http://gz.people.com.cn/GB/200190/370430/370434/index.html news 贵州省,"  # 贵州_钟山要闻
        # "http://gz.people.com.cn/GB/200190/373838/373839/index.html news 贵州省,"  # 贵州_白云要闻
        # "http://gz.people.com.cn/GB/200190/374043/389293/index.html news 贵州省,"  # 贵州_独山新闻资讯
        # "http://gz.people.com.cn/GB/200190/375852/index.html news 贵州省,"  # 贵州_仁怀资讯
        # "http://gz.people.com.cn/GB/200190/375818/389361/index.html news 贵州省,"  # 贵州_汇川资讯
        # "http://gz.people.com.cn/GB/200190/372859/372860/index.html news 贵州省,"  # 贵州_思南时政要闻
        # "http://gz.people.com.cn/GB/200190/381330/381334/index.html news 贵州省,"  # 贵州_黎平要闻
        # "http://gz.people.com.cn/GB/200190/381250/381251/index.html news 贵州省,"  # 贵州_修文要闻
        # "http://gz.people.com.cn/GB/200190/201510/index.html news 贵州省,"  # 贵州_瓮安视窗
        # "http://gz.people.com.cn/GB/200190/382947/index.html news 贵州省,"  # 贵州_凤岗动态
        # "http://gz.people.com.cn/GB/200190/384347/384377/index.html news 贵州省,"  # 贵州_开阳资讯
        # "http://gz.people.com.cn/GB/200190/385321/385322/index.html news 贵州省,"  # 贵州_罗甸要闻
        # "http://gz.people.com.cn/GB/200190/386184/389087/index.html news 贵州省,"  # 贵州_镇宁新闻
        # "http://gz.people.com.cn/GB/200190/386253/389359/index.html news 贵州省,"  # 贵州_紫云要闻
        # "http://gz.people.com.cn/GB/369465/386107/index.html news 贵州省,"  # 贵州_安顺开发区要闻
        # "http://gz.people.com.cn/GB/200190/387242/387244/index.html news 贵州省,"  # 贵州_平坝时政
        # "http://gz.people.com.cn/GB/200190/387242/387245/index.html news 贵州省,"  # 贵州_聚焦平坝
        # "http://gz.people.com.cn/GB/200190/386478/386480/index.html news 贵州省,"  # 贵州_西秀时政
        # "http://gz.people.com.cn/GB/200190/386478/386481/index.html news 贵州省,"  # 贵州_聚焦西秀
        # "http://gz.people.com.cn/GB/200190/387063/389149/index.html news 贵州省,"  # 贵州_道真资讯
        # "http://gz.people.com.cn/GB/200190/387830/387832/index.html news 贵州省,"  # 贵州_印江时政
        # "http://gz.people.com.cn/GB/200190/387830/387833/index.html news 贵州省,"  # 贵州_聚焦印江
        # "http://gz.people.com.cn/GB/200190/389356/389357/index.html news 贵州省,"  # 贵州_花溪资讯
        # "http://yn.people.com.cn/GB/378442/index.html news 云南省,"  # 云南_要闻
        # "http://yn.people.com.cn/GB/378439/index.html news 云南省,"  # 云南_云南新闻
        # "http://yn.people.com.cn/GB/372461/index.html news 云南省,"  # 云南_本网原创
        # "http://yn.people.com.cn/GB/372451/index.html news 云南省,"  # 云南_州市要闻
        # "http://yn.people.com.cn/GB/361322/index.html news 云南省,"  # 云南_法治云南
        # "http://yn.people.com.cn/GB/372456/index.html news 云南省,"  # 云南_社会
        # "http://yn.people.com.cn/GB/372452/index.html news 云南省,"  # 云南_生态
        # "http://yn.people.com.cn/GB/372457/index.html news 云南省,"  # 云南_公益
        # "http://yn.people.com.cn/GB/387914/387915/index.html news 云南省,"  # 云南_人民报看云南1
        # "http://yn.people.com.cn/GB/387914/387916/index.html news 云南省,"  # 云南_人民报看云南2
        # "http://yn.people.com.cn/GB/387914/387917/index.html news 云南省,"  # 云南_人民报看云南3
        # "http://yn.people.com.cn/GB/387914/387918/index.html news 云南省,"  # 云南_人民报看云南4
        # "http://yn.people.com.cn/GB/372441/index.html news 云南省,"  # 云南_梅里评论
        # "http://yn.people.com.cn/GB/372450/index.html news 云南省,"  # 云南_州市领导
        # "http://yn.people.com.cn/GB/news/yunnan/375157/index.html news 云南省,"  # 云南_临沧沧源
        # "http://yn.people.com.cn/GB/news/yunnan/376835/379801/index.html news 云南省,"  # 云南_澜沧新闻
        # "http://xz.people.com.cn/GB/389272/index.html news 西藏,"  # 西藏_要闻
        # "http://xz.people.com.cn/GB/389273/index.html news 西藏,"  # 西藏_精准扶贫
        # "http://xz.people.com.cn/GB/389274/index.html news 西藏,"  # 西藏_党建要闻
        # "http://xz.people.com.cn/GB/389275/index.html news 西藏,"  # 西藏_七地市
        # "http://xz.people.com.cn/GB/389276/index.html news 西藏,"  # 西藏_省市援藏
        # "http://xz.people.com.cn/GB/389277/index.html news 西藏,"  # 西藏_央企援藏
        # "http://xz.people.com.cn/GB/349479/index.html news 西藏,"  # 西藏_本网专稿
        # "http://xz.people.com.cn/GB/378471/index.html news 西藏,"  # 西藏_医疗
        # "http://xz.people.com.cn/GB/389271/index.html news 西藏,"  # 西藏_藏区时讯
        # "http://sn.people.com.cn/GB/378310/index.html news 陕西省,"  # 陕西_陕西资讯
        # "http://sn.people.com.cn/GB/378289/379591/index.html news 陕西省,"  # 陕西_208坊
        # "http://sn.people.com.cn/GB/226647/index.html news 陕西省,"  # 陕西_人民网看陕西
        # "http://sn.people.com.cn/GB/190197/index.html news 陕西省,"  # 陕西_要闻
        # "http://sn.people.com.cn/GB/378288/index.html news 陕西省,"  # 陕西_陕西要闻
        # "http://sn.people.com.cn/GB/378311/index.html news 陕西省,"  # 陕西_观点
        # "http://sn.people.com.cn/GB/378291/index.html news 陕西省,"  # 陕西_反腐
        # "http://sn.people.com.cn/GB/378287/index.html news 陕西省,"  # 陕西_国内
        # "http://sn.people.com.cn/GB/378286/index.html news 陕西省,"  # 陕西_国际
        # "http://sn.people.com.cn/GB/378296/index.html news 陕西省,"  # 陕西_社会
        # "http://sn.people.com.cn/GB/378297/index.html news 陕西省,"  # 陕西_法治
        # "http://sn.people.com.cn/GB/378308/index.html news 陕西省,"  # 陕西_盘点
        # "http://sn.people.com.cn/GB/346932/index.html news 陕西省,"  # 陕西_万象
        # "http://gs.people.com.cn/GB/183283/index.html news 甘肃省,"  # 甘肃_要闻
        # "http://gs.people.com.cn/GB/183348/index.html news 甘肃省,"  # 甘肃_本网专稿
        # "http://gs.people.com.cn/GB/183341/index.html news 甘肃省,"  # 甘肃_各地动态
        # "http://gs.people.com.cn/GB/183342/index.html news 甘肃省,"  # 甘肃_特别关注
        # "http://gs.people.com.cn/GB/372500/index.html news 甘肃省,"  # 甘肃_政在回应
        # "http://gs.people.com.cn/GB/183343/index.html news 甘肃省,"  # 甘肃_丝路时评
        # "http://gs.people.com.cn/GB/358973/363516/index.html news 甘肃省,"  # 甘肃_新闻盘点
        # "http://gs.people.com.cn/GB/358973/362596/index.html news 甘肃省,"  # 甘肃_往期回顾
        # "http://gs.people.com.cn/GB/183346/index.html news 甘肃省,"  # 甘肃_人民日报看甘肃
        # "http://gs.people.com.cn/GB/188868/index.html news 甘肃省,"  # 甘肃_杂谈
        # "http://gs.people.com.cn/GB/191680/index.html news 甘肃省,"  # 甘肃_社会
        # "http://gs.people.com.cn/GB/183365/184318/184701/index.html news 甘肃省,"  # 甘肃_兰州要闻
        # "http://gs.people.com.cn/GB/374354/376098/376239/index.html news 甘肃省,"  # 甘肃_武威要闻
        # "http://gs.people.com.cn/GB/183365/183927/386625/index.html news 甘肃省,"  # 甘肃_陇南要闻
        # "http://qh.people.com.cn/GB/182775/index.html news 青海省,"  # 青海_要闻
        # "http://qh.people.com.cn/GB/182757/index.html news 青海省,"  # 青海_社会
        # "http://qh.people.com.cn/GB/378416/index.html news 青海省,"  # 青海_反腐倡廉
        # "http://qh.people.com.cn/GB/382226/index.html news 青海省,"  # 青海_舆情热点
        # "http://qh.people.com.cn/GB/182756/index.html news 青海省,"  # 青海_环保
        # "http://qh.people.com.cn/GB/182755/index.html news 青海省,"  # 青海_科教文卫
        # "http://qh.people.com.cn/GB/378418/index.html news 青海省,"  # 青海_本网专稿
        # "http://qh.people.com.cn/GB/182781/index.html news 青海省,"  # 青海_人民日报看青海
        # "http://nx.people.com.cn/GB/192482/index.html news 宁夏回族自治区,"  # 宁夏_要闻
        # "http://nx.people.com.cn/GB/192465/index.html news 宁夏回族自治区,"  # 宁夏_党政在线
        # "http://nx.people.com.cn/GB/192493/index.html news 宁夏回族自治区,"  # 宁夏_本网原创
        # "http://nx.people.com.cn/GB/212079/index.html news 宁夏回族自治区,"  # 宁夏_评论
        # "http://nx.people.com.cn/GB/378081/index.html news 宁夏回族自治区,"  # 宁夏_环保
        # "http://nx.people.com.cn/GB/192490/index.html news 宁夏回族自治区,"  # 宁夏_法治
        # "http://nx.people.com.cn/GB/192480/index.html news 宁夏回族自治区,"  # 宁夏_健康
        # "http://nx.people.com.cn/GB/378082/index.html news 宁夏回族自治区,"  # 宁夏_公益
        # "http://nx.people.com.cn/GB/192494/index.html news 宁夏回族自治区,"  # 宁夏_农业
        # "http://nx.people.com.cn/GB/192496/index.html news 宁夏回族自治区,"  # 宁夏_教育
        # "http://nx.people.com.cn/GB/192150/index.html news 宁夏回族自治区,"  # 宁夏_人民日报看宁夏
        # "http://nx.people.com.cn/GB/192488/index.html news 宁夏回族自治区,"  # 宁夏_时政
        # "http://xj.people.com.cn/GB/188514/index.html news 新疆维吾尔自治区,"  # 新疆_要闻
        # "http://xj.people.com.cn/GB/219188/index.html news 新疆维吾尔自治区,"  # 新疆_援疆潮涌
        # "http://xj.people.com.cn/GB/388946/388963/index.html news 新疆维吾尔自治区,"  # 新疆_纪检_滚动新闻
        # "http://xj.people.com.cn/GB/388946/388964/index.html news 新疆维吾尔自治区,"  # 新疆_纪检_党风党政
        # "http://xj.people.com.cn/GB/188524/index.html news 新疆维吾尔自治区,"  # 新疆_地州
        # "http://xj.people.com.cn/GB/188522/index.html news 新疆维吾尔自治区,"  # 新疆_经济
        # "http://xj.people.com.cn/GB/188521/index.html news 新疆维吾尔自治区,"  # 新疆_社会
        # "http://xj.people.com.cn/GB/188539/index.html news 新疆维吾尔自治区,"  # 新疆_健康
        # "http://xj.people.com.cn/GB/188518/index.html news 新疆维吾尔自治区,"  # 新疆_人民日报看新疆
        # "http://sz.people.com.cn/GB/235389/index.html news 广东省深圳市,"  # 深圳_人民网看深圳
        # "http://sz.people.com.cn/GB/235382/index.html news 广东省深圳市,"  # 深圳_要闻
        # "http://sz.people.com.cn/cpc/GB/360496/index.html news 广东省深圳市,"  # 深圳_领导动态
        # "http://sz.people.com.cn/cpc/GB/360472/index.html news 广东省深圳市,"  # 深圳_党建要闻
        # "http://sz.people.com.cn/cpc/GB/360498/index.html news 广东省深圳市,"  # 深圳_反腐倡廉
        # "http://sz.people.com.cn/GB/235384/index.html news 广东省深圳市,"  # 深圳_评论
        # "http://sz.people.com.cn/GB/235349/index.html news 广东省深圳市,"  # 深圳_城区
        # "http://sz.people.com.cn/GB/235346/index.html news 广东省深圳市,"  # 深圳_社会
        # "http://sz.people.com.cn/GB/235343/index.html news 广东省深圳市,"  # 深圳_科技
        # "http://sz.people.com.cn/GB/235345/index.html news 广东省深圳市,"  # 深圳_财经
        # "http://sz.people.com.cn/GB/235348/index.html news 广东省深圳市,"  # 深圳_法治
        # "http://sz.people.com.cn/GB/347983/index.html news 广东省深圳市,"  # 深圳_生态
        # "http://sz.people.com.cn/GB/235327/index.html news 广东省深圳市,"  # 深圳_教育
        # "http://sz.people.com.cn/GB/235330/index.html news 广东省深圳市,"  # 深圳_文化
        # "http://sz.people.com.cn/GB/358620/index.html news 广东省深圳市,"  # 深圳_健康
        ]

    old_start_urls = [
        # "http://politics.people.com.cn/GB/1024/index.html news", #时政-高层动态
        # "http://politics.people.com.cn/GB/1027/index.html news", #时政-中央部委
        # "http://politics.people.com.cn/GB/369059/index.html news",#时政-反腐镰鲳
        # "http://politics.people.com.cn/GB/389979/index.html news", #时政-时事解读
        #
        # "http://society.people.com.cn/GB/136657/index.html news",#社会-滚动新闻
        # "http://society.people.com.cn/GB/86800/index.html news",#社会-本网原创
        # "http://society.people.com.cn/GB/41158/index.html news",#百姓民生
        # "http://society.people.com.cn/GB/1062/index.html news",#社会万象

        # "http://legal.people.com.cn/GB/188502/index.html news",#法治-滚动新闻
        # "http://legal.people.com.cn/GB/42729/index.html news",#法治-立法动态
        # "http://legal.people.com.cn/GB/204446/index.html news",#法治-司法关注
        # "http://legal.people.com.cn/GB/204445/index.html news",#法治-行政执法
        # "http://legal.people.com.cn/GB/204447/index.html news",#法治-法制监督

        # "http://world.people.com.cn/GB/157278/index.html news", #国际 - 滚动
        # "http://world.people.com.cn/GB/1030/index.html news",#国际-国际观察
        # "http://world.people.com.cn/GB/1029/index.html news",#国际-时事快报
        # "http://world.people.com.cn/GB/57507/index.html news",#国际-独家
        # "http://world.people.com.cn/GB/57505/index.html news",#国际-图说世界
        # "http://world.people.com.cn/GB/57506/index.html news",#国际-关注中国

        # "http://military.people.com.cn/GB/172467/index.html news",#军事-滚动新闻
        # "http://military.people.com.cn/GB/52963/index.html news",#军事-高层动态
        # "http://military.people.com.cn/GB/115150/index.html news",#军事-国防部
        # "http://military.people.com.cn/GB/52936/index.html news",#军事-本网原创
        # "http://military.people.com.cn/GB/367527/index.html news",#军事-中国军情
        # "http://military.people.com.cn/GB/42969/index.html news",#军事-评论
        # "http://military.people.com.cn/GB/43331/index.html news",#军事-图片报道
        # "http://military.people.com.cn/GB/367540/index.html news",#军事-名家论剑
        # "http://military.people.com.cn/GB/367619/index.html news",#军事-军史

        # "http://tw.people.com.cn/GB/104510/index.html news",#台湾-滚动新闻
        # "http://tw.people.com.cn/GB/14812/14875/index.html news",#台湾-岛内要闻
        # "http://tw.people.com.cn/GB/14812/14874/index.html news",#台湾-社会要闻
        # "http://tw.people.com.cn/GB/71483/index.html news",#台湾-台湾文娱
        # "http://tw.people.com.cn/GB/14810/index.html news",#台湾-涉台新闻
        # "http://tw.people.com.cn/GB/14813/index.html news",#台湾-两岸交流
        # "http://tw.people.com.cn/GB/88649/index.html news",#台湾-台湾军史
        # "http://tw.people.com.cn/GB/157509/index.html news",#台湾-史海珍闻

        # "http://hm.people.com.cn/GB/230533/index.html news",#港澳-滚动新闻
        # "http://hm.people.com.cn/GB/42273/index.html news",#港澳-政经要闻
        # "http://hm.people.com.cn/GB/85423/index.html news",#港澳-港澳内地
        # "http://hm.people.com.cn/GB/85418/index.html news",#港澳-科教文卫
        # "http://hm.people.com.cn/GB/42275/index.html news",#港澳-社会法制
        # "http://hm.people.com.cn/GB/415667/index.html news",#港澳-图说港澳
        ### "http://hm.people.com.cn/GB/42280/index.html news",#港澳-专题  特殊结构

        # "http://pic.people.com.cn/GB/165652/index.html news",#图片-国内
        # "http://pic.people.com.cn/GB/166071/index.html news",#图片-国际
        # "http://pic.people.com.cn/GB/159992/index.html news",#图片-社会
        # "http://pic.people.com.cn/GB/162952/index.html news",#图片-娱乐
        # "http://pic.people.com.cn/GB/164931/index.html news",#图片-探索
        # "http://pic.people.com.cn/GB/164277/index.html news",#图片-档案
        # "http://pic.people.com.cn/GB/224199/index.html news",#图片-记事
        # "http://pic.people.com.cn/GB/224198/index.html news",#图片-趣闻
        # "http://pic.people.com.cn/GB/415374/index.html news",#图片-摄影动态
        # "http://pic.people.com.cn/GB/224560/index.html news",#图片-滚动

        # "http://energy.people.com.cn/GB/71890/index.html news",#能源-滚动
        # "http://energy.people.com.cn/GB/133190/index.html news",#能源-能源经济
        # "http://energy.people.com.cn/GB/140056/index.html news",#能源-本网观点
        # "http://energy.people.com.cn/GB/71894/index.html news",#能源-行业辣评
        # "http://energy.people.com.cn/GB/71891/index.html news",#能源-海外市场
        # "http://energy.people.com.cn/GB/71895/index.html news",#能源-公司新闻
        # "http://energy.people.com.cn/GB/71897/index.html news",#能源-石油
        # "http://energy.people.com.cn/GB/71900/index.html news",#能源-天然气
        # "http://energy.people.com.cn/power/ news",#能源-电力
        # "http://energy.people.com.cn/GB/71898/index.html news",#能源-煤炭
        # "http://energy.people.com.cn/GB/71896/index.html news",#能源-新能源
        # "http://energy.people.com.cn/GB/133184/index.html news",#能源-能人
        # "http://energy.people.com.cn/GB/396326/index.html news",#能源-部委快讯

        # "http://env.people.com.cn/GB/74877/index.html news",#环保-滚动
        # "http://env.people.com.cn/GB/359626/index.html news",#环保-本网原创
        # "http://env.people.com.cn/GB/217507/index.html news",#环保-天气新闻速度
        # "http://env.people.com.cn/GB/219130/index.html news",#环保-曝光台
        # "http://env.people.com.cn/GB/193224/index.html news",#环保-部委信息
        # "http://env.people.com.cn/GB/1075/index.html news",#环保-绿色生活
        # "http://env.people.com.cn/GB/1074/index.html news",#环保-自然生态
        # "http://env.people.com.cn/GB/36686/index.html news",#环保-环保产业
        # "http://env.people.com.cn/GB/1073/index.html news",#环保-防止污染
        # "http://env.people.com.cn/GB/35525/index.html news",#环保-人民环评

        # "http://gongyi.people.com.cn/GB/151650/index.html news",#公益-滚动
        # "http://gongyi.people.com.cn/GB/419333/index.html news",#公益-原创
        # "http://gongyi.people.com.cn/GB/151650/152516/index.html news",#公益-政策法规
        # "http://gongyi.people.com.cn/GB/151650/152542/index.html news",#公益-助学成长
        # "http://gongyi.people.com.cn/GB/151650/152544/index.html news",#公益-医疗救助
        # "http://gongyi.people.com.cn/GB/151650/152511/index.html news",#公益-公益观点
        # "http://gongyi.people.com.cn/GB/151662/index.html news",#公益-公益任务
        # "http://gongyi.people.com.cn/GB/191114/index.html news",#公益-公益组织
        # "http://gongyi.people.com.cn/GB/151658/153096/index.html news",#公益-公益曝光
        # "http://gongyi.people.com.cn/GB/151658/186202/index.html news",#公益-公益活动
        # "http://gongyi.people.com.cn/GB/413802/index.html news",#公益-社会责任

        # "http://chinese.people.com.cn/GB/420164/index.html news",#华人华侨- 滚动新闻
        # "http://chinese.people.com.cn/GB/207230/index.html news",#华人华侨- 本网原创
        # "http://chinese.people.com.cn/GB/420181/index.html news",#华人华侨- 创业投资
        # "http://chinese.people.com.cn/GB/42314/index.html news",#华人华侨- 华人新闻
        # "http://chinese.people.com.cn/GB/89895/index.html news",#华人华侨- 出国提示
        # "http://chinese.people.com.cn/GB/42315/index.html news",#华人华侨- 侨务动态
        # "http://chinese.people.com.cn/GB/155405/index.html news",#华人华侨- 留学移民

        # "http://ccnews.people.com.cn/GB/142052/index.html news",#央企-新闻
        # "http://ccnews.people.com.cn/GB/355691/index.html news",#央企-人事
        # "http://ccnews.people.com.cn/GB/354509/index.html news",#央企-广角
        # "http://ccnews.people.com.cn/GB/142066/index.html news",#央企-直播访谈
        # "http://ccnews.people.com.cn/GB/242789/index.html news",#央企-企业舆情
        # "http://ccnews.people.com.cn/GB/142053/index.html news",#央企-视觉图片
        # "http://ccnews.people.com.cn/GB/142052/index.html news",#央企-滚动
        # "http://ccnews.people.com.cn/GB/142036/index.html news",#央企-独家新闻
        # "http://ccnews.people.com.cn/GB/142058/index.html news",#央企-社会责任化

        # "http://fashion.people.com.cn/GB/157207/157213/index.html news",#时尚-时装-明星穿衣
        # "http://fashion.people.com.cn/GB/157207/157215/index.html news",#时尚-时装-潮流
        # "http://fashion.people.com.cn/GB/157207/157209/index.html news",#时尚-时装-单品
        # "http://fashion.people.com.cn/GB/235956/index.html news",#时尚-时装-产业
        # "http://fashion.people.com.cn/GB/157207/157216/index.html news",#时尚-时装-秀场
        # "http://fashion.people.com.cn/GB/157228/157237/index.html news",#时尚-美容-彩妆
        # "http://fashion.people.com.cn/GB/157228/157235/index.html news",#时尚-美容-评测
        # "http://fashion.people.com.cn/GB/157228/157236/index.html news",#时尚-美容-新品
        # "http://fashion.people.com.cn/GB/157228/157238/index.html news",#时尚-美容-美发
        # "http://fashion.people.com.cn/GB/157229/index.html news",#时尚-美容-美体
        # "http://fashion.people.com.cn/GB/157219/157220/index.html news",#时尚-尚品-珠宝
        # "http://fashion.people.com.cn/GB/157219/157221/index.html news",#时尚-尚品-腕表
        # "http://fashion.people.com.cn/GB/157207/157209/index.html news",#时尚-尚品-名品
        # "http://fashion.people.com.cn/GB/389868/389873/index.html news",#时尚-乐活-美食
        # "http://fashion.people.com.cn/GB/389868/389872/index.html news",#时尚-乐活-健康
        # "http://fashion.people.com.cn/GB/389868/389870/index.html news",#时尚-乐活-家居
        # "http://fashion.people.com.cn/GB/389868/389869/index.html news",#时尚-乐活-婚嫁
        # "http://fashion.people.com.cn/GB/389868/389874/index.html news",#时尚-乐活-玩乐
        # "http://fashion.people.com.cn/GB/156425/156431/index.html news",#时尚-名流-设计师
        # "http://fashion.people.com.cn/GB/156425/389895/index.html news",#时尚-名流-模特
        # "http://fashion.people.com.cn/GB/156425/156426/index.html news",#时尚-名流-星尚情报
        # "http://fashion.people.com.cn/GB/156425/156432/index.html news",#时尚-名流-封面大片

        # "http://auto.people.com.cn/GB/1052/98358/98363/index.html news",#汽车-独家
        # "http://auto.people.com.cn/GB/1049/index.html news",#汽车-国内新闻
        # "http://auto.people.com.cn/GB/173005/index.html news",#汽车-国际新闻
        # "http://auto.people.com.cn/GB/1051/index.html news",#汽车-政策法规
        # "http://auto.people.com.cn/GB/14555/index.html news",##汽车-行业动态
        # "http://auto.people.com.cn/GB/1052/25089/index.html news",#汽车-价格行情
        # "http://auto.people.com.cn/GB/1052/27602/index.html news",#汽车-汽车导购
        # "http://auto.people.com.cn/GB/10309/120257/index.html news",#汽车-先测
        # "http://auto.people.com.cn/GB/1052/81336/index.html news",#汽车-上市新车

        # "http://tc.people.com.cn/GB/183206/index.html news",#通信-原创
        # "http://tc.people.com.cn/GB/183760/index.html news",#通信-运营商
        # "http://tc.people.com.cn/GB/183199/index.html news",#通信-手机导购
        # "http://tc.people.com.cn/GB/183784/index.html news",#通信-手机测评

        # "http://homea.people.com.cn/GB/41392/index.html news",#家电-企业视点
        # "http://homea.people.com.cn/GB/41391/index.html news",#家电-行业焦点

        # "http://jiaju.people.com.cn/GB/151419/index.html news",#家居-人民出品
        # "http://jiaju.people.com.cn/GB/151426/index.html news",#家居-滚动播报
        # "http://jiaju.people.com.cn/GB/155381/index.html news",#家居-潮流世家

        # "http://dengshi.people.com.cn/GB/402720/index.html news",#灯饰频道-灯都要闻
        # "http://dengshi.people.com.cn/GB/402719/index.html news",#灯饰频道-行业资讯
        # "http://dengshi.people.com.cn/GB/402718/index.html news",#灯饰频道-灯会
        # "http://dengshi.people.com.cn/GB/402715/index.html news",#灯饰频道-专利展示
        # "http://dengshi.people.com.cn/GB/402714/index.html news",#灯饰频道-卖场
        # "http://dengshi.people.com.cn/GB/402713/index.html news",#灯饰频道-价格指数
        # "http://dengshi.people.com.cn/GB/402712/index.html news",#灯饰频道-直销基地
        # "http://dengshi.people.com.cn/GB/402711/index.html news",#灯饰频道-精品导购
        # "http://dengshi.people.com.cn/GB/402707/index.html news",#灯饰频道-灯都论坛
        # "http://dengshi.people.com.cn/GB/402606/index.html news",#灯饰频道-高端访谈

        # "http://hongmu.people.com.cn/GB/392170/index.html news",#红木频道-产业资讯
        # "http://hongmu.people.com.cn/GB/392171/index.html news",#红木频道-直播访谈
        # "http://hongmu.people.com.cn/GB/392172/index.html news",#红木频道-行业大家
        # "http://hongmu.people.com.cn/GB/392173/index.html news",#红木频道-特色产区
        # "http://hongmu.people.com.cn/GB/392174/index.html news",#红木频道-名企动态
        # "http://hongmu.people.com.cn/GB/392175/index.html news",#红木频道-工艺鉴赏
        # "http://hongmu.people.com.cn/GB/392176/index.html news",#红木频道-展会信息

        # "http://it.people.com.cn/GB/243510/index.html news",#IT-最新资讯
        # "http://it.people.com.cn/GB/114490/index.html news",#IT-本网原创
        # "http://it.people.com.cn/GB/410496/index.html news",#IT-人民日报报道集
        # "http://it.people.com.cn/GB/411530/index.html news",#IT-图说互联网
        # "http://it.people.com.cn/GB/119390/118342/415651/index.html news",#IT-中国好网民

        # "http://shipin.people.com.cn/GB/114668/index.html news",#食品-政策信息
        # "http://shipin.people.com.cn/GB/395905/index.html news",#食品-24小时
        # "http://shipin.people.com.cn/GB/115280/index.html news",#食品-原创
        # "http://shipin.people.com.cn/GB/395906/index.html news",#食品-百宝袋
        # "http://shipin.people.com.cn/GB/86117/index.html news",#食品-曝光台
        # "http://shipin.people.com.cn/GB/215731/index.html news",#食品-滚动新闻
        # "http://shipin.people.com.cn/GB/418903/index.html news",#食品-原创

        # "http://sports.people.com.cn/GB/22176/index.html news",#体育-滚动
        # "http://sports.people.com.cn/GB/35862/index.html news",#体育-原创
        # "http://sports.people.com.cn/GB/22134/index.html news",#体育-国内足球
        # "http://sports.people.com.cn/GB/22141/index.html news",#体育-国际足球
        # "http://sports.people.com.cn/GB/22149/index.html news",#体育-篮球
        # "http://sports.people.com.cn/GB/22155/index.html news",#体育-综合
        # "http://sports.people.com.cn/GB/22172/index.html news",#体育-评论
        # "http://sports.people.com.cn/GB/31928/242574/index.html news",#体育-图片
        # "http://sports.people.com.cn/GB/31928/index.html news",#体育-专题

        # "http://edu.people.com.cn/GB/1053/index.html news",#教育-滚动
        # "http://edu.people.com.cn/GB/367001/index.html news",#教育-原创
        # "http://edu.people.com.cn/GB/239203/index.html news",#教育-图库
        # "http://edu.people.com.cn/GB/226718/index.html news",#教育-婴幼儿
        # "http://edu.people.com.cn/GB/227057/index.html news",#教育-中小学
        # "http://edu.people.com.cn/GB/227065/index.html news",#教育-大学
        # "http://edu.people.com.cn/GB/208610/index.html news",#教育-职场

        # "http://scitech.people.com.cn/GB/1057/index.html news",#科技-滚动
        # "http://scitech.people.com.cn/GB/59405/index.html news",#科技-独家
        # "http://scitech.people.com.cn/GB/1056/index.html news",#科技-科学界
        # "http://scitech.people.com.cn/GB/41163/index.html news",#科技-产业动态
        # "http://scitech.people.com.cn/GB/53752/index.html news",#科技-发明·创新
        # "http://scitech.people.com.cn/GB/25895/index.html news",#科技-探索·发现
        # "http://scitech.people.com.cn/GB/25893/index.html news",#科技-医学·健康
        # "http://scitech.people.com.cn/GB/25892/index.html news",#科技-航空·航天
        # "http://scitech.people.com.cn/GB/53753/index.html news",#科技-评论

        # "http://ip.people.com.cn/GB/179663/index.html news",#知识产权-滚动
        # "http://ip.people.com.cn/GB/417806/index.html news",#知识产权-地方动态
        # "http://ip.people.com.cn/GB/192430/index.html news",#知识产权-本网原创
        # "http://ip.people.com.cn/GB/417807/index.html news",#知识产权-发明世界
        # "http://ip.people.com.cn/GB/192427/index.html news",#知识产权-法律法规

        # "http://culture.people.com.cn/GB/172318/index.html news",#文化-滚动
        # "http://culture.people.com.cn/GB/87423/index.html news",#文化-原创
        # "http://culture.people.com.cn/GB/27296/index.html news",#文化-评论
        # "http://culture.people.com.cn/GB/22219/index.html news",#文化-媒体联播
        # "http://culture.people.com.cn/GB/40473/70988/index.html news",#文化-影视
        # "http://culture.people.com.cn/GB/40473/40476/index.html news",#文化-演出
        # "http://culture.people.com.cn/GB/405419/index.html news",#文化-文艺星青年

        # "http://book.people.com.cn/GB/69363/index.html news",#读书-新书推荐
        # "http://book.people.com.cn/GB/69365/index.html news",#读书-大众书评

        # "http://media.people.com.cn/GB/40606/index.html news",#传媒-资讯
        # "http://media.people.com.cn/GB/40628/index.html news",#传媒-研究
        # "http://media.people.com.cn/GB/40710/index.html news",#传媒-出刊
        # "http://media.people.com.cn/GB/40757/index.html news",#传媒-出版
        # "http://media.people.com.cn/GB/40724/index.html news",#传媒-广电
        # "http://media.people.com.cn/GB/138367/index.html news",#传媒-电影
        # "http://media.people.com.cn/GB/40728/index.html news",#传媒-互联网
        # "http://media.people.com.cn/GB/408724/index.html news",#传媒-社交媒体
        # "http://media.people.com.cn/GB/40641/index.html news",#传媒-产业
        # "http://media.people.com.cn/GB/408725/index.html news",#传媒-新技术
        # "http://media.people.com.cn/GB/408721/index.html news",#传媒-媒介素养
        # "http://media.people.com.cn/GB/40698/index.html news",#传媒-媒介批评
        # "http://media.people.com.cn/GB/40701/index.html news",#传媒-传媒人物
        # "http://media.people.com.cn/GB/408709/index.html news",#传媒-传媒教育

        # "http://ent.people.com.cn/GB/233357/index.html news",#娱乐-独家
        # "http://ent.people.com.cn/GB/86889/index.html news",#娱乐-图片
        # "http://ent.people.com.cn/GB/1082/index.html news",#娱乐-明星
        # "http://ent.people.com.cn/GB/81372/index.html news",#娱乐-电影
        # "http://ent.people.com.cn/GB/81374/index.html news",#娱乐-电视
        # "http://ent.people.com.cn/GB/1085/index.html news",#娱乐-音乐
        # "http://ent.people.com.cn/GB/42073/index.html news",##娱乐-时尚秀场
        # "http://ent.people.com.cn/GB/42074/index.html news",#娱乐-写真
        # "http://ent.people.com.cn/GB/1083/index.html news",#娱乐-评论
        # "http://ent.people.com.cn/GB/86955/ news",##娱乐-滚动新闻

        # "http://leaders.people.com.cn/GB/70117/index.html news",#领导-人事任免
        # "http://leaders.people.com.cn/GB/70149/index.html news",#领导-执政新举
        # "http://leaders.people.com.cn/GB/70118/index.html news",#领导-贪腐曝光
        # "http://leaders.people.com.cn/GB/70120/index.html news",#领导-热评官场
        # "http://leaders.people.com.cn/GB/70116/index.html news",#领导-理论文章

        # "http://travel.people.com.cn/GB/41636/41644/index.html news",#旅游-业界
        # "http://travel.people.com.cn/GB/41636/41642/index.html news",#旅游-国内
        # "http://travel.people.com.cn/GB/41636/41641/index.html news",#旅游-国际
        # "http://travel.people.com.cn/GB/41636/41640/index.html news",#旅游-争鸣
        # "http://travel.people.com.cn/GB/203376/index.html news",#旅游-原创

        # "http://art.people.com.cn/GB/226026/index.html news",#艺术收藏-资讯
        # "http://art.people.com.cn/GB/206244/356129/index.html news",##艺术收藏-绘画
        # "http://art.people.com.cn/GB/206254/206256/index.html news",#艺术收藏-书法
        # "http://art.people.com.cn/GB/206254/206255/index.html news",#艺术收藏-瓷器
        # "http://art.people.com.cn/GB/206244/356130/index.html news",#艺术收藏-玉石
        # "http://art.people.com.cn/GB/206246/408046/index.html news",#艺术收藏-拍卖
        # "http://art.people.com.cn/GB/206246/408047/index.html news",#艺术收藏-一瓶
        # "http://art.people.com.cn/GB/206261/index.html news",#艺术收藏-论谈
        # "http://art.people.com.cn/GB/206322/index.html news",##艺术收藏-策划

        # "http://caipiao.people.com.cn/GB/373930/index.html news",#彩票-资讯   其余频道打不开

        # "http://game.people.com.cn/GB/48662/index.html news",#游戏-业界动态
        # "http://game.people.com.cn/GB/48661/index.html news",#游戏-游戏资讯
        # "http://game.people.com.cn/GB/163384/index.html news",#游戏-人民评游
        # "http://game.people.com.cn/GB/69328/index.html news",#游戏-美图

        # "http://comic.people.com.cn/ news",#动漫

        # "http://japan.people.com.cn/GB/368232/index.html news",#日本-滚动     #会抽到右侧的公共页，会导致重复，不碍事
        # "http://japan.people.com.cn/GB/35469/index.html news",#日本-时政
        # "http://japan.people.com.cn/GB/35463/index.html news",#日本-财经
        # "http://japan.people.com.cn/GB/35467/index.html news",#日本-社会
        # "http://japan.people.com.cn/GB/35465/index.html news",#日本-文化
        # "http://japan.people.com.cn/GB/368549/index.html news",#日本-旅游
        # "http://japan.people.com.cn/GB/35468/index.html news",#日本-娱乐
        # "http://japan.people.com.cn/GB/35466/index.html news",#日本-数码
        # "http://japan.people.com.cn/GB/368567/index.html news",##日本-图库

        # "http://korea.people.com.cn/GB/407862/index.html news",#韩国-滚动
        # "http://korea.people.com.cn/GB/407881/index.html news",#韩国-时政
        # "http://korea.people.com.cn/GB/407882/index.html news",#韩国-经济
        # "http://korea.people.com.cn/GB/407864/index.html news",#韩国-社会
        # "http://korea.people.com.cn/GB/407883/index.html news",#韩国-文体
        # "http://korea.people.com.cn/GB/407885/index.html news",#韩国-韩愈
        # "http://korea.people.com.cn/GB/407886/index.html news",#韩国-旅游
        # "http://korea.people.com.cn/GB/407887/index.html news",#韩国-留学
        # "http://korea.people.com.cn/GB/407888/index.html news",#韩国-地方
        # "http://korea.people.com.cn/GB/407889/index.html news",#韩国-企业
        # "http://korea.people.com.cn/GB/407890/index.html news",#韩国-视频
        # "http://korea.people.com.cn/GB/407863/index.html news",#韩国-图片

        # "http://bj.people.com.cn/GB/233088/index.html news" , #北京-原创
        # "http://bj.people.com.cn/GB/82837/index.html news" , #北京-时政
        # "http://bj.people.com.cn/GB/82840/index.html news" , #北京-社会
        # "http://bj.people.com.cn/GB/82838/index.html news" , #北京-十六区
        # "http://bj.people.com.cn/GB/233092/index.html news" , #北京-任免
        # "http://bj.people.com.cn/GB/14545/index.html news" , #北京-观察
        # "http://bj.people.com.cn/GB/233086/index.html news" , #北京-国内
        # "http://bj.people.com.cn/GB/233087/index.html news" , #北京-国际
        # "http://bj.people.com.cn/GB/82839/index.html news" , #北京-财经
        # "http://bj.people.com.cn/GB/349239/index.html news" , #北京-科技
        # "http://bj.people.com.cn/GB/82846/index.html news" , #北京-文化
        # "http://bj.people.com.cn/GB/233082/index.html news" , #北京-娱乐
        # "http://bj.people.com.cn/GB/339781/index.html news" , #北京-体育
        # "http://bj.people.com.cn/GB/82841/index.html news" , #北京-教育
        # "http://bj.people.com.cn/GB/233080/index.html news" , #北京-旅游
        # "http://bj.people.com.cn/GB/233081/index.html news" , #北京-健康
        # "http://bj.people.com.cn/video/ news" , #北京-视频
        # "http://bj.people.com.cn/GB/82847/index.html news" , #北京-图片

        # "http://tj.people.com.cn/GB/378596/index.html news" , #天津-国内
        # "http://tj.people.com.cn/GB/375887/index.html news" , #天津-原创
        # "http://tj.people.com.cn/GB/375555/index.html news" , #天津-要闻
        # "http://tj.people.com.cn/GB/375548/index.html news" , #天津-高层
        # "http://tj.people.com.cn/GB/375550/index.html news" , #天津-区县
        # "http://tj.people.com.cn/GB/375551/index.html news" , #天津-财经
        # "http://tj.people.com.cn/GB/375549/index.html news" , #天津-民生
        # "http://tj.people.com.cn/GB/375557/index.html news" , #天津-环保
        # "http://tj.people.com.cn/GB/375799/index.html news" , #天津-法治
        # "http://tj.people.com.cn/GB/375552/index.html news" , #天津-文教
        # "http://tj.people.com.cn/GB/375786/index.html news" , #天津-旅游
        # "http://tj.people.com.cn/GB/378595/index.html news" , #天津-体育
        # "http://tj.people.com.cn/GB/375558/index.html news" , #天津-娱乐
        # "http://tj.people.com.cn/GB/375800/index.html news" , #天津-健康
        # "http://tj.people.com.cn/GB/375560/index.html news" , #天津-视频
        # "http://tj.people.com.cn/GB/375563/index.html news" , #天津-图片
        ### "http://tj.people.com.cn/GB/375899/index.html news" , #天津-专题  特殊结构

        # "http://he.people.com.cn/GB/200202/index.html news" , #河北-原创
        # "http://he.people.com.cn/GB/197034/index.html news" , #河北-时政
        # "http://he.people.com.cn/GB/197037/index.html news" , #河北-经济
        # "http://he.people.com.cn/GB/338616/index.html news" , #河北-国际
        # "http://he.people.com.cn/GB/197039/index.html news" , #河北-社会
        # "http://he.people.com.cn/GB/197043/index.html news" , #河北-法治
        # "http://he.people.com.cn/GB/338626/index.html news" , #河北-地方
        # "http://he.people.com.cn/GB/197046/index.html news" , #河北-科教
        # "http://he.people.com.cn/GB/197339/index.html news" , #河北-旅游
        # "http://he.people.com.cn/GB/197355/index.html news" , #河北-健康
        # "http://he.people.com.cn/GB/197048/index.html news" , #河北-文娱
        # "http://he.people.com.cn/GB/198140/index.html news" , #河北-体育
        # "http://he.people.com.cn/GB/198137/index.html news" , #河北-图片
        # "http://he.people.com.cn/GB/201421/index.html news" , #河北-视频
        # ### "http://he.people.com.cn/GB/197089/index.html news" , #河北-专题  特殊结构
        # "http://he.people.com.cn/GB/197051/379525/index.html news" , #河北-交通
        # "http://he.people.com.cn/GB/337249/index.html news" , #河北-滚动

        # "http://sx.people.com.cn/GB/189132/index.html news" , #山西-本网关注
        # "http://sx.people.com.cn/GB/189130/index.html news" , #山西-山西要闻
        # "http://sx.people.com.cn/GB/352664/index.html news" , #山西-国际国内
        # "http://sx.people.com.cn/GB/189134/index.html news" , #山西-人民日报看山西
        # "http://sx.people.com.cn/GB/189137/index.html news" , #山西-时评
        # "http://sx.people.com.cn/GB/189133/index.html news" , #山西-地市新闻
        # "http://sx.people.com.cn/GB/189147/index.html news" , #山西-社会
        # ### "http://liuyan.people.com.cn/ news" , #山西-地方领导留言板
        # "http://sx.people.com.cn/GB/355362/index.html news" , #山西-人事
        # "http://sx.people.com.cn/GB/353623/index.html news" , #山西-反腐

        # "http://nm.people.com.cn/GB/196667/index.html news",#内蒙古-要闻
        # "http://nm.people.com.cn/GB/196820/index.html news",#内蒙古-看报
        # "http://nm.people.com.cn/GB/196689/index.html news",#内蒙古-撰稿
        # "http://nm.people.com.cn/GB/196689/index.html news",#内蒙古-高清图片
        # "http://nm.people.com.cn/GB/196693/index.html news",#内蒙古-要闻
        # "http://nm.people.com.cn/GB/196690/index.html news",#内蒙古-名声
        # "http://nm.people.com.cn/GB/196692/index.html news",#内蒙古-旅游
        # "http://nm.people.com.cn/GB/196687/index.html news",#内蒙古-文化

        # "http://jl.people.com.cn/GB/351793/index.html news" , #吉林-要闻
        # "http://jl.people.com.cn/GB/351542/index.html news" , #吉林-日报
        # "http://jl.people.com.cn/GB/351549/index.html news" , #吉林-专稿
        # "http://jl.people.com.cn/GB/351756/index.html news" , #吉林-人事
        # "http://jl.people.com.cn/GB/351113/index.html news" , #吉林-地方
        # "http://jl.people.com.cn/GB/351109/index.html news" , #吉林-时政
        # "http://jl.people.com.cn/GB/351120/index.html news" , #吉林-产经
        # "http://jl.people.com.cn/GB/351124/index.html news" , #吉林-旅游
        # "http://jl.people.com.cn/GB/351118/index.html news" , #吉林-社会
        # "http://jl.people.com.cn/GB/351119/index.html news" , #吉林-民生
        # "http://jl.people.com.cn/GB/351122/index.html news" , #吉林-科教
        # "http://jl.people.com.cn/GB/351123/index.html news" , #吉林-文娱
        # "http://jl.people.com.cn/GB/351125/index.html news" , #吉林-健康
        # "http://jl.people.com.cn/GB/351547/index.html news" , #吉林-图片新闻
        # ### "http://travel.people.com.cn/GB/136588/418209/index.html news" , #吉林-对话访谈

        # "http://sh.people.com.cn/GB/138654/index.html news" , #上海-要闻
        # "http://sh.people.com.cn/GB/346252/index.html news" , #上海-原创
        # "http://sh.people.com.cn/GB/138656/index.html news" , #上海-看上海
        # "http://sh.people.com.cn/GB/134829/index.html news" , #上海-区闻
        # "http://sh.people.com.cn/GB/176738/index.html news" , #上海-经济
        # "http://sh.people.com.cn/GB/139965/index.html news" , #上海-金融
        # "http://sh.people.com.cn/GB/176737/index.html news" , #上海-社会
        # "http://sh.people.com.cn/GB/350122/index.html news" , #上海-文娱
        # "http://sh.people.com.cn/GB/176739/index.html news" , #上海-科教
        # "http://sh.people.com.cn/GB/134819/index.html news" , #上海-健康
        # "http://sh.people.com.cn/GB/134836/index.html news" , #上海-图片
        # ###"http://sh.people.com.cn/GB/134855/index.html news" , #上海-视频
        # ###"http://sh.people.com.cn/GB/134952/index.html news" , #上海-专题

        # "http://sd.people.com.cn/GB/166192/index.html news" , #山东-山东要闻
        # "http://sd.people.com.cn/GB/364532/index.html news" , #山东-本网原创
        # "http://sd.people.com.cn/GB/386905/index.html news" , #山东-产经
        # "http://sd.people.com.cn/GB/386903/index.html news" , #山东-教育
        # "http://sd.people.com.cn/GB/386907/index.html news" , #山东-能源
        # "http://sd.people.com.cn/GB/386900/index.html news" , #山东-社会
        # "http://sd.people.com.cn/GB/386901/index.html news" , #山东-军事
        # "http://sd.people.com.cn/GB/386909/index.html news" , #山东-旅游
        # "http://sd.people.com.cn/GB/386915/index.html news" , #山东-娱乐
        # "http://sd.people.com.cn/GB/386784/index.html news" , #山东-理论

        # "http://ah.people.com.cn/GB/358073/358321/index.html news" , #安徽-有话网上说
        # "http://ah.people.com.cn/GB/358073/358428/index.html news" , #安徽-安徽要闻
        # "http://ah.people.com.cn/GB/358073/358266/index.html news" , #安徽-本网关注
        # "http://ah.people.com.cn/GB/358322/index.html news" , #安徽-文体

        # "http://fj.people.com.cn/GB/234469/index.html news" , #福建-头条
        # "http://fj.people.com.cn/GB/350390/350391/index.html news" , #福建-要闻
        # "http://fj.people.com.cn/GB/337006/index.html news" , #福建-原创
        # "http://fj.people.com.cn/GB/234949/index.html news" , #福建-综合
        # "http://fj.people.com.cn/GB/339483/index.html news" , #福建-人民日报看福建
        # "http://fj.people.com.cn/GB/384193/index.html news" , #福建-驻闽央企

        # "http://gx.people.com.cn/GB/179430/index.html news" , #广西-广西要闻
        # "http://gx.people.com.cn/GB/179464/index.html news" , #广西-本网原创
        # "http://gx.people.com.cn/GB/179452/349385/index.html news" , #广西-人事任免
        # "http://gx.people.com.cn/GB/179435/index.html news" , #广西-看壮乡
        # "http://gx.people.com.cn/GB/229247/index.html news" , #广西-国内
        # "http://gx.people.com.cn/GB/229256/index.html news" , #广西-国际
        # "http://gx.people.com.cn/GB/229260/index.html news" , #广西-市县
        # "http://gx.people.com.cn/GB/347802/index.html news" , #广西-行业
        # "http://gx.people.com.cn/GB/179461/index.html news" , #广西-社会
        # "http://gx.people.com.cn/GB/352278/352281/index.html news" , #广西-房产

        # "http://js.people.com.cn/GB/360297/index.html news" , #江苏-江苏要闻
        # "http://js.people.com.cn/GB/359574/index.html news" , #江苏-国际国内
        # "http://js.people.com.cn/GB/360298/index.html news" , #江苏-评论
        # "http://js.people.com.cn/GB/360300/index.html news" , #江苏-政治
        # "http://js.people.com.cn/GB/360299/index.html news" , #江苏-舆情
        # "http://js.people.com.cn/GB/360301/index.html news" , #江苏-经济
        # "http://js.people.com.cn/GB/360309/index.html news" , #江苏-房产
        # "http://js.people.com.cn/GB/360302/index.html news" , #江苏-民生
        # "http://js.people.com.cn/GB/360303/index.html news" , #江苏-社会
        # "http://js.people.com.cn/GB/360307/index.html news" , #江苏-教育
        # "http://js.people.com.cn/culture/GB/index.html news" , #江苏-文化
        # "http://js.people.com.cn/GB/360311/index.html news" , #江苏-旅游
        # "http://js.people.com.cn/GB/360313/index.html news" , #江苏-娱乐
        # "http://js.people.com.cn/GB/359726/index.html news" , #江苏-专稿
        # "http://js.people.com.cn/GB/360445/index.html news" , #江苏-视频
        # "http://js.people.com.cn/GB/360444/index.html news" , #江苏-图片

        # "http://gd.people.com.cn/GB/218365/index.html news" , #广东-原创
        # "http://gd.people.com.cn/GB/378386/index.html news" , #广东-要闻
        # "http://gd.people.com.cn/GB/378375/index.html news" , #广东-地市
        # "http://gd.people.com.cn/GB/378376/index.html news" , #广东-社会
        # "http://gd.people.com.cn/GB/378373/index.html news" , #广东-教育
        # "http://gd.people.com.cn/GB/378377/index.html news" , #广东-科技
        # "http://gd.people.com.cn/GB/378378/index.html news" , #广东-财经
        # "http://gd.people.com.cn/GB/378379/index.html news" , #广东-法治
        # "http://gd.people.com.cn/GB/378380/index.html news" , #广东-生态
        # "http://gd.people.com.cn/GB/378381/index.html news" , #广东-旅游
        # "http://gd.people.com.cn/GB/378382/index.html news" , #广东-文化
        # "http://gd.people.com.cn/GB/378383/index.html news" , #广东-娱乐
        # "http://gd.people.com.cn/GB/378384/index.html news" , #广东-体育
        # "http://gd.people.com.cn/GB/378385/index.html news" , #广东-健康
        # "http://gd.people.com.cn/GB/367502/index.html news" , #广东-图说

        # "http://jx.people.com.cn/GB/190181/index.html news" , #江西-江西要闻
        # "http://jx.people.com.cn/GB/190260/index.html news" , #江西-本网专稿
        # "http://jx.people.com.cn/GB/373329/index.html news" , #江西-强赣排行
        # "http://jx.people.com.cn/GB/190316/index.html news" , #江西-国内国际
        # "http://jx.people.com.cn/GB/190268/index.html news" , #江西-人事
        # "http://jx.people.com.cn/GB/190271/index.html news" , #江西-财经

        # "http://hb.people.com.cn/GB/194146/194147/index.html news" , #湖北-湖北
        # "http://hb.people.com.cn/GB/337099/index.html news" , #湖北-原创
        # "http://hb.people.com.cn/GB/194083/355457/index.html news" , #湖北-舆情
        # "http://hb.people.com.cn/GB/194084/365909/index.html news" , #湖北-国内
        # "http://hb.people.com.cn/GB/194084/355474/index.html news" , #湖北-国际
        # "http://hb.people.com.cn/GB/195932/343732/index.html news" , #湖北-法制
        # "http://hb.people.com.cn/GB/195932/index.html news" , #湖北-民生
        # "http://hb.people.com.cn/GB/194087/194097/index.html news" , #湖北-健康
        # "http://hb.people.com.cn/GB/194087/194088/index.html news" , #湖北-文体
        # "http://hb.people.com.cn/GB/194086/index.html news" , #湖北-产经
        # "http://hb.people.com.cn/GB/343605/index.html news" , #湖北-娱乐

        # "http://hn.people.com.cn/GB/195194/index.html news" , #湖南-湖南要闻
        # "http://hn.people.com.cn/GB/337651/index.html news" , #湖南-本网专稿
        # "http://hn.people.com.cn/GB/208814/index.html news" , #湖南-人民日报看湖南
        # "http://hn.people.com.cn/GB/356376/index.html news" , #湖南-人事任免
        # "http://hn.people.com.cn/GB/356887/index.html news" , #湖南-市州县域
        # "http://hn.people.com.cn/GB/356338/index.html news" , #湖南-旅游

        # "http://ha.people.com.cn/GB/363904/index.html news" , #河南-要闻
        # "http://ha.people.com.cn/GB/356896/index.html news" , #河南-专稿
        # "http://ha.people.com.cn/GB/378395/index.html news" , #河南-舆情
        # "http://ha.people.com.cn/GB/357261/index.html news" , #河南-时评
        # "http://ha.people.com.cn/GB/378397/index.html news" , #河南-各地
        # "http://ha.people.com.cn/GB/357262/index.html news" , #河南-人事
        # "http://ha.people.com.cn/GB/356900/index.html news" , #河南-社会
        # "http://ha.people.com.cn/GB/378401/index.html news" , #河南-文化
        # "http://ha.people.com.cn/GB/378405/index.html news" , #河南-卫生
        # "http://ha.people.com.cn/GB/378404/index.html news" , #河南-旅游
        # "http://ha.people.com.cn/GB/378403/index.html news" , #河南-汽车

        # "http://hlj.people.com.cn/GB/220024/index.html news" , #黑龙江-原创
        # "http://hlj.people.com.cn/GB/220027/ news" , #黑龙江-要闻
        # "http://hlj.people.com.cn/GB/220031/index.html news" , #黑龙江-人事
        # "http://hlj.people.com.cn/GB/220075/index.html news" , #黑龙江-地市
        # "http://hlj.people.com.cn/GB/220021/index.html news" , #黑龙江-视频
        # "http://hlj.people.com.cn/GB/338545/338550/index.html news" , #黑龙江-旅游
        # "http://hlj.people.com.cn/GB/369793/index.html news" , #黑龙江-国内
        # "http://hlj.people.com.cn/GB/369794/index.html news" , #黑龙江-国际
        # "http://hlj.people.com.cn/GB/338553/index.html news" , #黑龙江-社会
        # "http://hlj.people.com.cn/GB/338545/338546/index.html news" , #黑龙江-文化
        # "http://hlj.people.com.cn/GB/220036/index.html news" , #黑龙江-娱乐
        # "http://hlj.people.com.cn/GB/220037/ news" , #黑龙江-体育
        # "http://hlj.people.com.cn/GB/368181/index.html news" , #黑龙江-健康
        # "http://hlj.people.com.cn/GB/338554/index.html news" , #黑龙江-教育

        # "http://cq.people.com.cn/GB/365401/ news" , #重庆-原创
        # "http://cq.people.com.cn/GB/365402/ news" , #重庆-重庆
        # "http://cq.people.com.cn/GB/365411/ news" , #重庆-区县
        # "http://cq.people.com.cn/GB/365403/ news" , #重庆-国内
        # "http://cq.people.com.cn/GB/365405/ news" , #重庆-社会
        # "http://cq.people.com.cn/GB/365408/ news" , #重庆-评论
        # "http://cq.people.com.cn/GB/365425/ news" , #重庆-人民日报看重庆

        # "http://sc.people.com.cn/GB/345452/345453/index.html news" , #四川-人民日报看四川
        # "http://sc.people.com.cn/GB/345452/345509/index.html news" , #四川-资讯
        # "http://sc.people.com.cn/GB/345452/345510/index.html news" , #四川-调查
        # "http://sc.people.com.cn/GB/345452/379469/index.html news" , #四川-政商
        # "http://sc.people.com.cn/GB/345452/346033/index.html news" , #四川-一周热点
        # "http://sc.people.com.cn/GB/365870/367402/index.html news" , #四川-市州书记之声
        # "http://sc.people.com.cn/GB/345452/379470/index.html news" , #四川-四川
        # "http://sc.people.com.cn/GB/345452/379471/index.html news" , #四川-成都
        # "http://sc.people.com.cn/GB/345452/345458/index.html news" , #四川-市州

        # "http://yn.people.com.cn/GB/378442/index.html news" , #云南-要闻
        # "http://yn.people.com.cn/GB/378439/index.html news" , #云南-云南
        # "http://yn.people.com.cn/GB/372463/index.html news" , #云南-图片
        # "http://yn.people.com.cn/GB/372461/index.html news" , #云南-原创
        # "http://yn.people.com.cn/GB/372451/index.html news" , #云南-州市
        # "http://yn.people.com.cn/GB/361322/index.html news" , #云南-法治
        # "http://yn.people.com.cn/GB/372456/index.html news" , #云南-社会
        # "http://yn.people.com.cn/GB/372455/index.html news" , #云南-财经
        # "http://yn.people.com.cn/GB/372453/index.html news" , #云南-旅游
        # "http://yn.people.com.cn/GB/372452/index.html news" , #云南-生态
        # "http://yn.people.com.cn/GB/372314/index.html news" , #云南-体育
        # "http://yn.people.com.cn/GB/372315/index.html news" , #云南-娱乐
        # "http://yn.people.com.cn/GB/372457/index.html news" , #云南-公益
        # "http://yn.people.com.cn/GB/372458/index.html news" , #云南-历史

        # "http://gz.people.com.cn/GB/344124/index.html news" , #贵州-头条
        # "http://gz.people.com.cn/GB/194827/index.html news" , #贵州-要闻
        # "http://gz.people.com.cn/GB/222152/index.html news" , #贵州-原创
        # "http://gz.people.com.cn/GB/222174/index.html news" , #贵州-时评
        # "http://gz.people.com.cn/GB/194834/index.html news" , #贵州-人事
        # "http://gz.people.com.cn/GB/369574/index.html news" , #贵州-纪委
        # "http://gz.people.com.cn/GB/194849/index.html news" , #贵州-地方
        # "http://gz.people.com.cn/GB/222162/index.html news" , #贵州-视频
        # "http://gz.people.com.cn/GB/344102/index.html news" , #贵州-社会
        # "http://gz.people.com.cn/GB/344103/index.html news" , #贵州-军事
        # "http://gz.people.com.cn/GB/358160/index.html news" , #贵州-教育
        # "http://gz.people.com.cn/GB/370110/index.html news" , #贵州-文化
        # "http://gz.people.com.cn/GB/372080/index.html news" , #贵州-企业

        # "http://xz.people.com.cn/GB/378509/index.html news" , #西藏-热点新闻
        # "http://xz.people.com.cn/GB/139208/index.html news" , #西藏-时政
        # "http://xz.people.com.cn/GB/139188/index.html news" , #西藏-经济
        # "http://xz.people.com.cn/GB/139196/index.html news" , #西藏-援藏
        # "http://xz.people.com.cn/GB/139189/index.html news" , #西藏-社会
        # "http://xz.people.com.cn/GB/139190/index.html news" , #西藏-科教
        # "http://xz.people.com.cn/GB/139194/index.html news" , #西藏-环保
        # "http://xz.people.com.cn/GB/378508/index.html news" , #西藏-驻村故事
        # "http://xz.people.com.cn/GB/349479/index.html news" , #西藏-本网原创

        # "http://sn.people.com.cn/GB/190197/190210/index.html news" , #陕西-政务
        # "http://sn.people.com.cn/GB/378313/index.html news" , #陕西-人事
        # "http://sn.people.com.cn/GB/378311/index.html news" , #陕西-观点
        # "http://sn.people.com.cn/GB/226647/index.html news" , #陕西-原创
        # "http://sn.people.com.cn/GB/226647/364905/ news" , #陕西-视界
        # "http://sn.people.com.cn/GB/378303/index.html news" , #陕西-旅游
        # "http://sn.people.com.cn/GB/378289/379591/index.html news" , #陕西-208坊
        # "http://sn.people.com.cn/GB/378310/index.html news" , #陕西-资讯回看
        # "http://sn.people.com.cn/GB/378298/378371/index.html news" , #陕西-人民娱乐

        # "http://gs.people.com.cn/GB/183283/index.html news",#甘肃-甘肃要闻
        # "http://gs.people.com.cn/GB/183348/index.html news",#甘肃-本网撰稿
        # "http://gs.people.com.cn/GB/183341/index.html news",#甘肃-各地动态
        # "http://gs.people.com.cn/GB/183342/index.html news",#甘肃-特别关注
        # "http://gs.people.com.cn/GB/372500/index.html news",##甘肃-正在回应
        # "http://gs.people.com.cn/GB/183343/index.html news",#甘肃-丝路食品
        # "http://gs.people.com.cn/GB/366766/index.html news",#甘肃-绚丽甘肃
        # "http://gs.people.com.cn/GB/358973/363516/index.html news",#甘肃-新闻盘点
        # "http://gs.people.com.cn/GB/358973/362596/index.html news",#甘肃-头条回顾

        # "http://xj.people.com.cn/GB/188514/index.html news" , #新疆-要闻
        # "http://xj.people.com.cn/GB/219188/index.html news" , #新疆-援疆
        # "http://xj.people.com.cn/GB/188535/index.html news" , #新疆-政务
        # "http://xj.people.com.cn/GB/188524/index.html news" , #新疆-地州
        # "http://xj.people.com.cn/GB/188522/index.html news" , #新疆-经济
        # "http://xj.people.com.cn/GB/188521/index.html news" , #新疆-社会
        # "http://xj.people.com.cn/GB/188533/index.html news" , #新疆-旅游
        # "http://xj.people.com.cn/GB/188539/index.html news" , #新疆-健康
        # "http://xj.people.com.cn/GB/188532/index.html news" , #新疆-文体
        # "http://xj.people.com.cn/GB/219077/index.html news" , #新疆-历史
        # "http://xj.people.com.cn/GB/362096/index.html news" , #新疆-原创

        # "http://qh.people.com.cn/GB/182775/index.html news" , #青海-青海要闻
        # "http://qh.people.com.cn/GB/182757/index.html news" , #青海-社会法治
        # "http://qh.people.com.cn/GB/378416/index.html news" , #青海-反腐倡廉
        # "http://qh.people.com.cn/GB/382226/index.html news" , #青海-舆情热点
        # "http://qh.people.com.cn/GB/182756/index.html news" , #青海-环保城建
        # "http://qh.people.com.cn/GB/182792/index.html news" , #青海-旅行生活
        # "http://qh.people.com.cn/GB/182754/index.html news" , #青海-金融财税
        # "http://qh.people.com.cn/GB/182762/index.html news" , #青海-体育娱乐
        # "http://qh.people.com.cn/GB/182755/index.html news" , #青海-科教文卫

        # "http://nx.people.com.cn/GB/192482/index.html news" , #宁夏-要闻
        # "http://nx.people.com.cn/GB/192465/index.html news" , #宁夏-党政
        # "http://nx.people.com.cn/GB/357515/index.html news" , #宁夏-人事
        # "http://nx.people.com.cn/GB/192493/index.html news" , #宁夏-原创
        # "http://nx.people.com.cn/GB/212079/index.html news" , #宁夏-评论
        # "http://nx.people.com.cn/GB/192484/index.html news" , #宁夏-财经
        # "http://nx.people.com.cn/GB/192483/index.html news" , #宁夏-旅游
        # "http://nx.people.com.cn/GB/378080/index.html news" , #宁夏-园区
        # "http://nx.people.com.cn/GB/378081/index.html news" , #宁夏-环保
        # "http://nx.people.com.cn/GB/192490/index.html news" , #宁夏-法治
        # "http://nx.people.com.cn/GB/192480/index.html news" , #宁夏-健康
        # "http://nx.people.com.cn/GB/192494/index.html news" , #宁夏-农业
        # "http://nx.people.com.cn/GB/192496/index.html news" , #宁夏-教育
        # "http://nx.people.com.cn/GB/192481/index.html news" , #宁夏-娱乐
        #
        # "http://sz.people.com.cn/GB/235389/index.html news" , #深圳-原创
        # "http://sz.people.com.cn/GB/235382/index.html news" , #深圳-要闻
        # "http://sz.people.com.cn/GB/235349/index.html news" , #深圳-城区
        # "http://sz.people.com.cn/GB/235346/index.html news" , #深圳-社会
        # "http://sz.people.com.cn/GB/235343/index.html news" , #深圳-科技
        # "http://sz.people.com.cn/GB/235345/index.html news" , #深圳-财经
        # "http://sz.people.com.cn/GB/235348/index.html news" , #深圳-法治
        # "http://sz.people.com.cn/GB/347983/index.html news" , #深圳-生态
        # "http://sz.people.com.cn/GB/235326/index.html news" , #深圳-旅游
        # "http://sz.people.com.cn/GB/235327/index.html news" , #深圳-教育
        # "http://sz.people.com.cn/GB/235330/index.html news" , #深圳-文化
        # "http://sz.people.com.cn/GB/235328/index.html news" , #深圳-娱乐
        # "http://sz.people.com.cn/GB/358620/index.html news" , #深圳-健康
        # "http://sz.people.com.cn/GB/352055/index.html news" , #深圳-视界

        # "http://bbs1.people.com.cn/board/1.html forum",#论坛-强国论坛
        # "http://bbs1.people.com.cn/board/1/129.html forum",#论坛-新闻论坛
        # "http://bbs1.people.com.cn/board/6.html forum",#论坛-纵横国际
        # "http://bbs1.people.com.cn/board/7.html forum",#论坛-军迷营地
        # "http://bbs1.people.com.cn/board/71.html forum",#论坛-百姓监督
        # "http://bbs1.people.com.cn/board/60.html forum",#论坛-煮酒论史
        # "http://bbs1.people.com.cn/board/124.html forum",#论坛-人民瓷坛
        # "http://bbs1.people.com.cn/board/131.html forum",#论坛-育儿宝
        # "http://bbs1.people.com.cn/board/8.html forum",#论坛-教育
        # "http://bbs1.people.com.cn/board/57.html forum",#论坛-房产
        # "http://bbs1.people.com.cn/board/11.html forum",#论坛-经济
        # "http://bbs1.people.com.cn/board/2.html forum",#论坛-深入讨论
        # "http://bbs1.people.com.cn/board/1/29.html forum",#论坛-贴图园地
        # "http://bbs1.people.com.cn/board/1/27.html forum",#论坛-娱乐杂谈
        # "http://bbs1.people.com.cn/board/26.html forum",#论坛-女性论坛
        # "http://bbs1.people.com.cn/board/23.html forum",#论坛-时尚生活
        # "http://bbs1.people.com.cn/board/44.html forum",#论坛-文化沙龙
        # "http://bbs1.people.com.cn/board/24.html forum",#论坛-联谊会馆
        # "http://bbs1.people.com.cn/board/80.html forum",#论坛-大学生

        # "http://blog.people.com.cn/jsp/type/politics.jsp blog",#博客-时政
        # "http://blog.people.com.cn/jsp/type/society.jsp blog",#博客-社会
        # "http://blog.people.com.cn/jsp/type/lianzheng.jsp blog",#博客-廉政
        # "http://blog.people.com.cn/jsp/type/zatan.jsp blog",#博客-杂谈
        # "http://blog.people.com.cn/jsp/type/military.jsp blog",#博客-军事
        # "http://blog.people.com.cn/jsp/type/economic.jsp blog",#博客-经济
        # "http://blog.people.com.cn/jsp/type/edu.jsp blog",#博客-教育
        # "http://blog.people.com.cn/jsp/type/cul.jsp blog",#博客-文史
        # "http://blog.people.com.cn/jsp/type/ent.jsp blog",#博客-娱乐
        # "http://blog.people.com.cn/jsp/type/life.jsp blog",#博客-生活

        # "http://qgblog.people.com.cn/society/ blog",#博客-社会2
        # "http://qgblog.people.com.cn/lianzheng/ blog",#博客-廉政2
        # "http://qgblog.people.com.cn/zatan/ blog",#博客-杂谈2
        # "http://qgblog.people.com.cn/economic/ blog",#博客-经济2
        # "http://qgblog.people.com.cn/edu/ blog",#博客-教育2
        # "http://qgblog.people.com.cn/military/ blog",#博客-军队2
        # "http://qgblog.people.com.cn/ent/ blog",#博客-娱乐2
        # "http://qgblog.people.com.cn/cul/ blog",#博客-文史2
        # "http://qgblog.people.com.cn/life/ blog",#博客-生活2
        # "http://qgblog.people.com.cn/peopledaily/ blog",#博客-记者
    ]
    Debug = True
    doredis = True
    source = u"人民网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {'DEFAULT_REQUEST_HEADERS': {
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'},
                       "DOWNLOAD_TIMEOUT": 120.0, "DOWNLOAD_DELAY": 0.25, "ROBOTSTXT_OBEY": False,
                       "CLOSESPIDER_TIMEOUT": 10800}
    sta = {"eff": 0, "inv": 0, "warn": 0, "all": 0, "inv2": 0, "no_time": 0, "no_medianame": 0}

    def print_info(self, info, flag="success", count=True):
        if flag == "error":
            color = "31"
            self.sta["inv"] += [0, 1][count]
        elif flag == "no_time":
            color = "33"
            self.sta["no_time"] += [0, 1][count]
        elif flag == "no_medianame":
            color = "33"
            self.sta["no_medianame"] += [0, 1][count]
        elif flag == "error2":
            color = "35"
            self.sta["inv2"] += [0, 1][count]
        elif flag == "warn":
            color = "33"
            self.sta["warn"] += [0, 1][count]
        else:
            self.sta["eff"] += [0, 1][count]
            color = "32"
        print('\033[0;' + color + ';0m')
        print('*' * 100)
        if color == "31":
            print "抛出异常: ", info
        elif color == "33":
            print "警告： ", info
        else:
            print "信息: ", info
        print "统计: ",
        print "有效:", self.sta["eff"], " 无效: ", self.sta["inv"], " 警告: ", self.sta["warn"], " 人为失效:", self.sta["inv2"], \
            " 乐观总计:", self.sta["all"], " 采集率:", "%.2f%%" % (
                    float(self.sta["eff"]) / float(self.sta["all"] - self.sta["warn"] - self.sta["inv"]) * 100), \
            "无时间: ", self.sta["no_time"], " 无发布源: ", self.sta["no_medianame"]
        print('*' * 100)
        print('\033[0m')

    def __init__(self, start_url=None):
        super(people_news, self).__init__()
        jobs = self.start_urls
        self.debug_file = codecs.open('people_com_ajax_json.log', 'a', encoding='utf-8')
        for job in jobs:
            self.post_params.append({"url": job.split()[0], "ba_type": job.split()[1],
                                     "area": job.split()[-1]})
        dispatcher.connect(self.initial, signals.engine_started)

    def __del__(self):
        self.debug_file.close()

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                                     port=self.configure.yq_filter_db_other.port,
        #                                     db=self.configure.yq_filter_db_other.db,
        #                                     password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            yield Request(url=channel["url"], method='get', meta={"ba_type": channel["ba_type"],
                                                                  },
                          callback=self.parse_link)

    def get_parse_link_urls(self, response, url):  # 排序有讲究，有改良方案，后续再说吧
        urls_list = [
            "//div[@id='Searchresult']/ul/li/a/@href" # 首页滚动新闻
            "//div[@class='ej_img_box clear clearfix']/div/strong/a/@href",  # 日本-图库
            "//div[@class='ej_list_box clear']//ul[contains(@class,'mt10')]/li[not(contains(@class,'more'))]/a/@href",
            # 时政
            "//ul[contains(@class,'mt20')]/li[not(contains(@class,'more'))]/a/@href",  # 国际
            "//dd/h2/a/@href",  # 国际-国际观察，
            "//div[@class='p2j_list fl']/ul/li/a/@href",  # 社会
            "//i[@class='gray']/../a/@href",  # 法制， 半通用
            "//div[contains(@class,'mt30')]/div/div[2]/div/strong/a/@href",  # 军事-图片报道
            "//div[contains(@class,'hdNews clearfix')]/p/strong/a/@href",  # 能源-通用
            "//div[contains(@class,'hdNews clearfix')]//h4/a/@href",  # 艺术收藏-通用
            "//h6[@class='purple2']/../ul/li/b/a/@href",  # 时尚-通用
            "//dl/dd/a/@href",  # 汽车-通用
            "//h2[@class='tit1']/../ul/li/a/@href",  # 灯饰频道-通用
            "//div[@class='ej_list']/ul/li/a/@href",  # IT-通用
            "//h3[@class='clear']/../ul/li/a/@href",  # 食品-通用
            "//div[@class='pic clearfix']/ul/li/a[1]/@href",  # 教育-图库
            "//h3[@class='blue']/../ul/li/a/@href",  # 彩票-通用
            "//h6[@class='lujing clearfix m10']/../ul/li/a/@href",  # 游戏-通用
            "//div[@class='ej_left ']/ul[@class='list_14  ']/li/a/@href",  # 安徽-通用
            "//b/../../h3/../ul/li/a/@href",  # 广西-通用
            "//ul[@class='list_14 d2_2']/li/a/@href",  # 湖北-通用
            "//p[contains(@class,'treeTitle')]//a[@class='treeReply']/@href",  # 论坛类
            "//p[@class='tableTitle']/a/@href",  # 论坛类2
            "//ul[@class='dot14']/li/span/a/@href",  # 博客类
            "//img[@alt]/../../../../ul//li/a[1]/@href",  # 垫底 最特别 IT-图说互联网 通用，
        ]

        for url_xpath in urls_list:
            print(response.body)
            if len(response.xpath(url_xpath).extract()) > 0:
                print url, " 本次套用:", url_xpath, " 条目数:", len(response.xpath(url_xpath).extract())
                return url_xpath

        raise Exception("error: 未发现合适的频道页xpath")

    def parse_link(self, response):
        try:
            if "qgblog.people.com" in response.url:  # 博客类2 特别
                urls_list_string = response.xpath("//div[@id='Searchresult']/..").extract()[0]
                urls_list = re.findall(r"http.*?html?", str(urls_list_string))
                urls = urls_list[0:30]
            else:
                urls = response.xpath(self.get_parse_link_urls(response, response.url)).extract()
            self.sta["all"] += len(urls)
            for index, url in enumerate(urls):
                final = urlparse.urljoin(response.url, url).strip()
                # if self.doredis and self.expire_redis.exists(final):
                #     continue
                if re.search(r"-(\d{1})\.html", final):
                    final = re.sub(r"-(\d{1})\.html", ".html", final)  # 修正一些翻页的，不从第一页开始
                yield Request(url=final, method='get',
                              meta={"ba_type": response.meta["ba_type"], "parse_for_content": True},
                              callback=self.parse_item, errback=self.parse_err_detail)
        except Exception, e:
            print response.url, e.message

    def parse_err_detail(self, failure):
        response = failure.value.response
        self.print_info("页面异常: " + response.url + "  状态：" + str(response.status), "error")
        self.debug_file.write("页面异常: " + response.url + "  状态：" + str(response.status), "error")

    def parse_item(self, response):
        try:
            if response.meta["parse_for_content"]:
                item = DataItem()

                pubtime1 = response.xpath("//*[@id='pubTime']/text()").extract() or \
                           response.xpath("//div[@class='tips']/p[4]/span/text()").extract()
                if len(pubtime1) > 0:
                    item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", pubtime1[0]).group(0)

                # 4视频类  #5 tw.people 通用  #6极少数  #第三种图片新闻的来源格式  #7 极少数   #9 论坛类  #10 博客类
                pubtime2 = response.xpath("//div[@class='box01']//div[@class='fl']") or \
                           response.xpath("//div[@class='tool']/h5") or \
                           response.xpath("//div[@class='page_c']//div[@class='fr']") or \
                           response.xpath("//h3[@class='sub']/../p") or \
                           response.xpath("//div[@class='page_c']/a/..") or \
                           response.xpath("//i[@id='p_publishtime']") or \
                           response.xpath(u"//h2[contains(text(),'来源：')]") or \
                           response.xpath(u"//h1/p[contains(text(),'来源：')]") or \
                           response.xpath("//p[@class='replayInfo']") or \
                           response.xpath("//div[@class='p1_right wb_left']//p[@class='txt_c'][1]/i")

                if len(pubtime2) > 0 and len(pubtime1) == 0:
                    pubtime2 = pubtime2[0].xpath('string(.)').extract()[0].strip().replace("年", "-").replace("月",
                                                                                                             "-").replace(
                        "日", " ")
                    item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                                                pubtime2.replace(".", "-")).group(0)

                if len(pubtime2) == 0 and len(pubtime1) == 0:
                    self.print_info(response.url + "  这个详细页无发布时间！！！", "no_time", True)
                    if response.headers.has_key('Last-Modified'):
                        item['pubtime'] = datetime.datetime.strptime(response.headers["Last-Modified"],
                                                                     '%a, %d %b %Y %H:%M:%S GMT').strftime(
                            "%Y-%m-%d %H:%M")

                item["type"] = response.meta["ba_type"]
                # item["area"] = response.meta["area"]
                if "//world.people.com" in response.url:
                    item['area'] = u'国际'
                else:
                    item['area'] = u'全国'
                item['source'] = self.source
                item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
                item['url'] = response.url

                #   #2 论坛类通用  #3博客通用
                title1 = response.xpath("//h1[@id='p_title']") or \
                         response.xpath("//div[@class='navBar']/h2") or \
                         response.xpath("//div[@class='p1_right wb_left']/h2/b") or \
                         response.xpath("//h1")
                item["title"] = ""
                if len(title1) > 0:
                    item['title'] = title1[0].xpath('string(.)').extract()[0].strip()
                if item["title"] == "":
                    self.print_info(response.url + "  这个详细页无标题！！！", "warn", False)
                    item["title"] = response.xpath("//title/text()").extract()[0]

                item['content'] = ""
                # 1 普通  #3 论坛类  #4 博客类
                content = response.xpath("//div[@class='box_con']").extract() or \
                          response.xpath("//div[@id='p_content']").extract() or \
                          response.xpath("//div[@class='article scrollFlag']").extract() or \
                          response.xpath("//div[@class='p1_right wb_left']").extract()
                if len(content) > 0:
                    item['content'] = content[0]
                # 图片类   垫底 极少数-http://gx.people.com.cn/n2/2018/0615/c179461-31709650.html   #
                content2 = response.xpath("//div[@class='pic']").extract() or \
                           response.xpath("//div[@class='pic_c clearfix']").extract() or \
                           response.xpath("//div[@class='content clear clearfix']").extract() or \
                           response.xpath("//dd[@id='picG']/..").extract() or \
                           response.xpath("//dl[@class='clearfix']/..").extract()
                if len(content2) > 0 and len(content) == 0:
                    item['content'] = content2[0]
                # 视频类
                content3 = response.xpath("//div[@class='v-intro']").extract()
                if len(content3) > 0 and len(content2) == 0 and len(content) == 0:
                    item['content'] = content3[0]
                if item['content'] == "":
                    raise Exception("无详细内容！！！！")

                medianame1 = response.xpath("//div[@class='box01']//div[@class='fl']") or \
                             response.xpath("//span[@id='p_origin']") or \
                             response.xpath("//div[@class='tool']/h5") or \
                             response.xpath(u"//h2[contains(text(),'来源：')]/a")

                # 1图片通用  2tw.people 通用  #3 4极少数  #5论坛类  #6博客类
                medianame2 = response.xpath("//div[@class='pic_c clearfix']//div[@class='fr']/a/text()").extract() or \
                             response.xpath("//div[@class='page_c']/a/text()").extract() or \
                             response.xpath("//i[@id='p_origin']/a/text()").extract() or \
                             response.xpath(u"//h1/p[contains(text(),'来源：')]/a/text()").extract() or \
                             response.xpath("//ul[contains(@class,'author')]//font/text()").extract() or \
                             response.xpath("//div[@class='p1_left wb_right']//h2/text()").extract()

                item['medianame'] = ""
                if len(medianame1) > 0:
                    medianame1 = medianame1.xpath('string(.)').extract()[0].strip()
                    if len(re.findall(ur"(来源|出处|来自|稿源|出自|来源于)", medianame1)) > 0:
                        item["medianame"] = re.search(u'.*?(来源|出处|来自|稿源|出自|来源于)\s*[：:]\s*(\S*)', medianame1).group(2)
                    else:
                        item["medianame"] = medianame1
                if len(medianame2) > 0 and len(medianame1) == 0:
                    item["medianame"] = medianame2[0].strip()

                if item["medianame"] == "" or (u"年" in item["medianame"] and u"月" in item["medianame"]):
                    self.print_info(item['title'] + " " + response.url + "  这个详细页无来源！！！", "no_medianame", True)
                    item["medianame"] = u"人民网"

                # 论坛类部分页面需要额外获取content内容
                if item['type'] == "forum" and (
                        len(response.xpath("//div[@class='article scrollFlag']/@content_path").extract()) > 0):
                    url = response.xpath("//div[@class='article scrollFlag']/@content_path").extract()[0].strip()
                    yield Request(url=url, method='get', meta={"item": item}, callback=self.parse_forum_detail,
                                  errback=self.parse_err_detail)
                    return

                # 图片类专有
                total_pages1 = response.xpath("//div[@class='page_n']/a").extract()
                total_pages2 = response.xpath("//div[@class='zdfy clearfix']/a").extract()

                if len(total_pages1) > 0:
                    total_pages = len(total_pages1) - 1
                elif len(total_pages2) > 0 and len(total_pages1) == 0:
                    total_pages = len(total_pages2)
                else:
                    total_pages = 1  # 图片类
                if total_pages > 1:
                    if len(response.xpath("//div[@class='content clear clearfix']").extract()) > 0:
                        item["content"] += response.xpath("//div[@class='content clear clearfix']").extract()[
                            0]  # 这个网站的图片类详细页很特殊，分为图片内容和文字内容。
                    url = response.url.replace(".html", "-2.html")
                    yield Request(url=url, method='get',
                                  meta={"ba_type": response.meta["ba_type"], "item": item,
                                        "parse_for_content": False, "total_pages": total_pages, "current_page": 2},
                                  callback=self.parse_item, errback=self.parse_err_detail)
                else:
                    if item['pubtime'] and item['title'] and item['content']:
                        self.print_info("发布时间: " + item['pubtime'] + " 标题: " + item["title"] + '\n' + " 发布源: " + item[
                            'medianame'] + " url: " + response.url + "  共1页")
                        yield item
                    else:
                        print "*******************************************************************************不合格？"
                        print "pubtime:", item['pubtime']
                        print "title:", item['title']
                        print response.url
            else:
                item = response.meta["item"]
                content = response.xpath("//div[@class='pic_c clearfix']").extract() or \
                          response.xpath("//div[@class='content clear clearfix']").extract() or \
                          response.xpath("//div[@class='box_con']").extract() or \
                          response.xpath("//dd[@id='picG']/..").extract() or \
                          response.xpath("//div[@id='p_content']").extract() or \
                          response.xpath("//dl[@class='clearfix']/..").extract()
                content = content[0]
                item["content"] += "/n" + content
                if int(response.meta["current_page"]) == int(response.meta["total_pages"]):
                    if item['pubtime'] and item['title'] and item['content']:
                        self.print_info("发布时间: " + item['pubtime'] + " 标题: " + item["title"] + '\n' + " 发布源: " + item[
                            'medianame'] + " url: " + response.url + "  共" + str(response.meta["current_page"]) + "页")
                        yield item
                else:
                    url = response.url.replace("-" + str(response.meta["current_page"]) + ".html",
                                               "-" + str(response.meta["current_page"] + 1) + ".html")
                    yield Request(url=url, method='get',
                                  meta={"ba_type": response.meta["ba_type"], "item": item,
                                        "parse_for_content": False, "total_pages": response.meta["total_pages"],
                                        "current_page": response.meta["current_page"] + 1},
                                  callback=self.parse_item, errback=self.parse_err_detail)
        except Exception:
            if len(response.xpath("//title/text()").extract()) > 0 and \
                    (u"页面没有找到" in response.xpath("//title/text()").extract()[0] or u"出错啦" in
                     response.xpath("//title/text()").extract()[0]):
                self.print_info(traceback.format_exc() + "url:" + response.url + "  status: " + str(response.status),
                                "error")
            else:
                self.print_info(traceback.format_exc() + "url:" + response.url + "  status: " + str(response.status),
                                "error2")

    def parse_forum_detail(self, response):
        item = response.meta["item"]
        item["content"] = response.body
        if item['pubtime'] and item['title'] and item['content']:
            self.print_info("发布时间: " + item['pubtime'] + " 标题: " + item["title"] + '\n' + " 发布源: " + item[
                'medianame'] + " url: " + response.url + "  共1页")
            yield item
