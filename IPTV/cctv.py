# -*- coding: utf-8 -*-
"""
cctv.live —— TVBox / FongMi Python 爬虫（cctv.py）

一、定位
  静态聚合源，不抓网页：把 6 个每日自动测速的 IPTV 名单现成结果合并成一份「一站一台」的频道表，
  内嵌进本文件，运行时零请求出列表。接口形态与 TVBox/FongMi 的 Python 源一致（Spider 类 +
  homeContent / categoryContent / detailContent / playerContent / searchContent），可直接被壳加载。

  数据源（抓取与合并由 cctv-live-iptv 技能完成，本文件只承载结果）：
    · guovin 每日输出  Guovin/iptv-api gd/output/result.m3u
    · BigBigGrandG    BigBigGrandG/IPTV-URL release/all.m3u
    · aptv            Kimentanm/aptv master/m3u/iptv.m3u
    · vbskycn         vbskycn/iptv master/tv/iptv4.m3u
    · ZBDS            live.zbds.top/tv/iptv4.txt
    · iptv-org        iptv-org.github.io/iptv/countries/cn.m3u

二、设计（列表清爽，播放不将就）
  · 列表只出 56 条主条目（一站一条，永不出现「CCTV-1 #2 #3」这种同名重复项）；
  · 点开某台，detailContent 把该台全部备用线路（通常 2~3 条，来自不同源）按质量排序后
    一次性挂成多条「线路」，点哪条播哪条；某条失效时手选下一条即可，不用回列表重找；
  · 线路按打分排序（1080p +40 / 720p +25 / HD +18 / Not 24/7 -10 / Geo-blocked -25，
    再叠加源权重与 IPv6 惩罚），第一条就是历史最优线；
  · 分类三个：央视 / 卫视 / 特色，另加「全部」；搜索支持频道名、id、分类名三向模糊匹配。

三、接口约定（与壳对齐，照抄 TVBox 通行写法）
  · 源名「cctv.live」：模块级 NAME/SITE_NAME/siteName/title/name、Spider 类属性、
    getName/getTitle/getSiteName、init 全部同值；壳从哪个字段读都是这个名字；
  · play id：`线路N·源 清晰度$cv:base64url({"url":..,"header":{..}})`，前缀 cv: 便于与别的源共存；
    playerContent 解出真链，恒 parse:0（直播直链无需解析器）；
  · 分类/搜索返回补齐 page / pagecount / limit / total 五项（_lines_result 统一补）；
  · 四个入口全部异常兜底，任何一个出错只返回空列表，不会把壳打崩；
  · 详情与播放地址各带短缓存，来回进出详情页不重复算。

四、自测：python3 cctv.py
  （离线跑一遍首页/分类/详情/播放/搜索，并逐台逐线校验 play id 能否完整往返）
"""

from __future__ import annotations
import base64
import binascii
import json
import os
import re
import sys
import time

# ── 常量（壳里显示的源名，各别名同值） ─────────────────────────────────
KEY = "cctv"                                                 # meta.key
NAME = "cctv.live"                                           # 壳里显示的源名
SITE_NAME = NAME                                             # 别名：有的壳读 SITE_NAME / siteName / title
siteName = NAME
title = NAME
name = NAME                                                  # 模块级 name：壳若直接读模块属性用的就是它

UPDATED = "2026-11-25 14:55:47"                                  # 数据更新时间
COUNT = 56                                        # 频道数
LINES = 163                                        # 线路总数

PAGE_SIZE = 60                                               # 分类/搜索每页条数（56 台一页装得下）
EPG_URL = "https://epg.112114.xyz/pp.xml"                    # 节目单（壳若支持 EPG 可用）
UA_PC = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
         "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
UA_MOBILE = ("Mozilla/5.0 (Linux; Android 12; SM-G981B) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36")
PLAY_HEADERS = {"User-Agent": UA_PC}                         # 直播源基本都是裸 m3u8，PC UA 通吃
ID_PREFIX = "cv:"                                            # play id 前缀
DEBUG = os.environ.get("CV_DEBUG") == "1"                    # CV_DEBUG=1 才写 stderr

DETAIL_TTL = 600                                             # 详情缓存 10 分钟（数据静态，长一点无妨）
PLAY_TTL = 120                                               # 播放地址缓存 2 分钟

# 分类：type_id -> 显示名。tid 空 / "all" 时返回全部
GROUPS = [("all", "全部"), ("cctv", "央视"), ("weishi", "卫视"), ("tese", "特色")]
GROUP_NAME = dict(GROUPS)

LINE_PREFIX = "线路"                                          # 详情里线路名的前缀

# ── 频道表（id / 名称 / 分类 / 台标 / 线路[url, src, score]） ───────────
CHANNELS = [
    {
        "id": "cctv1",
        "name": "CCTV-1 综合",
        "group": "央视",
        "logo": "https://i.imgur.com/TpA3cUl.png",
        "lines": [
            {
                "url": "http://69.30.245.50/live/cctv1.m3u8",
                "src": "iptvorg",
                "score": 48
            },
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv1hd",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV1",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv2",
        "name": "CCTV-2 财经",
        "group": "央视",
        "logo": "https://i.imgur.com/ILamhwU.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv2hd.m3u8",
                "src": "iptvorg",
                "score": 33
            },
            {
                "url": "http://204.12.221.218:8181/3m1080p/cctv2.m3u8",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV2",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv3",
        "name": "CCTV-3 综艺",
        "group": "央视",
        "logo": "https://i.imgur.com/iFlkIuw.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv3hd.m3u8",
                "src": "iptvorg",
                "score": 33
            },
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv3hd",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV3",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv4",
        "name": "CCTV-4 中文国际",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv4hd.m3u8",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "https://raw.githubusercontent.com/ChiSheng9/iptv/master/TV20.m3u8",
                "src": "bbg",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV4",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv5",
        "name": "CCTV-5 体育",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "https://zby.130519.xyz/PLTV/11/224/3221225734/index.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV5",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001187/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "cctv5p",
        "name": "CCTV-5+ 体育赛事",
        "group": "央视",
        "logo": "https://i.imgur.com/OK8mdJV.png",
        "lines": [
            {
                "url": "https://php.jdshipin.com/TVOD/iptv.php?id=cctv5p",
                "src": "iptvorg",
                "score": 50
            },
            {
                "url": "https://myip.pdtvhd.com/Sports/streams/CCTV5pul.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV5p",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv6",
        "name": "CCTV-6 电影",
        "group": "央视",
        "logo": "https://i.imgur.com/rFiaef7.png",
        "lines": [
            {
                "url": "http://69.30.245.50/live/cctv6.m3u8",
                "src": "iptvorg",
                "score": 48
            },
            {
                "url": "http://198.204.240.250:82/live/cctv6.m3u8",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV6",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv7",
        "name": "CCTV-7 国防军事",
        "group": "央视",
        "logo": "https://i.imgur.com/CKcPMQC.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv7hd.m3u8",
                "src": "iptvorg",
                "score": 33
            },
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv7hd",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV7",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv8",
        "name": "CCTV-8 电视剧",
        "group": "央视",
        "logo": "https://i.imgur.com/fxVPMJF.png",
        "lines": [
            {
                "url": "http://192.151.150.154/live/cctv8k.m3u8",
                "src": "iptvorg",
                "score": 48
            },
            {
                "url": "http://bztv.tvbus.cc:8081/cdnlive/cctv8.m3u8",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV8",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv9",
        "name": "CCTV-9 纪录",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv9hd",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV9",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001237/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "cctv10",
        "name": "CCTV-10 科教",
        "group": "央视",
        "logo": "https://i.imgur.com/sSSO7UD.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv10hd.m3u8",
                "src": "iptvorg",
                "score": 33
            },
            {
                "url": "http://38.75.136.137:98/gslb/dsdqbv/cctv10hd.m3u8?auth=test20251009",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV10",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv11",
        "name": "CCTV-11 戏曲",
        "group": "央视",
        "logo": "https://i.imgur.com/CjOWx7L.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv11hd.m3u8",
                "src": "iptvorg",
                "score": 33
            },
            {
                "url": "http://38.75.136.137:98/gslb/dsdqbv/cctv11hd.m3u8?auth=test20251009",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV11",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv12",
        "name": "CCTV-12 社会与法",
        "group": "央视",
        "logo": "https://i.imgur.com/3yTuiOM.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv12hd.m3u8",
                "src": "iptvorg",
                "score": 33
            },
            {
                "url": "http://107.150.60.122/live/cctv12hd.m3u8",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV12",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv13",
        "name": "CCTV-13 新闻",
        "group": "央视",
        "logo": "https://i.imgur.com/6MTar6J.png",
        "lines": [
            {
                "url": "http://go.bkpcp.top/mg/cctv13",
                "src": "iptvorg",
                "score": 48
            },
            {
                "url": "http://38.75.136.137:98/gslb/dsdqbv/cctv13hd.m3u8?auth=test20251009",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV13",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv14",
        "name": "CCTV-14 少儿",
        "group": "央视",
        "logo": "https://i.imgur.com/c5SXW7i.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv14hd.m3u8",
                "src": "iptvorg",
                "score": 48
            },
            {
                "url": "http://198.204.228.26/live/cctv14hd.m3u8",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV14",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv15",
        "name": "CCTV-15 音乐",
        "group": "央视",
        "logo": "https://i.imgur.com/CCV0eRG.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv15hd.m3u8",
                "src": "iptvorg",
                "score": 33
            },
            {
                "url": "https://zby.130519.xyz/PLTV/11/224/3221226147/index.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV15",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv16",
        "name": "CCTV-16 奥林匹克",
        "group": "央视",
        "logo": "https://i.imgur.com/ZzV6JQp.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv16hd.m3u8",
                "src": "iptvorg",
                "score": 48
            },
            {
                "url": "https://zby.130519.xyz/PLTV/11/224/3221226120/index.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV16",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv17",
        "name": "CCTV-17 农业农村",
        "group": "央视",
        "logo": "https://i.imgur.com/jSQURxS.png",
        "lines": [
            {
                "url": "http://74.91.26.218:82/live/cctv17hd.m3u8",
                "src": "iptvorg",
                "score": 48
            },
            {
                "url": "https://live.264788.xyz/channel/cctv17?streamid=348c8c0c04a6d2b900e5a3bcb4af8ce1&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV17",
                "src": "aptv",
                "score": 18
            }
        ]
    },
    {
        "id": "cctv4k",
        "name": "CCTV-4K 超高清",
        "group": "央视",
        "logo": "https://i.imgur.com/fxusYlX.png",
        "lines": [
            {
                "url": "http://198.204.240.250:82/live/cctv4k.m3u8",
                "src": "iptvorg",
                "score": 53
            },
            {
                "url": "http://113.117.74.17:8081/hls/144/index.m3u8",
                "src": "bbg",
                "score": 25
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=CCTV4K",
                "src": "aptv",
                "score": 23
            }
        ]
    },
    {
        "id": "cctvhhjc",
        "name": "CCTV怀旧剧场",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "https://live.264788.xyz/channel/huaijiujuchang?streamid=7e5d1abdddde08f588234f3f640f75ff&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://[2409:8087:7001:20:2::3]:80/dbiptv.sn.chinamobile.com/PLTV/88888893/224/3221226972/index.m3u8",
                "src": "bbg",
                "score": 14
            },
            {
                "url": "https://hls-gateway.vpstv.net/streams/708853.m3u8",
                "src": "guovin",
                "score": 24
            }
        ]
    },
    {
        "id": "cctvdiyi",
        "name": "CCTV第一剧场",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "https://live.264788.xyz/channel/diyijuchang?streamid=e9b0fb1ca135a4aeae12944494883794&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "https://live.264788.xyz/channel/diyijuchang?streamid=d81e188b59ece96b7e8f1ce34aea3ef8&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "zbds",
                "score": 16
            },
            {
                "url": "http://[2409:8087:7001:20:2::3]:80/dbiptv.sn.chinamobile.com/PLTV/88888893/224/3221226959/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "cctvfyyy",
        "name": "CCTV风云音乐",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "https://live.264788.xyz/channel/fengyunyinyue?streamid=be37d16b874e7ba11dd383d7ecd75752&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "https://live.264788.xyz/channel/fengyunyinyue?streamid=1b41fb9153cba3ee19bd5d1b323da27e&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "zbds",
                "score": 16
            },
            {
                "url": "http://[2409:8087:7001:20:2::3]:80/dbiptv.sn.chinamobile.com/PLTV/88888893/224/3221226953/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "cctvfyzq",
        "name": "CCTV风云足球",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "https://hls-gateway.vpstv.net/streams/708859.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://[2409:8087:7001:20:2::3]:80/dbiptv.sn.chinamobile.com/PLTV/88888893/224/3221226984/index.m3u8",
                "src": "bbg",
                "score": 14
            },
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=fyzq",
                "src": "guovin",
                "score": 22
            }
        ]
    },
    {
        "id": "cctvfyjc",
        "name": "CCTV风云剧场",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "https://live.264788.xyz/channel/fengyunjuchang?streamid=31e7b5b7032d25dd215a4069cdee1a48&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://[2409:8087:7001:20:2::3]:80/dbiptv.sn.chinamobile.com/PLTV/88888893/224/3221226950/index.m3u8",
                "src": "bbg",
                "score": 14
            },
            {
                "url": "https://hls-gateway.vpstv.net/streams/708861.m3u8",
                "src": "guovin",
                "score": 24
            }
        ]
    },
    {
        "id": "cctvwhjp",
        "name": "CCTV文化精品",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "https://live.264788.xyz/channel/yangshiwenhuajingpin?streamid=bc185d1ef1e528922e83efd845006277&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://[2409:8087:7001:20:2::3]:80/dbiptv.sn.chinamobile.com/PLTV/88888893/224/3221226981/index.m3u8",
                "src": "bbg",
                "score": 14
            },
            {
                "url": "https://hls-gateway.vpstv.net/streams/708832.m3u8",
                "src": "guovin",
                "score": 24
            }
        ]
    },
    {
        "id": "cctvnxjs",
        "name": "CCTV女性时尚",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "http://38.75.136.137:98/gslb/dsdqpub/nxss.m3u8?auth=testpub",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://[2409:8087:7001:20:2::3]:80/dbiptv.sn.chinamobile.com/PLTV/88888893/224/3221226969/index.m3u8",
                "src": "bbg",
                "score": 14
            },
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=nxss",
                "src": "guovin",
                "score": 22
            }
        ]
    },
    {
        "id": "cgtn",
        "name": "CGTN 英语",
        "group": "央视",
        "logo": "https://live.fanmingming.com/tv/CGTNDoc.png",
        "lines": [
            {
                "url": "https://livedoc.cgtn.com/500d/prog_index.m3u8",
                "src": "bbg",
                "score": 22
            },
            {
                "url": "https://english-livebkali.cgtn.com/live/encgtn_0.m3u8",
                "src": "aptv",
                "score": 20
            },
            {
                "url": "https://0472.org/hls/cgtn.m3u8",
                "src": "zbds",
                "score": 16
            }
        ]
    },
    {
        "id": "cgtnfr",
        "name": "CGTN 法语",
        "group": "央视",
        "logo": "https://live.fanmingming.com/tv/CGTN法语.png",
        "lines": [
            {
                "url": "https://livefr.cgtn.com/1000f/prog_index.m3u8",
                "src": "bbg",
                "score": 22
            },
            {
                "url": "https://0472.org/hls/cgtnf.m3u8",
                "src": "aptv",
                "score": 20
            },
            {
                "url": "http://espanol-liveali.cgtn.com/hls/LSveOGBaBw41Ea7ukkVAUdKQ220802LSTexu6xAuFH8VZNBLE1ZNEa220802cd.m3u8",
                "src": "zbds",
                "score": 14
            }
        ]
    },
    {
        "id": "cgtnes",
        "name": "CGTN 西语",
        "group": "央视",
        "logo": "https://live.fanmingming.com/tv/CGTN西语.png",
        "lines": [
            {
                "url": "https://livees.cgtn.com/1000e/prog_index.m3u8",
                "src": "bbg",
                "score": 22
            },
            {
                "url": "https://0472.org/hls/cgtnx.m3u8",
                "src": "aptv",
                "score": 20
            }
        ]
    },
    {
        "id": "cgtnar",
        "name": "CGTN 阿语",
        "group": "央视",
        "logo": "https://live.fanmingming.com/tv/CGTN阿语.png",
        "lines": [
            {
                "url": "https://livear.cgtn.com/1000a/prog_index.m3u8",
                "src": "bbg",
                "score": 22
            },
            {
                "url": "https://0472.org/hls/cgtna.m3u8",
                "src": "aptv",
                "score": 20
            }
        ]
    },
    {
        "id": "cgtnru",
        "name": "CGTN 俄语",
        "group": "央视",
        "logo": "https://live.fanmingming.com/tv/CGTN俄语.png",
        "lines": [
            {
                "url": "https://liveru.cgtn.com/1000r/prog_index.m3u8",
                "src": "bbg",
                "score": 22
            },
            {
                "url": "https://0472.org/hls/cgtne.m3u8",
                "src": "aptv",
                "score": 20
            }
        ]
    },
    {
        "id": "cgtndoc",
        "name": "CGTN 纪录",
        "group": "央视",
        "logo": "",
        "lines": [
            {
                "url": "https://english-livebkali.cgtn.com/live/doccgtn_0.m3u8",
                "src": "aptv",
                "score": 20
            },
            {
                "url": "https://0472.org/hls/cgtnd.m3u8",
                "src": "zbds",
                "score": 16
            },
            {
                "url": "https://english-livetx.cgtn.com/hls/yypdjlctzb_hd.m3u8",
                "src": "zbds",
                "score": 16
            }
        ]
    },
    {
        "id": "hunan",
        "name": "湖南卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://txmov2.a.kwimgs.com/bs3/video-hls/5199687338554291078_hlsb.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=湖南卫视4K",
                "src": "aptv",
                "score": 23
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001026/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "zhejiang",
        "name": "浙江卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://ali-m-l.cztv.com/channels/lantian/channel001/1080p.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=浙江卫视4K",
                "src": "aptv",
                "score": 23
            },
            {
                "url": "https://ali-m-l.cztv.com/channels/lantian/channel001/1080p.m3u8?",
                "src": "zbds",
                "score": 16
            }
        ]
    },
    {
        "id": "jiangsu",
        "name": "江苏卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "http://101.35.240.114:88/live.php?id=江苏卫视4K",
                "src": "aptv",
                "score": 23
            },
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=jswshd",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001033/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "dongfang",
        "name": "东方卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://txmov2.a.kwimgs.com/bs3/video-hls/5219953535631090825_hlsb.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=东方卫视4K",
                "src": "aptv",
                "score": 23
            },
            {
                "url": "https://bp-resource-dfl.bestv.cn/148/3/video.m3u8",
                "src": "zbds",
                "score": 21
            }
        ]
    },
    {
        "id": "beijing",
        "name": "北京卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "http://101.35.240.114:88/live.php?id=北京卫视",
                "src": "aptv",
                "score": 23
            },
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=bjwshd",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001029/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "shenzhen",
        "name": "深圳卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://zby.130519.xyz/PLTV/11/224/3221225728/index.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=深圳卫视4K",
                "src": "aptv",
                "score": 23
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001030/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "guangdong",
        "name": "广东卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://txmov2.a.kwimgs.com/upic/2023/01/26/09/BMjAyMzAxMjYwOTE3NDVfNzM5MzQzNzIyXzk0NjI1OTUwNTA3XzBfMw==_b_B81ddda927d33445d544befd008e60109.mp4",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=广东卫视4K",
                "src": "aptv",
                "score": 23
            },
            {
                "url": "http://113.117.74.17:8081/hls/140/index.m3u8",
                "src": "bbg",
                "score": 20
            }
        ]
    },
    {
        "id": "anhui",
        "name": "安徽卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "http://107.150.60.122/live/ahwshd.m3u8",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=安徽卫视",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001037/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "shandong",
        "name": "山东卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "http://101.35.240.114:88/live.php?id=山东卫视4K",
                "src": "aptv",
                "score": 23
            },
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=sdwshd",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001028/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "tianjin",
        "name": "天津卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://zby.130519.xyz/PLTV/11/224/3221225742/index.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=天津卫视",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001036/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "hubei",
        "name": "湖北卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://zby.130519.xyz/PLTV/11/224/3221225729/index.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=湖北卫视",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001027/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "henan",
        "name": "河南卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "http://107.150.60.122/live/hawshd.m3u8",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=河南卫视",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001222/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "hebei",
        "name": "河北卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://event.pull.hebtv.com/live/live101.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=河北卫视",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001229/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "sichuan",
        "name": "四川卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://live.264788.xyz/channel/sichuanweishi4k?streamid=21be5901ee81559c827dc84e46f26452&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=四川卫视4K",
                "src": "aptv",
                "score": 23
            },
            {
                "url": "https://live.264788.xyz/channel/sichuanweishi4k?streamid=401bf692a1a8b91298f26077d53316d6&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "zbds",
                "score": 16
            }
        ]
    },
    {
        "id": "chongqing",
        "name": "重庆卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://zby.130519.xyz/PLTV/11/224/3221226171/index.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=重庆卫视",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001129/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "liaoning",
        "name": "辽宁卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=lnwshd",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=辽宁卫视",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001035/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "jiangxi",
        "name": "江西卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "https://live.264788.xyz/channel/jiangxiweishi?streamid=555198f31caa33506ac6abb70d788959&livekey=01WgOR41rriMmMkzNsd0UoaxJRwetZdxIvtVk",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=江西卫视",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001034/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "fujian",
        "name": "东南卫视",
        "group": "卫视",
        "logo": "",
        "lines": [
            {
                "url": "http://63.141.230.178:82/gslb/zbdq5.m3u8?id=dnwshd",
                "src": "guovin",
                "score": 22
            },
            {
                "url": "http://101.35.240.114:88/live.php?id=东南卫视",
                "src": "aptv",
                "score": 18
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001201/index.m3u8",
                "src": "bbg",
                "score": 14
            }
        ]
    },
    {
        "id": "kaku",
        "name": "卡酷少儿",
        "group": "特色",
        "logo": "",
        "lines": [
            {
                "url": "https://zby.130519.xyz/PLTV/11/224/3221226019/index.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001245/index.m3u8",
                "src": "bbg",
                "score": 14
            },
            {
                "url": "https://migu.188766.xyz/?migutoken=1023983db6b5249e61d4950c1654cd84&id=%E5%8C%97%E4%BA%AC%E5%8D%A1%E9%85%B7%E5%B0%91%E5%84%BF&type=yy",
                "src": "guovin",
                "score": 24
            }
        ]
    },
    {
        "id": "jinyingjishi",
        "name": "金鹰纪实",
        "group": "特色",
        "logo": "",
        "lines": [
            {
                "url": "https://hls-gateway.vpstv.net/streams/708834.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001230/index.m3u8",
                "src": "bbg",
                "score": 14
            },
            {
                "url": "https://stream1.freetv.fun/jin-ying-ji-shi-35.m3u8",
                "src": "guovin",
                "score": 24
            }
        ]
    },
    {
        "id": "jinyingkatong",
        "name": "金鹰卡通",
        "group": "特色",
        "logo": "",
        "lines": [
            {
                "url": "https://zby.130519.xyz/PLTV/11/224/3221226094/index.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://223.151.51.27:85/tsfile/live/1016_1.m3u8?key=txiptv&playlive=1&authid=0",
                "src": "bbg",
                "score": 20
            },
            {
                "url": "https://stream1.freetv.fun/jin-ying-qia-tong-22.m3u8",
                "src": "guovin",
                "score": 24
            }
        ]
    },
    {
        "id": "jishiwh",
        "name": "纪实人文",
        "group": "特色",
        "logo": "",
        "lines": [
            {
                "url": "https://stream1.freetv.fun/ipv6-ji-shi-ren-wen-12.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "http://[2409:8087:1e03:21::2]:6060/cms001/ch00000090990000001019/index.m3u8",
                "src": "bbg",
                "score": 14
            },
            {
                "url": "http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225738/index.m3u8",
                "src": "guovin",
                "score": 22
            }
        ]
    },
    {
        "id": "xingkong",
        "name": "星空卫视",
        "group": "特色",
        "logo": "",
        "lines": [
            {
                "url": "https://stream1.freetv.fun/xing-kong-wei-shi-12.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "https://stream1.freetv.fun/xing-kong-wei-shi-4.ctv",
                "src": "guovin",
                "score": 24
            }
        ]
    },
    {
        "id": "youman",
        "name": "优漫卡通",
        "group": "特色",
        "logo": "",
        "lines": [
            {
                "url": "https://stream1.freetv.fun/you-man-qia-tong-11.m3u8",
                "src": "guovin",
                "score": 24
            },
            {
                "url": "https://www.freetv.top/migu/626064703.m3u8?migutoken=7f7c4b909389a0cd5172701768041a0f3887534c4534a68bf1dc85550389e9ab156655484be16e89604513fde9da2f036ebae28d31515b0be32eb12462f5de9d9cab8f00c44671241d5c6e1356",
                "src": "guovin",
                "score": 24
            }
        ]
    }
]

# 按 id 建索引，detail/search 走 O(1)
_INDEX = {}
for _c in CHANNELS:
    _INDEX[_c["id"]] = _c


# ── 小工具 ────────────────────────────────────────────────────────────
def _s(v):
    """等价 JS fs()：None/'' → ''，其余转字符串并去首尾空白。"""
    return "" if v is None else str(v).strip()


def _log(msg):
    """唯一日志出口：只有 CV_DEBUG=1 时才写 stderr。"""
    if DEBUG:
        try:
            sys.stderr.write("[cctv.live] %s\n" % (msg,))
        except Exception:
            pass


def _page(v):
    """等价 JS Mct()：取开头整数，非正数回落 1。"""
    m = re.match(r"\s*[+-]?\d+", "" if v is None else str(v))
    n = int(m.group(0)) if m else 0
    return n if n > 0 else 1


def _alist(v):
    return v if isinstance(v, list) else []


def _obj(v):
    """等价 JS Ej()：dict 原样；字符串尝试 JSON；其余给 {}。"""
    if isinstance(v, dict):
        return v
    if isinstance(v, (bytes, bytearray)):
        return {}
    try:
        o = json.loads(str(v or ""))
        return o if isinstance(o, dict) else {}
    except Exception:
        return {}


def _b64(v):
    """等价 JS Qbe()：严格 base64 校验后解码，失败 None。"""
    s = re.sub(r"\s+", "", _s(v))
    if not s or not re.match(r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$", s):
        return None
    try:
        return base64.b64decode(s)
    except (binascii.Error, ValueError):
        return None


def _b64url_decode(v):
    s = _s(v)
    pad = len(s) % 4
    if pad:
        s += "=" * (4 - pad)
    return base64.urlsafe_b64decode(s.encode("utf-8"))


def _b64url_encode(b):
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")


def _valid_url(t):
    """只认 http/https 且带主机名的地址；空、相对路径、magnet 一律 False。"""
    u = _s(t)
    if not u or len(u) > 4096 or re.search(r"[\s\"'<>]", u):
        return False
    return bool(re.match(r"^(?:https?)://[^/?#]+", u, re.I))


def _is_stream(t):
    """直播流后缀判定（m3u8/m3u/ts/flv/mp4），不含 query 部分。"""
    p = _s(t).split("?")[0].split("#")[0].lower()
    return any(p.endswith(x) for x in (".m3u8", ".m3u", ".ts", ".flv", ".mp4"))


def _is_ipv6(t):
    """地址里出现 [xxxx:xxxx::] 字面量视为 IPv6 源（不少壳播不了，排序时已扣分）。"""
    return bool(re.match(r"^https?://\[[0-9a-fA-F:]+\]", _s(t)))


def _clean_headers(h):
    """请求头白名单：只留字符串、无换行、非 hop-by-hop。"""
    out = {}
    for k, v in (_obj(h) or {}).items():
        if not isinstance(k, str) or not re.match(r"^[\w-]+$", k):
            continue
        if re.match(r"^(host|content-length|connection)$", k, re.I):
            continue
        if not isinstance(v, str) or re.search(r"[\r\n]", v):
            continue
        out[k] = v
    return out


def _lines_result(resp, page, limit=PAGE_SIZE):
    """补齐 page / pagecount / limit / total —— 壳对这五项是硬要求，缺任一可能整页空白。"""
    r = dict(resp or {})
    n = _alist(r.get("list"))
    i = _page(r.get("page", page))
    try:
        s = int(r.get("limit"))
    except (TypeError, ValueError):
        s = 0
    a = s if s > 0 else (limit if limit > 0 else PAGE_SIZE)
    try:
        o = int(r.get("pagecount"))
    except (TypeError, ValueError):
        o = 0
    c = o > 0
    u = o if c else i + (1 if len(n) >= a else 0)
    x = r.get("total")
    try:
        l = int(x) if x is not None else -1
    except (TypeError, ValueError):
        l = -1
    d = x is not None and l >= 0
    f = l if (c and d) else (i - 1) * a + len(n) + (1 if u > i else 0)
    return {"page": i, "pagecount": u, "limit": a, "total": f, "list": n}


def _filters_in(body):
    """壳传来的筛选参数 filters / extend / ext / filter 都认。"""
    b = body or {}
    r = b.get("filters", b.get("extend", b.get("ext", b.get("filter", {}))))
    if isinstance(r, str):
        return _obj(r)
    return r if isinstance(r, dict) else {}


def _norm_group(tid):
    """分类 tid 归一：空 / all / 全选 → ''，表示不限分类。"""
    t = _s(tid).lower()
    return "" if t in ("", "all", "全部") else t


def _quality_tag(url):
    """从 url 里猜清晰度标签，给线路名加个尾巴，方便肉眼挑线。"""
    t = _s(url).lower()
    if re.search(r"4k|2160", t):
        return "4K"
    if re.search(r"1080|fhd|fullhd", t):
        return "1080P"
    if re.search(r"720", t):
        return "720P"
    if re.search(r"hd", t):
        return "HD"
    return ""


def _pack_line(label, url, header=None):
    """把一条线路打包成 play id：`名称$cv:base64url({"url":..,"header":..})`。"""
    u = _s(url)
    if not _valid_url(u):
        return ""
    hdr = _clean_headers(header) or dict(PLAY_HEADERS)
    raw = json.dumps({"url": u, "header": hdr}, ensure_ascii=False,
                     separators=(",", ":")).encode("utf-8")
    nm = re.sub(r"[$#]", " ", _s(label)) or LINE_PREFIX
    return "%s$%s%s" % (nm, ID_PREFIX, _b64url_encode(raw))


def _unpack_line(vid):
    """反向解 play id，拿到 {url, header}；坏数据返回 None。"""
    p = _s(vid)
    pos = p.rfind("$" + ID_PREFIX)
    if pos < 0:
        if p.startswith(ID_PREFIX):
            pos = -1
        else:
            return None
    body = p[pos + 1 + len(ID_PREFIX):]
    if not body or len(body) > 65536:
        return None
    try:
        o = json.loads(_b64url_decode(body).decode("utf-8", "ignore"))
    except Exception:
        return None
    if not isinstance(o, dict) or not _valid_url(o.get("url")):
        return None
    return {"url": _s(o.get("url")), "header": _clean_headers(o.get("header"))}


def _vod_of(c):
    """频道 → 列表项（56 条主条目就是这么来的，一站一条）。"""
    lines = _alist(c.get("lines"))
    return {
        "vod_id": _s(c.get("id")),
        "vod_name": _s(c.get("name")),
        "vod_pic": _s(c.get("logo")),
        "vod_remarks": "%d 线路" % len(lines),
        "vod_area": _s(c.get("group")),
        "vod_year": "",
        "type_name": _s(c.get("group")),
    }


# ── 站点主体 ──────────────────────────────────────────────────────────
class _CctvSpider(object):

    key = KEY
    name = NAME
    title = NAME
    siteName = NAME
    site_name = NAME

    def __init__(self):
        self.name = NAME
        self.title = NAME
        self.siteName = NAME
        self.extend = ""
        self.channels = CHANNELS
        self.groups = list(GROUPS)
        self._detail_cache = {}
        self._play_cache = {}

    def init(self, extend=""):
        self.name = NAME          # 源名：cctv.live（别名一起写，防止壳读别的字段）
        self.title = NAME
        self.siteName = NAME
        self.extend = extend or ""
        self._detail_cache.clear()
        self._play_cache.clear()
        return None

    def getName(self):
        return self.name

    def getTitle(self):
        return self.title

    def getSiteName(self):
        return self.name

    # 首页：只给分类，列表留空（列表由 categoryContent 出，避免壳首屏灌 56 条）
    def homeContent(self, filter=False):
        classes = [{"type_id": tid, "type_name": nm} for tid, nm in self.groups]
        return {"class": classes, "filters": {}, "list": []}

    # 首页推荐位：按要求留空
    def homeVideoContent(self):
        return {"list": []}

    # 分类：一站一条，翻页按 PAGE_SIZE 切
    def categoryContent(self, tid, pg, filter, extend):
        page = _page(pg)
        want = _norm_group(tid)
        try:
            pool = [c for c in self.channels
                    if not want or _s(c.get("group")) == GROUP_NAME.get(want, want)]
            total = len(pool)
            start = (page - 1) * PAGE_SIZE
            part = pool[start:start + PAGE_SIZE]
            lst = [_vod_of(c) for c in part]
            count = (total + PAGE_SIZE - 1) // PAGE_SIZE if total else 1
            return _lines_result({"page": page, "pagecount": max(count, 1),
                                  "limit": PAGE_SIZE, "total": total, "list": lst}, page)
        except Exception as exc:
            _log("categoryContent %s p%s 失败: %r" % (tid, page, exc))
            return _lines_result({"list": []}, page)

    # 详情：把该台全部备用线路展开成多条「线路」，按分数排序
    def detailContent(self, ids):
        if isinstance(ids, (list, tuple)):
            src = list(ids)
        else:
            src = _s(ids).split(",")
        out = []
        for h in src:
            vid = _s(h)
            if not vid:
                continue
            item = self._detail(vid)
            if item:
                out.append(item)
        return {"list": out}

    def _detail(self, vid):
        now = time.time()
        hit = self._detail_cache.get(vid)
        if hit and hit["expires"] > now:
            return hit["value"]
        c = _INDEX.get(vid)
        if not c:
            low = vid.lower()      # 兜底：id 大小写差异
            c = next((x for x in self.channels if _s(x.get("id")).lower() == low), None)
        if not c:
            _log("detailContent %s 未找到" % (vid,))
            return None
        lines = sorted(_alist(c.get("lines")),
                       key=lambda x: int(x.get("score") or 0), reverse=True)
        names, urls = [], []
        for i, ln in enumerate(lines):
            u = _s(ln.get("url"))
            if not _valid_url(u):
                continue
            src = _s(ln.get("src")) or "src"
            tag = _quality_tag(u)
            label = "%s%d·%s%s" % (LINE_PREFIX, i + 1, src, (" " + tag) if tag else "")
            packed = _pack_line(label, u, PLAY_HEADERS)
            if not packed:
                continue
            names.append(label)
            urls.append(packed)
        if not urls:
            _log("detailContent %s 无可用线路" % (vid,))
            return None
        item = {
            "vod_id": _s(c.get("id")),
            "vod_name": _s(c.get("name")),
            "vod_pic": _s(c.get("logo")),
            "vod_area": _s(c.get("group")),
            "vod_remarks": "%d 线路" % len(urls),
            "vod_content": "%s —— %s 频道，共 %d 条备用线路（按质量排序，第一条最优）。\n"
                           "数据更新：%s\n来源：guovin / BigBigGrandG / aptv / vbskycn / ZBDS / iptv-org"
                           % (_s(c.get("name")), _s(c.get("group")), len(urls), UPDATED),
            "vod_play_from": "$$$".join(names),
            "vod_play_url": "$$$".join(urls),
            "vod_duration": "",
            "type_name": _s(c.get("group")),
        }
        if len(self._detail_cache) >= 200:
            self._detail_cache.pop(next(iter(self._detail_cache)))
        self._detail_cache[vid] = {"expires": now + DETAIL_TTL, "value": item}
        return item

    # 搜索：频道名 / id / 分类名三向模糊匹配
    def searchContent(self, key, quick, pg="1"):
        page = _page(pg)
        wd = _s(key).lower().replace(" ", "")
        if not wd:
            return _lines_result({"list": []}, page)
        hit = []
        for c in self.channels:
            nm = _s(c.get("name")).lower()
            cid = _s(c.get("id")).lower()
            grp = _s(c.get("group")).lower()
            if wd in nm or wd in cid or wd in grp or \
               nm.replace("-", "").replace(" ", "") in wd:
                hit.append(_vod_of(c))
        total = len(hit)
        start = (page - 1) * PAGE_SIZE
        part = hit[start:start + PAGE_SIZE]
        count = (total + PAGE_SIZE - 1) // PAGE_SIZE if total else 1
        return _lines_result({"page": page, "pagecount": max(count, 1),
                              "limit": PAGE_SIZE, "total": total, "list": part}, page)

    # 播放：解 play id → 真链，parse 恒 0（直播直链不走解析器）
    def playerContent(self, flag, vid, vipFlags=None):
        out = {"parse": 0, "url": "", "header": dict(PLAY_HEADERS), "jx": 0}
        p = _s(vid)
        # 兼容壳直接塞裸地址（有些壳会把上次的 url 原样回传）
        if not p.startswith(ID_PREFIX) and _valid_url(p):
            u, hdr = p, dict(PLAY_HEADERS)
            now = time.time()
            hit = self._play_cache.get(u)
            if hit and hit["expires"] > now:
                hdr = dict(hit["header"])
            else:
                if len(self._play_cache) >= 200:
                    self._play_cache.pop(next(iter(self._play_cache)))
                self._play_cache[u] = {"expires": now + PLAY_TTL, "header": dict(hdr)}
            return {"parse": 0, "url": u, "header": hdr, "jx": 0}
        got = _unpack_line(p)
        if not got:
            _log("playerContent 无法解析 play id")
            return out
        u = got["url"]
        hdr = dict(PLAY_HEADERS)
        hdr.update(got["header"])
        ck = json.dumps([u, hdr], sort_keys=True, ensure_ascii=False)
        now = time.time()
        hit = self._play_cache.get(ck)
        if hit and hit["expires"] > now:
            return {"parse": 0, "url": u, "header": dict(hit["header"]), "jx": 0}
        if len(self._play_cache) >= 200:
            self._play_cache.pop(next(iter(self._play_cache)))
        self._play_cache[ck] = {"expires": now + PLAY_TTL, "header": dict(hdr)}
        return {"parse": 0, "url": u, "header": hdr, "jx": 0}


# ── 壳入口：TVBox / FongMi 只认 Spider 这一个类名 ─────────────────────
try:
    from base.spider import Spider as _BaseSpider
except Exception:
    try:
        sys.path.append("..")
        from base.spider import Spider as _BaseSpider
    except Exception:
        class _BaseSpider(object):
            pass


class Spider(_BaseSpider):
    """壳里只认这一个入口类：源名 cctv.live。"""

    key = KEY
    name = NAME
    title = NAME
    siteName = NAME
    site_name = NAME

    def __init__(self):
        self.name = NAME
        self.title = NAME
        self.siteName = NAME
        self.extend = ""
        self._core = _CctvSpider()
        self.channels = self._core.channels
        self.groups = self._core.groups

    # ── 生命周期 ─────────────────────────────────────────────
    def init(self, extend=""):
        self.name = NAME
        self.title = NAME
        self.siteName = NAME
        self.extend = extend or ""
        try:
            self._core.init(extend)
        except Exception as exc:
            _log("init 失败: %r" % (exc,))
        return None

    def getName(self):
        return self.name

    def getTitle(self):
        return self.title

    def getSiteName(self):
        return self.name

    def destroy(self):
        try:
            self._core._detail_cache.clear()
            self._core._play_cache.clear()
        except Exception:
            pass

    def isVideoFormat(self, url):
        return _is_stream(url)

    def manualVideoCheck(self):
        return False

    def getDependence(self):
        return []

    def getEpg(self):
        return EPG_URL

    # ── 四个主入口（全部异常兜底，出错只给空，不炸壳） ─────────
    def homeContent(self, filter=False):
        try:
            return self._core.homeContent(filter)
        except Exception as exc:
            _log("homeContent 失败: %r" % (exc,))
            return {"class": [{"type_id": t, "type_name": n} for t, n in GROUPS],
                    "filters": {}, "list": []}

    def homeVideoContent(self):
        return {"list": []}

    def categoryContent(self, tid, pg="1", filter=False, extend=None):
        try:
            return self._core.categoryContent(tid, pg, filter, extend)
        except Exception as exc:
            _log("categoryContent %s 失败: %r" % (tid, exc))
            return _lines_result({"list": []}, _page(pg))

    def detailContent(self, ids):
        try:
            return self._core.detailContent(ids)
        except Exception as exc:
            _log("detailContent %s 失败: %r" % (ids, exc))
            return {"list": []}

    def searchContent(self, key, quick=False, pg="1"):
        try:
            return self._core.searchContent(key, quick, pg)
        except Exception as exc:
            _log("searchContent %s 失败: %r" % (key, exc))
            return _lines_result({"list": []}, _page(pg))

    def playerContent(self, flag, vid, vipFlags=None):
        try:
            return self._core.playerContent(flag, vid, vipFlags)
        except Exception as exc:
            _log("playerContent 失败: %r" % (exc,))
            return {"parse": 0, "url": "", "header": dict(PLAY_HEADERS), "jx": 0}

    # 壳若无条件调 localProxy 也不至于抛异常（本源不需要代理）
    def localProxy(self, param):
        return None

    def proxy(self, param):
        return self.localProxy(param)

    # ── 兼容：老式 home/category/detail/play 直调写法 ─────────
    def home(self):
        return self.homeContent(True)

    def category(self, tid, pg=1, filter=None, extend=None):
        return self.categoryContent(tid, pg, filter, extend)

    def detail(self, vid):
        return self.detailContent(vid)

    def play(self, flag, vid):
        return self.playerContent(flag, vid)

    def search(self, wd, quick=False, pg="1"):
        return self.searchContent(wd, quick, pg)


# 模块级函数别名：个别壳不实例化、直接调模块函数
def homeContent(filter=False):
    return Spider().homeContent(filter)


def categoryContent(tid, pg="1", filter=False, extend=None):
    return Spider().categoryContent(tid, pg, filter, extend)


def detailContent(ids):
    return Spider().detailContent(ids)


def searchContent(key, quick=False, pg="1"):
    return Spider().searchContent(key, quick, pg)


def playerContent(flag, vid, vipFlags=None):
    return Spider().playerContent(flag, vid, vipFlags)


# ── 自测：python3 cctv.py（离线，逐台逐线校验 play id 往返） ───────────
if __name__ == "__main__":
    sp = Spider()
    sp.init()
    print("源名:", sp.getName(), "| 更新:", UPDATED, "| 频道:", len(sp.channels),
          "| 线路:", sum(len(x["lines"]) for x in sp.channels))

    home = sp.homeContent(True)
    print("分类:", " ".join("%s:%s" % (c["type_id"], c["type_name"]) for c in home["class"]))

    for tid, nm in GROUPS:
        cat = sp.categoryContent(tid, 1, True, {})
        print("  %-6s %2d 条（page %s/%s, total %s）"
              % (nm, len(cat["list"]), cat["page"], cat["pagecount"], cat["total"]))
        exp = len(sp.channels) if tid == "all" else \
            sum(1 for c in sp.channels if c["group"] == nm)
        assert len(cat["list"]) == exp, "%s 条数不符：%d != %d" % (tid, len(cat["list"]), exp)

    # 逐台逐线：详情 → play id → 解回 → 原 url 必须一模一样
    bad, nline = [], 0
    for c in sp.channels:
        det = sp.detailContent([c["id"]])["list"]
        if not det:
            bad.append((c["id"], "详情为空"))
            continue
        d = det[0]
        froms = d["vod_play_from"].split("$$$")
        eps = d["vod_play_url"].split("$$$")
        if len(froms) != len(eps):
            bad.append((c["id"], "线路名与线路数不匹配"))
            continue
        for i, ep in enumerate(eps):
            got = _unpack_line(ep)
            if not got:
                bad.append((c["id"], "play id 解不开 #%d" % (i + 1)))
                continue
            nline += 1
            pl = sp.playerContent(froms[i], ep, {})
            if pl.get("url") != got["url"] or pl.get("parse") != 0:
                bad.append((c["id"], "播放返回与原 url 不一致 #%d" % (i + 1)))
    print("线路往返校验:", nline, "条 →", "全部通过" if not bad else "异常 %d 处" % len(bad))
    for x in bad[:10]:
        print("   !", x)

    d = sp.detailContent(["cctv1"])["list"][0]
    print("\n示例详情:", d["vod_name"], "|", d["vod_remarks"])
    print("  线路:", " / ".join(d["vod_play_from"].split("$$$")))
    p = sp.playerContent("", d["vod_play_url"].split("$$$")[0], {})
    print("  播放:", _s(p.get("url"))[:100])

    for kw in ("cctv1", "湖南", "卫视", "cctv5"):
        r = sp.searchContent(kw, False, 1)
        print("搜索「%s」:" % kw, r["total"], "条",
              " / ".join(x["vod_name"] for x in r["list"][:4]))

    print("\n自测", "通过" if not bad else "存在异常，请检查上面带 ! 的行")
    if bad:
        sys.exit(1)          # 有异常就非零退出，脚本/CI 才能感知失败
