#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
__author__ = 'wjm'
import re
import time
import sys
import scrapy
import json
import codecs
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


class chinanews(scrapy.Spider):
    # name和文件名一致
    name = 'china_news'
    start_urls = [
        ### "http://channel.chinanews.com/cns/cl/ty-sc.shtml news",  # 赛车  这个频道没有url可取
        ### "http://www.zj.chinanews.com/detail/1506512.shtml news",  # 中国新闻社图文信息发布网_详细 显示不存在
        "http://www.bt.chinanews.com/zhongya/index.shtml news",  # 中亚信息
        "http://www.yn.chinanews.com/pub/news/fashion/lvyou/ news",  # 云南新闻网_旅游
        ### "http://www.hn.chinanews.com/news/hxrwyw/ news",  # 中国新闻网_人物聚焦 # 空的
        ### "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=131&ClassTitle=%26%2320307%3B%26%2332946%3B%26%2323089%3B%26%2320048%3B news",  # 中国新闻网_重庆体娱 404

        "http://channel.chinanews.com/cns/cl/hwjy-hxdt.shtml news",  # 中国新闻网_华校动态 太旧了 很多都删了

        ## "http://www.gd.chinanews.com/index/hwqp.html news",  # 中国新闻网_海外侨批 太旧了
        ## ### "http://sports.chinanews.com/ news",  # 中国新闻网_体育娱乐 这是个首页类型
        ## "http://www.ln.chinanews.com/qicheweiquan news",  # 辽宁新闻网_汽车维权 404
        ## "http://www.jx.chinanews.com/gangao/ news",  # 中国新闻网_江西港澳 404
        ## "http://www.jx.chinanews.com/entertainment/ news",  # 中国新闻网_娱乐 404
        ## "http://www.bt.chinanews.com/YanL/ news",  # 兵团新闻网_言论 404
        ## "http://www.hn.chinanews.com/whcy/ news",  # 中国新闻网_文化创意 访问超时
        ## "http://www.sd.chinanews.com/html/channel/gnrd_1_0.html news",  # 中国新闻网_山东国内热点 404
        ## "http://channel.chinanews.com/u/yl/shishang.shtml news",  # 时尚 504
        ## "http://channel.chinanews.com/cns/cl/it-tx.shtml news",  # 通信 空的

        ## "http://channel.chinanews.com/cns/cl/estate-nr.shtml news",  # 中国新闻网_牛人 太旧了
        ## "http://www.bt.chinanews.com/Zhong/ news",  # 兵团新闻网_纵横 404
        ## "http://www.gz.chinanews.com/wsqw/index.shtml news",  # 中国新闻网_贵州外事侨务 空的
        "http://channel.chinanews.com/cns/cl/edu-qzcy.shtml news",  # 中国新闻网_教育求职就业 太旧
        ## "http://www.bt.chinanews.com/Article/xinshu/ news",  # 兵团新闻网_新书 404
        ### "http://www.gs.chinanews.com/ news",  # 中国新闻网_甘肃频道 首页
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=125&ClassTitle=%26%2326333%3B%26%2320809%3B%26%2321488%3B news",  # 中国新闻网_重庆曝光台 404
        ## "http://www.zj.chinanews.com/list/31/1.html news",  # 中国新闻网_社会百态 删除了
        ## "http://www.ln.chinanews.com/liangxing news",  # 辽宁新闻网_两性 404
        ### "http://www.chinanews.com/huaren/index.shtml news",  # 中国新闻网_华人 首页
        ### "http://www.chinanews.com/shipin/cnstv/view.shtml news",  # 中国新闻网_中新网视频 首页
        "http://channel.chinanews.com/cns/cl/edu-jsyd.shtml news",  # 中国新闻网_教育教师园地 太旧
        ## "http://www.sd.chinanews.com/html/channel/sdyw_1_0.html news",  # 中国新闻网_山东要闻 404
        ## "http://www.qd.chinanews.com/health/focus/ news",  # 中国新闻网_健康热点 找不到服务器
        ## "http://www.sd.chinanews.com/html/channel/zxsjzksd_1_0.html news",  # 中国新闻网_记者看山东 404

        ### "http://www.yn.chinanews.com/pub/html/special/dehong/ news",  # 中国新闻网_美丽的地方 算是首页的结构

        ## "http://www.gs.chinanews.com/lsjy1/m1.html news",  # 中国新闻网_人物访谈 空的
        ## "http://www.gz.chinanews.com/spxw/index.shtml news",  # 中国新闻网_贵州视频新闻 空的
        ## "http://bbs.chinanews.com/forumdisplay.php?fid=44 news",  # 论坛 找不到服务器
        ## "http://www.ln.chinanews.com/nongyejishu news",  # 辽宁新闻网_农业技术 404
        ## "http://www.qd.chinanews.com/house/jjkx/ news",  # 中国新闻网_家居快讯 找不到服务器
        ## "http://www.bt.chinanews.com/PhotoS/zhanting/ news",  # 兵团新闻网_展厅 404
        ## "http://www.ln.chinanews.com/tiyu news",  # 辽宁新闻网_体育 504
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=158&ClassTitle=%26%2328207%3B%26%2328595%3B%26%2321488%3B%26%2328286%3B news",  # 中国新闻网_重庆港澳台湾 404
        ## "http://www.bt.chinanews.com/News/yaowen/Index.html news",  # 中新网兵团新闻网_要闻 404
        ## "http://www.bt.chinanews.com/info/zhaoshang/ news",  # 兵团新闻网_招商 404
        ## "http://www.ln.chinanews.com/mingyi news",  # 辽宁新闻网_名医 404
        "http://channel.chinanews.com/cns/cl/tw-lasq.shtml news",  # 中国新闻网_台湾钱进两岸 太旧
        ## "http://www.ah.chinanews.com/portal.php?mod=list&catid=46 news",  # 中国新闻网_安徽国际新闻 404
        "http://www.ln.chinanews.com/yule news",  # 辽宁新闻网_娱乐 504
        ### "http://life.chinanews.com/ news",  # 中国新闻网_生活频道 首页
        ### "http://www.chinanews.com/ny/ft/index.shtml news",  # 中国新闻网_访谈间 首页
        ### "http://auto.chinanews.com/#zxjxc news",  # 重型机械车 首页
        "http://channel.chinanews.com/cns/cl/tw-lajl.shtml news",  # 中国新闻网_台湾互通往来 太旧了
        "http://www.sx.chinanews.com/4/2011/0720/66.html news",  # 中国新闻网_山西国际
        ## "http://www.bt.chinanews.com/Lilun/ news",  # 兵团新闻网_理论  404
        ### "http://photo.chinanews.com/ news",  # 中国新闻网_精彩图片 首页
        ## "http://www.ln.chinanews.com/shangxun news",  # 辽宁新闻网_商讯 504
        ## "http://www.gz.chinanews.com/gjxw/index.shtml news",  # 中国新闻网_贵州国际新闻  空的
        "http://channel.chinanews.com/cns/cl/ny-mt.shtml news",  # 中国新闻网_煤炭 太旧了
        ## "http://www.hn.chinanews.com/news/zxpl/ news",  # 中国新闻网_中新评论 空的
        ### "http://www.jx.chinanews.com/zt/hwmtjxx/ news",  # 中国新闻网_江西崛起 首页
        ## "http://www.cq.chinanews.com/yq news",  # 中国新闻网_重庆园区 404
        ### "http://www.hn.chinanews.com/News/Dlny/ news",  # 中国新闻网_电力 首页
        "http://www.bt.chinanews.com/zhuangao/index.shtml news",  # 图文专稿
        ### "http://www.hn.chinanews.com/newgyyq/ news",  # 中国新闻网_工业园区  还有更多可点  算是首页
        ## "http://www.xj.chinanews.com/html/L_54.htm news",  # 中国新闻网_摄影美图  重定向了
        ## "http://www.sd.chinanews.com/channel/channel.html?lmjc=hwksd news",  # 中国新闻网_海外看山东 404
        "http://www.chinanews.com/shipin/products/index.shtml news",  # 中国新闻网_节 news",  # 目 # 特殊结构
        ## "http://www.chinanews.com/shipin/paike/index.shtml news",  # 中国新闻网_拍客  空的

        "http://www.fj.chinanews.com/new/jryw/list.shtml news",  # 福建新闻网_今日要闻  # 这个源码里可以抽出1081条 最新的是2016年的 有些旧， 文章格式太多了

        ### "http://www.chinanews.com/piaowu/index.html news",  # 演出 首页
        ## "http://www.jl.chinanews.com/cfrs.html news",  # 中国新闻网_百味人生 404
        ## "http://channel.chinanews.com/cns/cl/edu-zgks.shtml news",  # 中国新闻网_教育资格考试 太旧
        ## "http://www.ln.chinanews.com/nongye news",  # 辽宁新闻网_农业 504
        ## "http://www.sd.chinanews.com/channel/channel.html?lmjc=itxw news",  # 中国新闻网_山东IT新闻  404
        ## "http://bbs.chinanews.com/ news",  # 论坛  找不到网页
        ### "http://finance.chinanews.com/#fyrw news",  # 股市  去掉锚点是财经首页
        ## "http://www.hb.chinanews.com/edong/index.html news",  # 中国新闻网_湖北鄂东  页面乱的
        ## "http://channel.chinanews.com/cns/cl/edu-czfn.shtml news",  # 中国新闻网_教育成长烦恼  太旧
        ### "http://www.nmg.chinanews.com/ news",  # 中国新闻网_内蒙古首页
        ## "http://www.qd.chinanews.com/health/topnews/ news",  # 中国新闻网_健康新闻  找不到网页
        "http://www.gd.chinanews.com/index/zx.html news",  # 中国新闻网_资讯

        "http://channel.chinanews.com/cns/cl/edu-tszs.shtml news",  # 中国新闻网_教育他山之石  很旧
        "http://channel.chinanews.com/cns/cl/gj-gjzj.shtml news",  # 中国新闻网_国际战略 很旧
        ### "http://www.chinanews.com/fz/index.shtml news",  # 中国新闻网_法治频道 首页
        "http://www.bt.chinanews.com/Art/shufa/ news",  # 兵团新闻网_书法 404
        "http://www.sd.chinanews.com/html/channel/szxw_1_0.html news",  # 中国新闻网_山东政治新闻 404
        "http://www.jl.chinanews.com/shipin_more.html news",  # 中国新闻网_在线直播 404
        "http://www.sd.chinanews.com/channel/channel.html?lmjc=dfxw news",  # 中国新闻网_山东地方新闻 404

        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=116&ClassTitle=%26%2320013%3B%26%2326032%3B%26%2331038%3B%26%2335760%3B%26%2332773%3B%26%2330475%3B%26%2337325%3B%26%2324198%3B news",  # 中国新闻网_中新社记者看重庆 404
        "http://channel.chinanews.com/cns/cl/estate-qyj.shtml news",  # 中国新闻网_企业家  很旧
        "http://www.yn.chinanews.com/pub/news/world/keji/ news",  # 云南新闻网_科技新闻
        "http://channel.chinanews.com/cns/cl/edu-qzjy.shtml news",  # 中国新闻网_教育就业风向标 很旧
        ## "http://www.gz.chinanews.com/gzr/index.shtml news",  # 中国新闻网_贵州人  空的
        "http://channel.chinanews.com/cns/cl/edu-zkzx.shtml news",  # 中国新闻网_教育招考资讯 很旧
        "http://www.ln.chinanews.com/shipin news",  # 辽宁新闻网_视频中心 504
        "http://channel.chinanews.com/cns/cl/gj-ztch.shtml news",  # 专题  很旧
        ## "http://www.gx.chinanews.com/service/1502/ news",  # 中国新闻网_广西金融 404
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=141&ClassTitle=%26%2328023%3B%26%2322806%3B%26%2321002%3B%26%2337325%3B%26%2324198%3B news",  # 中国新闻网_海外刊重庆
        "http://www.ln.chinanews.com/yingshixinwen news",  # 辽宁新闻网_影视 404
        "http://www.bt.chinanews.com/shehui/index.shtml news",  # 社会民生
        ### "http://cul.chinanews.com/ news",  # 中国新闻网_文化教育  首页
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=138&ClassTitle=%26%2319977%3B%26%2320892%3B news",  # 中国新闻网_重庆三农
        "http://channel.chinanews.com/cns/cl/edu-xxgl.shtml news",  # 中国新闻网_教育应考策略  很旧
        ## "http://channel.chinanews.com/cns/cl/ty-pyw.shtml news",  # 乓羽网 空的
        ### "http://www.chinanews.com/huaren/ news",  # 中国新闻网_华人频道 首页
        "http://channel.chinanews.com/cns/cl/edu-yyks.shtml news",  # 中国新闻网_教育语言考试  很旧
        ## "http://edu.chinanews.com/ news",  # 中国新闻网_教育频道  找不到服务器
        "http://www.yn.chinanews.com/pub/news/fashion/yule/ news",  # 云南新闻网_娱乐
        ## "http://www.sc.chinanews.com/my/ news",  # 中国新闻网_四川绵阳 404
        ## "http://www.bt.chinanews.com/News/ news",  # 中新网兵团新闻网_新闻中心 404
        ## "http://www.bt.chinanews.com/Life/ news",  # 兵团新闻网_生活 404
        ## "http://www.jl.chinanews.com/tbgz.html news",  # 中国新闻网_吉林特别关注 404
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=137&ClassTitle=%26%2335835%3B%26%2320070%3B news",  # 中国新闻网_重庆读书
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=120&ClassTitle=%26%2322269%3B%26%2320869%3B news",  # 中国新闻网_重庆国内
        "http://channel.chinanews.com/cns/cl/it-jdxw.shtml news",  # 中国新闻网_家电 很旧
        ### "http://www.cq.chinanews.com/ news",  # 中国新闻网_重庆园区 首页
        "http://www.yn.chinanews.com/pub/news/fashion/jiankang/ news",  # 云南新闻网_健康
        "http://channel.chinanews.com/cns/cl/tw-dlyw.shtml news",  # 中国新闻网_台湾大陆之声  很旧
        "http://channel.chinanews.com/cns/cl/life-jrgz.shtml news",  # 中国新闻网_今日关注 很旧
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=24&ClassTitle=%26%2331038%3B%26%2320250%3B%26%2319975%3B%26%2335937%3B news",  # 中国新闻网_社会万象
        ## "http://www.yn.chinanews.com/pub/youyue/ news",  # 中国新闻网_中新有约
        ### "http://www.hb.chinanews.com/channel/photo.html news",  # 湖北新闻网_图片新闻 首页
        ## "http://www.bt.chinanews.com/Article/ news",  # 兵团新闻网_文学 404
        ## "http://www.sd.chinanews.com/channel/channel.html?lmjc=qwxw news",  # 404 中国新闻网_山东侨务新闻
        ## "http://www.yn.chinanews.com/pub/meinv/ news",  # 中国新闻网_美女 2014年的 很旧
        "http://www.yn.chinanews.com/pub/zxft/ news",  # 云南新闻网_中新访谈
        ## "http://www.gz.chinanews.com/ly/index.shtml news",  # 中国新闻网_旅游  空的
        ### "http://www.chinanews.com/entertainment/index.shtml news",  # 娱乐 首页
        "http://www.ln.chinanews.com/shishang/ news",  # 中国新闻网_时尚
        "http://www.yn.chinanews.com/pub/news/southasia/ news",  # 云南新闻网_东盟南亚
        "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=134 news",  # 中国新闻网_重庆健康生活 404
        "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=138 news",  # 中国新闻网_重庆三农 404
        "http://www.yn.chinanews.com/pub/news/yunnan/ news",  # 云南新闻网_网友之声
        "http://www.bt.chinanews.com/shituan/index.shtml news",  # 师团新闻
        "http://www.hn.chinanews.com/news/qwsp/ news",  # 中国新闻网_视频
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=126&ClassTitle=%26%2326102%3B%26%2325919%3B%26%2326032%3B%26%2338395%3B news",  # 中国新闻网_重庆时政
        ## "http://www.qd.chinanews.com/house/bgt/ news",  # 中国新闻网_曝光台 找不到服务器
        ## "http://www.ha.chinanews.com/qiaowu/html/qiaozaizhongyuan/ news",  # 中国新闻网_河南侨在中原 找不到服务器

        ### "http://www.yn.chinanews.com/pub/video/ news",  # 中国新闻网_视频 首页
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=166 news",  # 中国新闻网_房产列表 404
        ## "http://www.gz.chinanews.com/hwkgz/index.shtml news",  # 中国新闻网_海外刊贵州 空的
        ## "http://www.qd.chinanews.com/house/focus/ news",  # 中国新闻网_图文焦点 找不到服务器
        ## "http://www.chinanews.com/it/ft/index.shtml news",  # 中国新闻网_IT访谈间 特殊结构
        "http://channel.chinanews.com/cns/cl/it-qydt.shtml news",  # 中国新闻网_企业动态  很旧
        "http://www.gz.chinanews.com/qsyh/index.shtml news",  # 中国新闻网_评论 空的
        "http://channel.chinanews.com/cns/cl/tw-jmdt.shtml news",  # 中国新闻网_台湾经贸动态  很旧
        ### "http://www.gs.chinanews.com/travel/index.html news",  # 中国新闻网_旅游 首页
        ### "http://www.chinanews.com/xmtyw/ news",  # 中国新闻网_手机版  这个是下载页面
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Id=129 news",  # 中国新闻网_重庆区县 404
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Id=128 news",  # 中国新闻网_重庆社会 404
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Id=127 news",  # 中国新闻网_重庆经济
        ### "http://finance.chinanews.com/#gj news",  # 国际财经 首页
        ## "http://www.jl.chinanews.com/mqtj.html news",  # 中国新闻网_名企推介 404
        ## "http://www.ha.chinanews.com/shipin/ news",  # 中国新闻网_河南食品 404
        ## "http://www.yn.chinanews.com/pub/microfilm/ news",  # 中国新闻网_云南微电影 太旧了
        ## "http://www.bt.chinanews.com/PhotoS/ news",  # 兵团新闻网_摄影 404
        "http://channel.chinanews.com/cns/cl/tw-twyw.shtml news",  # 中国新闻网_台湾政局  很旧
        ## "http://www.ln.chinanews.com/wenhua news",  # 辽宁新闻网_文化 504
        ## "http://www.sd.chinanews.com/channel/channel.html?lmjc=zfsh news",  # 中国新闻网_山东社会新闻 404
        ## "http://www.qd.chinanews.com/wenhua/zixun/ news",  # 中国新闻网_文化资讯 找不到服务器
        ## "http://www.gs.chinanews.com/shishang1/m1.html news",  # 中国新闻网_时尚 空的
        "http://channel.chinanews.com/cns/cl/edu-fmxt.shtml news",  # 中国新闻网_教育父母学堂 很旧
        "http://www.jl.chinanews.com/gnyw_more.html news",  # 中国新闻网_吉林国内要闻 404
        ## "http://www.jx.chinanews.com/photo/ news",  # 中国新闻网_江西图片新闻 访问超时
        "http://www.bt.chinanews.com/gongsi/index.shtml news",  # 公司动态
        "http://www.sd.chinanews.com/html/channel/ywdd_1_0.html news",  # 中国新闻网_山东要闻导读 404
        ## "http://channel.chinanews.com/cns/cl/it-hddc.shtml news",  # 调查 空的
        "http://www.bt.chinanews.com/fazhi/index.shtml news",  # 法制新闻
        "http://channel.chinanews.com/cns/cl/tw-jsdt.shtml news",  # 中国新闻网_台湾军情动态 很旧
        "http://www.bt.chinanews.com/tupian/index.shtml news",  # 图片新闻  有40个页面是没有来源的
        ### "http://www.gd.chinanews.com/lypd.html news",  # 中国新闻网_广东旅游 首页
        ## "http://www.zz.chinanews.com/ news",  # 中国新闻网_福建漳州新闻 找不到服务器
        ## "http://www.heb.chinanews.com/4/20111018/322.shtml news",  # 中国新闻网_外媒刊河北 页面不存在
        "http://www.shx.chinanews.com/kjww.html news",  # 中国新闻网_科教文卫
        ## "http://www.gz.chinanews.com/dcgz/index.shtml news",  # 中国新闻网_多彩贵州 空的
        ## "http://www.bt.chinanews.com/Tour/ news",  # 兵团新闻网_旅游 404
        ### "http://www.chinanews.com/shipin/index.shtml news",  # 中国新闻网_视频新闻 首页
        ## "http://www.yn.chinanews.com/pub/mingxing/ news",  # 中国新闻网_明星 太旧
        ## "http://www.xj.chinanews.com/html/L_103.htm news",  # 中国新闻网_铁路资讯 跳转
        ## "http://www.jx.chinanews.com/finance/ news",  # 中国新闻网_江西财政 请求超时
        "http://www.bj.chinanews.com/4/2009/0306/12.html news",  # 中国新闻网_经济新闻
        ## "http://www.ha.chinanews.com/yiliaoweisheng2012/html/yiliaoweisheng2012/yiyuan/ news",  # 中国新闻网_医院 404
        "http://channel.chinanews.com/cns/cl/estate-gy.shtml news",  # 中国新闻网_官员 很旧
        ### "http://www.fj.chinanews.com/ news",  # 中国新闻网_福建_福建频道 首页
        ## "http://www.qd.chinanews.com/health/news/ news",  # 中国新闻网_社会关注 找不到服务器
        ### "http://www.chinanews.com/finance/duihj/wahaha.shtml news",  # 总裁 首页
        ## "http://www.zj.chinanews.com/zhejiang/ news",  # 中国新闻网_浙江 跳转
        "http://channel.chinanews.com/cns/cl/edu-xyztc.shtml news",  # 中国新闻网_教育校园联播 很旧
        ## "http://www.chinanews.com/gn/2014/02-14/5837136.shtml news",  # 中国新闻社图文信息发布网_解读 这个是个详情页
        "http://www.sd.chinanews.com/html/channel/gzgat_1_0.html news",  # 中国新闻网_山东关注港澳台 404
        "http://channel.chinanews.com/cns/cl/tw-lydl.shtml news",  # 中国新闻网_台湾旅游观光 很旧
        "http://www.gd.chinanews.com/index/cnstv.html news",  # 中国新闻网_CNSTV 全是视频
        ## "http://www.gz.chinanews.com/zt/index.shtml news",  # 中国新闻网_专题 空的

        "http://channel.chinanews.com/video/showchannel?tid=4&currentpage=0&pagenum=16&_= news", # "http://www.chinanews.com/shipin/scroll/index.shtml news",  # 视频  Ajax的

        "http://www.fj.chinanews.com/new/dsxw/list.shtml news",  # 福建新闻网_地市新闻  这个页面能抽3300多个url 曰
        "http://channel.chinanews.com/cns/cl/it-dzsw.shtml news",  # 中国新闻网_电商动态  很旧
        "http://www.ln.chinanews.com/jiaoyu news",  # 辽宁新闻网_教育 504
        ## "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=166&ClassTitle=%26%2325151%3B%26%2320135%3B news",  # 中国新闻网_重庆房产
        "http://channel.chinanews.com/cns/cl/estate-yt.shtml news",  # 中国新闻网_亚太 很旧
        "http://channel.chinanews.com/cns/cl/hwjy-jxyd.shtml news",  # 教学园地 很旧
        "http://channel.chinanews.com/cns/cl/it-itftj2.shtml news",  # 中国新闻网_IT访谈间 很旧
        ## "http://www.heb.chinanews.com/4/20111018/336.shtml news",  # 中国新闻网_国际传真 太旧了
        ## "http://www.qd.chinanews.com/house/xiangmu/2012/0928/14769.html news",  # 中国新闻网_详细 找不到服务器
        "http://www.ln.chinanews.com/caijing/ news",  # 中国新闻网_财经
        "http://www.bt.chinanews.com/lvyou/index.shtml news",  # 娱乐旅游
        ### "http://www.js.chinanews.com/ks/ news",  # 中国新闻网_昆山  首页
        ## "http://www.jl.chinanews.com/shzt.html news",  # 中国新闻网_吉林社会民生 404
        ## "http://www.zj.chinanews.com/international/ news",  # 中国新闻网_浙江国际新闻 跳转
        ## "http://www.bt.chinanews.com/Art/ news",  # 兵团新闻网_书画 404
        ## "http://www.bt.chinanews.com/News/jiangnei/ news",  # 中新网兵团新闻网_疆内 404
        "http://channel.chinanews.com/cns/cl/hwjy-cybx.shtml news",  # 词语辨析 很旧
        "http://www.hi.chinanews.com/gundong/yule.html news",  # 中国新闻网_娱乐
        ## "http://www.sd.chinanews.com/channel/channel.html?lmjc=kjww news",  # 中国新闻网_山东文教新闻 404
        ## "http://www.nd.chinanews.com/ news",  # 中国新闻网_福建宁德新闻 找不到服务器
        ## "http://www.yn.chinanews.com/pub/qrqw/ news",  # 中国新闻网_奇人趣闻  太旧了
        "http://www.ln.chinanews.com/qicheceping news",  # 辽宁新闻网_测评 404
        "http://channel.chinanews.com/cns/cl/edu-zcdt.shtml news",  # 中国新闻网_教育政策动态 很旧
        "http://www.sx.chinanews.com/linfen/list/3.html news",  # 中国新闻网_山西临汾政情
        "http://channel.chinanews.com/cns/cl/tw-ztjz.shtml news",  # 中国新闻网_驻台专栏 很旧
        ## "http://www.hn.chinanews.com/news/mqzx/ news",  # 中国新闻网_名企在线 空的
        ## "http://www.sd.chinanews.com/channel/channel.html?lmjc=cjxw news",  # 中国新闻网_山东经济新闻 404
        ## "http://channel.chinanews.com/cns/cl/it-itxw.shtml news",  # 业界  很旧
        ## "http://www.gz.chinanews.com/lddt/index.shtml news",  # 中国新闻网_政务动态 空的
        ## "http://channel.chinanews.com/cns/cl/tw-jjwh.shtml news",  # 中国新闻网_台湾经济脉动 很旧
        "http://fortune.chinanews.com/#gs news",  # 股市
        ## "http://www.ln.chinanews.com/zhaoshang news",  # 辽宁新闻网_招商  # 404
        ## "http://www.ha.chinanews.com/yiliaoweisheng2012/ news",  # 中国新闻网_河南健康  # 404
        "http://www.gd.chinanews.com/index/zxzt.html news",  # 中新专题
        ### "http://channel.chinanews.com/cns/cl/ty-tczjj.shtml news",  # 体操·重竞技  # timeout
        ### "http://www.ln.chinanews.com/qiche news",  # 辽宁新闻网_汽车  # 404
        ### "http://www.ln.chinanews.com/shenghuo news",  # 辽宁新闻网_生活  # timeout
        "http://finance.chinanews.com/#rmbhy news",  # 区域
        ### "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=119&ClassTitle=%26%2337325%3B%26%2324198%3B news",  # 中国新闻网_重庆  # 404
        "http://house.chinanews.com/ news",  # 中国新闻网_房产频道
        ### "http://www.bt.chinanews.com/Art/hualang/ news",  # 兵团新闻网_名家  # 404
        ### "http://qd.chinanews.com/sh/ news",  # 中国新闻网_青岛社会  # timeout
        ### "http://channel.chinanews.com/cns/cl/edu-dxxy.shtml news",  # 中国新闻网_教育风尚文化  # timeout
        ### "http://www.xj.chinanews.com/html/L_41.htm news",  # 中国新闻网_外媒看新疆  # 404
        "http://www.bt.chinanews.com/jingji/index.shtml news",  # 经济新闻
        ### "http://www.ln.chinanews.com/keji news",  # 辽宁新闻网_科技  # timeout
        "http://www.jx.chinanews.com/travel/ news",  # 中国新闻社图文信息发布网_旅游
        "http://www.bt.chinanews.com/bingtuan/index.shtml news",  # 兵团要闻
        "http://www.chinanews.com/entertainment/photo/yltkphoto-1.html news",  # 热辣图库
        ### "http://channel.chinanews.com/cns/cl/edu-kczj.shtml news",  # 中国新闻网_教育考场速递  # timeout
        ### "http://channel.chinanews.com/cns/cl/it-ydczxt.shtml news",  # 中国新闻网_行业动态  # timeout
        ### "http://www.chinanews.com/sportchannel/index.shtml news",  # 体育  # 首页
        ### "http://qd.chinanews.com/xinwen/qdnews/ news",  # 中国新闻网_青岛要闻  # timeout
        ### "http://www.qd.chinanews.com/house/lszx/ news",  # 中国新闻网_楼市资讯  # timeout
        ### "http://www.ha.chinanews.com/qiaowu/html/qiaowu/feiyizhichuang/ news",  # 中国新闻网_非遗之窗  # 404
        ### "http://channel.chinanews.com/cns/cl/tw-thsp.shtml news",  # 中国新闻网_台湾海峡时评  # timeout
        ### "http://www.bt.chinanews.com/Article/shige/ news",  # 兵团新闻网_诗歌  # 404
        ### "http://www.bt.chinanews.com/News/guonei/ news",  # 中新网兵团新闻网_国内  # 404
        ### "http://www.chinanews.com/zgqj/index.shtml news",  # 中国新闻网_中国侨界  # 首页
        ### "http://channel.chinanews.com/cns/cl/tw-mswx.shtml news",  # 中国新闻网_台湾社会万象  # timeout
        ### "http://channel.chinanews.com/cns/cl/tw-tgqy.shtml news",  # 中国新闻网_台湾同根亲缘  # timeout
        ### "http://bbs.chinanews.com/forum-43-1.html news",  # 论坛  # timeout
        "http://www.bj.chinanews.com/focus/11.html news",  # 中国新闻网_怀旧
        ### "http://channel.chinanews.com/cns/cl/gj-sp.shtml news",  # 视频  # timeout
        ### "http://www.yn.chinanews.com/pub/news/headline/ news",  # 云南新闻网_文字头条 很特殊
        ### "http://www.sc.chinanews.com/bz/ news",  # 中国新闻网_四川巴中  # 404
        ### "http://www.bt.chinanews.com/Video/xpxw/ news",  # 兵团新闻网_视频  # 404
        ### "http://www.chinanews.com/home/ news",  # 中国新闻网_新闻首页
        ###"http://www.chinanews.com/jk/jkzc/index.shtml news",  # 中国新闻网_健康自测  # 这个是自测 不是新闻
        ### "http://channel.chinanews.com/cns/cl/ty-tjyy.shtml news",  # 田径·游泳  # timeout
        ### "http://channel.chinanews.com/cns/cl/tw-jfhz.shtml news",  # 中国新闻网_警法互助  # timeout
        "http://www.gs.chinanews.com/gsyw1.html news",  # 甘肃新闻网_甘肃要闻
        ### "http://channel.chinanews.com/cns/cl/edu-xjy.shtml news",  # 中国新闻网_教育青春私语  # timeout
        ### "http://www.bt.chinanews.com/info/qiugou/ news",  # 兵团新闻网_求购  # 404
        "http://www.heb.chinanews.com/4/20111018/335.shtml news",  # 中国新闻网_河北中新聚焦
        ### "http://www.bt.chinanews.com/News/Photonews/ news",  # 兵团新闻网_图片  # 404
        ###"http://www.chinanews.com/shipin/qwqs/view.shtml news",  # 中国新闻网_趣闻八卦  #空的
        ### "http://www.sc.chinanews.com/bz news",  # 中国新闻网_巴中  # 404
        ### "http://channel.chinanews.com/cns/cl/edu-lljy.shtml news",  # 中国新闻网_教育另类  # timeout
        ### "http://www.bt.chinanews.com/News/guoji/ news",  # 中新网兵团新闻网_国际  # 404
        ### "http://www.chinanews.com/life/z/masterkong/index.shtml news",  # 巡访 专题类
        ### "http://www.bt.chinanews.com/PhotoT/ news",  # 兵团新闻网_图文  # 404
        ### "http://www.ln.chinanews.com/errenzhuan news",  # 辽宁新闻网_二人转  # 404
        ###"http://www.shx.chinanews.com/news/zltx.shtml news",  # 中国新闻网_纵览天下 太旧了
        ### "http://www.jx.chinanews.com/taiwan/ news",  # 中国新闻网_台湾  # 404
        ### "http://www.ha.chinanews.com/yiliaoweisheng2012/html/yiliaoweisheng2012/weishengxinwen/ news",  # 中国新闻网_卫生新闻  # 404
        "http://www.chinanews.com/health/index.shtml news",  # 中国新闻网_健康频道
        ### "http://www.bt.chinanews.com/PhotoS/renwu/ news",  # 兵团新闻网_人物  # 404
        ### "http://www.jl.chinanews.com/szjj.html news",  # 中国新闻网_吉林时事聚焦  # 404
        ### "http://www.chinanews.com/lxsh/news.html news",  # 中国新闻网_留学 空的
        ### "http://www.ha.chinanews.com/qiaowu/html/qiaowu/shoucang/ news",  # 中国新闻网_收藏  # 404
        ### "http://www.ln.chinanews.com/caijing news",  # 辽宁新闻网_财经  # timeout
        ### "http://www.ln.chinanews.com/jiankang news",  # 辽宁新闻网_健康  # timeout
        ### "http://www.chinanews.com/cj/ft/yth2011/index.shtml news",  # 访谈间  # 首页
        ### "http://www.chinanews.com/shipin/2014/02-10/news375575.shtml news",  # 中国新闻网_小贩刺城管 # 这是个具体的 ???
        ### "http://www.jl.chinanews.com/sddc.html news",  # 中国新闻网_吉林深度观察  # 404
        ### "http://www.chinanews.com/auto/z/model/index.shtml news",  # 车模  首页类型
        ### "http://bbs.chinanews.com/forum-55-1.html news",  # 体坛热议  # timeout
        "http://www.yn.chinanews.com/pub/news/world/guoji/ news",  # 云南新闻网_国际新闻
        ### "http://www.ln.chinanews.com/fangchanweiquan news",  # 辽宁新闻网_房产维权  # 404
        ### "http://www.qd.chinanews.com/house/xiangmu/ news",  # 中国新闻网_项目推介汇  # timeout
        ### "http://www.sd.chinanews.com/html/channel/jrtt_1_0.html news",  # 中国新闻网_山东今日头条  # 404
        ### "http://www.sc.chinanews.com/gy/ news",  # 中国新闻网_四川广元  # 404
        "http://www.hn.chinanews.com/jrhn/340/ newspaper",  # 中国新闻网_今日湖南
        ### ### "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=118&ClassTitle=%26%2339318%3B%26%2339029%3B%26%2335201%3B%26%2338395%3B news",  # 中国新闻网_首页要闻  # 404
        ### "http://www.jl.chinanews.com/jlyw.html news",  # 中国新闻网_吉林要闻  # 404
        ### "http://channel.chinanews.com/cns/cl/tw-whjl.shtml news",  # 中国新闻网_台湾文化交流  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-zbzj.shtml news",  # 主编周记  # timeout
        ### "http://auto.chinanews.com/#guoji news",  # 国际  # 首页
        ### "http://www.ln.chinanews.com/lvyou news",  # 辽宁新闻网_旅游  # timeout
        ### "http://www.ln.chinanews.com/shangye news",  # 辽宁新闻网_商业  # timeout
        ### "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=182&ClassTitle=%26%2325151%3B%26%2320135%3B%26%2335201%3B%26%2338395%3B news",  # 中国新闻网_房产要闻  # 404
        ### "http://www.cq.chinanews.com/Include/newsmenu.asp?Id=163 news",  # 中国新闻网_重庆汽车旅游  # 404
        ### "http://www.xj.chinanews.com news",  # 中国新闻网_新疆频道  # 首页
        ### "http://channel.chinanews.com/cns/cl/edu-rwsy.shtml news",  # 中国新闻网_教育人物声音  # timeout
        ### "http://www.chinanews.com/shipin/zxft/view.shtml news",  # 中国新闻网_访谈 # 首页
        ### "http://www.chinanews.com/taiwan/ news",  # 中国新闻网_台湾  # 首页
        ### "http://channel.chinanews.com/cns/cl/edu-xljt.shtml news",  # 中国新闻网_教育心理  # timeout
        ### "http://www.ln.chinanews.com/lvyouyouji news",  # 辽宁新闻网_驴友游记  # 404
        ### "http://www.ln.chinanews.com/tupian news",  # 辽宁新闻网_图片中心  # 404
        ### "http://www.bt.chinanews.com/news/jijian/ news",  # 中国新闻网_兵团党建  # 404
        "http://www.chinanews.com/edu.shtml news",  # 教育  太旧了
        ### "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=140&ClassTitle=%26%2334892%3B%26%2319994%3B news",  # 中国新闻网_重庆行业  # 404
        ### "http://www.ln.chinanews.com/fangchan news",  # 辽宁新闻网_房产  # timeout
        ### "http://www.jl.chinanews.com/xw_cc.html news",  # 中国新闻网_吉林长春  # 404
        ### "http://www.chinanews.com/taiwan/index.shtml news",  # 中国新闻网_台湾频道  首页
        ### "http://channel.chinanews.com/cns/cl/tw-rwtw.shtml news",  # 中国新闻网_人文台湾  # timeout
        ### "http://channel.chinanews.com/cns/cl/it-hygc.shtml news",  # 中国新闻网_行业观察  # timeout
        ### "http://www.cq.chinanews.com/Include/newsmenu.asp?Parent=133&ClassTitle=%26%2332844%3B%26%2322330%3B%26%2326102%3B%26%2323578%3B news",  # 中国新闻网_重庆职场时尚  # 404
        ### "http://www.ln.chinanews.com/gangkou news",  # 中国新闻网_港口  # 404
        ### "http://channel.chinanews.com/cns/cl/hwjy-kzxy.shtml news",  # 中国新闻网_孔子学院  # timeout
        ### "http://channel.chinanews.com/cns/cl/edu-jysp.shtml news",  # 中国新闻网_教育观点  # timeout
        ### "http://www.js.chinanews.com/house/ news",  # 中国新闻网_房产 # 首页
        ### "http://www.sd.chinanews.com/html/channel/xyxw_1_0.html news",  # 中国新闻网_山东校园新闻  # 404
        ### "http://www.ln.chinanews.com/qichebaoyang news",  # 辽宁新闻网_保养  # 404
        ### "http://www.hn.chinanews.com/jcxx/ news",  # 中国新闻网_决策信息 首页
        ### "http://www.jl.chinanews.com/cjbd.html news",  # 中国新闻网_吉林财经报道  # 404
        "http://www.bt.chinanews.com/yuanjiang/index.shtml news",  # 援疆信息
        ### "http://www.ha.chinanews.com/finance2012/ news",  # 中国新闻网_河南财经  # 404
        ### "http://www.gz.chinanews.com/more/9/50.shtml news",  # 中国新闻网_贵州外事侨务 太旧了
        ### "http://www.bt.chinanews.com/info/gongying/ news",  # 兵团新闻网_供应  # 404
        ### "http://channel.chinanews.com/cns/cl/tw-sp.shtml news",  # 视频  # timeout
        ### ### "http://www.chinanews.com/ news",  # 新闻 绝对首页
        ### "http://www.bt.chinanews.com/ news",  # 兵团新闻网_首页
        ### "http://www.hn.chinanews.com/News/hnsw/ news",  # 中国新闻网_税务 也不是列表页
        ### "http://channel.chinanews.com/cns/cl/estate-zxjc.shtml news",  # 中国新闻网_装修建房  # timeout
        ### "http://www.bt.chinanews.com/Art/huihua/ news",  # 兵团新闻网_新蕾  # 404
        "http://www.bt.chinanews.com/shipin/index.shtml news",  # 视频新闻
        "http://www.yn.chinanews.com/pub/video/zixun/ news",  # 中国新闻网_中新资讯
        ### "http://channel.chinanews.com/cns/cl/tw-qxcy.shtml news",  # 中国新闻网_台湾求学从业  # timeout
        ### "http://www.heb.chinanews.com/ news",  # 中国新闻网_河北新闻  首页
        "http://www.yn.chinanews.com/pub/news/world/pinglun/ news",  # 云南新闻网_云南评论
        ### "http://bbs.chinanews.com/forum-137-1.html news",  # 网上谈兵  # timeout
        ### "http://www.chinanews.com/gangao/index.shtml news",  # 中国新闻网_港澳频道  首页
        ### "http://www.jl.chinanews.com/dcls.html news",  # 中国新闻网_地产楼市  # 404
        ### "http://channel.chinanews.com/cns/cl/estate-wy.shtml news",  # 中国新闻网_物业  # timeout
        "http://www.gz.chinanews.com/tsxw/index.shtml news",  # 中国新闻网_贵州图说新闻  空的
        ### "http://www.bt.chinanews.com/Yule/ news",  # 兵团新闻网_娱乐  # 404
        ### "http://www.bt.chinanews.com/PhotoT/rwft/ news",  # 兵团新闻网_访谈  # 404
        ### "http://www.chinanews.com/hwjy/index.shtml news",  # 中国新闻网_华文教育频道  首页
        ### "http://www.jl.chinanews.com/hqrd_more.html news",  # 中国新闻网_吉林环球热点  # 404
        "http://www.chinanews.com/allspecial/index.shtml news",  # 中国新闻网_新闻专题回顾  特殊结构
        ### "http://www.ha.chinanews.com/qiaowu/html/waishi/ news",  # 中国新闻网_河南特别关注.维权  # 404
        "http://www.yn.chinanews.com/pub/zt/ news",  # 中国新闻网_专题报道  专题
        ### "http://www.sd.chinanews.com/html/channel/gjjd_1_0.html news",  # 中国新闻网_山东国际焦点  # 404
        ### "http://www.gs.chinanews.com/mzyj/index.html news",  # 中国新闻网_每周一荐 首页
        ### "http://www.ln.chinanews.com/shishang news",  # 中国新闻网_时尚生活  # timeout
        ### "http://www.chinanews.com/qxcz/news.html news",  # 中国新闻网_侨乡传真 空的
        "http://www.hn.chinanews.com/news/qcxw/ news",  # 中国新闻网_汽车房产
        "http://www.heb.chinanews.com/4/20111205/362.shtml news",  # 中国新闻网_河北燕山夜话  页面不存在
        ### "http://channel.chinanews.com/cns/cl/tw-hxdw.shtml news",  # 中国新闻网_台湾海峡对望  # timeout
        ### "http://life.chinanews.com/#lovehousecommend news",  # 美图  首页
        "http://www.bt.chinanews.com/liandui/index.shtml news",  # 连队新闻
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=27 news",  # 中国新闻网_安徽决策参考  # 404
        "http://www.hn.chinanews.com/news/zfqy/ news",  # 中国新闻网_政法前沿
        "http://www.js.chinanews.com/comment/ news",  # 焦点评论
        "http://www.js.chinanews.com/4/17.html news",  # 江苏各地
        "http://www.js.chinanews.com/76/hzzx.html news",  # 合作资讯
        "http://www.js.chinanews.com/photo/highlights/ news",  # 江苏图片热点聚焦
        "http://www.js.chinanews.com/photo/citynews/ news",  # 江苏图片社会百态
        "http://www.js.chinanews.com/photo/sports/ news",  # 江苏图片娱乐体育
        "http://www.js.chinanews.com/photo/business/ news",  # 江苏图片财经企业
        "http://www.js.chinanews.com/photo/science/ news",  # 江苏图片科教文卫
        "http://www.js.chinanews.com/photo/fashion/ news",  # 江苏图片时尚生活
        "http://www.js.chinanews.com/76/2.html news",  # 市场信息
        "http://www.sc.chinanews.com/ChengduNews/ms/index.shtml news",  # 民生
        "http://www.sc.chinanews.com/ChengduNews/rd/index.shtml news",  # 热点
        "http://www.sc.chinanews.com/ChengduNews/mtbd/index.shtml news",  # 媒体报道
        "http://www.sc.chinanews.com/ChengduNews/bm/index.shtml news",  # 市级部门
        "http://www.sc.chinanews.com/ChengduNews/qx/index.shtml news",  # 区（市）县
        "http://www.sc.chinanews.com/ChengduNews/qt/index.shtml news",  # 其他
        ### "http://www.sc.chinanews.com/ChengduNews/xwfb/list.shtml news",  # 新闻发布 发布会
        ### "http://www.sc.chinanews.com/ChengduNews/xgtp/index.shtml news",  # 相关图片 就是图片
        ### "http://www.sc.chinanews.com/ChengduNews/wsp/index.shtml news",  # 微视频
        ### "http://www.sc.chinanews.com/ChengduNews/sjbm/index.shtml news",  # 成都市级部门新闻发布人
        ### "http://www.sc.chinanews.com/ChengduNews/qsx/index.shtml news",  # 成都区（市）县级新闻发布人
        "http://www.chinanews.com/jiaoyu.shtml news",  # 教育新闻
        ### "http://channel.chinanews.com/cns/cl/gn-gcdt.shtml news",  # 时政频道：高层  # timeout
        ### "http://channel.chinanews.com/cns/cl/gn-zcdt.shtml news",  # 时政频道：政策  # timeout
        ### "http://channel.chinanews.com/cns/cl/gn-rsbd.shtml news",  # 时政频道：人事  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-zxsjg.shtml news",  # 国际频道：中新世界观  # timeout
        ### "http://channel.chinanews.com/u/gj-rw.shtml news",  # 国际频道：人物  # timeout
        ### "http://channel.chinanews.com/u/fsh.shtml news",  # 浮世绘  # timeout
        ### "http://channel.chinanews.com/u/rdzz.shtml news",  # 热点追踪  # timeout
        ### "http://channel.chinanews.com/u/gn-rjbw.shtml news",  # 人间百味  # timeout
        ### "http://channel.chinanews.com/u/gn-dyxc.shtml news",  # 第一现场  # timeout
        ### "http://channel.chinanews.com/cns/cl/cj-msrd.shtml news",  # 财经频道：民生热点  # timeout
        "http://www.chinanews.com/business/gd.shtml news",  # 产经新闻
        "http://www.chinanews.com/house/gd.shtml news",  # 房产新闻
        ### "http://channel.chinanews.com/cns/cl/business-rw.shtml news",  # 产经频道：人物  # timeout
        "http://it.chinanews.com/it/gd.shtml news",  # IT新闻
        "http://www.chinanews.com/energy/gd.shtml news",  # 能源新闻
        ### "http://channel.chinanews.com/cns/cl/stock-scyw.shtml news",  # 金融频道：市场要闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/auto-cqrw.shtml news",  # 汽车频道：车人物  # timeout
        ### "http://channel.chinanews.com/cns/cl/auto-cyd.shtml news",  # 汽车频道：车运动  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-zmrs.shtml news",  # 港澳频道：人物  # timeout
        ### "http://channel.chinanews.com/cns/cl/tw-rw.shtml news",  # 台湾频道：人物  # timeout
        ### "http://channel.chinanews.com/cns/cl/tw-lahd.shtml news",  # 台湾频道：两岸  # timeout
        ### "http://channel.chinanews.com/cns/cl/tw-jjtw.shtml news",  # 台湾频道：时事  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-lszs.shtml news",  # 华人频道：领事之声  # timeout
        ### "http://channel.chinanews.com/u/hr/cgfx.shtml news",  # 华人频道：出国风向  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-qjdt.shtml news",  # 华人频道：侨界动态  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-qxcz.shtml news",  # 华人频道：侨乡传真  # timeout
        "http://www.chinanews.com/entertainment.shtml news",  # 娱乐新闻
        ### "http://channel.chinanews.com/cns/cl/yl-mxnd.shtml news",  # 娱乐频道：明星八卦  # timeout
        "http://www.chinanews.com/shipin/m/wy/wy-yl/views.shtml news",  # 文娱前线-娱乐  # 看起来是空的 可能有ajax
        ### "http://channel.chinanews.com/cns/cl/yl-ypkb.shtml news",  # 娱乐频道：影视博览  # timeout
        "http://www.chinanews.com/ty/gun-news.html news",  # 体育频道
        ### "http://channel.chinanews.com/cns/cl/ty-bdjj.shtml news",  # 体育频道：独家视角  # timeout
        "http://www.chinanews.com/shipin/m/tt/views.shtml news",  # 体坛风云  # 看起来是空的 可能有ajax
        ### "http://channel.chinanews.com/cns/cl/cul-rwzf.shtml news",  # 文化频道：人物对话  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-sckgd.shtml news",  # 文化频道：收藏考古  # timeout
        "http://www.chinanews.com/shipin/m/wy/wy-cul/views.shtml news",  # 文娱前线-文化
        "http://photo.chinanews.com/photo/zxhb.html news",  # 中新画报
        "http://photo.chinanews.com/photo/more/1.html news",  # 最新图片
        "http://photo.chinanews.com/photo/gnjj.html news",  # 国内聚焦
        "http://photo.chinanews.com/photo/shbt.html news",  # 社会百态
        "http://photo.chinanews.com/photo/gjbl.html news",  # 国际博览
        "http://photo.chinanews.com/photo/ylty.html news",  # 娱乐体育
        "http://photo.chinanews.com/photo/shmy.html news",  # 时尚魅影
        "http://photo.chinanews.com/photo/jskj.html news",  # 军事科技
        "http://photo.chinanews.com/photo/gatq.html news",  # 港澳台侨
        "http://photo.chinanews.com/tp/chart/index.shtml news",  # 图解新闻  就是没有来源的
        "http://channel.chinanews.com/video/showchannel?lanmu1=rd-rd&currentpage=0&pagenum=16&_= news",  # "http://www.chinanews.com/shipin/m/rd/views.shtml news",  # 热点新闻 # Ajax
        "http://channel.chinanews.com/video/showchannel?tid=4&currentpage=0&pagenum=16&_= news",  # "http://www.chinanews.com/shipin/m/gd/views.shtml news",  # 最新 # Ajax
        "http://channel.chinanews.com/video/showchannel?channel1=gn&currentpage=0&pagenum=16&_= news",  # "http://www.chinanews.com/shipin/m/gn/views.shtml news",  # 国内新闻 # Ajax
        "http://channel.chinanews.com/video/showchannel?channel1=sh&currentpage=0&pagenum=16&_= news", # "http://www.chinanews.com/shipin/m/sh/views.shtml news",  # 社会 # Ajax
        "http://channel.chinanews.com/video/showchannel?channel1=gj&currentpage=0&pagenum=16&_= news", # "http://www.chinanews.com/shipin/m/gj/views.shtml news",  # 国际新闻 # Ajax
        "http://channel.chinanews.com/video/showchannel?lanmu1=jq-mil&currentpage=0&pagenum=16&_= news", # "http://www.chinanews.com/shipin/m/jq/views.shtml news",  # 军情直击 # Ajax
        "http://channel.chinanews.com/video/showchannel?channel1=wy&currentpage=0&pagenum=16&_= news", # "http://www.chinanews.com/shipin/m/wy/views.shtml news",  # 文娱前线 # Ajax
        "http://channel.chinanews.com/video/showchannel?channel1=cj&currentpage=0&pagenum=16&_= news",  # "http://www.chinanews.com/shipin/m/cj/views.shtml news",  # 财经 # Ajax
        "http://channel.chinanews.com/video/showchannel?channel1=ga&currentpage=0&pagenum=16&_= news",  # "http://www.chinanews.com/shipin/m/ga/views.shtml news",  # 港澳台侨 # Ajax
        "http://www.chinanews.com/theory.shtml news",  # 理论新闻
        ### "http://channel.chinanews.com/cns/cl/ll-llqy.shtml news",  # 理论频道：理论前沿  # timeout
        ### "http://channel.chinanews.com/cns/cl/ll-sjts.shtml news",  # 理论频道：实践探索  # timeout
        ### "http://channel.chinanews.com/cns/cl/ll-dsdj.shtml news",  # 理论频道：党史党建  # timeout
        ### "http://channel.chinanews.com/cns/cl/ll-xzly.shtml news",  # 理论频道：学者论苑  # timeout
        "http://www.chinanews.com/jiankang.shtml news",  # 健康新闻
        ### "http://channel.chinanews.com/cns/cl/life-mstj.shtml news",  # 生活频道：吃喝玩乐  # timeout
        ### "http://channel.chinanews.com/cns/cl/wine-rwzf.shtml news",  # 葡萄酒频道：人物专访  # timeout
        ### "http://channel.chinanews.com/cns/cl/wine-sp.shtml news",  # 葡萄酒频道：视频  # timeout
        "http://www.chinanews.com/piaowu/hot-more.html news",  # 热门资讯  这个频道 节点有1061个 大多数很旧了
        "http://www.ah.chinanews.com/focus/5.html news",  # 中新网安徽_高端动态
        "http://www.ah.chinanews.com/focus/6.html news",  # 中新网安徽_社会民生
        "http://www.ah.chinanews.com/focus/7.html news",  # 中新网安徽_科技教育
        "http://www.ah.chinanews.com/focus/8.html news",  # 中新网安徽_财经时讯
        "http://www.ah.chinanews.com/focus/9.html news",  # 中新网安徽_旅游大观
        "http://www.ah.chinanews.com/focus/10.html news",  # 中新网安徽_企业资讯
        "http://www.ah.chinanews.com/focus/12.html news",  # 中新网安徽_房产汽车
        "http://www.ah.chinanews.com/focus/4.html news",  # 中新网安徽_中新记者看安徽
        "http://www.ah.chinanews.com/focus/14.html news",  # 中新网安徽_政策动态
        "http://www.ah.chinanews.com/focus/15.html news",  # 中新网安徽_人事任免
        "http://www.ah.chinanews.com/focus/18.html news",  # 中新网安徽_各地聚焦
        "http://www.ah.chinanews.com/focus/19.html news",  # 中新网安徽_经济园区
        "http://www.ah.chinanews.com/focus/20.html news",  # 中新网安徽_媒体监督
        "http://www.ah.chinanews.com/focus/26.html news",  # 中新网安徽_安徽好人
        "http://www.ah.chinanews.com/focus/27.html news",  # 中新网安徽_安徽警方
        "http://www.ah.chinanews.com/focus/28.html news",  # 中新网安徽_民生热线
        "http://www.ah.chinanews.com/focus/29.html news",  # 中新网安徽_社会热点
        "http://www.ah.chinanews.com/focus/30.html news",  # 中新网安徽_时尚风向
        "http://www.ah.chinanews.com/focus/31.html news",  # 中新网安徽_热点评论
        "http://www.ah.chinanews.com/focus/32.html news",  # 中新网安徽_突发事件
        "http://www.ah.chinanews.com/focus/33.html news",  # 中新网安徽_政策解读
        "http://www.ah.chinanews.com/focus/34.html news",  # 中新网安徽_安徽财经
        "http://www.ah.chinanews.com/focus/35.html news",  # 中新网安徽_保险银行
        "http://www.ah.chinanews.com/focus/36.html news",  # 中新网安徽_经济与法
        "http://www.ah.chinanews.com/focus/37.html news",  # 中新网安徽_金融理财
        "http://www.ah.chinanews.com/focus/38.html news",  # 中新网安徽_行业动态
        "http://www.ah.chinanews.com/focus/39.html news",  # 中新网安徽_中国霍邱
        "http://www.ah.chinanews.com/focus/40.html news",  # 中新网安徽_文坛皖军
        "http://www.ah.chinanews.com/focus/41.html news",  # 中新网安徽_皖籍名家
        "http://www.ah.chinanews.com/focus/42.html news",  # 中新网安徽_安徽出版
        "http://www.ah.chinanews.com/focus/43.html news",  # 中新网安徽_安徽戏剧
        "http://www.ah.chinanews.com/focus/44.html news",  # 中新网安徽_戏剧名家
        "http://www.ah.chinanews.com/focus/45.html news",  # 中新网安徽_徽学百家
        "http://www.ah.chinanews.com/focus/46.html news",  # 中新网安徽_安徽历史
        "http://www.ah.chinanews.com/focus/13.html news",  # 中新网安徽_时光密语娱乐专栏
        "http://www.ah.chinanews.com/focus/47.html news",  # 中新网安徽_时光密语文化专栏
        "http://www.ah.chinanews.com/focus/48.html news",  # 中新网安徽_文化活动
        "http://www.ah.chinanews.com/focus/49.html news",  # 中新网安徽_书画艺术
        "http://www.ah.chinanews.com/focus/50.html news",  # 中新网安徽_书画人物
        "http://www.ah.chinanews.com/focus/51.html news",  # 中新网安徽_徽视界
        "http://www.ah.chinanews.com/focus/52.html news",  # 中新网安徽_娱乐八卦
        "http://www.ah.chinanews.com/focus/53.html news",  # 中新网安徽_图说安徽
        "http://www.ah.chinanews.com/focus/54.html news",  # 中新网安徽_安徽名茶
        "http://www.ah.chinanews.com/focus/55.html news",  # 中新网安徽_安徽名酒
        "http://www.ah.chinanews.com/focus/56.html news",  # 中新网安徽_安徽美食
        "http://www.ah.chinanews.com/focus/57.html news",  # 中新网安徽_商业活动
        "http://www.ah.chinanews.com/focus/58.html news",  # 中新网安徽_家电信息
        "http://www.ah.chinanews.com/focus/21.html news",  # 中新网安徽_徽商故事
        "http://www.ah.chinanews.com/focus/59.html news",  # 中新网安徽_创业之路
        "http://www.ah.chinanews.com/focus/22.html news",  # 中新网安徽_招商引资
        "http://www.ah.chinanews.com/focus/23.html news",  # 中新网安徽_安徽名企
        "http://www.ah.chinanews.com/focus/24.html news",  # 中新网安徽_曝光台
        "http://www.ah.chinanews.com/focus/60.html news",  # 中新网安徽_IT快讯
        "http://www.ah.chinanews.com/focus/61.html news",  # 中新网安徽_商业资讯
        "http://www.ah.chinanews.com/focus/11.html news",  # 中新网安徽_文娱体育
        "http://www.bj.chinanews.com/focus/1.html news",  # 中新网北京_聚焦
        "http://www.bj.chinanews.com/focus/3.html news",  # 中新网北京_季风
        "http://www.bj.chinanews.com/focus/8.html news",  # 中新网北京_休闲
        "http://www.bj.chinanews.com/focus/10.html news",  # 中新网北京_科教
        "http://www.cq.chinanews.com/more/zxsbdcq.shtml news",  # 中新网重庆_中新社报道重庆
        "http://www.cq.chinanews.com/more/jucq.shtml news",  # 中新网重庆_聚焦重庆
        "http://www.cq.chinanews.com/more/lhcq.shtml news",  # 中新网重庆_乐活重庆
        "http://www.cq.chinanews.com/more/xzcq.shtml news",  # 中新网重庆_行走重庆
        "http://www.cq.chinanews.com/more/31.shtml news",  # 中新网重庆_重庆IN
        "http://www.cq.chinanews.com/more/45.shtml news",  # 中新网重庆_房产要闻
        "http://www.cq.chinanews.com/more/48.shtml news",  # 中新网重庆_楼市速递
        "http://www.cq.chinanews.com/more/44.shtml news",  # 中新网重庆_中新播报
        "http://www.cq.chinanews.com/more/49.shtml news",  # 中新网重庆_房产访谈间
        "http://www.cq.chinanews.com/more/50.shtml news",  # 中新网重庆_促销优惠
        "http://www.cq.chinanews.com/more/51.shtml news",  # 中新网重庆_业内
        "http://www.cq.chinanews.com/more/52.shtml news",  # 中新网重庆_报料台
        "http://www.cq.chinanews.com/more/53.shtml news",  # 中新网重庆_楼市观察
        "http://www.cq.chinanews.com/more/54.shtml news",  # 中新网重庆_业主声音
        "http://www.cq.chinanews.com/more/56.shtml news",  # 中新网重庆_楼市政策
        "http://www.cq.chinanews.com/more/55.shtml news",  # 中新网重庆_住房
        "http://www.cq.chinanews.com/more/59.shtml news",  # 中新网重庆_地产榜样
        "http://www.cq.chinanews.com/more/58.shtml news",  # 中新网重庆_热点评论
        "http://www.cq.chinanews.com/more/60.shtml news",  # 中新网重庆_看房
        "http://www.cq.chinanews.com/more/66.shtml news",  # 中新网重庆_活动看板
        "http://www.cq.chinanews.com/more/65.shtml news",  # 中新网重庆_家居
        "http://www.cq.chinanews.com/more/180.shtml news",  # 中新网重庆_银行资讯
        "http://www.cq.chinanews.com/more/182.shtml news",  # 中新网重庆_信贷资讯
        "http://www.cq.chinanews.com/more/173.shtml news",  # 中新网重庆_投资理财
        "http://www.cq.chinanews.com/more/181.shtml news",  # 中新网重庆_我爱银行卡
        "http://www.cq.chinanews.com/more/183.shtml news",  # 中新网重庆_贵金属理财
        "http://www.cq.chinanews.com/more/172.shtml news",  # 中新网重庆_直播访谈
        "http://www.cq.chinanews.com/more/185.shtml news",  # 中新网重庆_重保资讯
        "http://www.cq.chinanews.com/more/186.shtml news",  # 中新网重庆_产品点评
        "http://www.cq.chinanews.com/more/178.shtml news",  # 中新网重庆_协会动态
        "http://www.cq.chinanews.com/more/4.shtml news",  # 中新网重庆_中新记者看重庆
        "http://www.cq.chinanews.com/more/5.shtml news",  # 中新网重庆_本网报道
        "http://www.cq.chinanews.com/more/11.shtml news",  # 中新网重庆_社会新闻
        "http://www.cq.chinanews.com/more/szqx.shtml news",  # 中新网重庆_时政区县
        "http://www.cq.chinanews.com/more/10.shtml news",  # 中新网重庆_微话题
        "http://www.cq.chinanews.com/more/23.shtml news",  # 中新网重庆_娱乐
        "http://www.cq.chinanews.com/more/26.shtml news",  # 中新网重庆_旅游
        "http://www.cq.chinanews.com/more/21.shtml news",  # 中新网重庆_美食
        "http://www.cq.chinanews.com/more/jyxw.shtml news",  # 中新网重庆_教育新闻
        "http://www.cq.chinanews.com/more/25.shtml news",  # 中新网重庆_健康
        "http://www.cq.chinanews.com/more/33.shtml news",  # 中新网重庆_海外刊重庆
        "http://www.cq.chinanews.com/more/gatq.shtml news",  # 中新网重庆_港澳台侨
        "http://www.cq.chinanews.com/more/32.shtml news",  # 中新网重庆_人物故事
        "http://www.cq.chinanews.com/more/sqpl.shtml news",  # 中新网重庆_社区评论
        "http://www.cq.chinanews.com/more/zxfw.shtml news",  # 中新网重庆_资讯服务
        "http://www.fj.chinanews.com/fjnews/ttgz/list.html news",  # 中新网福建_头条关注
        "http://www.fj.chinanews.com/fjnews/sjkfj/list.html news",  # 中新网福建_世界看福建
        "http://www.fj.chinanews.com/fjnews/fjzzs/list.html news",  # 中新网福建_福建正在说
        "http://www.fj.chinanews.com/fjnews/qlxdb/list.html news",  # 中新网福建_侨领行动榜
        "http://www.fj.chinanews.com/fjnews/jsxw/list.html news",  # 中新网福建_即时新闻
        "http://www.fj.chinanews.com/fjnews/zxyc/list.html news",  # 中新网福建_中新原创
        "http://www.fj.chinanews.com/fjnews/zbgat/list.html news",  # 中新网福建_直播港澳台
        "http://www.fj.chinanews.com/fjnews/zxsp/list.html news",  # 中新网福建_中新时评
        "http://www.fj.chinanews.com/fjnews/wz/list.html news",  # 中新网福建_问政
        "http://www.fj.chinanews.com/fjnews/all_news.html news",  # 中新网福建_新闻汇总
        "http://www.gs.chinanews.com/gdxw/index.html news",  # 中新网甘肃_滚动新闻
        "http://www.gs.chinanews.com/qykx1/m1.html news",  # 中新网甘肃_企业快讯
        "http://www.gs.chinanews.com/lywx1/m1.html news",  # 中新网甘肃_陇原万象
        "http://www.gs.chinanews.com/rsrm/m1.html news",  # 中新网甘肃_人事变动
        "http://www.gs.chinanews.com/tyxw1/m1.html news",  # 中新网甘肃_体育
        "http://www.gs.chinanews.com/wsxw/m1.html news",  # 中新网甘肃_卫生
        "http://www.gs.chinanews.com/tpxw1/m1.html news",  # 中新网甘肃_图片新闻
        "http://www.gs.chinanews.com/qzlx1/m1.html news",  # 中新网甘肃_甘肃党建
        "http://www.gs.chinanews.com/dscy/m1.html news",  # 中新网甘肃_中新视频·电视采用
        "http://www.gs.chinanews.com/slxy1/m1.html news",  # 中新网甘肃_丝路新语
        "http://www.gs.chinanews.com/gsly1/m1.html news",  # 中新网甘肃_甘肃旅游
        "http://www.gs.chinanews.com/sp/xwsd.html news",  # 中新网甘肃_新闻速递
        "http://www.gs.chinanews.com/sp/shbl.html news",  # 中新网甘肃_社会博览
        "http://www.gs.chinanews.com/sp/wyly.html news",  # 中新网甘肃_文娱旅游
        "http://www.gs.chinanews.com/sp/kjtw.html news",  # 中新网甘肃_科教体卫
        "http://www.gs.chinanews.com/sp/jjzf.html news",  # 中新网甘肃_经济政法
        "http://www.gs.chinanews.com/jrtt1/m1.html news",  # 中新网甘肃_今日头条
        "http://www.gs.chinanews.com/hwkgs1/m1.html news",  # 中新网甘肃_海外媒体刊甘肃
        "http://www.gs.chinanews.com/gsgs60/m1.html news",  # 中新网甘肃_甘肃税务
        "http://www.gs.chinanews.com/ktszt/m1.html news",  # 中新网甘肃_崆峒风情
        "http://www.gs.chinanews.com/lzdl/m1.html news",  # 中新网甘肃_电力在线
        "http://www.gs.chinanews.com/mtkxq/m1.html news",  # 中新网甘肃_媒体看兰州新区
        "http://www.gs.chinanews.com/lshzt/m1.html news",  # 中新网甘肃_兰石化专题
        "http://www.gs.chinanews.com/gshszh/m1.html news",  # 中新网甘肃_甘肃红十字会
        "http://www.gz.chinanews.com/jujiaoguizhou/index.shtml news",  # 中新网贵州_聚焦贵州
        "http://www.gz.chinanews.com/haiwaikanguizhou/index.shtml news",  # 中新网贵州_海外刊贵州
        "http://www.gz.chinanews.com/guanzhu/index.shtml news",  # 中新网贵州_中新关注
        "http://www.gz.chinanews.com/xiaokang/index.shtml news",  # 中新网贵州_同步小康
        "http://www.gz.chinanews.com/lvyou/index.shtml news",  # 中新网贵州_游近走远
        "http://www.gz.chinanews.com/shenghuo/index.shtml news",  # 中新网贵州_时尚生活
        "http://www.gz.chinanews.com/jujiaoguizhou/news/index.shtml news",  # 中新网贵州_热点新闻
        "http://www.gz.chinanews.com/jujiaoguizhou/zhengwurenshi/index.shtml news",  # 中新网贵州_政务人事
        "http://www.gz.chinanews.com/jujiaoguizhou/cnsztsjw/index.shtml news",  # 中新网贵州_直通省纪委
        "http://www.gz.chinanews.com/guanzhu/kanguizhou/index.shtml news",  # 中新网贵州_中新记者看贵州
        "http://www.gz.chinanews.com/guanzhu/fangtan/index.shtml news",  # 中新网贵州_访谈
        "http://www.gz.chinanews.com/shizhou/index.shtml news",  # 中新网贵州_市州风采
        "http://www.gz.chinanews.com/xiaokang/chanjing/index.shtml news",  # 中新网贵州_产经
        "http://www.gz.chinanews.com/xiaokang/shengtai/index.shtml news",  # 中新网贵州_生态
        "http://www.gz.chinanews.com/xiaokang/jiaotong/index.shtml news",  # 中新网贵州_交通
        "http://www.gz.chinanews.com/xiaokang/dangjian/index.shtml news",  # 中新网贵州_党建
        "http://www.gz.chinanews.com/shehui/minsheng/index.shtml news",  # 中新网贵州_民生
        "http://www.gz.chinanews.com/shehui/jingfa/index.shtml news",  # 中新网贵州_警法
        "http://www.gz.chinanews.com/shehui/tiyu/index.shtml news",  # 中新网贵州_体育
        "http://www.gz.chinanews.com/shehui/gongyi/index.shtml news",  # 中新网贵州_公益
        "http://www.gz.chinanews.com/lvyou/dongtai/index.shtml news",  # 中新网贵州_动态
        "http://www.gz.chinanews.com/lvyou/yuanchengtai/index.shtml news",  # 中新网贵州_原生态文化
        "http://www.gz.chinanews.com/lvyou/jingqu/index.shtml news",  # 中新网贵州_景区
        "http://www.gz.chinanews.com/shenghuo/qiyezixun/index.shtml news",  # 中新网贵州_企业资讯
        "http://www.gz.chinanews.com/shenghuo/qiche/index.shtml news",  # 中新网贵州_娱乐
        "http://www.gz.chinanews.com/shenghuo/jiangkang/index.shtml news",  # 中新网贵州_健康
        "http://www.gd.chinanews.com/index/spzx.html news",  # 中新网广东_《品》栏目
        "http://www.gd.chinanews.com/index/heib.html news",  # 中新网广东_黑榜
        "http://www.gd.chinanews.com/index/hongb.html news",  # 中新网广东_红榜

        "http://www.gx.chinanews.com/top/ news",  # 中新网广西_新闻头条
        "http://www.gx.chinanews.com/sz/ news",  # 中新网广西_时政外事  广西的有问题
        "http://www.gx.chinanews.com/cj/ news",  # 中新网广西_财经
        "http://www.gx.chinanews.com/sh/ news",  # 中新网广西_社会
        "http://www.gx.chinanews.com/kjwt/ news",  # 中新网广西_科教文体
        "http://www.gx.chinanews.com/gatq/ news",  # 中新网广西_港澳台侨
        "http://www.gx.chinanews.com/dmsz/ news",  # 中新网广西_东盟时政
        "http://www.gx.chinanews.com/dmjj/ news",  # 中新网广西_东盟经济
        "http://www.gx.chinanews.com/dmsh/ news",  # 中新网广西_东盟社会
        "http://www.gx.chinanews.com/dmwt/ news",  # 中新网广西_东盟文体
        "http://www.gx.chinanews.com/gxgd/ news",  # 中新网广西_广西各地
        "http://www.gx.chinanews.com/ly/ news",  # 中新网广西_旅游
        "http://www.gx.chinanews.com/jr/ news",  # 中新网广西_金融
        "http://www.gx.chinanews.com/qc/ news",  # 中新网广西_汽车
        "http://www.gx.chinanews.com/video/ news",  # 中新网广西_中新视频
        "http://www.gx.chinanews.com/jqzh/ news",  # 中新网广西_节庆展会
        "http://www.gx.chinanews.com/xfwq/ news",  # 中新网广西_消费维权
        "http://www.gx.chinanews.com/mt/ news",  # 中新网广西_外媒看广西
        "http://www.gx.chinanews.com/special/gxzy/ news",  # 中新网广西_广西中烟工业有限责任公司
        "http://www.gx.chinanews.com/special/lzjx/ news",  # 中新网广西_柳州警讯
        "http://www.gx.chinanews.com/special/lzjt/ news",  # 中新网广西_柳州交警伴你出行
        "http://www.gx.chinanews.com/special/lbfy/ news",  # 中新网广西_柳北法院阳光司法专栏

        "http://www.hi.chinanews.com/travel/more/19.html news",  # 中新网海南_头条
        "http://www.hi.chinanews.com/travel/more/20.html news",  # 中新网海南_旅游新闻
        "http://www.hi.chinanews.com/travel/more/22.html news",  # 中新网海南_图片新闻
        "http://www.hi.chinanews.com/travel/more/21.html news",  # 中新网海南_视频
        "http://www.hi.chinanews.com/travel/more/31.html news",  # 中新网海南_线路
        "http://www.hi.chinanews.com/travel/more/27.html news",  # 中新网海南_民俗文化
        "http://www.hi.chinanews.com/jrtt.html news",  # 中新网海南_头条回顾
        "http://www.hi.chinanews.com/gundong/shxw.html news",  # 中新网海南_社会新闻
        "http://www.hi.chinanews.com/gundong/hnzw.html news",  # 中新网海南_海南政务
        "http://www.hi.chinanews.com/gundong/jyxw.html news",  # 中新网海南_教育
        "http://www.hi.chinanews.com/gundong/guoji.html news",  # 中新网海南_国际新闻
        "http://www.hi.chinanews.com/gundong/wenshi.html news",  # 中新网海南_文化历史
        "http://www.hi.chinanews.com/gundong/tiyu.html news",  # 中新网海南_体育新闻
        "http://www.hi.chinanews.com/nk/more/45.html news",  # 中新网海南_焦点图片
        "http://www.hi.chinanews.com/nk/more/44.html news",  # 中新网海南_今日海垦
        "http://www.hi.chinanews.com/nk/more/48.html news",  # 中新网海南_经济
        "http://www.hi.chinanews.com/nk/more/50.html news",  # 中新网海南_二次创业
        "http://www.hi.chinanews.com/nk/more/51.html news",  # 中新网海南_海垦影像
        "http://www.hi.chinanews.com/nk/more/52.html news",  # 中新网海南_海垦人物
        "http://www.hi.chinanews.com/nk/more/54.html news",  # 中新网海南_海垦民生
        "http://www.hi.chinanews.com/nk/more/55.html news",  # 中新网海南_农场联播
        "http://www.hi.chinanews.com/nk/more/59.html news",  # 中新网海南_公告政策
        "http://www.hi.chinanews.com/nk/more/49.html news",  # 中新网海南_旅游
        "http://www.hi.chinanews.com/nk/more/46.html news",  # 中新网海南_橡胶
        "http://www.hi.chinanews.com/nk/more/47.html news",  # 中新网海南_农业
        "http://www.hi.chinanews.com/nk/more/53.html news",  # 中新网海南_海垦印象
        "http://www.hi.chinanews.com/nk/more/58.html news",  # 中新网海南_海垦物产
        "http://www.hi.chinanews.com/movie/more/170.html news",  # 中新网海南_海南新闻
        "http://www.hi.chinanews.com/movie/more/169.html news",  # 中新网海南_天涯来客
        "http://www.hi.chinanews.com/movie/more/171.html news",  # 中新网海南_国内国际
        "http://www.hi.chinanews.com/movie/more/172.html news",  # 中新网海南_社会民生
        "http://www.hi.chinanews.com/movie/more/173.html news",  # 中新网海南_娱乐体育
        "http://www.hi.chinanews.com/movie/more/174.html news",  # 中新网海南_军情直击
        "http://www.hi.chinanews.com/movie/more/176.html news",  # 中新网海南_轻松幽默

        "http://www.hi.chinanews.com/picmore/6.html news",  # 中新网海南_养生
        "http://www.hi.chinanews.com/picmore/7.html news",  # 中新网海南_明星
        "http://www.hi.chinanews.com/picmore/8.html news",  # 中新网海南_奇趣
        "http://www.hi.chinanews.com/picmore/9.html news",  # 中新网海南_自然
        "http://www.hi.chinanews.com/picmore/10.html news",  # 中新网海南_其他
        "http://www.hi.chinanews.com/shiyao/more/177.html news",  # 中新网海南_头条
        "http://www.hi.chinanews.com/shiyao/more/178.html news",  # 中新网海南_焦点图片
        "http://www.hi.chinanews.com/shiyao/more/181.html news",  # 中新网海南_新闻动态
        "http://www.hi.chinanews.com/shiyao/more/188.html news",  # 中新网海南_食药监督
        "http://www.hi.chinanews.com/shiyao/more/184.html news",  # 中新网海南_管理整治
        "http://www.hi.chinanews.com/shiyao/more/212.html news",  # 中新网海南_健康养生
        "http://www.hi.chinanews.com/shiyao/more/187.html news",  # 中新网海南_饮食保健
        "http://www.hi.chinanews.com/zixun/more/64.html news",  # 中新网海南_资讯
        "http://www.hi.chinanews.com/zixun/more/79.html news",  # 中新网海南_生活资讯
        "http://www.hi.chinanews.com/gundong/zhbb.html news",  # 中新网海南_综合播报
        "http://www.hi.chinanews.com/gundong/yliao.html news",  # 中新网海南_科卫
        "http://www.hi.chinanews.com/gundong/72.html news",  # 中新网海南_海南社区热帖
        "http://www.hi.chinanews.com/gundong/qdfl.html news",  # 中新网海南_琼岛评论
        "http://www.hi.chinanews.com/gundong/wbhn.html news",  # 中新网海南_外报海南
        "http://www.hi.chinanews.com/zixun/more/60.html news",  # 中新网海南_演艺
        "http://www.hi.chinanews.com/zixun/more/62.html news",  # 中新网海南_活动
        "http://www.hi.chinanews.com/zixun/more/61.html news",  # 中新网海南_会展
        "http://www.hi.chinanews.com/zixun/more/63.html news",  # 中新网海南_讲座
        "http://www.hi.chinanews.com/zixun/more/76.html news",  # 中新网海南_便民
        "http://www.hi.chinanews.com/zixun/more/78.html news",  # 中新网海南_活动
        "http://www.hi.chinanews.com/zixun/more/77.html news",  # 中新网海南_优惠
        "http://www.hi.chinanews.com/zixun/more/75.html news",  # 中新网海南_招聘
        "http://www.hi.chinanews.com/gundong/qdjw.html news",  # 中新网海南_琼岛见闻

        "http://www.heb.chinanews.com/hbzy/334.shtml news",  # 中新网河北_河北要闻
        "http://www.heb.chinanews.com/jjjjj/445.shtml news",  # 中新网河北_聚焦京津冀
        "http://www.heb.chinanews.com/xaxq/469.shtml news",  # 中新网河北_雄安新区
        "http://www.heb.chinanews.com/shfz/327.shtml news",  # 中新网河北_社会
        "http://www.heb.chinanews.com/fazhi/490.shtml news",  # 中新网河北_法治
        "http://www.heb.chinanews.com/cjzx/329.shtml news",  # 中新网河北_财经
        "http://www.heb.chinanews.com/kjww/331.shtml news",  # 中新网河北_科教
        "http://www.heb.chinanews.com/ylxc/493.shtml news",  # 中新网河北_文体
        "http://www.heb.chinanews.com/jkqg/355.shtml news",  # 中新网河北_旅游
        "http://www.heb.chinanews.com/shenghuo/491.shtml news",  # 中新网河北_生活
        "http://www.heb.chinanews.com/fc/495.shtml news",  # 中新网河北_房产
        "http://www.heb.chinanews.com/jiankang/492.shtml news",  # 中新网河北_健康
        "http://www.heb.chinanews.com/zxjzkhb/321.shtml news",  # 中新网河北_中新社记者看河北
        "http://www.heb.chinanews.com/xabj/479.shtml news",  # 中新网河北_雄安笔记
        "http://www.heb.chinanews.com/part/69/hwkhb.html news",  # 中新网河北_海外看河北
        "http://www.heb.chinanews.com/hbqs/476.shtml news",  # 中新网河北_河北侨商
        "http://www.heb.chinanews.com/zgxwzk/338.shtml news",  # 中新网河北_中国新闻周刊
        "http://www.heb.chinanews.com/more/tupian.shtml news",  # 中新网河北_图片频道
        "http://www.ha.chinanews.com/news/hnxw/ news",  # 中新网河南_河南新闻
        "http://www.ha.chinanews.com/news/jdtp/ news",  # 中新网河南_河南图片
        "http://www.ha.chinanews.com/news/hntx/ news",  # 中新网河南_央企风采
        "http://www.ha.chinanews.com/news/hncj/ news",  # 中新网河南_河南财经
        "http://www.ha.chinanews.com/news/hnjk/ news",  # 中新网河南_河南健康
        "http://www.ha.chinanews.com/news/hnly/ news",  # 中新网河南_河南旅游
        "http://www.ha.chinanews.com/news/hnjy/ news",  # 中新网河南_河南教育
        "http://www.ha.chinanews.com/news/khn/ news",  # 中新网河南_看河南
        "http://www.ha.chinanews.com/news/hnzf/ news",  # 中新网河南_河南政法
        "http://www.ha.chinanews.com/news/hncs/ news",  # 中新网河南_河南慈善
        "http://www.ha.chinanews.com/news/hntc/index.shtml news",  # 中新网河南_河南体彩
        "http://www.ha.chinanews.com/news/fphn/ news",  # 中新网河南_飞拍中国
        "http://www.ha.chinanews.com/news/aqkt/ news",  # 中新网河南_安全课堂
        "http://www.ha.chinanews.com/news/hnty/index.shtml news",  # 中新网河南_河南体育
        "http://www.ha.chinanews.com/news/myhn/index.shtml news",  # 中新网河南_魅眼河南
        "http://www.ha.chinanews.com/news/jdxw/index.shtml news",  # 中新网河南_禁毒新闻
        "http://www.ha.chinanews.com/news/jddt/index.shtml news",  # 中新网河南_禁毒动态
        "http://www.ha.chinanews.com/news/jdfl/index.shtml news",  # 中新网河南_禁毒法律
        "http://www.ha.chinanews.com/news/jdfy/index.shtml news",  # 中新网河南_禁毒防御
        "http://www.hb.chinanews.com/ss.html news",  # 中新网湖北_时尚
        "http://www.hb.chinanews.com/photo/hubei.html news",  # 中新网湖北_图说湖北
        "http://www.hb.chinanews.com/photo/world.html#main news",  # 中新网湖北_国际图片
        "http://www.hb.chinanews.com/photo/ent.html#main news",  # 中新网湖北_娱乐时尚
        "http://www.hb.chinanews.com/photo/travel.html#main news",  # 中新网湖北_灵秀湖北
        "http://www.hb.chinanews.com/photo/fun.html#main news",  # 中新网湖北_趣图趣照
        "http://www.hn.chinanews.com/news/hwmtkhn/index.shtml news",  # 中新网湖南_海外媒体看湖南
        "http://www.hn.chinanews.com/news/hwsj/ news",  # 中新网湖南_视觉湖南
        "http://www.hn.chinanews.com/news/shsh/index.shtml news",  # 中新网湖南_社会生活
        "http://www.hn.chinanews.com/news/gyyq/ news",  # 中新网湖南_工业园区
        "http://www.hn.chinanews.com/news/dgzs/index.shtml news",  # 中新网湖南_打击走私
        "http://www.hn.chinanews.com/news/xzwxfc/index.shtml news",  # 中新网湖南_新作为新风采
        "http://www.hn.chinanews.com/news/gmaq/index.shtml news",  # 中新网湖南_国门安全
        "http://www.hn.chinanews.com/news/zlts/index.shtml news",  # 中新网湖南_质量提升
        "http://www.hn.chinanews.com/news/yhfw/index.shtml news",  # 中新网湖南_优化服务
        "http://www.hn.chinanews.com/news/cjzx/index.shtml news",  # 中新网湖南_财经资讯
        "http://www.hn.chinanews.com/news/hnjj/index.shtml news",  # 中新网湖南_湖南经济
        "http://www.hn.chinanews.com/news/sdbd/index.shtml news",  # 中新网湖南_深度报道
        "http://www.hn.chinanews.com/news/cjsxdt/index.shtml news",  # 中新网湖南_市县动态
        "http://www.hlj.chinanews.com/focus/zfjw.html news",  # 中新网黑龙江_政法警务
        "http://www.hlj.chinanews.com/focus/cjqy.html news",  # 中新网黑龙江_财经企业
        "http://www.hlj.chinanews.com/focus/whly.html news",  # 中新网黑龙江_文化旅游
        "http://www.hlj.chinanews.com/focus/sgnksy.html news",  # 中新网黑龙江_森工农垦油田
        "http://www.hlj.chinanews.com/focus/dsbb.html news",  # 中新网黑龙江_地市播报
        "http://www.hlj.chinanews.com/focus/blpt.html news",  # 中新网黑龙江_爆料平台
        "http://www.hlj.chinanews.com/focus/lylj.html news",  # 中新网黑龙江_绿业龙江
        "http://www.js.chinanews.com/video/citynews/ news",  # 中新网江苏_社会万象
        "http://www.js.chinanews.com/video/science/ news",  # 中新网江苏_科教人文
        "http://www.js.chinanews.com/video/overseas/ news",  # 中新网江苏_港澳台侨
        "http://www.js.chinanews.com/video/tour/ news",  # 中新网江苏_旅游休闲
        "http://www.js.chinanews.com/video/special/ news",  # 中新网江苏_专题报道
        ###江西 全部超时
        ### "http://www.jx.chinanews.com/bgt/ news",  # 中新网江西_曝光台
        ### "http://www.jx.chinanews.com/mil/ news",  # 中新网江西_军事
        ### "http://www.jx.chinanews.com/gongyi/ news",  # 中新网江西_公益
        ### "http://www.jx.chinanews.com/video/ news",  # 中新网江西_视频
        ### "http://www.jx.chinanews.com/chanxiu/ news",  # 中新网江西_禅修
        ### "http://www.jx.chinanews.com/caishui/ news",  # 中新网江西_财税

        "http://www.jl.chinanews.com/jlyw/index.shtml news",  # 中新网吉林_吉林要闻
        "http://www.jl.chinanews.com/shidian/index.shtml news",  # 中新网吉林_视点
        "http://www.jl.chinanews.com/hqrd/index.shtml news",  # 中新网吉林_环球热点
        "http://www.jl.chinanews.com/gnyw/index.shtml news",  # 中新网吉林_国内要闻
        "http://www.jl.chinanews.com/tsjl/index.shtml news",  # 中新网吉林_图说吉林
        "http://www.jl.chinanews.com/szjj/index.shtml news",  # 中新网吉林_时政聚焦
        "http://www.jl.chinanews.com/cjbd/index.shtml news",  # 中新网吉林_财经报道
        "http://www.jl.chinanews.com/shms/index.shtml news",  # 中新网吉林_社会民生
        "http://www.jl.chinanews.com/kjww/index.shtml news",  # 中新网吉林_科教文卫
        "http://www.jl.chinanews.com/sdgc/index.shtml news",  # 中新网吉林_深度观察
        "http://www.jl.chinanews.com/tbgz/index.shtml news",  # 中新网吉林_特别关注
        "http://www.jl.chinanews.com/rszl/index.shtml news",  # 中新网吉林_人参专栏
        "http://www.jl.chinanews.com/gclt/index.shtml news",  # 中新网吉林_高层论坛
        "http://www.jl.chinanews.com/jlly/index.shtml news",  # 中新网吉林_吉林旅游
        "http://www.jl.chinanews.com/rsbd/index.shtml news",  # 中新网吉林_人事变动
        "http://www.jl.chinanews.com/mqtj/index.shtml news",  # 中新网吉林_名企推介
        "http://www.jl.chinanews.com/gatq/index.shtml news",  # 中新网吉林_港澳台侨
        "http://www.jl.chinanews.com/msfq/index.shtml news",  # 中新网吉林_民俗风情
        "http://www.jl.chinanews.com/jkzx/index.shtml news",  # 中新网吉林_健康在线
        "http://www.jl.chinanews.com/dcls/index.shtml news",  # 中新网吉林_地产楼市
        "http://www.jl.chinanews.com/wcjl/index.shtml news",  # 中新网吉林_文萃交流
        "http://www.jl.chinanews.com/bwrs/index.shtml news",  # 中新网吉林_百味人生
        "http://www.jl.chinanews.com/hyhc/index.shtml news",  # 中新网吉林_行业荟萃
        "http://www.jl.chinanews.com/qccy/index.shtml news",  # 中新网吉林_汽车产业
        "http://www.jl.chinanews.com/jwmtsjl/index.shtml news",  # 中新网吉林_境外媒体说吉林
        "http://www.jl.chinanews.com/zxsjzzl/index.shtml news",  # 中新网吉林_中新社记者专栏
        "http://www.jl.chinanews.com/xwfbh/index.shtml news",  # 中新网吉林_新闻发布会
        "http://www.ln.chinanews.com/shipin/index.shtml news",  # 中新网辽宁_视频
        "http://www.ln.chinanews.com/dfxw/index.shtml news",  # 中新网辽宁_地方新闻
        "http://www.nmg.chinanews.com/zxxw/index.html news",  # 中新网内蒙古_中新新闻
        "http://www.nmg.chinanews.com/nmgxw/index.html news",  # 中新网内蒙古_内蒙古新闻
        "http://www.nmg.chinanews.com/zxtp/index.html news",  # 中新网内蒙古_中新图片
        "http://www.nmg.chinanews.com/kjww/index.html news",  # 中新网内蒙古_科技文卫
        "http://www.nmg.chinanews.com/zlqqzxd/index.html news",  # 中新网内蒙古_质量强区在行动
        "http://www.nmg.chinanews.com/msdt/index.html news",  # 中新网内蒙古_盟市动态
        "http://www.nmg.chinanews.com/hlnmg/index.html news",  # 中新网内蒙古_活力内蒙古
        "http://www.nmg.chinanews.com/shjd/index.html news",  # 中新网内蒙古_社会监督
        "http://www.nmg.chinanews.com/jyzx/index.html news",  # 中新网内蒙古_教育在线
        "http://www.nmg.chinanews.com/qyxw/index.html news",  # 中新网内蒙古_资讯广告
        "http://www.nmg.chinanews.com/nmgjy/index.html news",  # 中新网内蒙古_内蒙古精英
        "http://www.nmg.chinanews.com/bxsh/index.html news",  # 中新网内蒙古_百姓热点
        "http://www.nmg.chinanews.com/gatrd/index.html news",  # 中新网内蒙古_港澳台热点
        "http://www.nmg.chinanews.com/zxsj/index.html news",  # 中新网内蒙古_中新视角
        "http://www.qh.chinanews.com/yw/index.shtml news",  # 中新网青海_青海要闻
        "http://www.qh.chinanews.com/hwkqh/index.shtml news",  # 中新网青海_海外刊青海
        "http://www.qh.chinanews.com/zxjzzqh/index.shtml news",  # 中新网青海_中新记者在青海
        "http://www.qh.chinanews.com/qhsp/index.shtml news",  # 中新网青海_青海视频
        "http://www.qh.chinanews.com/dsp/index.shtml news",  # 中新网青海_短视频
        "http://www.qh.chinanews.com/zb/index.shtml news",  # 中新网青海_直播
        "http://www.qh.chinanews.com/qhgd/index.shtml news",  # 中新网青海_青海各地
        "http://www.qh.chinanews.com/dj/index.shtml news",  # 中新网青海_党建
        "http://www.qh.chinanews.com/zq/index.shtml news",  # 中新网青海_企业
        "http://www.qh.chinanews.com/sh/index.shtml news",  # 中新网青海_社会
        "http://www.qh.chinanews.com/cj/index.shtml news",  # 中新网青海_产经
        "http://www.qh.chinanews.com/ty/index.shtml news",  # 中新网青海_体育
        "http://www.qh.chinanews.com/wy/index.shtml news",  # 中新网青海_文娱
        "http://www.qh.chinanews.com/kj/index.shtml news",  # 中新网青海_科教
        "http://www.qh.chinanews.com/st/index.shtml news",  # 中新网青海_生态
        "http://www.qh.chinanews.com/xmt/index.shtml news",  # 中新网青海_新媒体
        ## "http://www.qh.chinanews.com/bwzt/index.shtml news",  # 中新网青海_本网专题 # 专题
        ## "http://www.qh.chinanews.com/wsj/index.shtml news",  # 中新网青海_微视界  # 特殊结构
        "http://www.sx.chinanews.com/list/yaowen.html news",  # 中新网山西_山西要闻
        "http://www.sx.chinanews.com/list/guanzhu.html news",  # 中新网山西_中新关注
        "http://www.sx.chinanews.com/list/shanxi.html news",  # 中新网山西_中新记者看山西
        "http://www.sx.chinanews.com/list/bwsp.html news",  # 中新网山西_中新视频
        "http://www.sx.chinanews.com/list/jujiao.html news",  # 中新网山西_聚焦
        "http://www.sx.chinanews.com/list/shizheng.html news",  # 中新网山西_时政
        "http://www.sx.chinanews.com/list/caijing.html news",  # 中新网山西_财经新闻
        "http://www.sx.chinanews.com/list/sxbaoxian.html news",  # 中新网山西_山西保险
        "http://www.sx.chinanews.com/list/bank.html news",  # 中新网山西_银行
        "http://www.sx.chinanews.com/list/shehui.html news",  # 中新网山西_社会新闻
        "http://www.sx.chinanews.com/list/chengshi.html news",  # 中新网山西_城市新闻
        "http://www.sx.chinanews.com/list/xingxian.html news",  # 中新网山西_红色兴县
        "http://www.sx.chinanews.com/list/yaodu.html news",  # 中新网山西_今日尧都
        "http://www.sx.chinanews.com/list/xtm.html news",  # 中新网山西_新同煤
        "http://www.sx.chinanews.com/list/lvyou.html news",  # 中新网山西_旅游新闻
        "http://www.sx.chinanews.com/list/wenhua.html news",  # 中新网山西_文化新闻
        "http://www.sx.chinanews.com/list/jiaoyu.html news",  # 中新网山西_教育新闻
        "http://www.sx.chinanews.com/list/tiyu.html news",  # 中新网山西_体育新闻
        "http://www.sx.chinanews.com/health/list/8.html news",  # 中新网山西_健康资讯
        "http://www.sx.chinanews.com/list/pinglun.html news",  # 中新网山西_评论
        "http://www.sx.chinanews.com/list/puzhou.html news",  # 中新网山西_蒲州新闻
        "http://www.sx.chinanews.com/list/czcq.html news",  # 中新网山西_长治城区新闻
        "http://www.sx.chinanews.com/list/pic.html news",  # 中新网山西_山西影像
        "http://www.sx.chinanews.com/linfen/list/2.html news",  # 中新网山西_山西临汾本网专稿
        "http://www.sx.chinanews.com/linfen/list/1.html news",  # 中新网山西_山西临汾要闻
        "http://www.sx.chinanews.com/linfen/list/3.html news",  # 中新网山西_山西临汾政情
        "http://www.sx.chinanews.com/linfen/list/4.html news",  # 中新网山西_山西临汾产经
        "http://www.sx.chinanews.com/linfen/list/5.html news",  # 中新网山西_山西临汾区县
        "http://www.sx.chinanews.com/linfen/list/6.html news",  # 中新网山西_山西临汾文化
        "http://www.sx.chinanews.com/linfen/list/7.html news",  # 中新网山西_山西临汾旅游
        "http://www.shx.chinanews.com/rsrm.html news",  # 中新网陕西_人事任免
        "http://www.shx.chinanews.com/zwjs.html news",  # 中新网陕西_政务建设
        "http://www.sh.chinanews.com/wenhua/index.shtml news",  # 中新网上海_文化
        "http://www.sh.chinanews.com/tiyu/index.shtml news",  # 中新网上海_体育
        "http://www.sh.chinanews.com/shishang/index.shtml news",  # 中新网上海_时尚
        "http://www.sh.chinanews.com/yule/index.shtml news",  # 中新网上海_娱乐
        "http://www.sh.chinanews.com/ckzx/index.shtml news",  # 中新网上海_创客
        "http://www.sh.chinanews.com/chanjing/index.shtml news",  # 中新网上海_产经
        "http://www.sh.chinanews.com/jinrong/index.shtml news",  # 中新网上海_金融
        "http://www.sh.chinanews.com/loushi/index.shtml news",  # 中新网上海_楼市
        "http://www.sh.chinanews.com/hgjj/index.shtml news",  # 中新网上海_宏观经济
        "http://www.sh.chinanews.com/bdrd/index.shtml news",  # 中新网上海_本地热点
        "http://www.sh.chinanews.com/yljk/index.shtml news",  # 中新网上海_医疗健康
        "http://www.sh.chinanews.com/kjjy/index.shtml news",  # 中新网上海_科技教育
        "http://www.sh.chinanews.com/fzzx/index.shtml news",  # 中新网上海_法制资讯
        "http://www.sh.chinanews.com/fengxian/index.shtml news",  # 中新网上海_奉贤
        "http://www.sh.chinanews.com/ckgs/index.shtml news",  # 中新网上海_创客故事
        "http://www.sh.chinanews.com/dangjian/index.shtml news",  # 中新网上海_党建
        "http://www.sc.chinanews.com/scxw/index.shtml news",  # 中新网四川_四川新闻
        "http://www.sc.chinanews.com/glgj/index.shtml news",  # 中新网四川_国内国际
        "http://www.sc.chinanews.com/bwbd/index.shtml news",  # 中新网四川_本网报道
        "http://www.sc.chinanews.com/tpxw/index.shtml news",  # 中新网四川_图片新闻
        "http://www.sc.chinanews.com/szjj/index.shtml news",  # 中新网四川_市州聚焦
        "http://www.sc.chinanews.com/spxw/index.shtml news",  # 中新网四川_视频新闻
        "http://www.sc.chinanews.com/szbd/index.shtml news",  # 中新网四川_时政报道
        "http://www.sc.chinanews.com/zxjzzsc/index.shtml news",  # 中新网四川_中新记者在四川
        "http://www.sc.chinanews.com/gatq/index.shtml news",  # 中新网四川_港澳台侨
        "http://www.sc.chinanews.com/cjbd/index.shtml news",  # 中新网四川_财经报道
        "http://www.sc.chinanews.com/ylss/index.shtml news",  # 中新网四川_时尚娱乐
        "http://www.sc.chinanews.com/hwmtksc/index.shtml news",  # 中新网四川_海外媒体刊四川
        "http://www.sc.chinanews.com/shms/index.shtml news",  # 中新网四川_社会民生
        "http://www.sc.chinanews.com/lyxw/index.shtml news",  # 中新网四川_旅游新闻
        "http://www.sc.chinanews.com/whty/index.shtml news",  # 中新网四川_文化体育
        "http://www.sc.chinanews.com/shfw/index.shtml news",  # 中新网四川_生活服务
        "http://www.sc.chinanews.com/kjws/index.shtml news",  # 中新网四川_科教卫生
        "http://www.sc.chinanews.com/fctt/index.shtml news",  # 中新网四川_房产头条
        "http://www.sc.chinanews.com/gsbd/index.shtml news",  # 中新网四川_公司报道
        "http://www.sc.chinanews.com/scyw/index.shtml news",  # 中新网四川_市场要闻
        "http://www.sc.chinanews.com/zcdt/index.shtml news",  # 中新网四川_政策动态
        "http://www.xj.chinanews.com/tupian/pic.d.html?nid=61 news",  # 中新网新疆_图片新闻
        "http://www.xj.chinanews.com/tupian/pic.d.html?nid=62 news",  # 中新网新疆_视频新闻
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=63 news",  # 中新网新疆_新疆要闻
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=64 news",  # 中新网新疆_国内新闻
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=65 news",  # 中新网新疆_经济新闻
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=66 news",  # 中新网新疆_社会民生
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=67 news",  # 中新网新疆_科教体育
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=68 news",  # 中新网新疆_华文报摘
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=69 news",  # 中新网新疆_援疆信息
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=70 news",  # 中新网新疆_旅游文化
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=71 news",  # 中新网新疆_资源开发
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=72 news",  # 中新网新疆_一带一路
        "http://www.xj.chinanews.com/tupian/pic.d.html?nid=73 news",  # 中新网新疆_图文专稿
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=74 news",  # 中新网新疆_兵团
        "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=75 news",  # 中新网新疆_地州
        "http://www.bt.chinanews.com/xinjiang/index.shtml news",  # 中新网兵团_新疆新闻
        "http://www.yn.chinanews.com/zxsd/index.shtml news",  # 中新网云南_中新速递
        "http://www.yn.chinanews.com/sp/index.shtml news",  # 中新网云南_视频中新
        "http://www.yn.chinanews.com/qw/index.shtml news",  # 中新网云南_侨务
        "http://www.yn.chinanews.com/dmny/index.shtml news",  # 中新网云南_东盟南亚
        "http://www.yn.chinanews.com/fszx/index.shtml news",  # 中新网云南_辐射中心
        "http://www.yn.chinanews.com/mztj/index.shtml news",  # 中新网云南_民族团结
        "http://www.yn.chinanews.com/stwm/index.shtml news",  # 中新网云南_生态文明
        "http://www.yn.chinanews.com/zsdt/index.shtml news",  # 中新网云南_州市动态
        "http://www.yn.chinanews.com/yl/index.shtml news",  # 中新网云南_娱乐
        "http://www.yn.chinanews.com/ly/index.shtml news",  # 中新网云南_旅游
        "http://www.yn.chinanews.com/edu/index.shtml news",  # 中新网云南_教育
        "http://www.yn.chinanews.com/qyzx/index.shtml news",  # 中新网云南_企业资讯
        "http://www.yn.chinanews.com/gyts/index.shtml news",  # 中新网云南_高原特色
        "http://www.yn.chinanews.com/car/index.shtml news",  # 中新网云南_汽车
        "http://www.yn.chinanews.com/fc/index.shtml news",  # 中新网云南_房产
        "http://www.yn.chinanews.com/cj/index.shtml news",  # 中新网云南_财经
        "http://www.yn.chinanews.com/tpgj/index.shtml news",  # 中新网云南_脱贫攻坚
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=50 news",  # 中新网浙江_中新记者看浙江
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=272 news",  # 中新网浙江_浙江要闻
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=273 news",  # 中新网浙江_侨乡侨务
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=276 news",  # 中新网浙江_视频
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=277 news",  # 中新网浙江_镜像浙江
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=278 news",  # 中新网浙江_图集
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=280 news",  # 中新网浙江_浙商
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=282 news",  # 中新网浙江_政策
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=281 news",  # 中新网浙江_金融
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=283 news",  # 中新网浙江_观点
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=285 news",  # 中新网浙江_政策直击
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=287 news",  # 中新网浙江_高校
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=291 news",  # 中新网浙江_中小学
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=288 news",  # 中新网浙江_创业
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=289 news",  # 中新网浙江_考研
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=290 news",  # 中新网浙江_留学
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=292 news",  # 中新网浙江_幼儿园
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=293 news",  # 中新网浙江_育儿
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=294 news",  # 中新网浙江_公考
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=295 news",  # 中新网浙江_司法考试
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=297 news",  # 中新网浙江_教师资格证
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=299 news",  # 中新网浙江_旅游直通车
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=302 news",  # 中新网浙江_健康产业
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=303 news",  # 中新网浙江_养生养老
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=304 news",  # 中新网浙江_浙江体育
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=305 news",  # 中新网浙江_体育产业
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=301 news",  # 中新网浙江_图说旅游
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=307 news",  # 中新网浙江_明星
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=313 news",  # 中新网浙江_视频
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=308 news",  # 中新网浙江_影视
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=309 news",  # 中新网浙江_音乐
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=310 news",  # 中新网浙江_文化·展览
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=311 news",  # 中新网浙江_非遗
        "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=312 news",  # 中新网浙江_图集
        ### "http://www.jx.chinanews.com/wenhua/ news",  # 中国新闻网_文化 # timeout
        ### "http://www.gx.chinanews.com/GBK/1912/ news",  # 中国新闻网_广西财经资讯  # 404
        ### "http://www.gx.chinanews.com/GBK/1913/ news",  # 中国新闻网_广西社会法制  # 404
        ### "http://www.jx.chinanews.com/house/ news",  # 中国新闻网_房产 timeout
        ### "http://www.jx.chinanews.com/life/ news",  # 中国新闻网_生活 timeout
        ### "http://www.jx.chinanews.com/sports/ news",  # 中国新闻网_体育  # 404
        ### "http://www.xj.chinanews.com/html/L_69.htm news",  # 中国新闻网_新疆要闻  # 404
        ### "http://www.xj.chinanews.com/html/L_56.htm news",  # 中国新闻网_新疆资源开发  # 404
        ### "http://www.xj.chinanews.com/html/L_63.htm news",  # 中国新闻网_新疆科教文卫  # 404
        ### "http://www.xj.chinanews.com/html/L_60.htm news",  # 中国新闻网_新疆侨务  # 404
        ### "http://www.xj.chinanews.com/html/L_65.htm news",  # 中国新闻网_新疆文化  # 404
        ### "http://www.sc.chinanews.com/news/News_SiChuan/list.html news",  # 中国新闻网_四川新闻  # 404
        ### "http://www.sc.chinanews.com/travel/Travel_News/list.html news",  # 中国新闻网_旅游  # 404
        ### "http://www.sc.chinanews.com/news/News_chengdu/list.html news",  # 中国新闻网_成都新闻  # 404
        ### "http://www.ln.chinanews.com/guojixinwen/ news",  # 中国新闻网_辽宁国际  # 404
        ### "http://www.bt.chinanews.com/News/huiyi/ news",  # 中新网兵团新闻网_会议  # 404
        ### "http://www.chinanews.com/photo/HD.html news",  # 中国新闻网_高清 空的
        "http://www.chinanews.com/photo/gnjj.html news",  # 中国新闻网_图片国内聚焦
        "http://www.chinanews.com/photo/shbt.html news",  # 中国新闻网_图片社会百态
        ### "http://www.jl.chinanews.com/bmfw.html news",  # 中国新闻网_文萃交流  # 404
        ### "http://www.ln.chinanews.com/zhichang news",  # 辽宁新闻网_职场  # 404
        ### "http://www.jx.chinanews.com/guonei/ news",  # 中国新闻网_江西国内新闻 timeout
        ### "http://www.jx.chinanews.com/jxnews/ news",  # 中国新闻网_江西新闻  # 404
        ### "http://www.jx.chinanews.com/shizhen/ news",  # 中国新闻网_江西时政  # 404
        ### "http://www.gx.chinanews.com/DM/1803/ news",  # 中国新闻网_广西东盟社会  # 404
        ### "http://www.gx.chinanews.com/DM/1802/ news",  # 中国新闻网_广西东盟经济  # 404
        ### "http://www.gx.chinanews.com/GBK/1916/ news",  # 中国新闻网_媒体看广西  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1604/ news",  # 中国新闻网_玉林  # 404
        ### "http://www.gx.chinanews.com/DM/1801/ news",  # 中国新闻网_广西科教文体  # 404
        ### "http://www.gx.chinanews.com/service/1501/ news",  # 中国新闻网_广西房地产  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1611/ news",  # 中国新闻网_贺州  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1610/ news",  # 中国新闻网_百色  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1612/ news",  # 中国新闻网_河池  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1605/ news",  # 中国新闻网_钦州  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1609/ news",  # 中国新闻网_贵港  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1606/ news",  # 中国新闻网_防城港  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1613/ news",  # 中国新闻网_来宾  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1608/ news",  # 中国新闻网_北海  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1607/ news",  # 中国新闻网_梧州  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1614/ news",  # 中国新闻网_崇左  # 404
        ### "http://www.gx.chinanews.com/GBK/1914/ news",  # 中国新闻网_科教文体  # 404
        ### "http://www.ha.chinanews.com/qiaowu/html/qiaowu/qiaojiedongtai/ news",  # 中国新闻网_侨界动态  # 404
        ### "http://www.jx.chinanews.com/auto news",  # 中国新闻网_汽车  # 404
        ### "http://www.gx.chinanews.com/GBK/1910/ news",  # 中国新闻网_广西时政外事  # 404
        ### "http://www.jx.chinanews.com/world/ news",  # 中国新闻网_江西国际 timeout
        ### "http://www.xj.chinanews.com/html/L_43.htm news",  # 中国新闻网_新疆新闻评论  # 404
        ### "http://www.xj.chinanews.com/html/L_57.htm news",  # 新疆新闻网_新疆彩票  # 404
        ### "http://www.xj.chinanews.com/html/L_46.htm news",  # 新疆新闻网_高端动态  # 404
        ### "http://www.xj.chinanews.com/html/L_49.htm news",  # 新疆新闻网_健康资讯  # 404
        ### "http://www.xj.chinanews.com/html/L_48.htm news",  # 新疆新闻网_体育新闻  # 404
        ### "http://www.xj.chinanews.com/html/L_58.htm news",  # 新疆新闻网_旅游资讯  # 404
        ### "http://www.xj.chinanews.com//html/L_50.htm news",  # 新疆新闻网_国际新闻  # 404
        ### "http://www.xj.chinanews.com/html/L_55.htm news",  # 新疆新闻网_中亚经济  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=14 news",  # 中国新闻网_安徽经济动态  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=17 news",  # 中国新闻网_安徽要闻  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=26 news",  # 中国新闻网_安徽企业新闻  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=25 news",  # 中国新闻网_安徽房产汽车  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=30 news",  # 中国新闻网_安徽法制新闻  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=20 news",  # 中国新闻网_安徽各地聚焦  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=48 news",  # 中国新闻网_安徽媒体聚焦  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=19 news",  # 中国新闻网_安徽经济观察  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=16 news",  # 中国新闻网_安徽舆论监督  # 404
        "http://www.gs.chinanews.com/whws1/m1.html news",  # 中国新闻网_文化
        "http://www.chinanews.com/entertainment/photo/gzjtphoto-1.html news",  # 狗仔镜头
        ### "http://www.bt.chinanews.com/News/yaowen/ news",  # 中国新闻网_兵团要闻  # 404
        "http://www.chinanews.com/photo/ylty.html news",  # 图片放送
        ### ### "http://www.js.chinanews.com/nt/ news",  # 江苏新闻网_首页  # 404
        ### "http://www.zj.chinanews.com/tech/ news",  # 中国新闻网_浙江科技  # 404
        ### "http://www.zj.chinanews.com/sports/ news",  # 中国新闻网_浙江体育  # 404
        ### "http://www.zj.chinanews.com/finance/ news",  # 中国新闻网_浙江财经  # 404
        ### "http://www.zj.chinanews.com/edu/ news",  # 中国新闻网_浙江教育  # 404
        ### "http://www.zj.chinanews.com/list/21/1.html news",  # 中国新闻网_港澳台  # 404
        ### "http://www.sc.chinanews.com/news/News_gat/list.html news",  # 中国新闻网_四川港澳台侨  # 404
        ### "http://www.sc.chinanews.com/house/Housing_News/list.html news",  # 中国新闻网_四川房产新闻  # 404
        ### "http://www.sc.chinanews.com/news/News_Social/list.html news",  # 中国新闻网_四川社会新闻  # 404
        ### "http://www.sc.chinanews.com/news/News_Municipal/list.html news",  # 中国新闻网_四川市州新闻  # 404
        ### "http://www.sc.chinanews.com/news/News_financial/list.html news",  # 中国新闻网_四川财经新闻  # 404
        ### "http://www.sc.chinanews.com/news/Homenews/list.html news",  # 中国新闻网_四川国内国际  # 404
        ### "http://www.sc.chinanews.com/news/News_SiChuanReporter/list.html news",  # 中国新闻网_中新社记者在四川  # 404
        ### "http://www.sc.chinanews.com/news/News_entertainment/list.html news",  # 中国新闻网_娱乐时尚  # 404
        ### "http://www.sc.chinanews.com/life/News/list.html news",  # 中国新闻网_生活服务  # 404
        ### "http://www.ln.chinanews.com/guoneixinwen news",  # 辽宁新闻网_国内  # 404
        ### "http://www.ln.chinanews.com/shenyang news",  # 辽宁新闻网_沈阳  # 404
        ### "http://www.ln.chinanews.com/yuanchuangxinwen news",  # 辽宁新闻网_原创新闻  # 404
        ### "http://www.ln.chinanews.com/shehuixinwen news",  # 辽宁新闻网_社会  # 404
        ### "http://www.ln.chinanews.com/liaoningxinwen news",  # 辽宁新闻网_辽宁  # 404
        ### "http://www.ln.chinanews.com/yuanchuangxinwen/ news",  # 中国新闻网_原创  # 404
        ### "http://www.ln.chinanews.com/chuxing/ news",  # 中国新闻网_出行  # 404
        ### "http://www.ln.chinanews.com/fuwu/ news",  # 中国新闻网_服务  # 404
        "http://www.chinanews.com/scroll-news/news1.html news",  # 中国新闻网_滚动新闻
        "http://www.gs.chinanews.com/kjxw1/m1.html news",  # 中国新闻网_甘肃科技
        "http://www.gs.chinanews.com/wsqw1/m1.html news",  # 中国新闻网_甘肃外事侨务
        "http://www.gs.chinanews.com/gsyw1/m1.html news",  # 中国新闻网_甘肃要闻
        "http://www.gs.chinanews.com/dishi/gannan.htm news",  # 中国新闻网_甘南新闻
        "http://www.gs.chinanews.com/zwrs1/m1.html news",  # 中国新闻网_甘肃政务
        "http://www.gs.chinanews.com/shms1/m1.html news",  # 中国新闻网_甘肃社会民生
        "http://www.gs.chinanews.com/fzxw/m1.html news",  # 中国新闻网_甘肃法制
        "http://www.gs.chinanews.com/jjxw1/m1.html news",  # 中国新闻网_甘肃财经新闻
        "http://www.yn.chinanews.com/pub/caijing/ news",  # 云南新闻网_财经新闻
        "http://www.yn.chinanews.com/pub/news/world/guonei/ news",  # 云南新闻网_国内新闻
        "http://www.yn.chinanews.com/pub/news/sudi/ news",  # 云南新闻网_中新速递
        ### "http://www.gx.chinanews.com/GBK/c/1602/ news",  # 中国新闻网_柳州新闻  # 404
        ### "http://www.gx.chinanews.com/GBK/c/1601/ news",  # 中国新闻网_南宁新闻  # 404
        ### "http://www.gx.chinanews.com/GBK/1911/ news",  # 中国新闻网_港澳台侨  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=28 news",  # 中国新闻网_安徽社会生活  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=21 news",  # 中国新闻网_安徽即时播报  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=29 news",  # 中国新闻网_安徽民生热线  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=47 news",  # 中国新闻网_安徽国内新闻  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=51 news",  # 中国新闻网_安徽新闻直播  # 404
        ### "http://www.bt.chinanews.com/News/jianghua/ news",  # 中国新闻网_兵团讲话  # 404
        ### "http://www.bt.chinanews.com/News/guotu/ news",  # 中国新闻网_兵团国土  # 404
        ### "http://www.bt.chinanews.com/News/shehui/ news",  # 中国新闻网_兵团社会  # 404
        ### "http://www.bt.chinanews.com/News/lingdao/ news",  # 中国新闻网_兵团领导  # 404
        ### "http://www.bt.chinanews.com/YanL/ysyy/ news",  # 中国新闻网_兵团一事一议  # 404
        ### "http://www.bt.chinanews.com/News/yuanjiang/ news",  # 中国新闻网_兵团援疆  # 404
        ### "http://www.bt.chinanews.com/News/shiju/ news",  # 中国新闻网_兵团师团  # 404
        ### "http://www.bt.chinanews.com/News/liandui/ news",  # 中国新闻网_兵团连队  # 404
        ### "http://www.bt.chinanews.com/News/tuanchang/ news",  # 中国新闻网_兵团团场  # 404
        ### "http://www.bt.chinanews.com/News/kejiao/ news",  # 中国新闻网_兵团科技  # 404
        ### "http://www.bt.chinanews.com/PhotoT/ddqy/ news",  # 兵团新闻网_企业  # 404
        ### "http://www.bt.chinanews.com/PhotoS/fengguang/ news",  # 兵团新闻网_风光  # 404
        ### "http://www.bt.chinanews.com/News/jiangnei news",  # 兵团新闻网_疆内  # 404
        ### "http://www.bt.chinanews.com/PhotoS/jingcui/ news",  # 兵团新闻网_精粹  # 404
        ### "http://www.bt.chinanews.com/PhotoT/jrnc/ news",  # 兵团新闻网_农场  # 404
        ### "http://www.bt.chinanews.com/PhotoT/jzbt/ news",  # 兵团新闻网_兵团  # 404
        ### "http://www.bt.chinanews.com/PhotoT/jsgs/ news",  # 兵团新闻网_讲述  # 404
        ### "http://www.bt.chinanews.com/Article/sanwen/ news",  # 兵团新闻网_散文  # 404
        ### "http://www.bt.chinanews.com/PhotoT/twzg/ news",  # 兵团新闻网_专稿  # 404
        ### "http://www.bt.chinanews.com/Article/xiaoshuo/ news",  # 兵团新闻网_小说  # 404
        ### "http://www.bt.chinanews.com/Gov/zwyw/ news",  # 兵团新闻网_民生  # 404
        "http://www.js.chinanews.com/business/ news",  # 江苏新闻网_财经企业
        "http://www.js.chinanews.com/citynews/ news",  # 江苏新闻网_社会民生
        "http://www.js.chinanews.com/sports/ news",  # 江苏新闻网_文化教育
        ### "http://www.js.chinanews.com/special/ news",  # 新闻专题  专题
        ### "http://www.js.chinanews.com/jstw/ news",  # 江苏新闻网_苏台交流 空的
        "http://www.js.chinanews.com/science/ news",  # 江苏新闻网_科技教育
        "http://www.js.chinanews.com/county/ news",  # 江苏新闻网_市县动态
        ### ### "http://www.js.chinanews.com/tour/ news",  # 江苏新闻网_流遍江苏  首页
        "http://www.js.chinanews.com/video/ news",  # 江苏新闻网_视频新闻
        ### "http://www.jx.chinanews.com/jiangxi/cidu/ news",  # 中国新闻网_瓷都新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/Pingxiang/ news",  # 中国新闻网_萍乡新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/nanchang/ news",  # 中国新闻网_南昌新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/Yichun/ news",  # 中国新闻网_宜春新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/Yingtan/ news",  # 中国新闻网_鹰潭新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/shangrao/ news",  # 中国新闻网_上饶新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/jiujiang/ news",  # 中国新闻网_九江新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/ganzhou/ news",  # 中国新闻网_赣州新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/fuzhou/ news",  # 中国新闻网_抚州新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/jian/ news",  # 中国新闻网_吉安新闻  # 404
        ### "http://www.jx.chinanews.com/jiangxi/xinyu/ news",  # 中国新闻网_新余新闻  # 404
        ### "http://www.jx.chinanews.com/fazhi/ news",  # 中国新闻网_江西法制  # 404
        ### "http://www.jx.chinanews.com/society/ news",  # 中国新闻网_江西社会网 # timeout
        ### "http://www.ha.chinanews.com/yiliaoweisheng2012/html/yiliaoweisheng2012/dajiankang/ news",  # 中国新闻网_滚动新闻  # 404
        ### "http://www.ha.chinanews.com/qiaowu/html/qiaowu/qiaozaizhongyuan/ news",  # 中国新闻网_华侨·华人  # 404
        ### "http://www.ha.chinanews.com/qiaowu/html/qiaowu/xingshixungen/ news",  # 中国新闻网_姓氏寻根  # 404
        ### "http://www.jx.chinanews.com/health/ news",  # 中国新闻网_健康  # 404
        ### "http://www.jx.chinanews.com/huaren/ news",  # 中国新闻网_华人  # 404
        "http://www.gz.chinanews.com/shehui/index.shtml news",  # 中国新闻网_社会
        ### ### "http://finance.chinanews.com/ news",  # 财经 首页
        "http://energy.chinanews.com/ news",  # 能源
        "http://it.chinanews.com/ news",  # IT
        ### "http://www.ln.chinanews.com/nengyuan news",  # 辽宁新闻网_能源  # 404
        ### "http://www.sh.chinanews.com/society news",  # 社会民生  # 404
        ### "http://channel.chinanews.com/cns/cl/mil-fwgc.shtml news",  # 防务观察  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-cl.shtml news",  # 潮流  # timeout
        "http://www.gd.chinanews.com/index/wsbl.html news",  # 文史博览
        "http://www.hn.chinanews.com/hnjjdy/jjzh/index1.html news",  # 经济纵横
        "http://www.zj.chinanews.com/cj/zc/index.html news",  # 政策
        "http://www.zj.chinanews.com/sh/zjty/index.html news",  # 浙江体育
        "http://www.zj.chinanews.com/sh/tycy/index.html news",  # 体育产业
        "http://www.zj.chinanews.com/qt/qtdt/index.html news",  # 侨团动态
        "http://www.zj.chinanews.com/zjskzj.html news",  # 中新记者看浙江
        ### "http://www.zj.chinanews.com/yw/qxqw/index.html news",  # 侨乡侨务  # 404
        "http://www.zj.chinanews.com/jy/yey/index.html news",  # 幼儿园
        "http://www.zj.chinanews.com/cj/jr/index.html news",  # 金融
        "http://www.zj.chinanews.com/sj/tj/index.html news",  # 图集
        "http://www.zj.chinanews.com/cj/zs/index.html news",  # 浙商
        "http://www.zj.chinanews.com/sh/tsly/index.html news",  # 图说旅游
        "http://www.zj.chinanews.com/qt/zhw/index.html news",  # 青田人在海外
        "http://www.zj.chinanews.com/qt/ssd/index.html news",  # 赏石雕
        "http://www.zj.chinanews.com/wy/yy/index.html news",  # 音乐
        "http://www.zj.chinanews.com/qt/qtws/index.html news",  # 青田网视
        "http://www.zj.chinanews.com/sj/sp/index.html news",  # 视频
        ### "http://www.zj.chinanews.com/yw/zjyw/index.html news",  # 浙江要闻  # 404
        "http://www.zj.chinanews.com/qt/tsqt/index.html news",  # 图说青田
        "http://www.zj.chinanews.com/jy/zxx/index.html news",  # 中小学
        "http://www.zj.chinanews.com/sj/jxzj/index.html news",  # 镜像浙江
        "http://www.zj.chinanews.com/wy/whzl/index.html news",  # 文化.展览
        "http://www.zj.chinanews.com/qt/rwfc/index.html news",  # 人物风采
        "http://www.zj.chinanews.com/jy/yr/index.html news",  # 育儿
        "http://www.zj.chinanews.com/wy/fy/index.html news",  # 非遗
        "http://www.zj.chinanews.com/qt/hmzy/index.html news",  # 华媒摘要
        "http://www.zj.chinanews.com/wy/sp/index.html news",  # 视频
        "http://www.zj.chinanews.com/qt/gyh/index.html news",  # 购洋货
        "http://www.zj.chinanews.com/qt/zcgg/index.html news",  # 政策公告
        "http://www.zj.chinanews.com/sh/ysyl/index.html news",  # 养生养老
        "http://www.zj.chinanews.com/qt/qszs/index.html news",  # 青商.浙商
        "http://www.zj.chinanews.com/qt/qtjj/index.html news",  # 侨团简介
        "http://www.zj.chinanews.com/jy/zgz/index.html news",  # 教师资格证
        "http://www.hb.chinanews.com/gatq.html news",  # 中国新闻网_港澳台侨
        ### "http://www.gd.chinanews.com/gdxw.html news",  # 中国新闻网_广东滚动新闻  太旧了
        ### "http://www.zj.chinanews.com/csj/ news",  # 中国新闻网_浙江长三角  # 404
        ### "http://www.jx.chinanews.com/jiangxi/ news",  # 中国新闻网_江西  # 404
        "http://www.heb.chinanews.com/4/20111018/325.shtml news",  # 中国新闻网_河北时政
        "http://www.gd.chinanews.com/index/zxtp.html news",  # 中国新闻网_中新图片
        ### "http://auto.chinanews.com/#chengyongche news",  # 乘用车
        ### "http://auto.chinanews.com/#zixun news",  # 资讯
        ### "http://auto.chinanews.com/#cheshi news",  # 车市
        ### "http://auto.chinanews.com/#qcjr news",  # 汽车金融
        ### "http://auto.chinanews.com/#mingxing news",  # 明星
        ### "http://life.chinanews.com/#sexestopic news",  # 两性
        ### "http://life.chinanews.com/#ilovemyhouse news",  # 家饰
        ### "http://life.chinanews.com/#funinfo news",  # 户外
        ### ""http://energy.chinanews.com/#dl news",  # 电力
        ### ""http://it.chinanews.com/#dgt news",  # 导购
        ### ""http://it.chinanews.com/#sdpl news",  # 评论
        ### ""http://house.chinanews.com/#zxmt news",  # 美图
        ### ""http://it.chinanews.com/#xz news",  # 下载
        ### ""http://energy.chinanews.com/#rdqyzb news",  # 热点企业展播
        ### ""http://house.chinanews.com/#jjzy news",  # 家居置业
        ### ""http://it.chinanews.com/#rmht news",  # 话题
        ### ""http://energy.chinanews.com/#kphd news",  # 科普活动
        ### ""http://it.chinanews.com/#xjh news",  # 新品
        ### ""http://stock.chinanews.com/#ybb news",  # 机构
        ### ""http://stock.chinanews.com/#tabs1 news",  # 创业板
        ### ""http://it.chinanews.com/#smyx news",  # 数码
        ### ""http://energy.chinanews.com/#yqtt news",  # 央企
        ### ""http://stock.chinanews.com/#dd-zqyw news",  # 要闻
        ### ""http://house.chinanews.com/#gzlw1111 news",  # 楼王
        ### ""http://stock.chinanews.com/#dd-scdt news",  # 公告
        ### ""http://stock.chinanews.com/#dd-jigou news",  # 监管
        ### ""http://house.chinanews.com/#xf news",  # 新房
        ### ""http://stock.chinanews.com/#zxjzb news",  # 专访
        ### ""http://stock.chinanews.com/#dd-jgdt news",  # 宏观
        ### ""http://it.chinanews.com/#sjfx news",  # 数据
        ### ""http://stock.chinanews.com/#tabs3 news",  # 访谈间
        ### "http://channel.chinanews.com/cns/cl/cul-kgfx.shtml news",  # 考古发现  # timeout
        ### "http://channel.chinanews.com/u/cul/cul-whsp.shtml news",  # 文化杂谈  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-gxzy.shtml news",  # 国学堂  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-shgc.shtml news",  # 史海钩沉  # timeout
        ### "http://channel.chinanews.com/cns/cl/auto-rscs.shtml news",  # 二手车  # timeout
        ### "http://channel.chinanews.com/u/cul/cul-xsjs.shtml news",  # 新书介绍  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-mjzy.shtml news",  # 民间文艺  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-shfz.shtml news",  # 历史珍闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/hwjy-lwxzw.shtml news",  # 老外学中文  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-sqfg.shtml news",  # 涉侨法规  # timeout
        ### "http://channel.chinanews.com/cns/cl/hwjy-hjsp.shtml news",  # 华教时评  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-hjcp.shtml news",  # 黄金  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-zcqs.shtml news",  # 职场情商  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-qgsd.shtml news",  # 企管商道  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-hqnc.shtml news",  # 华侨农场  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-lcs.shtml news",  # 理财师  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-th.shtml news",  # 投行  # timeout
        ### "http://channel.chinanews.com/cns/cl/estate-zxjzb.shtml news",  # 中新网记者报  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-yhj.shtml news",  # 银行家  # timeout
        ### "http://channel.chinanews.com/cns/cl/hwjy-zwjl.shtml news",  # 中外交流  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-ytjr.shtml news",  # 亚太  # timeout
        ### "http://channel.chinanews.com/u/cul/cul-whlx.shtml news",  # 文化流行  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-bwg.shtml news",  # 博物馆  # timeout
        ### "http://channel.chinanews.com/u/yl/djzb.shtml news",  # 独家重磅  # timeout
        "http://www.heb.chinanews.com/4/20111018/343.shtml news",  # 中国新闻网_河北财经动态
        ### "http://www.gz.chinanews.com/gnxw/index.shtml news",  # 中国新闻网_国内新闻 空的
        ### "http://www.gz.chinanews.com/ news",  # 中国新闻网_贵州频道
        ### "http://channel.chinanews.com/cns/cl/cul-wssm.shtml news",  # 网事扫描  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-xjgw.shtml news",  # 戏剧歌舞  # timeout
        "http://www.chinanews.com/compatriot.shtml news",  # 中国新闻网_港澳新闻
        "http://www.hi.chinanews.com/gundong/szxw.html news",  # 中国新闻网_海南时政
        "http://www.hi.chinanews.com/gundong/jjxw.html news",  # 中国新闻网_海南经济
        "http://www.hi.chinanews.com/gundong/dwnews.html news",  # 中国新闻网_海南岛外
        ### "http://channel.chinanews.com/cns/cl/hwjy-qzgx.shtml news",  # 亲子关系  # timeout
        ### "http://www.ln.chinanews.com/jinrong news",  # 辽宁新闻网_金融  # 404
        ### "http://www.ln.chinanews.com/guojixinwen news",  # 辽宁新闻网_国际  # 404
        ### "http://www.ln.chinanews.com/caijingxinwen news",  # 辽宁新闻网_财经新闻  # 404
        ### "http://www.ln.chinanews.com/wenhuaxinwen news",  # 辽宁新闻网_文化新闻  # 404
        ### "http://www.ln.chinanews.com/mingxing news",  # 辽宁新闻网_明星  # 404
        ### "http://www.ln.chinanews.com/jiankangxinwen news",  # 辽宁新闻网_健康新闻  # 404
        ### "http://www.ln.chinanews.com/fangchanxinwen news",  # 辽宁新闻网_房产新闻  # 404
        ### "http://www.ln.chinanews.com/jiaju news",  # 辽宁新闻网_家居  # 404
        ### "http://www.ln.chinanews.com/shanghui news",  # 辽宁新闻网_商会  # 404
        ### "http://www.ln.chinanews.com/weiquan news",  # 辽宁新闻网_维权  # 404
        ### "http://www.ln.chinanews.com/jingdian news",  # 辽宁新闻网_景点推荐  # 404
        ### "http://www.ln.chinanews.com/qichexinwen news",  # 辽宁新闻网_汽车新闻  # 404
        ### "http://www.ln.chinanews.com/zonghetiyu news",  # 辽宁新闻网_综合体育  # 404
        ### "http://www.ln.chinanews.com/shuma news",  # 辽宁新闻网_数码  # 404
        ### "http://www.ln.chinanews.com/lvyouxinwen news",  # 辽宁新闻网_旅游新闻  # 404
        ### "http://www.ln.chinanews.com/junshixinwen news",  # 辽宁新闻网_军事  # 404
        ### "http://www.ln.chinanews.com/yulexinwen news",  # 辽宁新闻网_娱乐新闻  # 404
        ### "http://www.ln.chinanews.com/pinglun news",  # 辽宁新闻网_评论  # 404
        ### "http://www.ln.chinanews.com/kaoshi news",  # 辽宁新闻网_考试  # 404
        ### "http://www.ln.chinanews.com/dushu news",  # 辽宁新闻网_读书  # 404
        ### "http://www.ln.chinanews.com/yangsheng news",  # 辽宁新闻网_养生  # 404
        ### "http://www.ln.chinanews.com/yiliao news",  # 辽宁新闻网_医疗  # 404
        ### "http://www.ln.chinanews.com/peixun news",  # 辽宁新闻网_培训  # 404
        ### "http://www.ln.chinanews.com/fangjiaohui news",  # 辽宁新闻网_房交会  # 404
        ### "http://www.ln.chinanews.com/licai news",  # 辽宁新闻网_理财  # 404
        ### "http://www.ln.chinanews.com/gongyi news",  # 辽宁新闻网_公益  # 404
        ### "http://www.ln.chinanews.com/chanjingxinwen news",  # 辽宁新闻网_产经  # 404
        ### "http://www.ln.chinanews.com/tiyuxinwen news",  # 辽宁新闻网_体育新闻  # 404
        ### "http://www.ln.chinanews.com/wangluo news",  # 辽宁新闻网_网络  # 404
        ### "http://www.ln.chinanews.com/nongyexinwen news",  # 辽宁新闻网_农业新闻  # 404
        ### "http://www.ln.chinanews.com/kejixinwen news",  # 辽宁新闻网_科技新闻  # 404
        ### "http://www.ln.chinanews.com/lanqiu news",  # 辽宁新闻网_篮球  # 404
        ### "http://www.ln.chinanews.com/zuqiu news",  # 辽宁新闻网_足球  # 404
        ### "http://www.ln.chinanews.com/jiaoyuxinwen news",  # 辽宁新闻网_教育新闻  # 404
        ### "http://www.ln.chinanews.com/anshan news",  # 中国新闻网_鞍山  # 404
        ### "http://www.ln.chinanews.com/liaoningxinwen/ news",  # 中国新闻网_辽宁新闻  # 404
        ### "http://www.ln.chinanews.com/guoneixinwen/ news",  # 中国新闻网_辽宁国内  # 404
        ### "http://www.ln.chinanews.com/shehuixinwen/ news",  # 中国新闻网_辽宁社会  # 404
        "http://www.hb.chinanews.com/travel.html news",  # 中国新闻网_灵秀湖北
        "http://www.shx.chinanews.com/jcca.html news",  # 中国新闻网_精彩长安
        "http://www.js.chinanews.com/nomocracy/ news",  # 中国新闻网_法治
        "http://www.hn.chinanews.com/news/cnsdc/ news",  # 中国新闻网_中新调查
        "http://www.bj.chinanews.com/focus/4.html news",  # 中国新闻网_北京政文
        "http://www.bj.chinanews.com/focus/6.html news",  # 中国新闻网_北京社会
        "http://www.bj.chinanews.com/focus/2.html news",  # 中国新闻网_北京话题
        "http://www.bj.chinanews.com/focus/7.html news",  # 中国新闻网_北京法警
        "http://www.bj.chinanews.com/focus/9.html news",  # 中国新闻网_北京健康
        "http://www.fj.chinanews.com/new/pgt/list.shtml news",  # 福建新闻网_曝光台
        "http://www.fj.chinanews.com/new/cjyw/list.shtml news",  # 福建新闻网_财经要闻
        "http://www.fj.chinanews.com/new/hwxq/list.shtml news",  # 福建新闻网_四海乡音
        "http://www.fj.chinanews.com/new/jjkd/list.shtml news",  # 福建新闻网_警界快递
        "http://www.fj.chinanews.com/new/gacz/list.shtml news",  # 福建新闻网_港澳传真
        "http://www.fj.chinanews.com/new/xwrp/list.shtml news",  # 福建新闻网_时评
        "http://www.fj.chinanews.com/new/thyw/list.shtml news",  # 福建新闻网_台海要闻
        "http://www.gs.chinanews.com/jywx1/m1.html news",  # 中国新闻网_甘肃教育
        "http://www.gs.chinanews.com/jrtt1.html news",  # 甘肃新闻网_今日头条
        "http://www.gs.chinanews.com/shms1.html news",  # 甘肃新闻网_社会民生
        "http://www.gs.chinanews.com/yljd1.html news",  # 甘肃新闻网_舆论监督
        "http://www.gs.chinanews.com/jjxw1.html news",  # 甘肃新闻网_经济新闻
        "http://www.gs.chinanews.com/zwrs1.html news",  # 甘肃新闻网_甘肃政务
        "http://www.shx.chinanews.com/shfz.html news",  # 中国新闻网_陕西社会
        "http://www.bj.chinanews.com/focus/5.html news",  # 中国新闻网_北京经济
        "http://www.js.chinanews.com/overseas/ news",  # 江苏新闻网_外事侨务
        "http://www.sx.chinanews.com/4/2009/0107/1.html news",  # 中国新闻网_山西要闻
        "http://www.hb.chinanews.com/cjxw.html news",  # 湖北新闻网_经济新闻
        "http://www.hb.chinanews.com/jk.html news",  # 湖北新闻网_生活健康
        "http://www.hb.chinanews.com/shipin/more.html news",  # 湖北新闻网_视频新闻
        "http://www.sx.chinanews.com/4/2009/0727/15.html news",  # 中国新闻网_山西国内要闻
        "http://www.sx.chinanews.com/4/2009/0728/21.html news",  # 中国新闻网_山西时政
        "http://www.shx.chinanews.com/wmksx.html news",  # 中国新闻网_陕西外媒刊
        "http://www.shx.chinanews.com/sxxw.html news",  # 中国新闻网_陕西市县新闻
        ### "http://www.chinanews.com/sh/z/Bund/index.shtml news",  # 中国新闻网_新闻专题回顾 太旧
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=18 news",  # 中国新闻网_安徽领导视角  # 404
        ### "http://www.ah.chinanews.com/portal.php?mod=list&catid=49 news",  # 中国新闻网_安徽热点评论  # 404
        ### "http://finance.chinanews.com/#kcyfz news",  # 品牌
        ### "http://finance.chinanews.com/#cfblt news",  # 辩论台
        ### "http://finance.chinanews.com/#zj news",  # 宏观
        ### "http://finance.chinanews.com/#cf news",  # 人物
        ### "http://finance.chinanews.com/#ct news",  # 项目
        ### "http://finance.chinanews.com/#zccc news",  # 热点
        ### "http://finance.chinanews.com/#fhb news",  # 富豪榜
        ### "http://www.jx.chinanews.com/zhuanlan/ news",  # 中国新闻网_江西记者专栏  # 404
        ### "http://channel.chinanews.com/cns/cl/cul-jd.shtml news",  # 中国新闻网_焦点  # timeout
        ### "http://www.sh.chinanews.com/culture news",  # 文化体育  # 404
        ### "http://www.sh.chinanews.com/videos news",  # 视频新闻  # 404
        ### "http://www.sh.chinanews.com/shnews news",  # 上海新闻  # 404
        ### "http://www.sh.chinanews.com/75 news",  # 创客在线  # 404
        ### "http://www.sh.chinanews.com/science news",  # 科教卫生  # 404
        ### "http://www.sh.chinanews.com/overseas news",  # 港澳台侨  # 404
        ### "http://www.sh.chinanews.com/business news",  # 财经新闻  # 404
        ### "http://www.sh.chinanews.com/shcustoms news",  # 区县动态  # 404
        ### "http://www.sh.chinanews.com/special news",  # 专题报道  # 404
        ### "http://www.sh.chinanews.com/shangwu news",  # 商务咨询  # 404
        ### "http://www.sh.chinanews.com/highlights news",  # 时政要闻  # 404
        ### "http://www.sh.chinanews.com/photos news",  # 图片新闻  # 404
        ### "http://www.zj.chinanews.com/social/ news",  # 中国新闻网_浙江社会新闻  # 404
        ### "http://www.zj.chinanews.com/today/index.html news",  # 中国新闻网_浙江今日新闻  # 404
        ### "http://channel.chinanews.com/cns/cl/edu-jygg.shtml news",  # 中国新闻网_教育改革  # timeout
        ### "http://www.bt.chinanews.com/Fazhi/ news",  # 兵团新闻网_法制  # 404
        ### "http://channel.chinanews.com/cns/cl/fortune-dfyh.shtml news",  # 地方  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-sjkj.shtml news",  # 中国新闻网_科技博览  # timeout
        ### "http://www.ha.chinanews.com/GNnews/1/index.shtml news",  # 中国新闻网_河南新闻  # 404
        ### "http://channel.chinanews.com/cns/cl/hb-scwj.shtml news",  # 收藏玩家  # timeout
        "http://www.hi.chinanews.com/gundong/guonei.html news",  # 中国新闻网_海南国内
        "http://house.chinanews.com/#tudi news",  # 土地
        ### "http://channel.chinanews.com/cns/cl/estate-jjjj.shtml news",  # 中国新闻网_家居置业  # timeout
        ### "http://channel.chinanews.com/cns/cl/estate-om.shtml news",  # 中国新闻网_欧美  # timeout
        ### "http://channel.chinanews.com/cns/cl/estate-tdxw.shtml news",  # 中国新闻网_土地  # timeout
        ### "http://channel.chinanews.com/cns/cl/estate-xf.shtml news",  # 中国新闻网_新房  # timeout
        ### "http://channel.chinanews.com/cns/cl/estate-zj.shtml news",  # 中国新闻网_专家  # timeout
        "http://www.shx.chinanews.com/dswy.html news",  # 中国新闻网_理论文苑
        "http://www.chinanews.com/news/tjyd/more_1.shtml news",  # 中国新闻网_阅读推荐
        ### "http://channel.chinanews.com/cns/cl/it-sdpl.shtml news",  # 中国新闻网_观点评论  # timeout
        ### "http://channel.chinanews.com/cns/cl/life-sdd.shtml news",  # 中国新闻网_生活频道  # timeout
        "http://www.shx.chinanews.com/ylty.html news",  # 中国新闻网_娱乐体育
        "http://www.hb.chinanews.com/kjww.html news",  # 中国新闻网_湖北科教文卫
        ### "http://www.hb.chinanews.com/ news",  # 中国新闻网_湖北首页
        ### "http://www.js.chinanews.com/complain/ news",  # 江苏新闻网_群众呼声 太旧了
        ### "http://www.jl.chinanews.com/ news",  # 中国新闻网_吉林首页
        "http://energy.chinanews.com/#lssh news",  # 绿色产业
        ### "http://energy.chinanews.com/#xyy news",  # 新能源 重复
        ### "http://channel.chinanews.com/cns/cl/ny-xny.shtml news",  # 中国新闻网_新能源  # timeout
        ### "http://channel.chinanews.com/cns/cl/ny-hn.shtml news",  # 中国新闻网_核能  # timeout
        ### "http://channel.chinanews.com/cns/cl/ny-sysh.shtml news",  # 中国新闻网_石油石化  # timeout
        ### "http://channel.chinanews.com/cns/cl/ny-trq.shtml news",  # 中国新闻网_天然气  # timeout
        ### "http://channel.chinanews.com/cns/cl/ny-sldl.shtml news",  # 中国新闻网_水利电力  # timeout
        "http://www.chinanews.com/stock/gd.shtml news",  # 证券新闻
        "http://www.chinanews.com/energy/news.shtml news",  # 能源
        "http://www.chinanews.com/stock/news.shtml news",  # 证券
        "http://www.chinanews.com/health.shtml news",  # 健康
        "http://www.chinanews.com/world.shtml news",  # 国际
        "http://www.chinanews.com/hb.shtml news",  # 报摘
        "http://www.chinanews.com/keji.shtml news",  # IT
        "http://finance.chinanews.com/cj/gd.shtml news",  # 财经_滚动
        ### "http://www.chinanews.com/stock/ft/index.shtml news",  # 牛人 不是详情页
        ### "http://www.chinanews.com/estate/ft/01/index.shtml news",  # 访谈间 不是详情页
        ### "http://www.chinanews.com/fortune/ft/index.shtml news",  # 访谈间 不是详情页
        ### "http://www.chinanews.com/ny/z/ditan/index.shtml news",  # 节能减排 不是详情页
        ### "http://www.chinanews.com/fortune/z/xinyongka/index.shtml news",  # 信用卡 不是详情页
        ### "http://auto.chinanews.com/#chejia news",  # 车价  首页
        ### "http://auto.chinanews.com/#shuju news",  # 数据 首页
        ### "http://auto.chinanews.com/#jinkou news",  # 进口 首页
        ### "http://auto.chinanews.com/#kache news",  # 卡车 首页
        ### "http://auto.chinanews.com/#daogou news",  # 导购 首页
        ### "http://auto.chinanews.com/#chexing news",  # 车型 首页
        ### "http://auto.chinanews.com/#renwu news",  # 人物 首页
        ### "http://auto.chinanews.com/#keche news",  # 客车 首页
        ### "http://auto.chinanews.com/#hezi news",  # 合资 首页
        ### "http://auto.chinanews.com/#huodong news",  # 活动 首页
        ### "http://auto.chinanews.com/#xinche news",  # 新车 首页
        ### "http://auto.chinanews.com/#ljrw news",  # 人物 首页
        ### "http://auto.chinanews.com/#lingbujian news",  # 零部件 首页
        ### "http://auto.chinanews.com/#chanye news",  # 产业 首页
        ### "http://auto.chinanews.com/#zhaohui news",  # 召回 首页
        ### "http://auto.chinanews.com/#ycsj news",  # 原创试驾 首页
        ### "http://auto.chinanews.com/#zizhu news",  # 自主 首页
        ### "http://auto.chinanews.com/#guancha news",  # 观察 首页
        ### "http://auto.chinanews.com/#yongche news",  # 用车 首页
        ### "http://auto.chinanews.com/#chanpinku news",  # 产品库 首页
        ### "http://www.chinanews.com/estate/z/baozhangfang/index.shtml news",  # 保障房  不是详情页
        "http://house.chinanews.com/#huanqiu news",  # 环球
        "http://house.chinanews.com/#ersf news",  # 二手房
        "http://house.chinanews.com/#qynd news",  # 房企拿地
        "http://house.chinanews.com/#jzkb news",  # 口碑
        "http://house.chinanews.com/#dcq news",  # 人物
        "http://house.chinanews.com/#slc news",  # 售楼处
        "http://house.chinanews.com/#rtph news",  # 论坛
        "http://house.chinanews.com/#sangy news",  # 商业地产
        "http://house.chinanews.com/#zyjff news",  # 纠纷
        "http://house.chinanews.com/#fdh news",  # 房贷
        "http://house.chinanews.com/#wq news",  # 维权
        "http://house.chinanews.com/#gzdw news",  # 地王
        "http://house.chinanews.com/#kfsyl news",  # 语录
        "http://house.chinanews.com/#dcjr news",  # 金融
        "http://house.chinanews.com/#zxjc news",  # 建材
        "http://house.chinanews.com/#fq news",  # 房企
        "http://house.chinanews.com/#fqlb news",  # 老板
        "http://house.chinanews.com/#fqdtt news",  # 房企动态
        "http://house.chinanews.com/#dlh news",  # 代理行
        "http://it.chinanews.com/#sdgc news",  # 观察
        "http://it.chinanews.com/#qydt news",  # 企业
        "http://it.chinanews.com/#sd news",  # 深度
        "http://it.chinanews.com/#rwsy news",  # 人物
        "http://it.chinanews.com/#bjb news",  # 笔记本
        "http://it.chinanews.com/#ztch news",  # 专题
        "http://it.chinanews.com/#zcjd news",  # 政策
        "http://it.chinanews.com/#yc news",  # 原创
        "http://it.chinanews.com/#jydq news",  # 电器
        "http://it.chinanews.com/#bg news",  # 报告
        "http://it.chinanews.com/#sj news",  # 手机
        "http://energy.chinanews.com/#qygy news",  # 企业公益
        "http://energy.chinanews.com/#dtsh news",  # 低碳生活
        "http://energy.chinanews.com/#qqjz news",  # 全球巨擘
        "http://energy.chinanews.com/#lsxd news",  # 绿色行动
        "http://energy.chinanews.com/#sysh news",  # 石油
        "http://energy.chinanews.com/#hn news",  # 核能
        "http://energy.chinanews.com/#yjzs news",  # 油价走势
        "http://energy.chinanews.com/#mt news",  # 煤炭
        "http://energy.chinanews.com/#trq news",  # 天然气
        "http://energy.chinanews.com/#mq news",  # 民企
        "http://energy.chinanews.com/#stzxx news",  # 视听在线
        "http://energy.chinanews.com/#jnzz news",  # 节能支招
        "http://stock.chinanews.com/#gsnrb news",  # 百家
        "http://stock.chinanews.com/#dd-jrts news",  # 提示
        "http://stock.chinanews.com/#iframe-jrlzbk news",  # 板块
        "http://stock.chinanews.com/#tzzjy news",  # 教育
        "http://stock.chinanews.com/#qsyth news",  # 董秘
        "http://stock.chinanews.com/#tabs2 news",  # 研报
        "http://stock.chinanews.com/#quanshang news",  # 券商
        "http://stock.chinanews.com/#ssgshhb news",  # 策划
        "http://stock.chinanews.com/#iframe-zssj news",  # 欧美
        "http://stock.chinanews.com/#jijin news",  # 基金
        "http://stock.chinanews.com/#ggzz news",  # 活动
        "http://stock.chinanews.com/#iframe-qqgshq news",  # 港股
        "http://stock.chinanews.com/#jiaoyisuo news",  # 红黑榜
        "http://stock.chinanews.com/#dd-gshqkb news",  # 报盘
        "http://stock.chinanews.com/#ssgs news",  # 个股
        "http://stock.chinanews.com/#gzqh news",  # 期指
        "http://stock.chinanews.com/#jjp news",  # 动态
        "http://stock.chinanews.com/#iframe-hqzx news",  # Ａ股
        ### "http://channel.chinanews.com/cns/cl/zgqj-qsgc.shtml news",  # 侨史钩沉  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-cbdt.shtml news",  # 书业观察  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-zsfy.shtml news",  # 战史风云  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-qxsz.shtml news",  # 情系桑梓  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-scpd.shtml news",  # 美术长廊  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-zxjrb.shtml news",  # 金融报  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-fwjl.shtml news",  # 访问交流  # timeout
        ### "http://channel.chinanews.com/u/sy/dsds.shtml news",  # 电视  # timeout
        ### "http://channel.chinanews.com/u/yl/mixing.shtml news",  # 明星  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-zgqx.shtml news",  # 中国侨讯  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-wtjs.shtml news",  # 文坛纪事  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-qjxx.shtml news",  # 侨界信箱  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-yzyz.shtml news",  # 引资引智  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-lcjn.shtml news",  # 理财锦囊  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-qjxy.shtml news",  # 侨界撷英  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-szlw.shtml news",  # 神州瞭望  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-tpbd.shtml news",  # 图片  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-wypp.shtml news",  # 文艺品评  # timeout
        ### "http://channel.chinanews.com/u/finance/gj.shtml news",  # 国际  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-whcp.shtml news",  # 外汇  # timeout
        ### "http://channel.chinanews.com/cns/cl/hwjy-hykt.shtml news",  # 汉语课堂  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-hbtt.shtml news",  # 华报头条  # timeout
        ### "http://channel.chinanews.com/cns/cl/auto-csh.shtml news",  # 生活  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-whyc.shtml news",  # 文化遗产  # timeout
        ### "http://channel.chinanews.com/u/news/xyxy.shtml news",  # 星语星愿  # timeout
        ### "http://channel.chinanews.com/u/sy/music1.shtml news",  # 音乐  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-wysb.shtml news",  # 文苑  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-rwbk.shtml news",  # 人文百科  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-gjss.shtml news",  # 国际时事  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-rwmdm.shtml news",  # 人物  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-gxjx.shtml news",  # 故乡纪行  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-qkjc.shtml news",  # 侨刊集粹  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-mlyz.shtml news",  # 魅力衣妆  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-tgaq.shtml news",  # 台港澳侨  # timeout
        ### "http://channel.chinanews.com/cns/cl/hwjy-hjzx.shtml news",  # 华教新闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-zzyh.shtml news",  # 中资  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-cpjl.shtml news",  # 经理  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-gqgs.shtml news",  # 归侨故事  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-jkys.shtml news",  # 健康养生  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-ysxc.shtml news",  # 艺术现场  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-ghzh.shtml news",  # 股海纵横  # timeout
        ### "http://channel.chinanews.com/cns/cl/hwjy-xsxz.shtml news",  # 学生习作  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-wssj.shtml news",  # 读书  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-rzlt.shtml news",  # 人在旅途  # timeout
        ### "http://channel.chinanews.com/cns/cl/hwjy-xgzl.shtml news",  # 寻根之旅  # timeout
        ### "http://channel.chinanews.com/cns/cl/auto-cxdb.shtml news",  # 对比  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-ysnn.shtml news",  # 饮食男女  # timeout
        ### "http://channel.chinanews.com/cns/cl/yl-zykx.shtml news",  # 综艺  # timeout
        ### "http://channel.chinanews.com/u/finance/yw.shtml news",  # 要闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-zqcp.shtml news",  # 债券  # timeout
        ### "http://channel.chinanews.com/cns/cl/tw-msfq.shtml news",  # 民俗风情  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-rwcq.shtml news",  # 人物春秋  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-gjqt.shtml news",  # 旧闻奇谈  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-qhcp.shtml news",  # 期货  # timeout
        ### "http://channel.chinanews.com/cns/cl/cul-cmyj.shtml news",  # 传媒业界  # timeout
        ### "http://channel.chinanews.com/cns/cl/tw-ylzy.shtml news",  # 娱乐综艺  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-bxal.shtml news",  # 案例  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-bfsj.shtml news",  # 缤纷世界  # timeout
        ### "http://channel.chinanews.com/cns/cl/tw-tppd.shtml news",  # 图片  # timeout
        ### "http://channel.chinanews.com/cns/cl/yl-zyy.shtml news",  # 众议院  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-omjr.shtml news",  # 欧美  # timeout
        ### "http://channel.chinanews.com/cns/cl/hb-kjxz.shtml news",  # 科技新知  # timeout
        ### "http://channel.chinanews.com/u/sy/dygd.shtml news",  # 电影  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-wzyh.shtml news",  # 外资  # timeout
        "http://www.chinanews.com/fortune/news.shtml news",  # 金融
        "http://www.chinanews.com/mil/news.shtml news",  # 军事
        "http://www.chinanews.com/taiwan.shtml news",  # 台湾
        "http://www.chinanews.com/estate.html news",  # 房产
        "http://www.chinanews.com/wenhua.shtml news",  # 文化
        "http://finance.chinanews.com/stock/gd.shtml news",  # 金融_股票
        "http://www.chinanews.com/china.shtml news",  # 国内
        "http://www.chinanews.com/qiche.shtml news",  # 汽车
        ### "http://channel.chinanews.com/cns/cl/ga-tlga.shtml news",  # 图片新闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-zgjqsclb.shtml news",  # 沙场砺兵  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-zgjqzgbhf.shtml news",  # 中国边海防  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-shyybqmw.shtml news",  # 兵器秘闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-mrhf.shtml news",  # 美容  # timeout
        ### "http://channel.chinanews.com/cns/cl/cj-jjyw.shtml news",  # 财经_趣闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-ylgg.shtml news",  # 医改  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-fxpl.shtml news",  # 评论  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-rwbg.shtml news",  # 八卦  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-zb.shtml news",  # 金融_资本圈  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-yqgc.shtml news",  # 金融_舆情观察  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-zypf.shtml news",  # 民间偏方  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-sqfg.shtml news",  # 涉侨  # timeout
        ### "http://channel.chinanews.com/cns/cl/stock-gsxw.shtml news",  # 金融_上市公司  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-xywy.shtml news",  # 健康  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-xfsd.shtml news",  # 新法速递  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-flfg.shtml news",  # 法律法规  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-gjjqwjdt.shtml news",  # 外军动态  # timeout
        ### "http://channel.chinanews.com/cns/cl/cj-cfgcz.shtml news",  # 财经_观察者  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-hqcz.shtml news",  # 财经  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-ltzh.shtml news",  # 篮坛纵横  # timeout
        ### "http://channel.chinanews.com/cns/cl/cj-sczx.shtml news",  # 财经_市场  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-ldbz.shtml news",  # 劳动保障  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-jzzj.shtml news",  # 急症自救  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-zhplc.shtml news",  # 评论  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-qqjs.shtml news",  # 军事  # timeout
        ### "http://channel.chinanews.com/u/hrdd.shtml news",  # 要闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-ms.shtml news",  # 美食  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-hyxw.shtml news",  # 业界  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-nxbj.shtml news",  # 男性保健  # timeout
        ### "http://channel.chinanews.com/u/news/ffcl.shtml news",  # 反腐倡廉  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-kjww.shtml news",  # 文化街区  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-gjjqjsqw.shtml news",  # 军事趣闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-fztc.shtml news",  # 法治图萃  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-qsqx.shtml news",  # 侨商  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hwbz.shtml news",  # 视角  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-zqkp.shtml news",  # 足球酷评  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-oz.shtml news",  # 欧洲  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-qzjy.shtml news",  # 亲子  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-ylmt.shtml news",  # 娱乐  # timeout
        ### "http://channel.chinanews.com/u/ty/hytt.shtml news",  # 体坛万花筒  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-klsk.shtml news",  # 篮球综合  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hydx.shtml news",  # 行业动态  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-xxsh.shtml news",  # 休闲  # timeout
        ### "http://channel.chinanews.com/u/news/gnmtjc.shtml news",  # 国内媒体精粹  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-shyymjfc.shtml news",  # 名将风采  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-fzsj.shtml news",  # 泛珠三角  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-jdrw.shtml news",  # 焦点人物  # timeout
        ### "http://channel.chinanews.com/cns/cl/cj-gjcj.shtml news",  # 财经_国际  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-hyjt.shtml news",  # 婚姻家庭  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-zcdt.shtml news",  # 政策  # timeout
        ### "http://channel.chinanews.com/u/news/rsrm.shtml news",  # 人事任免  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hsfc.shtml news",  # 商界名流  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hrjy.shtml news",  # 精英  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-jkpl.shtml news",  # 评论  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-my.shtml news",  # 孕婴  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-stwx.shtml news",  # 世态万象  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-lccp.shtml news",  # 金融_理财  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-zwgc.shtml news",  # 中外  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-gaynd.shtml news",  # 港澳与内地  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-zhqt.shtml news",  # 其它综合  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-yytx.shtml news",  # 悠游天下  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-yyxq.shtml news",  # 乡情  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-yhzj.shtml news",  # 医患  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-gjjqlbsm.shtml news",  # 邻邦扫描  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-zgjqxwfbh.shtml news",  # 国防发布会  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hrry.shtml news",  # 荣誉  # timeout
        ### "http://channel.chinanews.com/cns/cl/cj-alfx.shtml news",  # 财经_案例  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-sszqf.shtml news",  # 时事正前方  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-xxbp.shtml news",  # 新鲜报评  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-zgjqgfgj.shtml news",  # 国防广角  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-st-mz.shtml news",  # 社团  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hljt.shtml news",  # 婚恋  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-cfjm.shtml news",  # 百科  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hrzxz.shtml news",  # 咨询  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hwsh.shtml news",  # 人在他乡  # timeout
        ### "http://channel.chinanews.com/u/ty/zgxg.shtml news",  # 中国星光  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-shyysjxy.shtml news",  # 世界硝烟  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-sfgg.shtml news",  # 司法改革  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-lxxt.shtml news",  # 身体密码  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-nba.shtml news",  # NBA  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-gjjqdqct.shtml news",  # 地区冲突  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-wsry.shtml news",  # 往事如烟  # timeout
        ### "http://channel.chinanews.com/cns/cl/cj-hgds.shtml news",  # 财经_宏观  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-cjxw.shtml news",  # 财经直通车  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-lyyw.shtml news",  # 绿茵轶闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-qzzc.shtml news",  # 签证  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-bgjgl.shtml news",  # 职场攻略  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-tszj.shtml news",  # 庭审直击  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-pq.shtml news",  # 排球  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-dqsj.shtml news",  # 趣闻  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-jsjf.shtml news",  # 减肥  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-ysyy.shtml news",  # 饮食  # timeout
        ### "http://channel.chinanews.com/cns/cl/cj-chjxw.shtml news",  # 财经_产业  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-gamy.shtml news",  # 旅游  # timeout
        ### "http://channel.chinanews.com/cns/cl/cj-ctcf.shtml news",  # 财经_创富  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-trj.shtml news",  # 唐人街  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-jtyx.shtml news",  # 家庭药箱  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hrshq.shtml news",  # 生活圈  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-gjrw.shtml news",  # 人物  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-jssp.shtml news",  # 军事视频  # timeout
        ### "http://www.chinanews.com/it/z/ceping/index.shtml news",  # 测评中国 不是列表页
        ### "http://www.chinanews.com/auto/ft/index.shtml news",  # 访谈间不是列表页
        "http://www.chinanews.com/life.shtml news",  # 生活
        ### "http://channel.chinanews.com/cns/cl/cj-fyrw.shtml news",  # 财经_人物  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-zgjqjgkj.shtml news",  # 军工科技  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-jg.shtml news",  # 金融_金融机构  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-gnzq.shtml news",  # 中国足球  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hrdt.shtml news",  # 动态  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-rdgz.shtml news",  # 热点  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-shyyzgzs.shtml news",  # 中国战史  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-lfjc.shtml news",  # 立法进程  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-wmck.shtml news",  # 外媒  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-qybh.shtml news",  # 权益保护  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-yt.shtml news",  # 亚太  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-pajq.shtml news",  # 拍案惊奇  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-xpxz.shtml news",  # 新知  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-gmsy.shtml news",  # 闺蜜私语  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-gw.shtml news",  # 购物  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-lsbh.shtml news",  # 出国  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hszx.shtml news",  # 华商  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-yfxz.shtml news",  # 依法行政  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hrwy.shtml news",  # 文苑  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-shts.shtml news",  # 生活贴士  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-hjlw.shtml news",  # 火箭·篮网  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-zckd.shtml news",  # 看点  # timeout
        ### "http://channel.chinanews.com/u/finance/gs.shtml news",  # 财经_公司  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-ymfb.shtml news",  # 移民  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-bm.shtml news",  # 美洲  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-jjjf.shtml news",  # 经济纠纷  # timeout
        ### "http://channel.chinanews.com/cns/cl/ty-gjzq.shtml news",  # 国际足球  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-xljk.shtml news",  # 心理健康  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-jgdtyh.shtml news",  # 金融_监管  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-zd.shtml news",  # 中东非洲  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-xjlh.shtml news",  # 学界论衡  # timeout
        ### "http://channel.chinanews.com/cns/cl/mil-gjjqysjs.shtml news",  # 影视鉴赏  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-sh.shtml news",  # 生活  # timeout
        ### "http://channel.chinanews.com/cns/cl/fz-ffcl.shtml news",  # 反腐倡廉  # timeout
        ### "http://channel.chinanews.com/cns/cl/jk-jbcs.shtml news",  # 疾病常识  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hrgs.shtml news",  # 故事  # timeout
        ### "http://channel.chinanews.com/cns/cl/hr-hwqz.shtml news",  # 求职  # timeout
        ### "http://channel.chinanews.com/cns/cl/gj-sswh.shtml news",  # 时尚  # timeout
        ### "http://channel.chinanews.com/cns/cl/fortune-hlwjr.shtml news",  # 金融_互联网金融  # timeout
        ### "http://channel.chinanews.com/u/cl/mil-zgjq.shtml news",  # 中国军情  # timeout
        ## "http://fortune.chinanews.com/#hdm9 news",  # 外汇
        ## "http://fortune.chinanews.com/#hdm4 news",  # 策划
        ##"http://fortune.chinanews.com/#gzb news",  # 关注榜
        ## "http://fortune.chinanews.com/#yhg news",  # 银行股
        ## "http://fortune.chinanews.com/#club news",  # 俱乐部
        ## "http://fortune.chinanews.com/#jy news",  # 教育
        ## "http://fortune.chinanews.com/#hg news",  # 宏观
        ## "http://fortune.chinanews.com/#yj news",  # 业界
        ## "http://fortune.chinanews.com/#hdm1 news",  # 利率
        ## "http://fortune.chinanews.com/#bxg news",  # 保险股
        ## "http://fortune.chinanews.com/#hyq news",  # 舆情
        ## "http://fortune.chinanews.com/#sc news",  # 市场
        ## "http://fortune.chinanews.com/#bx news",  # 保险
        ## "http://fortune.chinanews.com/#hyb news",  # 毁誉榜
        ## "http://life.chinanews.com/#worldfunthing news",  # 娱乐
        ## "http://life.chinanews.com/#chinatravel news",  # 国内
        ## "http://life.chinanews.com/#foodculture news",  # 养生
        ## "http://life.chinanews.com/#menclothing news",  # 名品
        ## "http://life.chinanews.com/#famousshop news",  # 资讯
        ## "http://life.chinanews.com/#findfamousshop news",  # 名店
        ## "http://life.chinanews.com/#delicacy news",  # 美食
        ## "http://life.chinanews.com/#facebody news",  # 美容
        ## "http://life.chinanews.com/#styletrend news",  # 风尚
        ## "http://life.chinanews.com/#focus news",  # 资讯
        ## "http://life.chinanews.com/#fitment news",  # 空间
        ## "http://life.chinanews.com/#iplay news",  # 互动
        ## "http://life.chinanews.com/#hairstyle news",  # 秀场
        ## "http://life.chinanews.com/#clothing1 news",  # 服饰
        ## "http://life.chinanews.com/#baby news",  # 母婴
        ## "http://life.chinanews.com/#leisurefitness news",  # 休闲
        ## "http://life.chinanews.com/#lovetopic news",  # 情感
        "http://www.gd.chinanews.com/index/gfgl.html news",  # 中国新闻网_广府观澜
        "http://www.gd.chinanews.com/index/nysz.html news",  # 中国新闻网_南粤时政
        "http://www.gd.chinanews.com/index/zxdc.html news",  # 中国新闻网_中新调查
        "http://www.gd.chinanews.com/index/ztgot.html news",  # 中国新闻网_直通港澳台
        "http://www.gd.chinanews.com/index/dfpd.html news",  # 中国新闻网_地方频道
        "http://www.gd.chinanews.com/index/qxlf.html news",  # 中国新闻网_侨乡来风
        "http://www.gd.chinanews.com/index/shyx.html news",  # 中国新闻网_社会粤象
        "http://www.gd.chinanews.com/index/rwgd.html news",  # 中国新闻网_人文广东
        "http://www.gd.chinanews.com/index/lnrw.html news",  # 中国新闻网_岭南人物
        "http://www.gd.chinanews.com/index/gg.html news",  # 中国新闻网_广东高官
        "http://www.gs.chinanews.com/gssj/index.shtml news",  # 中国新闻网_视觉甘肃
        "http://www.gd.chinanews.com/index/lnwh.html news",  # 中国新闻网_广东岭南文化
        "http://www.chinanews.com/economic.shtml news",  # 中国新闻网_经济新闻
        "http://stock.chinanews.com/#iframe-ggxcb news",  # 薪酬
        "http://stock.chinanews.com/#qsmdm news",  # 研讨
        "http://stock.chinanews.com/#bjjt news",  # 交易所
        ### "http://channel.chinanews.com/u/news/sbx.shtml news",  # 审判席  # timeout
        ### "http://channel.chinanews.com/u/news/jfb.shtml news",  # 剿绯办  # timeout
        ### "http://channel.chinanews.com/cns/cl/zgqj-qwlt.shtml news",  # 侨务论坛  # timeout
        "http://www.hb.chinanews.com/zixun.html news",  # 中国新闻社图文信息发布网_资讯
        "http://www.shx.chinanews.com/szjj.html news",  # 中国新闻网_陕西时政
        "http://www.shx.chinanews.com/zltx.html news",  # 中国新闻网_陕西纵览天下
        ### "http://www.sd.chinanews.com/ news",  # 中国新闻网_山东频道 首页
        ### "http://www.sx.chinanews.com/4/2009/0728/22.html news",  # 中国新闻网_山西民生 太旧了
        ### "http://www.sx.chinanews.com/4/2010/1207/49.html news",  # 中国新闻网_聚焦山西 太旧了
        "http://www.gd.chinanews.com/index/whjy.html news",  # 文化教育
        "http://www.gd.chinanews.com/index/zxzxg.html news",  # 走转改
        "http://www.gd.chinanews.com/index/hd.html news",  # 活动
        "http://www.gd.chinanews.com/index/gdsz.html news",  # 广东时政
        "http://www.gd.chinanews.com/index/kjyn.html news",  # 客家语浓
        "http://www.gd.chinanews.com/index/gdfs.html news",  # 广东分社
        ### "http://www.gd.chinanews.com/index/zxs.html news",  # 中新社 太旧了
        "http://www.gd.chinanews.com/index/shjk.html news",  # 生活健康
        "http://www.gd.chinanews.com/index/ls.html news",  # 楼市
        "http://www.gd.chinanews.com/index/cxgd.html news",  # 创新广东
        "http://www.gd.chinanews.com/index/dqsj.html news",  # 大千世界
        "http://www.gd.chinanews.com/index/nsq.html news",  # 娱乐八卦
        "http://www.gd.chinanews.com/index/kjgd.html news",  # 科技广东
        "http://www.gd.chinanews.com/index/hlwjr.html news",  # 互联网金融
        "http://www.gd.chinanews.com/index/qcsh.html news",  # 汽车生活
        "http://www.gd.chinanews.com/index/gdjj.html news",  # 广东经济
        ### "http://www.chinanews.com/df/news.shtml news",  # 中国新闻网_地方新闻 空的
        "http://www.gd.chinanews.com/index/cstt.html news",  # 中国新闻网_潮汕听涛
        "http://www.gd.chinanews.com/index/gz.html news",  # 中国新闻网_广东关注
        ### "http://www.gd.chinanews.com/index/ymtt.html news",  # 中国新闻网_粤媒头条 这个全是404
        "http://www.gd.chinanews.com/index/gddt.html news",  # 中国新闻网_广东动态
        "http://www.gd.chinanews.com/index/yjcj.html news",  # 中国新闻网_粤界财经
        "http://www.chinanews.com/society.shtml news",  # 中国新闻网_社会新闻
        "http://www.ln.chinanews.com/tiyu/index.shtml news",  # 体育
        "http://www.ln.chinanews.com/yule/index.shtml news",  # 娱乐
        "http://www.ln.chinanews.com/zxjzbln/index.shtml news",  # 中新记者报辽宁
        "http://www.ln.chinanews.com/wenhua/index.shtml news",  # 文化
        "http://www.ln.chinanews.com/liaoning/index.shtml news",  # 辽宁
        "http://www.ln.chinanews.com/shenghuo/index.shtml news",  # 生活
        "http://www.ln.chinanews.com/shangye/index.shtml news",  # 商业
        "http://www.ln.chinanews.com/shishang/index.shtml news",  # 时尚
        "http://www.ln.chinanews.com/keji/index.shtml news",  # 科技
        "http://www.ln.chinanews.com/jiankang/index.shtml news",  # 健康
        "http://www.ln.chinanews.com/caijing/index.shtml news",  # 财经
        "http://www.ln.chinanews.com/shehui/index.shtml news",  # 社会
        "http://www.ln.chinanews.com/guoji/index.shtml news",  # 国际
        "http://www.ln.chinanews.com/nongye/index.shtml news",  # 农业
        "http://www.ln.chinanews.com/guonei/index.shtml news",  # 国内
        "http://www.ln.chinanews.com/hwmtkln/index.shtml news",  # 外媒
        "http://www.ln.chinanews.com/lvyou/index.shtml news",  # 旅游
        "http://www.ln.chinanews.com/fangchan/index.shtml news",  # 房产
        "http://www.ln.chinanews.com/jiaoyu/index.shtml news",  # 教育
        "http://www.heb.chinanews.com/4/20111018/327.shtml news",  # 中国新闻网_河北社会
        "http://www.fj.chinanews.com/new/fjxw/list.shtml news",  # 福建新闻网_福建新闻
        "http://www.fj.chinanews.com/new2015/jryw/list.html news",  # 中国新闻网_福建_导读
        "http://www.ha.chinanews.com/news/ news",  # 中国新闻网_河南新闻
        ### "http://www.jx.chinanews.com/ news",  # 中国新闻网_江西新闻 首页
        ### "http://www.heb.chinanews.com/# news",  # 中国新闻网_地方报道 首页
        "http://www.hb.chinanews.com/gnxw.html news",  # 中国新闻网_湖北国内新闻
        "http://www.hb.chinanews.com/xnc.html news",  # 中国新闻网_湖北新农村
        "http://www.shx.chinanews.com/jzyx.html news",  # 中国新闻网_陕西记者一线
        "http://www.shx.chinanews.com/sqjz.html news",  # 三秦骄子
        "http://www.shx.chinanews.com/shmj.html news",  # 书画名家
        "http://www.shx.chinanews.com/ztbd.html news",  # 专题报道
        "http://www.shx.chinanews.com/mtsp.html news",  # 媒体时评
        "http://www.shx.chinanews.com/sssh.html news",  # 时尚生活
        "http://www.shx.chinanews.com/zxsp.html news",  # 中新视频
        "http://www.hn.chinanews.com/hnjjdy/gzyj/index1.html news",  # 工作研究
        "http://www.hn.chinanews.com/hnjjdy/qyjw/index1.html news",  # 企业经纬
        "http://www.hn.chinanews.com/hnjjdy/ldlt/index1.html news",  # 领导论坛
        "http://www.hn.chinanews.com/hnjjdy/fzfl/index1.html news",  # 发展纪实
        ### "http://www.zj.chinanews.com/national/ news",  # 中国新闻网_国内浙江  # 404
        ### "http://www.zj.chinanews.com/ news",  # 中国新闻网_浙江首页
        ### "http://www.gx.chinanews.com/ news",  # 中国新闻网_广西新闻  首页
        ### "http://www.gs.chinanews.com/lanzhou/index.html news",  # 中国新闻网_兰州新闻 首页
        "http://www.hn.chinanews.com/news/jzyx/ news",  # 中国新闻网_记者一线
        ### "http://www.bt.chinanews.com/Index.html news",  # 中国新闻网_兵团新闻网  # 404
        ### "http://www.bj.chinanews.com/4/2009/0306/5.html news",  # 中国新闻网_京华季风 太旧
        ### "http://www.bj.chinanews.com/4/2009/0306/4.html news",  # 中国新闻网_海外看北京 太旧
        "http://www.hn.chinanews.com/news/lyxw/index.shtml news",  # 旅游新闻
        "http://www.hn.chinanews.com/news/cnsdc/index.shtml news",  # 热点追踪
        "http://www.hn.chinanews.com/news/gatq/index.shtml news",  # 港澳台侨
        "http://www.hn.chinanews.com/news/shsh/ news",  # 社会生活
        "http://www.hn.chinanews.com/news/cjxx/ news",  # 财经信息
        "http://www.hn.chinanews.com/news/gnxw/ news",  # 国内新闻
        "http://www.hn.chinanews.com/news/szws/ news",  # 时政外事
        "http://www.hn.chinanews.com/news/fcxw/ news",  # 房产新闻
        "http://www.hn.chinanews.com/news/hnyw/index.shtml news",  # 湖南要闻
        "http://www.hn.chinanews.com/news/gngj/ news",  # 国内国际
        "http://www.hn.chinanews.com/news/sxdt/ news",  # 市县动态
        "http://www.hn.chinanews.com/news/tyxw/index.shtml news",  # 体育新闻
        "http://www.hn.chinanews.com/news/kjww/ news",  # 科教文卫
        "http://www.hn.chinanews.com/news/ylty/ news",  # 娱乐体育
        "http://www.heb.chinanews.com/4/20111018/321.shtml news",  # 中国新闻网_中新社记者看河北
        "http://www.chinanews.com/importnews.html news",  # 中国新闻网_要闻导读
        "http://www.sh.chinanews.com/swzx/index.shtml news",  # 商企资讯
        "http://www.sh.chinanews.com/gatq/index.shtml news",  # 港澳台侨
        "http://www.sh.chinanews.com/ztbd/index.shtml news",  # 专题报道
        "http://www.sh.chinanews.com/szyw/index.shtml news",  # 时政要闻
        "http://www.sh.chinanews.com/whty/index.shtml news",  # 文化体育
        "http://www.sh.chinanews.com/ckzx/ckzx-cyxx/index.shtml news",  # 创业新秀
        "http://www.sh.chinanews.com/qxdt/index.shtml news",  # 区县动态
        "http://www.sh.chinanews.com/kjws/index.shtml news",  # 科教卫生
        "http://www.sh.chinanews.com/ckzx/ckzx-hqck/index.shtml news",  # 环球创客
        "http://www.sh.chinanews.com/cjxw/index.shtml news",  # 财经新闻
        "http://www.sh.chinanews.com/ckzx/ckzx-ckkj/index.shtml news",  # 创客空间
        "http://www.sh.chinanews.com/shms/index.shtml news",  # 社会民生
        "http://www.sh.chinanews.com/ckzx/ckzx-kcsd/index.shtml news",  # 科创时代
        "http://www.sh.chinanews.com/spxw/index.shtml news",  # 视频新闻
        "http://www.sh.chinanews.com/shxw/index.shtml news",  # 上海新闻
        "http://www.zj.chinanews.com/sh/jkcy/index.html news",  # 健康产业
        "http://www.zj.chinanews.com/qt/yss/index.html news",  # 游山水
        "http://www.zj.chinanews.com/qt/kqt/index.html news",  # 中新记者看青田
        "http://www.zj.chinanews.com/qt/hzzx/index.html news",  # 华助中心
        "http://www.zj.chinanews.com/sh/ztc/index.html news",  # 旅讯直通车
        "http://www.zj.chinanews.com/jy/cy/index.html news",  # 创业
        "http://www.zj.chinanews.com/jy/kjs/index.html news",  # 会计师
        "http://www.zj.chinanews.com/qt/ltpl/index.html news",  # 论坛评论
        "http://www.zj.chinanews.com/jy/ky/index.html news",  # 考研
        "http://www.zj.chinanews.com/cj/gd/index.html news",  # 观点
        "http://www.zj.chinanews.com/wy/mx/index.html news",  # 明星
        "http://www.zj.chinanews.com/jy/gx/index.html news",  # 高校
        "http://www.zj.chinanews.com/jy/gk/index.html news",  # 公考
        "http://www.zj.chinanews.com/jy/zczj/index.html news",  # 政策直击
        "http://www.zj.chinanews.com/wy/ys/index.html news",  # 影视
        "http://www.zj.chinanews.com/jy/lx/index.html news",  # 留学
        "http://www.zj.chinanews.com/jy/sfks/index.html news",  # 司法考试
        "http://www.zj.chinanews.com/wy/tj/index.html news",  # 图集
        "http://www.sh.chinanews.com/tpxw/index.shtml news",  # 图片新闻
        "http://www.sd.chinanews.com/more/news/4.html news",  # 山东新闻
        "http://www.sd.chinanews.com/more/news/7.html news",  # 中新社记者看山东
        "http://www.sd.chinanews.com/more/news/10.html news",  # 社会
        "http://www.sd.chinanews.com/more/news/11.html news",  # 文化
        "http://www.sd.chinanews.com/more/news/1.html news",  # 头条
        "http://www.sd.chinanews.com/more/news/26.html news",  # 经济
        "http://www.sd.chinanews.com/more/news/6.html news",  # 国际新闻
        "http://www.sd.chinanews.com/more/news/9.html news",  # 政治
        "http://www.sd.chinanews.com/more/news/5.html news",  # 国内新闻
        "http://www.sd.chinanews.com/more/news/12.html news",  # 娱乐
        "http://www.bt.chinanews.com/kejiao/index.shtml news",  # 科教文卫
        ### "http://www.js.chinanews.com/ news",  # 江苏新闻网_江苏新闻 首页
        ### "http://www.gz.chinanews.com/gzxw/index.shtml news",  # 中国新闻网_贵州新闻
        "http://www.sx.chinanews.com/4/2009/0110/2.html news",  # 中国新闻网_山西舆情
        ### "http://www.jx.chinanews.com/minsheng/ news",  # 中国新闻网_江西民生
        ### "http://www.jx.chinanews.com/edu/ news",  # 中国新闻网_教育
        ###"http://www.jx.chinanews.com/qiaowu/ news",  # 中国新闻网_侨务
        ### "http://www.sc.chinanews.com/ news",  # 中国新闻网_四川频道
        ### "http://www.yn.chinanews.com/pub/news/world/ news",  # 云南新闻网_网闻天下
        ### "http://www.yn.chinanews.com/pub/news/ news",  # 云南新闻网_新闻中心
        ### "http://www.ln.chinanews.com/ news",  # 辽宁新闻网_首页
        ### "http://www.ln.chinanews.com/XinWen news",  # 辽宁新闻网_新闻  # 404
        ### "http://www.bj.chinanews.com/ news",  # 中国新闻网_北京新闻
        "http://www.bj.chinanews.com/4/2009/0306/1.html news",  # 中国新闻网_京华聚焦
        ### "http://www.shx.chinanews.com/ news",  # 中国新闻网_陕西新闻
        ### "http://www.ha.chinanews.com/GNnews/4/index.shtml news",  # 中国新闻网_河南国际新闻  # 404
        ### "http://www.ha.chinanews.com/GNnews/5/index.shtml news",  # 中国新闻网_河南国内新闻  # 404
        "http://www.shx.chinanews.com/news/jjxw.shtml news",  # 中国新闻网_经济新闻
        ### "http://www.sx.chinanews.com/ news",  # 中国新闻网_山西新闻
        "http://www.js.chinanews.com/highlights/ news",  # 时政民生
        "http://www.hb.chinanews.com/wbhb.html news",  # 中国新闻网_湖北外报湖北
        "http://www.hb.chinanews.com/jzyx.html news",  # 中国新闻网_湖北记者一线
        "http://www.hb.chinanews.com/shxw.html news",  # 中国新闻网_湖北社会新闻
        "http://www.hb.chinanews.com/hbxw.html news",  # 中国新闻网_湖北要闻
        "http://www.hb.chinanews.com/dsxw.html news",  # 中国新闻网_湖北地市新闻
        "http://www.hb.chinanews.com/gjxw.html news",  # 中国新闻网_湖北国际新闻
        "http://www.hb.chinanews.com/pinglun.html news",  # 中国新闻网_湖北媒体评论
        ### "http://www.js.chinanews.com/wx/17/7.html news",  # 中国新闻网_江阴新闻  # 404
        ### "http://www.chinanews.com/edu/index.shtml news",  # 中国新闻网_教育频道
        "http://www.heb.chinanews.com/4/20111018/326.shtml news",  # 中国新闻网_河北外事
        "http://www.heb.chinanews.com/4/20111018/329.shtml news",  # 中国新闻网_河北经济
        "http://www.chinanews.com/huaren.shtml news",  # 中国新闻网_华人新闻
        ### "http://www.gd.chinanews.com/ news",  # 中国新闻网_广东新闻首页
        "http://www.gd.chinanews.com/gnxw.html news",  # 中国新闻网_国内新闻
        "http://www.chinanews.com/it.shtml news",  # 中国新闻网_IT频道
        ### "http://news.chinanews.com/ news",  # 中国新闻网_新闻中心  # timeout
        ### "http://www.ah.chinanews.com/ news",  # 中国新闻网_安徽新闻网
        "http://www.js.chinanews.com/photo/ news",  # 图片报道
        ### "http://www.js.chinanews.com/xz/ news",  # 徐州  # 404
        ### "http://channel.chinanews.com/cns/cl/it-hlw.shtml news",  # 中国新闻网_互联网  # timeout
        ### "http://channel.chinanews.com/cns/cl/it-txxw.shtml news",  # 中国新闻网_通信  # timeout
        ### "http://channel.chinanews.com/cns/cl/ga-zlg.shtml news",  # 资料馆  # timeout
        ### "http://www.yn.chinanews.com/ news",  # 云南新闻网_首页
        "http://www.chinanews.com/photo/shmy.html news",  # 时尚魅影
        ### "http://www.chinanews.com/shipin_more/ayzq/1.html news",  # 文体视频 太旧了
        "http://www.chinanews.com/photo/gatq.html news",  # 港澳台侨
        "http://www.chinanews.com/photo/more/1.html news",  # 图片
        "http://www.chinanews.com/photo/gjbl.html news",  # 国际博览
        "http://www.chinanews.com/photo/jskj.html news",  # 军事图片
        "http://www.fj.chinanews.com/new2014/xmxw/list.shtml news",  # 中国新闻网_厦门
        ### "http://www.xj.chinanews.com/html/L_64.htm news",  # 中国新闻网_新疆社会民生  # 404
        ### "http://www.xj.chinanews.com/html/L_62.htm news",  # 中国新闻网_新疆地州新闻  # 404
        ### "http://www.xj.chinanews.com/html/L_50.htm news",  # 中国新闻网_新疆国际  # 404
        ### "http://www.xj.chinanews.com/html/L_59.htm news",  # 中国新闻网_新疆法制报道  # 404
        ### "http://www.xj.chinanews.com/html/L_53.htm news",  # 中国新闻网_新疆曝光台  # 404
        ### "http://www.xj.chinanews.com/html/L_66.htm news",  # 中国新闻网_新疆经济资讯  # 404
        ### "http://www.xj.chinanews.com/html/L_51.htm news",  # 中国新闻网_新疆国内  # 404
        ### "http://www.xj.chinanews.com/html/L_47.htm news",  # 中国新闻网_新疆兵团新闻  # 404
        ### "http://www.xj.chinanews.com/html/L_42.htm news",  # 中国新闻网_看新疆专版  # 404
        ### "http://www.xj.chinanews.com/html/L_61.htm news",  # 中国新闻网_图文专稿  # 404
        ### "http://www.sc.chinanews.com/news/News_OverseasMedia/list.html news",  # 中国新闻网_海外媒体刊四川  # 404

    ]
    Debug = True
    doredis = True
    source = u"中国新闻网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"DOWNLOAD_TIMEOUT": 120.0, "DOWNLOAD_DELAY": 0.25, "ROBOTSTXT_OBEY": False}
    sta = {"eff": 0, "inv": 0, "warn": 0, "all": 0, "inv2": 0, "no_title": 0, "no_time": 0, "no_medianame": 0}

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
            self.log.write(info+'\n')
        elif color == "33":
            print "警告： ", info
            self.log.write(info+'\n')
        else:
            print "信息: ", info
        print "统计: ",
        print "有效:", self.sta["eff"], " 无效: ", self.sta["inv"], " 警告: ", self.sta["warn"]," 人为失效:", self.sta["inv2"], \
            " 乐观总计:", self.sta["all"], " 去重后数量:", len(set(self.test_list)) ," 采集率:", "%.2f%%" % (float(self.sta["eff"])/float(len(set(self.test_list)) - self.sta["warn"]-self.sta["inv"])*100), \
            " 无发布源:", self.sta['no_medianame'], " 无时间:", self.sta['no_time'], " 无标题:", self.sta['no_title']
        print('*' * 100)
        print('\033[0m')

    def __init__(self, start_url=None):
        super(chinanews, self).__init__()
        # jobs = start_url.split('|')
        self.test_list = list()
        self.log = codecs.open('URL_ERROR.log', 'a', encoding='utf-8')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url": job.split()[0], "ba_type": job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

    def __del__(self):
        self.log.close()

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

    def get_parse_link_urls(self, response, url):   # 有改良方案，再说吧
        # 进入列表页　然后抽取列表页的详情页
        urls_list = [
            # url　xpath规则　待加入
            '//div[@class="content_list"]/ul/li/div[@class="dd_bt"]/a/@href',  # 时政滚动
            '//div[@class="content_list"]/ul/li/div/a/@href',  # 时政滚动
            '//div[contains(@class, "con2")]//a/@href',  # 时政半通用
            '//ul[contains(@class,"LB_list")]/li/h2/a/@href',  # 一带一路
            '//div[@class="sec_left_1"]/ul/li/a/@href',  # 广东
            '//div[@id="newsArea"]/ul/li/a/@href', # 云南旅游
            '//ul[contains(@class, "newsList")]//a/@href',  # 山西国际
            '//div[@class="libox"]/a/@href',  # 图文专稿
            '//li/div[@class="dd_bt"]/a/@href',  # 广东资讯
            '//div[@class="list"]/ul/li/a/@href',  # 时尚
            '//div[@class="list_li"]/a/@href',  # 福建导读
            '//div[@class="map_left"]/ul/li/a/@href',  # 云南 网友之声
            '//ul[@class="NLPul"]//span/a/@href',  # 趣味视频
            '//div[@id="frameContent1"]/div/div/a[contains(@class, "link")]/@href',  # 陕西频道
            '//table[@class="v12"]/following-sibling::table//tr//td/a/@href',  # 北京分频
            '//div[@class="content_list"]/ul/li//div/a/@href',  # CNSTV
            '//ul[@id="ul_news"]/li/div/a/@href',  # 福建新闻网
            '//div[@class="list_con"]/ul/li/div/a/@href',  # 福建新闻网
            '//ul[@class="news_list_ul"]/li/div/a/@href',  # 视频频道
            '//ul[contains(@class, "contentlist")][position()<51]/li/span/a/@href',
            '//ul[contains(@class, "contentlist")]/li[position()<101]/span/a/@href',  # 娱乐新闻
            '//ul[@class="list_16"]/li/a/@href',
            '//div[@class="pmbox1"]/a/@href',  # 热辣图库
            '//ul[contains(@class, "branch_list_ul")]/li/a/@href',  # 中新社北京分社
            '//div[@class="listbox"]/ul//li/a/@href',  # 甘肃要闻
            '//div[@class="left_zw"]/div/table//ul/li/a/@href',  # 河北新闻
            '//a[@class="title2"]/@href',  # 纵览天下
            '//ul[@id="JrhnNews"]/li/a/@href',  # 湖南新闻报
            '//div[@class="videoList"]/dl/dd/a/@href',  # 视频新闻
            '//div[@id="list"]/ul/li/a/@href',  # 江苏频道
            '//div[@class="list"]/div[@class="pic"]/a/@href',  # 江苏图片频道
            '//ul[@class="paging"]/li/a/@href',  # 成都频道
            '//div[@class="container"]/div[contains(@class, "img")]/div/a/@href',  # 中新图片频道
            '//div[@class="picdiv"]/div/a/@href',  # 图解新闻
            '//div[@id="news_list"]/ul/li[position()<50]/a/@href', # 演出频道 热门资讯
            '//ul[@id="DataList"]/li/a/@href',  # 重庆频道 每次重庆的频道都是单独一种 真有牌面
            '//ul[@id="listContainer"]/li/h2/a/@href',  # 福建频道
            '//ul[@id="ul_news"]/li/a/@href',  # 贵州频道
            '//span[@class="rt"]/following-sibling::a/@href',  # 广西频道
            '//ul[contains(@class, "contentlist")]/li[position()<101]//a/@href',  # 海南新闻
            '//ul[contains(@class, "contentlist")]/div[position()<101]//a/@href',  # 海南图片新闻
            '//ul[@id="tablelsw"]/li//a/@href',  # 海南养生频道  这个图片翻页又是新的一种
            '//div[contains(@class, "liebiao")]/ul/li/a/@href',  # 河南频道
            '//div[@id="content_list"]/p//a/@href',  # 湖北
            '//li[@class="Timg2"]/span[1]/a/@href',  # 湖北图片
            '//div[@class="news_list_box"]//a/@href',  # 黑龙江频道
            '//div[@id="sy_list_left"]//ul/li[position()<21]/a/@href',  # 内蒙古频道
            '//ul[@class="branch_list_ul paging"]/li[position()<41]/div[2]/a/@href',  # 上海频道
            '//div[@id="showtypeli"]/ul//tr/td/a/@href',  # 经济纵横
            '//div[@class="wz"]/ul[@class="e2"]//a/@href',  # 甘肃新闻
            '//div[@class="content-bt"]/a[1]/@href',  # 推荐阅读
            '//td[@id="TT"]/li[position()<51]/a/@href',  # 国内新闻
        ]
        for url_xpath in urls_list:
            if len(response.xpath(url_xpath).extract()) > 0:
                print url, " 本次套用:", url_xpath," 条目数:", len(response.xpath(url_xpath).extract())
                return url_xpath
        print response.url, " 没有适当规则"
        content = response.url + '  这个频道需要url规则!\n'
        self.log.write(content)

    def parse_link(self, response):
        try:
            if 'currentpage=0&' in response.url:
                # ajax接口处理
                urls = re.findall(r"url':\s?'(http:.+?.shtml)", response.body)
            else:
                xpath = self.get_parse_link_urls(response, response.url)
                # print "xpath: ", xpath
                urls = response.xpath(xpath).extract()
                self.sta["all"] += len(urls)
            print "看看数量吧, 总量: ",self.sta["all"]
            for index, url in enumerate(urls):
                if '../' in url:
                    url = url.replace('../', '')
                final = urlparse.urljoin(response.url, url)
                # print final
                # 海南频道的2012和2013年的新闻会乱入 一：太旧了 二：会有无法解释的bug发生
                if 'chinanews' in final and ('2012-' not in final and '2013-' not in final):
                    self.test_list.append(final)
                    # print 'final_url is %s'%final
                    # if index>0:
                    #     break
                    # if self.doredis and self.expire_redis.exists(final):
                    #    continue

                    yield Request(url=final, method='get',
                                  meta={"ba_type": response.meta["ba_type"], "parse_for_content": True},
                                  callback=self.parse_item, errback=self.parse_err_detail)
        except Exception,e:
            print response.url, e.message
            content = response.url + e.message
            self.log.write(content)

    def parse_err_detail(self, failure):
        response = failure.value.response
        self.print_info("页面异常: " + response.url + "  状态：" + str(response.status), "error")

    def parse_item(self, response):
        try:
            if response.meta["parse_for_content"]:
                item = DataItem()

                # 标题
                title1 = response.xpath('//div[@id="xw_title"]/h2') or \
                         response.xpath('//div[@id="newsTitle"]') or \
                         response.xpath('//div[@id="biaoti"]') or \
                         response.xpath('//div[@class="thi_left_1"]/h2') or \
                         response.xpath('//div[@class="blkContainerSblk"]/h1') or \
                         response.xpath('//div[@class="content-title"]') or \
                         response.xpath('//div[@class="con-titl"]') or \
                         response.xpath('//div[@class="con_titl"]') or \
                         response.xpath('//div[@class="newbiaoti"]/strong') or \
                         response.xpath('//td[@id="content"]//strong') or \
                         response.xpath('//div[@id="mian"]/div/i') or \
                         response.xpath('//div[@class="window1"]/div[@class="h6"]') or \
                         response.xpath('//div[contains(@class, "biaoti")]') or \
                         response.xpath('//td[@id="content"]/table[1]/tbody[1]/tr[1]/td[1]') or \
                         response.xpath('//div[@class="neir_bt"]') or \
                         response.xpath('//div[@class="title"]/h1') or \
                         response.xpath('//div[@class="title"]') or \
                         response.xpath('//div[@class="c_title"]') or \
                         response.xpath('//div[@id="title"]') or \
                         response.xpath('//div[@class="pagetitle"]') or \
                         response.xpath('//dt[@class="wryh"]') or \
                         response.xpath('//span[@id="txtTitle"]') or \
                         response.xpath('//div[@class="neiron_title"]') or \
                         response.xpath('//div[@class="news_title"]') or \
                         response.xpath('//td[contains(@class, "black_titnews")]') or \
                         response.xpath('//h1[@id="tit"]') or \
                         response.xpath('//h1') or \
                         response.xpath('//div[@class="left_five1"]') or \
                         response.xpath('//div[@class="cms-news-article-title"]/span') or \
                         response.xpath('//div[@class="neiyect"]/h3') or \
                         response.xpath('//div[@class="incont_t"]/h2') or \
                         response.xpath('//div[@class="atitle"]/div[@class="f_l"]') or \
                         response.xpath('//div[@class="listbox"]/div[@class="dd"]')
                         # response.xpath('//head/title')  # 云南每日专题  没时间 没来源
                item["title"] = ""
                if len(title1) > 0:
                    item['title'] = title1[0].xpath('string(.)').extract()[0].strip()
                if item["title"] == "":
                    self.print_info(response.url + "  这个详细页无标题！！！", "warn", False)
                    self.sta['no_title'] += 1
                    item["title"] = response.xpath("//title/text()").extract()[0]


                # 发布时间
                # pubtime1 存放 text()等不用再处理的
                pubtime1 = response.xpath('//strong/li/a/div/text()').extract()

                pubtime2 = response.xpath('//div[@class="left-time"]//div[@class="left-t"]') or \
                           response.xpath('//div[@id="xw_xinxi"]/span[1]') or \
                           response.xpath('//div[@class="cms-news-article-title-source"]') or \
                           response.xpath('//p[@class="fabushijian"]') or \
                           response.xpath('//div[@class="neiron_hh"]/li[1]') or \
                           response.xpath('//div[@id="newsInfo"]') or \
                           response.xpath('//div[@id="sendday"]') or \
                           response.xpath('//div[@class="thi_left_1"]/dl/dt') or \
                           response.xpath('//div[@class="artInfo"]/span[@id="pub_date"]') or \
                           response.xpath('//div[@class="con_time"]/ul/li[1]') or \
                           response.xpath('//div[contains(@class, "content-time")]/div[1]') or \
                           response.xpath('//div[@id="anthornew"]') or \
                           response.xpath('//div[@id="anthor"]') or \
                           response.xpath('//div[@class="video_con"]/p/span[1]') or \
                           response.xpath('//div[@class="tit-bar fl"]/span[3]') or \
                           response.xpath('//div[@class="t3"]/following-sibling::div[1]') or \
                           response.xpath('//div[@class="window21"]/div[@class="h5"]') or \
                           response.xpath('//div[@class="biaoti"]/following-sibling::div[@class="suoying"]') or \
                           response.xpath('//div[@class="atime"]') or \
                           response.xpath('//div[@class="p1"]') or \
                           response.xpath('//div[@id="time"]') or \
                           response.xpath('//div[@class="news_info"]/span[1]') or \
                           response.xpath('//div[@class="addtime"]') or \
                           response.xpath('//div[@class="pagetop"]') or \
                           response.xpath('//div[@class="c_info"]/div[@class="f_l"]') or \
                           response.xpath('//dl[@class="headline"]/dd/span[1]') or \
                           response.xpath('//div[@class="left_five2"]') or \
                           response.xpath('//div[@class="neiyectime"]') or \
                           response.xpath('//div[@id="xw_xinxi"]/span[1]') or \
                           response.xpath('//div[contains(@class, "laiyuan")]') or \
                           response.xpath(u'//td[contains(text(), "发布时间")]') or \
                           response.xpath(u'//div[contains(text(), "来源")]') or \
                           response.xpath(u'//span[contains(text(), "时间")]') or \
                           response.xpath(u'//*[contains(text(), "来源")]') or \
                           response.xpath('//h1/following-sibling::span') or \
                           response.xpath('//h1/following-sibling::p') or \
                           response.xpath('//div[@class="zwbei01 div_12px zw_01"]')
                    # response.xpath('//td[@class="jiathis_style"]/ancestor::tr/td[1]') or \
                           # response.xpath('//div[@class="xdd"]/table/tbody/tr/td[1]')

                # print pubtime1,'----',pubtime2
                item['pubtime'] = ''
                if len(pubtime1) > 0:
                    print pubtime1
                    item['pubtime'] = re.search(r'\d{4}.\d{1,2}.\d{1,2}\s+\d{1,2}[:：]\d{1,2}', pubtime1[0]).group(0)
                if len(pubtime2) > 0 and len(pubtime1) == 0:
                    pubtime2 = pubtime2[0].xpath('string(.)').extract()[0].strip().replace("年", "-").replace("月",
                                                                                                             "-").replace(
                        "日", " ")
                    if re.search(r"(\d{4}-\d{1,2}-\d{1,2}.+\d)", pubtime2):
                        # 这里re规则 作了些修改 可能后续有不兼容的情况
                        # 出现了不需要的字段 虽然不影响
                        item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}.+\d)", pubtime2).group(0)
                    elif re.search(r"\d+", pubtime2):
                        # item["pubtime"] = re.search(r"(\d{4}.\d{1,2}.\d{1,2}\s\d{1,2}:\d{1,2})",
                        item["pubtime"] = re.search(r"(\d+.+\d)",
                                                    pubtime2.replace(".", "-")).group(0)

                if len(pubtime2) == 0 and len(pubtime1) == 0:
                    self.print_info(response.url + "  这个详细页无发布时间！！！", "warn", False)
                    self.sta['no_time'] += 1
                    pubtime3 = re.findall(r"published.+at.+(\d{4}.+:\d{2})", response.body)
                    # print 'Pubtime3: ---------', pubtime3
                    print 'response.headers: ', response.headers
                    if len(pubtime3) > 0:
                        item["pubtime"] = pubtime3[0]

                    elif 'Last-Modified' in response.headers:
                        item['pubtime'] = datetime.datetime.strptime(response.headers["Last-Modified"],
                                                                     '%a, %d %b %Y %H:%M:%S GMT').strftime(
                            "%Y-%m-%d %H:%M")
                    elif 'Date' in response.headers:
                        item['pubtime'] = datetime.datetime.strptime(response.headers["Date"], '%a, %d %b %Y %H:%M:%S GMT').strftime("%Y-%m-%d %H:%M")

                # 来源
                item['medianame'] = ""

                # medianame1 是存放需要string()处理的xpath规则
                medianame1 = response.xpath('//div[@class="left-time"]//div[@class="left-t"]') or \
                             response.xpath('//div[@id="newsInfo"]/a') or \
                             response.xpath('//div[@class="cms-news-article-title-source"]') or \
                             response.xpath('//p[@class="fabulaiyuan"]') or \
                             response.xpath('//div[@id="newsInfo"]') or \
                             response.xpath('//div[@class="thi_left_1"]/dl/dt') or \
                             response.xpath('//div[@class="artInfo"]/span[@id="media_name"]') or \
                             response.xpath('//div[@class="con_time"]/ul/li[2]') or \
                             response.xpath('//div[contains(@class, "content-time")]/div[2]') or \
                             response.xpath('//div[@id="anthor"]') or \
                             response.xpath('//div[@class="suoying"]') or \
                             response.xpath('//div[@class="biaoti"]/following-sibling::div[@class="suoying"]') or \
                             response.xpath('//div[@class="video_con"]/p/span[2]') or \
                             response.xpath('//div[@class="tit-bar fl"]/span[1]') or \
                             response.xpath('//div[@class="window23"]/div[@class="h5"]/a') or \
                             response.xpath('//div[@class="biaoti"]/following-sibling::div[@class="suoying"]/a') or \
                             response.xpath('//div[@class="atime"]') or \
                             response.xpath('//div[@class="news_info"]/strong[1]') or \
                             response.xpath('//div[@class="p1"]') or \
                             response.xpath('//div[@id="come"]') or \
                             response.xpath('//div[@id="xw_xinxi"]/span[2]') or \
                             response.xpath('//div[@class="c_info"]/div[@class="f_l"]') or \
                             response.xpath('//div[@class="nrfbtime"]/span/i') or \
                             response.xpath('//div[@class="other"]/div[@class="l"]') or \
                             response.xpath('//div[@class="pagetop"]') or \
                             response.xpath('//dl[@class="headline"]/dd/span[2]/a') or \
                             response.xpath('//div[contains(@class, "laiyuan")]') or \
                             response.xpath('//div[@class="left_five2"]') or \
                             response.xpath('//div[@class="neiyecontent"]/following-sibling::em') or \
                             response.xpath('//div[@class="neiron_hh"]/li[2]') or \
                             response.xpath('//div[@class="window23"]/div[@class="h5"]') or \
                             response.xpath(u'//td/div[contains(text(), "来源")]') or \
                             response.xpath(u'//span[contains(text(), "来源")]') or \
                             response.xpath(u'//p[contains(text(), "来源")][position()=last()]') or \
                             response.xpath(u'//em[contains(text(), "来源")]') or \
                             response.xpath('//h1/following-sibling::span') or \
                             response.xpath('//h1/following-sibling::p') or \
                             response.xpath(u'//td[contains(text(), "发布时间")]')
                            # response.xpath(u'//div[contains(text(), "来源")]') or \
                            # response.xpath('//td[@class="jiathis_style"]/ancestor::tr/td[1]') or \
                             # response.xpath('//div[@class="xdd"]/table/tbody/tr/td[1]')

                # medianame2 存放的是最终的xpath规则
                medianame2 = response.xpath('//div[@id="xw_xinxi"]/span[2]/text()').extract()

                medianame3 = response.xpath('//div[@id="anthornew"]')
                if len(medianame1) > 0:
                    medianame1 = medianame1.xpath('string(.)').extract()[0].strip()
                    # print medianame1
                    if len(re.findall(ur"(来源|出处|来自|稿源|出自|来源于)", medianame1)) > 0:
                        # 这里会有一个坑 来源： 后面没了 有些网站没有来源还把来源：3个字写上去 kao
                        if not re.search(u'来源[：:]\s*$', medianame1):
                            item["medianame"] = re.search(u'.*?(来源|出处|来自|稿源|出自|来源于)\s*[：:]\s*(\S*)\s?', medianame1).group(2)
                    else:
                        item["medianame"] = medianame1

                if len(medianame2) > 0 and len(medianame1) == 0:
                    item["medianame"] = medianame2[0].strip()

                if len(medianame3) > 0 and len(medianame2) == 0 and len(medianame1) == 0:
                    medianame3 = medianame3.xpath('string(.)').extract()[0]
                    item['medianame'] = medianame3.split()[0]

                if u'参与互动' in item['medianame']:
                    item['medianame'] = re.search(ur'(.+)参与互动.+', item['medianame']).group(1)

                if u"年" in item["medianame"] and u"月" in item["medianame"]:
                    self.print_info(item['title'] + " " + response.url + "  这个来源包括了时间，检查！！！", "warn", False)
                    item["medianame"] = u"中国新闻网"

                if item["medianame"] == "":
                    # self.print_info(item['title'] + " " + response.url + "  这个详细页无来源！！！", "warn", False)
                    self.print_info(item['title'] + " " + response.url + "  这个详细页无来源！！！", "warn", False)
                    self.sta['no_medianame'] += 1
                    item["medianame"] = u"中国新闻网"
                # print item["medianame"]


                # 种类/地区/源/收集时间/url
                item["type"] = response.meta["ba_type"]
                if "//gj" in response.url:
                    item['area'] = u'国际'
                else:
                    item['area'] = u'全国'
                item['source'] = self.source
                item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
                item['url'] = response.url

                # 内容
                content = response.xpath('//div[@id="MyContent"]').extract() or \
                          response.xpath('//div[contains(@class, "content-time")]/following-sibling::div[not(@class)]').extract() or \
                          response.xpath('//div[@class="left_zw"]').extract() or \
                          response.xpath('//div[@id="newsText"]').extract()or \
                          response.xpath('//td[@id="TT"]').extract()or \
                          response.xpath('//div[@id="artibody"]').extract() or \
                          response.xpath('//div[@id="xw_content"]').extract() or \
                          response.xpath('//div[@id="zoom"]').extract() or \
                          response.xpath('//div[@id="txt"]').extract() or \
                          response.xpath('//div[@class="txt"]').extract() or \
                          response.xpath('//div[@class="con_con"]').extract() or \
                          response.xpath('//div[@class="art-con"]').extract() or \
                          response.xpath('//div[@class="content_desc"]').extract() or \
                          response.xpath('//div[@id="d1d"]').extract() or \
                          response.xpath('//div[@id="cont_show"]').extract() or \
                          response.xpath('//div[@id="window"]/ancestor::div[@id="container"]').extract() or \
                          response.xpath('//div[@class=" branch_con_text"]').extract() or \
                          response.xpath('//div[@class="zhenwen"]/..').extract() or \
                          response.xpath('//div[@class="article-content"]').extract() or \
                          response.xpath('//div[@class="neiron_kong"]').extract() or \
                          response.xpath('//div[@class="content"]').extract() or \
                          response.xpath('//div[@class="main"]').extract() or \
                          response.xpath('//div[@class="wz"]').extract() or \
                          response.xpath('//td[@id="content"]').extract() or \
                          response.xpath('//div[@class="nrfbtime"]/span/i').extract() or \
                          response.xpath('//div[@class="picnr_con"]').extract() or \
                          response.xpath('//div[@class="pagecon"]').extract() or \
                          response.xpath('//div[@id="content"]').extract() or \
                          response.xpath('//div[@id="ArticleCnt"]').extract() or \
                          response.xpath('//div[@id="eFramePic"]').extract() or \
                          response.xpath('//div[@id="ArticleBody"]').extract() or \
                          response.xpath('//div[contains(@class,"tp_bdiv dh-")]').extract() or \
                          response.xpath('//div[contains(@class, "bigdiv4")]').extract() or \
                          response.xpath('//div[@id="content_text"]').extract() or \
                          response.xpath('//td[contains(@class, "black_titnews")]/ancestor::tr/following-sibling::tr[last()]').extract() or \
                          response.xpath('//div[@class="left_five3"]').extract() or \
                          response.xpath('//div[@class="cms-news-article-content-block"]').extract() or \
                          response.xpath('//div[@id="txt_content"]').extract() or \
                          response.xpath('//div[@class="incont_txt"]').extract() or \
                          response.xpath('//div[@class="neiyecontent"]').extract() or \
                          response.xpath('//div[@class="t3"]').extract() or \
                          response.xpath('//div[@class="thi_left_1"]/dl').extract() or \
                          response.xpath('//div[@class=" row-fluid content-time "]/following-sibling::div[@style]').extract()
                if len(content) > 0:
                    item['content'] = content[0]
                if item['content'] == "":
                    content0 = response.url
                    self.log.write(content0)
                    print '没有抓到内容', response.url
                    raise Exception("无详细内容！！！！")


                # 页数 ，图片类的要翻页
                total_pages = response.xpath("//span[@id='showTotal']/text()").extract() or \
                              response.xpath("//a[@class='ptfontcon'][2]/@href").extract()

                total_pages1 = response.xpath('//span[@class="cC00"]/ancestor::span[@id="total"]')

                # 又是另一种翻页规则
                total_pages2 = response.xpath('//span[@id="_function_code_page"]//*[contains(text(), "[")]') or \
                               response.xpath('//span[@id="_function_code_page"]/p/a[last()-1]')

                # print 'total : ', total_pages , 'len(): ', len(total_pages)
                # print 'total1 : ', total_pages1 , 'len(): ', len(total_pages1)
                # print 'total2 : ', total_pages2 , 'len(): ', len(total_pages2)
                if len(total_pages) > 0:
                    # print 'total_page: %s'%total_pages[0]
                    # total_pages = int(re.search(ur"(\d+).", total_pages[0]).group(1)
                    total_pages = int(total_pages[0])

                elif len(total_pages1) > 0:
                    total_pages1 = int(re.search(r'1/(\d{1,2})', response.body).group(1))

                elif len(total_pages2) > 0:
                    num = total_pages2.xpath('string(.)').extract()[0]
                    try:
                        # 如果上一页 下一页在test_page中，认为不是图片类
                        test_page = re.search(r'\D{2,5}', num).group(0)
                        total_pages2 = 1
                        # print 'test_page', test_page
                    except Exception, e:
                        total_pages2 = int(re.search(r'[(\d+)]', num).group(0))

                else:
                    total_pages = 1
                    total_pages1 = 1
                    total_pages2 = 1

                # print 'total_pages', total_pages ,type(total_pages)
                # print 'total_pages1', total_pages1,type(total_pages1)
                # print 'total_pages2', total_pages2,type(total_pages2)
                # print '测试 测试'
                if total_pages == []:
                    total_pages = 1
                if total_pages1 == []:
                    total_pages1 = 1
                if total_pages2 == []:
                    total_pages2 = 1

                if total_pages > 1:
                    # 翻页规则　需要定制
                    # url = response.url.replace(".htm","_2.htm")
                    page = int(re.search(r'/(\d+).shtml', response.url).group(1))
                    # for i in range(1, total_pages+1):
                    page_nav = page + 1
                    final_page = page + total_pages -1
                    url_str = '/%d.shtml'%page_nav
                    url = response.url.rpartition('/')[0] + url_str
                    print '处理 total_pages 图片类 %s'%url
                    yield Request(url=url,method='get',
                                  meta={"ba_type": response.meta["ba_type"],"item": item,
                                        "parse_for_content": False,"total_pages": total_pages,"current_page": 2, "final_page": final_page},
                                  callback=self.parse_item,errback=self.parse_err_detail)

                elif total_pages1 > 1:
                    url = response.url + '#p=2'
                    print '处理 total_pages1 图片类 %s'%url
                    yield Request(url=url,method='get',
                                  meta={"ba_type": response.meta["ba_type"],"item": item,
                                        "parse_for_content": False,"total_pages": total_pages1,"current_page": 2, "final_page": "total_page1"},
                                  callback=self.parse_item,errback=self.parse_err_detail)

                elif total_pages2 > 1:
                    url = response.url.rpartition('.')[0] + '_2.%s'%response.url.rpartition('.')[-1]
                    print '处理 total_pages2 图片类 %s'%url
                    yield Request(url=url,method='get',
                                  meta={"ba_type": response.meta["ba_type"],"item": item,
                                        "parse_for_content": False,"total_pages": total_pages2,"current_page": 2, "final_page": "total_page2"},
                                  callback=self.parse_item,errback=self.parse_err_detail)

                else:
                    if len(response.xpath("//*[@id='gmweqxiu']").extract()) > 0:
                        self.print_info("被主动舍弃的详细页: " + response.url + " 原因: 无content",  "warn")
                        pass
                    else:
                        if item['pubtime'] and item['title'] and item['content']:
                            self.print_info("发布时间: " + item['pubtime'] + " 标题: " + item["title"] +'\n'+ " 发布源: " + item['medianame'] + " url: " + response.url + "  共1页")
                            yield item
            else:
                # 中国新闻网的翻页不一样 这段代码特殊点
                print '图片翻页类: 正在处理 %s'%response.url
                item = response.meta["item"]
                final_page = response.meta["final_page"]
                total_pages = response.meta["total_pages"]
                content = response.xpath('//div[@id="cont_show"]').extract() or \
                          response.xpath('//div[@id="eFramePic"]').extract() or \
                          response.xpath('//div[contains(@class,"tp_bdiv dh-")]').extract() or \
                          response.xpath('//div[contains(@class, "bigdiv3")]').extract() or \
                          response.xpath('//div[@id="txt_content"]').extract() or \
                          response.xpath('//td[@id="TT"]').extract() or \
                          response.xpath('//div[@class=" row-fluid content-time "]/following-sibling::div[@style]').extract()

                if len(content) > 0:
                    content = content[0]
                item["content"] += "\n" + content

                if int(response.meta["current_page"]) == int(response.meta["total_pages"]):
                    if item['pubtime'] and item['title'] and item['content']:
                        self.print_info("发布时间: " + item['pubtime'] + " 标题: "+item["title"] +'\n' + " 发布源: " + item['medianame'] + " url: " + response.url + "  共" + str(response.meta["current_page"]) + "页")
                        yield item
                elif final_page == "total_page1":
                    # 因为两个图片频道完全不一样 需要新写一个方法
                    url = response.url.split('#')[0] + '#p=%d'%(int(response.meta['current_page'])+1)
                    yield Request(url=url,method='get',
                                  meta={"ba_type":response.meta["ba_type"],"item":item,
                                        "parse_for_content":False,"total_pages":response.meta["total_pages"],"current_page": response.meta["current_page"] + 1, "final_page": "total_page1"},
                                  callback=self.parse_item,errback=self.parse_err_detail)
                elif final_page == "total_page2":
                    # 又是一个新 翻页规则
                    url = response.url.rpartition('_')[0] + '_%d.%s'%(response.meta['current_page']+1, response.url.rpartition('.')[-1])
                    yield Request(url=url,method='get',
                                  meta={"ba_type":response.meta["ba_type"],"item":item,
                                        "parse_for_content":False,"total_pages":response.meta["total_pages"],"current_page": response.meta["current_page"] + 1, "final_page": "total_page2"},
                                  callback=self.parse_item,errback=self.parse_err_detail)
                else:
                    page = int(re.search(r'/(\d+).shtml', response.url).group(1))
                    if page < final_page:
                        # for i in range(1, total_pages+1):
                        page_nav = page + 1
                        url_str = '/%d.shtml'%page_nav
                        url = response.url.rpartition('/')[0] + url_str
                        # url = response.url.replace("_"+ str(response.meta["current_page"]) + ".htm","_" + str(response.meta["current_page"] + 1 ) +".htm")
                        yield Request(url=url,method='get',
                                      meta={"ba_type":response.meta["ba_type"],"item":item,
                                            "parse_for_content":False,"total_pages":response.meta["total_pages"],"current_page": response.meta["current_page"] + 1, "final_page": final_page},
                                      callback=self.parse_item,errback=self.parse_err_detail)
        except Exception:
            if len(response.xpath("//title/text()").extract()) > 0 and \
                    (u"页面没有找到" in response.xpath("//title/text()").extract()[0] or u"出错啦" in response.xpath("//title/text()").extract()[0]):
                self.print_info(traceback.format_exc() + "url:" + response.url + "  status: "+str(response.status), "error")
            else:
                self.print_info(traceback.format_exc() + "url:" + response.url + "  status: "+str(response.status), "error2")

