# -*- coding: utf-8 -*-
# 央视 / 卫视直播 TVBox、AVBox spider
#
# 设计取向与「橘汁视频」那份一致：
#   1. 纯标准库。只用到 json/re/ssl/urllib，不依赖 requests、pyquery、Crypto。
#      客户端 pip 环境里这些常常没有，模块顶层 import 失败会让整个源在加载阶段就崩，
#      表现是「配置无效」而不是「这个台放不了」。
#   2. init 阶段不联网。频道表内置在文件里，打开即出列表。
#      网络请求全部延迟到真正取数据时，且失败一律回退内置表，不会把源锁死。
#   3. 异常就地吞掉，每个对外方法都兜一层 try。
#      直播源失效是常态，单条线路挂掉不应该让整个分类空白。
#
# 内置 56 个频道、153 条线路，按「主线路 + 备用线路」组织，
# 每个频道在播放器里能看到多条线路可选。
import base64
import json
import re
import ssl
import time
import urllib.request

try:
    from base.spider import Spider as _Base
except Exception:
    class _Base:
        pass

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

# 节目单。客户端若自行配置 EPG，可忽略这一项。
EPG = 'https://epg.zsdc.eu.org/t.xml'

# 在线订阅的缓存时长（秒）。直播源几天就变，缓存太久等于没更新。
CACHE_TTL = 6 * 3600

# ---------------------------------------------------------------- 内置频道表
# 每条：name 频道名 / group 分组 / logo 台标 / urls[0] 主线路，其余为备用。
# 排序规则：广电台 CDN 直连 → 境内运营商 IP → 海外中转。
CHANNELS = [
    {'name': 'CCTV-1 综合', 'id': 'CCTV1', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-1.png',
     'urls': [
         'http://74.91.26.218:82/live/cctv1hd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv1hd',
         'http://38.75.136.137:98/gslb/dsdqbv/cctv1hd.m3u8?auth=test20251009',
     ]},
    {'name': 'CCTV-2 财经', 'id': 'CCTV2', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-2.png',
     'urls': [
         'http://192.151.150.154/live/cctv2hd.m3u8',
         'http://198.204.228.26/live/cctv2hd.m3u8',
         'http://107.150.60.122/live/cctv2hd.m3u8',
     ]},
    {'name': 'CCTV-3 综艺', 'id': 'CCTV3', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-3.png',
     'urls': [
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv3hd',
         'http://107.150.60.122/live/cctv3hd.m3u8',
         'http://74.91.26.218:82/live/cctv3hd.m3u8',
     ]},
    {'name': 'CCTV-4 中文国际', 'id': 'CCTV4', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-4.png',
     'urls': [
         'http://107.150.60.122/live/cctv4hd.m3u8',
         'http://173.208.212.130:8181/1080p/cctv4.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/cctv4k.m3u8?auth=testpub',
     ]},
    {'name': 'CCTV-5 体育', 'id': 'CCTV5', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-5.png',
     'urls': [
         'http://107.150.60.122/live/cctv5hd.m3u8',
     ]},
    {'name': 'CCTV-6 电影', 'id': 'CCTV6', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-6.png',
     'urls': [
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv6hd',
         'http://74.91.26.218:82/live/cctv6hd.m3u8',
     ]},
    {'name': 'CCTV-7 国防军事', 'id': 'CCTV7', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-7.png',
     'urls': [
         'http://107.150.60.122/live/cctv7hd.m3u8',
         'http://74.91.26.218:82/live/cctv7hd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv7hd',
     ]},
    {'name': 'CCTV-8 电视剧', 'id': 'CCTV8', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-8.png',
     'urls': [
         'http://74.91.26.218:82/live/cctv8hd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv8k',
     ]},
    {'name': 'CCTV-9 纪录', 'id': 'CCTV9', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-9.png',
     'urls': [
         'http://107.150.60.122/live/cctv9hd.m3u8',
         'http://74.91.26.218:82/live/cctv9hd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv9hd',
     ]},
    {'name': 'CCTV-10 科教', 'id': 'CCTV10', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-10.png',
     'urls': [
         'http://74.91.26.218:82/live/cctv10hd.m3u8',
         'http://38.75.136.137:98/gslb/dsdqbv/cctv10hd.m3u8?auth=test20251009',
     ]},
    {'name': 'CCTV-11 戏曲', 'id': 'CCTV11', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-11.png',
     'urls': [
         'http://38.75.136.137:98/gslb/dsdqbv/cctv11hd.m3u8?auth=test20251009',
         'http://74.91.26.218:82/live/cctv11hd.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/cctv11hd.m3u8?auth=testpub',
     ]},
    {'name': 'CCTV-12 社会与法', 'id': 'CCTV12', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-12.png',
     'urls': [
         'http://124.165.251.82:85/tsfile/live/0012_1.m3u8?key=txiptv&playlive=1&authid=0',
         'http://38.75.136.137:98/gslb/dsdqbv/cctv12hd.m3u8?auth=test20251009',
         'http://74.91.26.218:82/live/cctv12hd.m3u8',
     ]},
    {'name': 'CCTV-13 新闻', 'id': 'CCTV13', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-13.png',
     'urls': [
         'http://ali-m-l.cztv.com/channels/lantian/channel21/1080p.m3u8',
         'http://120.76.248.139/live/bfgd/4200000067.m3u8',
         'http://38.75.136.137:98/gslb/dsdqbv/cctv13hd.m3u8?auth=test20251009',
     ]},
    {'name': 'CCTV-14 少儿', 'id': 'CCTV14', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-14.png',
     'urls': [
         'http://38.75.136.137:98/gslb/dsdqbv/cctv14hd.m3u8?auth=test20251009',
         'http://74.91.26.218:82/live/cctv14hd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv14hd',
     ]},
    {'name': 'CCTV-15 音乐', 'id': 'CCTV15', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-15.png',
     'urls': [
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv15hd',
         'http://74.91.26.218:82/live/cctv15hd.m3u8',
         'http://38.75.136.137:98/gslb/dsdqbv/cctv15hd.m3u8?auth=test20251009',
     ]},
    {'name': 'CCTV-16 奥林匹克', 'id': 'CCTV16', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-16.png',
     'urls': [
         'http://38.75.136.137:98/gslb/dsdqbv/cctv16hd.m3u8?auth=test20251009',
         'http://74.91.26.218:82/live/cctv16hd.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/cctv16hd.m3u8?auth=testpub',
     ]},
    {'name': 'CCTV-17 农业农村', 'id': 'CCTV17', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-17.png',
     'urls': [
         'http://38.75.136.137:98/gslb/dsdqbv/cctv17hd.m3u8?auth=test20251009',
         'http://74.91.26.218:82/live/cctv17hd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cctv17hd',
     ]},
    {'name': 'CCTV-5+', 'id': 'CCTV5+', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-5%2B.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000246.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/cctv5p.m3u8?auth=testpub',
         'http://223.78.65.165:9901/tsfile/live/0006_1.m3u8?key=txiptv&playlive=1&authid=0',
         'http://38.75.136.137:98/gslb/dsdqbv/cctv5p.m3u8?auth=test20251009',
     ]},
    {'name': 'CCTV-8K', 'id': 'CCTV8K', 'group': '央视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/CCTV-8K.png',
     'urls': [
         'http://192.151.150.154/live/cctv8k.m3u8',
     ]},
    {'name': '北京卫视', 'id': '北京卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%8C%97%E4%BA%AC%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000083.m3u8',
         'http://38.75.136.137:98/gslb/dsdqbv/bjwshd.m3u8?auth=test20251009',
         'http://107.150.60.122/live/bjwshd.m3u8',
     ]},
    {'name': '天津卫视', 'id': '天津卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%A4%A9%E6%B4%A5%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://38.75.136.137:98/gslb/dsdqpub/tjwshd.m3u8?auth=testpub',
         'http://107.150.60.122/live/tjwshd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=tjwshd',
     ]},
    {'name': '河北卫视', 'id': '河北卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%B2%B3%E5%8C%97%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'https://event.pull.hebtv.com/live/live101.m3u8',
         'http://120.76.248.139/live/bfgd/4200000108.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/hewshd.m3u8?auth=testpub',
     ]},
    {'name': '山西卫视', 'id': '山西卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%B1%B1%E8%A5%BF%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://m3u8.channel.wsrtv.com.cn/cms/videos/nmip-media/channellive/channel7/playlist.m3u8',
         'http://204.12.221.218:8181/3m1080p/sxws.m3u8',
         'http://107.150.60.122/live/sxwshd.m3u8',
     ]},
    {'name': '内蒙古卫视', 'id': '内蒙古卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%86%85%E8%92%99%E5%8F%A4%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://play1-qk.nmtv.cn/live/1769652018126032.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=nmgws',
         'http://107.150.60.122/live/nmgws.m3u8',
     ]},
    {'name': '辽宁卫视', 'id': '辽宁卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E8%BE%BD%E5%AE%81%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://198.204.228.26/live/lnwshd.m3u8',
         'http://204.12.221.218:8181/3m1080p/lnws.m3u8',
         'http://107.150.60.122/live/lnwshd.m3u8',
     ]},
    {'name': '吉林卫视', 'id': '吉林卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%90%89%E6%9E%97%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://221.7.175.154:8445/tsfile/live/1014_1.m3u8?key=txiptv&playlive=1&authid=0',
         'http://38.75.136.137:98/gslb/dsdqpub/jlwshd.m3u8?auth=testpub',
         'http://107.150.60.122/live/jlwshd.m3u8',
     ]},
    {'name': '黑龙江卫视', 'id': '黑龙江卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E9%BB%91%E9%BE%99%E6%B1%9F%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'https://idclive.hljtv.com:4430/live/hljws_own.m3u8',
         'http://120.76.248.139/live/bfgd/4200000095.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/hljwshd.m3u8?auth=testpub',
     ]},
    {'name': '东方卫视', 'id': '东方卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E4%B8%9C%E6%96%B9%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://bp-resource-dfl.bestv.cn/148/3/video.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/dfwshd.m3u8?auth=testpub',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=dfwshd',
     ]},
    {'name': '江苏卫视', 'id': '江苏卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%B1%9F%E8%8B%8F%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://38.75.136.137:98/gslb/dsdqbv/jswshd.m3u8?auth=test20251009',
         'http://107.150.60.122/live/jswshd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=jswshd',
     ]},
    {'name': '浙江卫视', 'id': '浙江卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%B5%99%E6%B1%9F%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://ali-xwl.cztv.com/live/channel011080Plxw.m3u8',
         'https://ali-m-l.cztv.com/channels/lantian/channel001/1080p.m3u8',
         'http://107.150.60.122/live/zjwshd.m3u8',
     ]},
    {'name': '安徽卫视', 'id': '安徽卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%AE%89%E5%BE%BD%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://107.150.60.122/live/ahwshd.m3u8',
         'http://204.12.221.218:8181/3m1080p/ahws.m3u8',
         'http://198.204.228.26/live/ahwshd.m3u8',
     ]},
    {'name': '东南卫视', 'id': '东南卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E4%B8%9C%E5%8D%97%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://live.zohi.tv/video/s10001-fztv-3/index.m3u8',
         'http://120.76.248.139/live/bfgd/4200000483.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/dnwshd.m3u8?auth=testpub',
     ]},
    {'name': '江西卫视', 'id': '江西卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%B1%9F%E8%A5%BF%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://112.27.5.218:9901/tsfile/live/faacts/0138_1.m3u8?key=txiptv&playlive=1&authid=0',
         'http://38.75.136.137:98/gslb/dsdqpub/jxwshd.m3u8?auth=testpub',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=jxwshd',
     ]},
    {'name': '山东卫视', 'id': '山东卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%B1%B1%E4%B8%9C%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000099.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/sdwshd.m3u8?auth=testpub',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=sdwshd',
     ]},
    {'name': '河南卫视', 'id': '河南卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%B2%B3%E5%8D%97%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://38.75.136.137:98/gslb/dsdqpub/hawshd.m3u8?auth=testpub',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=hawshd',
     ]},
    {'name': '湖北卫视', 'id': '湖北卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%B9%96%E5%8C%97%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000102.m3u8',
         'http://107.150.60.122/live/hbwshd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=hbwshd',
     ]},
    {'name': '湖南卫视', 'id': '湖南卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%B9%96%E5%8D%97%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://hlsal-ldvt.qing.mgtv.com/nn_live/nn_x64/dWlwPTEyNy4wLjAuMSZ1aWQ9cWluZy1jbXMmbm5fdGltZXpvbmU9OCZjZG5leF9pZD1hbF9obHNfbGR2dCZ1dWlkPTliODY4NmU5ZTM2YzYwMmMmZT02OTE0NjA0JnY9MSZpZD1ITldTWkdTVCZzPTcwN2RiYTc2YzJjNmJmMTQ4MmUyZGYzOWU2NWM3YWFi/HNWSZGST.m3u8',
         'https://txmov2.a.kwimgs.com/bs3/video-hls/5199687338554291078_hlsb.m3u8',
         'http://107.150.60.122/live/hnwshd.m3u8',
     ]},
    {'name': '广东卫视', 'id': '广东卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%B9%BF%E4%B8%9C%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000092.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/gdwshd.m3u8?auth=testpub',
     ]},
    {'name': '广西卫视', 'id': '广西卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%B9%BF%E8%A5%BF%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000116.m3u8',
         'http://198.204.228.26/live/gxwshd.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/gxwshd.m3u8?auth=testpub',
     ]},
    {'name': '海南卫视', 'id': '海南卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%B5%B7%E5%8D%97%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000473.m3u8',
     ]},
    {'name': '重庆卫视', 'id': '重庆卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E9%87%8D%E5%BA%86%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://107.150.60.122/live/cqwshd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=cqwshd',
     ]},
    {'name': '四川卫视', 'id': '四川卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%9B%9B%E5%B7%9D%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://107.150.60.122/live/scwshd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=scwshd',
         'http://38.75.136.137:98/gslb/dsdqpub/scwshd.m3u8?auth=testpub',
     ]},
    {'name': '贵州卫视', 'id': '贵州卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E8%B4%B5%E5%B7%9E%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://204.12.221.218:8181/3m1080p/gzws.m3u8',
         'http://107.150.60.122/live/gzwshd.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/gzwshd.m3u8?auth=testpub',
     ]},
    {'name': '云南卫视', 'id': '云南卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E4%BA%91%E5%8D%97%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000482.m3u8',
         'http://107.150.60.122/live/ynwshd.m3u8',
         'http://192.151.150.154/live/ynwshd.m3u8',
     ]},
    {'name': '西藏卫视', 'id': '西藏卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E8%A5%BF%E8%97%8F%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000121.m3u8',
         'http://112.27.5.218:9901/tsfile/live/0111_1.m3u8?key=txiptv&playlive=1&authid=0',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=xzws',
     ]},
    {'name': '陕西卫视', 'id': '陕西卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E9%99%95%E8%A5%BF%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://192.151.150.154/live/snwshd.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=snwshd',
         'http://107.150.60.122/live/snwshd.m3u8',
     ]},
    {'name': '甘肃卫视', 'id': '甘肃卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E7%94%98%E8%82%83%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000119.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/gswshd.m3u8?auth=testpub',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=gswshd',
     ]},
    {'name': '青海卫视', 'id': '青海卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E9%9D%92%E6%B5%B7%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000111.m3u8',
         'http://107.150.60.122/live/qhws.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=qhws',
     ]},
    {'name': '宁夏卫视', 'id': '宁夏卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%AE%81%E5%A4%8F%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://107.150.60.122/live/nxws.m3u8',
         'http://198.204.228.26/live/nxws.m3u8',
     ]},
    {'name': '新疆卫视', 'id': '新疆卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%96%B0%E7%96%86%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://218.84.12.186:8001/hls/main/playlist.m3u8',
         'http://107.150.60.122/live/xjws.m3u8',
         'http://198.204.228.26/live/xjws.m3u8',
     ]},
    {'name': '大湾区卫视', 'id': '大湾区卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%A4%A7%E6%B9%BE%E5%8C%BA%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://107.150.60.122/live/nfws.m3u8',
         'http://198.204.228.26/live/nfws.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/nfws.m3u8?auth=testpub',
     ]},
    {'name': '深圳卫视', 'id': '深圳卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E6%B7%B1%E5%9C%B3%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://120.76.248.139/live/bfgd/4200000100.m3u8',
         'http://107.150.60.122/live/szwshd.m3u8',
         'http://38.75.136.137:98/gslb/dsdqpub/szwshd.m3u8?auth=testpub',
     ]},
    {'name': '安多卫视', 'id': '安多卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%AE%89%E5%A4%9A%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'https://liveout.xntv.tv/a65jur/96iln2.m3u8',
     ]},
    {'name': '延边卫视', 'id': '延边卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%BB%B6%E8%BE%B9%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'https://srs.iyb983.cn:443/video/CYS/index.m3u8',
         'https://srs.iyb983.cn/video/CYS/index.m3u8',
     ]},
    {'name': '厦门卫视', 'id': '厦门卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E5%8E%A6%E9%97%A8%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://198.204.228.26/live/xmws.m3u8',
         'http://192.151.150.154/live/xmws.m3u8',
         'http://107.150.60.122/live/xmws.m3u8',
     ]},
    {'name': '三沙卫视', 'id': '三沙卫视', 'group': '卫视', 'logo': 'https://www.xn--rgv465a.top/tvlogo/%E4%B8%89%E6%B2%99%E5%8D%AB%E8%A7%86.png',
     'urls': [
         'http://107.150.60.122/live/ssws.m3u8',
         'http://63.141.230.178:82/gslb/zbdq5.m3u8?id=ssws',
         'http://198.204.228.26/live/ssws.m3u8',
     ]},
]


# ---------------------------------------------------------------- 工具
def _txt(s):
    """反转义 m3u 里常见的 HTML 实体。"""
    try:
        return (str(s or '').replace('&amp;', '&').replace('&lt;', '<')
                .replace('&gt;', '>').replace('&quot;', '"')
                .replace('&#39;', "'").replace('&apos;', "'"))
    except Exception:
        return ''


def _base(name):
    """去掉 "CCTV-1 #2" 里的编号，用于把多线路合并成同一个频道。"""
    try:
        return re.sub(r'\s*#\d+$', '', str(name or '')).strip()
    except Exception:
        return str(name or '')


def parse_m3u(text):
    """m3u 文本 -> CHANNELS 同构的列表。

    解析时顺手处理两类脏数据，这类源里很常见：
      - 同一行用 ";" 拼了两个地址（新疆卫视那个源就是这样），只取第一个；
      - 同名频道带 "#2 #3" 后缀，合并回一个频道的 urls 数组。
    """
    rows = {}
    order = []
    cur = None
    try:
        for line in str(text or '').replace('\r', '').split('\n'):
            l = line.strip()
            if not l:
                continue
            if l.startswith('#EXTINF'):
                head, _, title = l.partition(',')
                g = re.search(r'group-title="([^"]*)"', head)
                p = re.search(r'tvg-logo="([^"]*)"', head)
                cur = {
                    'name': _base(_txt(title)),
                    'group': _txt(g.group(1)) if g else '其他',
                    'logo': _txt(p.group(1)) if p else '',
                }
            elif not l.startswith('#') and cur is not None:
                u = _txt(l).split(';http')[0].strip()
                if u[:4].lower() in ('http', 'rtmp', 'rtsp') or u.startswith('udp://'):
                    key = cur['name']
                    if key and key not in rows:
                        rows[key] = {'name': key, 'group': cur['group'],
                                     'logo': cur['logo'], 'urls': []}
                        order.append(key)
                    if key and u not in rows[key]['urls']:
                        rows[key]['urls'].append(u)
                cur = None
    except Exception:
        return []
    return [rows[k] for k in order if rows[k]['urls']]


# ---------------------------------------------------------------- Spider
class Spider(_Base):
    """央视 / 卫视直播源。

    对外方法末尾的 *args/**kw 是防御性的：不同 TVBox 分支会多传参数
    （比如 searchContent(key, quick, pg, filters)、detailContent(ids, filters)），
    签名对不上就直接 TypeError，用户看到的是「搜索失败」「加载失败」。
    """

    HOST_NAME = '央视卫视直播'

    # 频道表缓存。None 表示还没加载过。
    _rows = None
    _ts = 0
    _sub = ''

    def getName(self):
        return '央视卫视'

    # init 只做本地初始化：不联网、不抛异常。
    # extend 支持三种写法：
    #   ''                        用内置表
    #   'https://.../xxx.m3u'     在线订阅
    #   '{"m3u":"https://..."}'   带配置的订阅
    def init(self, extend=''):
        try:
            self.extend = extend or ''
            self._rows = None
            self._ts = 0
            self._sub = ''
            self._cfg(extend)
        except Exception:
            self._rows = None
            self._ts = 0
            self._sub = ''

    def _cfg(self, extend):
        try:
            s = str(extend or '').strip()
            if not s:
                return
            if s[:1] == '{':
                d = json.loads(s)
                self._sub = str(d.get('m3u') or d.get('url') or d.get('sub') or '').strip()
            elif s.startswith('http'):
                self._sub = s
        except Exception:
            self._sub = ''

    def _http(self, url, headers=None):
        # 不少直播源的证书链不完整，校验证书会直接握手失败；
        # 这里和原文件一样关掉校验，只是取 m3u 文本，不涉及账号。
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(url, headers=headers or {'User-Agent': UA})
        return urllib.request.urlopen(req, timeout=20, context=ctx).read()

    def _fetch(self, url):
        try:
            raw = self._http(url, {'User-Agent': UA, 'Accept': '*/*'})
            if isinstance(raw, bytes):
                raw = raw.decode('utf-8', 'replace')
            rows = parse_m3u(raw)
            return rows or None
        except Exception:
            return None

    # 取频道表：在线优先，失败回退内置，结果缓存 CACHE_TTL 秒。
    # 注意：不能让异常冒出去，否则客户端会把整个分类渲染成空白。
    def _channels(self):
        try:
            now = time.time()
            if self._rows and now - self._ts < CACHE_TTL:
                return self._rows
            rows = None
            if self._sub:
                rows = self._fetch(self._sub)
            if not rows:
                rows = CHANNELS
            self._rows = rows
            self._ts = now
            return rows
        except Exception:
            return CHANNELS

    def _groups(self):
        """按出现顺序返回分组名，在线订阅换了数据源也能自适应。"""
        out = []
        try:
            for c in self._channels():
                g = c.get('group') or '其他'
                if g not in out:
                    out.append(g)
        except Exception:
            return ['央视', '卫视']
        return out or ['央视', '卫视']

    def _classes(self):
        return [{'type_id': 'g%d' % i, 'type_name': g}
                for i, g in enumerate(self._groups())]

    def _pick(self, tid):
        """type_id -> 分组名。兼容客户端直接传中文分组名的情况。
        认不出来时返回空串，调用方会退回「全部频道」而不是给空白页。"""
        try:
            tid = str(tid or '')
            gs = self._groups()
            if tid.startswith('g') and tid[1:].isdigit():
                i = int(tid[1:])
                if 0 <= i < len(gs):
                    return gs[i]
            if tid in gs:
                return tid
        except Exception:
            pass
        return ''

    def _item(self, idx, c):
        """列表项。同时给两套字段名：
        vod_* 是点播模式用的，name/group/logo/urls 是直播模式（Live）用的。"""
        urls = [{'name': '线路%d' % (i + 1), 'url': u}
                for i, u in enumerate(c.get('urls') or [])]
        n = len(urls)
        return {
            'vod_id': 'ch:%d' % idx,
            'vod_name': c.get('name', ''),
            'vod_pic': c.get('logo', ''),
            'vod_remarks': ('%d 条线路' % n) if n > 1 else '单线路',
            'name': c.get('name', ''),
            'group': c.get('group', ''),
            'logo': c.get('logo', ''),
            'urls': urls,
        }

    # ---- 首页分类
    def homeContent(self, filter=False, *args, **kw):
        try:
            return {'class': self._classes()}
        except Exception:
            return {'class': [{'type_id': 'g0', 'type_name': '央视'},
                              {'type_id': 'g1', 'type_name': '卫视'}]}

    def homeVideoContent(self, *args, **kw):
        try:
            rows = self._channels()
            return {'list': [self._item(i, c) for i, c in enumerate(rows[:24])]}
        except Exception:
            return {'list': []}

    # ---- 分类列表。直播源没有分页，一次给全。
    def categoryContent(self, tid, pg, filter=False, extend=None, *args, **kw):
        try:
            rows = self._channels()
            g = self._pick(tid)
            lst = [self._item(i, c) for i, c in enumerate(rows)
                   if not g or c.get('group') == g]
            return {'list': lst, 'page': 1, 'pagecount': 1,
                    'limit': len(lst) or 1, 'total': len(lst)}
        except Exception:
            return {'list': [], 'page': 1, 'pagecount': 1, 'limit': 1, 'total': 0}

    # ---- 详情：把一个频道的多条线路摊成多线路
    def detailContent(self, ids, *args, **kw):
        try:
            ids = list(ids or [])
            if not ids:
                return {'list': []}
            rows = self._channels()
            s = str(ids[0])
            # 只认自己生成的 id。认不出来就返回空，
            # 不能默认取第 0 个频道——那会让「点了 A 播 B」。
            if not s.startswith('ch:'):
                return {'list': []}
            try:
                idx = int(s[3:] or 0)
            except Exception:
                return {'list': []}
            if not (0 <= idx < len(rows)):
                return {'list': []}
            c = rows[idx]
            urls = c.get('urls') or []
            if not urls:
                return {'list': []}
            froms = []
            plays = []
            for i, u in enumerate(urls):
                # vod_play_from 是播放器的线路 tab，vod_play_url 是「分集名$地址」。
                # 直播频道只有一集，分集名统一叫「直播」，否则列表里会出现
                # 「线路1（主）」「线路2」这种看着像剧集的条目。
                froms.append('线路%d%s' % (i + 1, '（主）' if i == 0 else ''))
                plays.append('直播$%s' % u)
            return {'list': [{
                'vod_id': 'ch:%d' % idx,
                'vod_name': c.get('name', ''),
                'vod_pic': c.get('logo', ''),
                'vod_remarks': c.get('group', ''),
                'vod_content': '%s（%s）\n共 %d 条线路，线路1 为主线路，其余为备用。\n\n%s' % (
                    c.get('name', ''), c.get('group', ''), len(urls),
                    '\n'.join(urls)),
                'vod_play_from': '$$$'.join(froms),
                'vod_play_url': '$$$'.join(plays),
            }]}
        except Exception:
            return {'list': []}

    # ---- 搜索：频道名匹配，精确名排前面
    def searchContent(self, key, quick, pg='1', *args, **kw):
        try:
            kw = str(key or '').strip().lower()
            if not kw:
                return {'list': [], 'page': 1}
            rows = self._channels()
            hit = []
            like = []
            for i, c in enumerate(rows):
                n = str(c.get('name', '')).lower()
                if n == kw:
                    hit.append(self._item(i, c))
                elif kw in n:
                    like.append(self._item(i, c))
            return {'list': hit + like, 'page': 1}
        except Exception:
            return {'list': [], 'page': 1}

    # ---- 播放。id 通常就是 m3u8 地址；也兼容 "ch:序号" 和 base64 包装。
    def playerContent(self, flag, id, vipFlags=None, *args, **kw):
        url = str(id or '')
        try:
            if url and not url.startswith('http'):
                if url.startswith('ch:'):
                    # 直播列表直接给了地址，正常走不到这里；
                    # 只有客户端拿频道 id 来播放时，才取第一条线路。
                    # 越界时置空，让播放器明确报「无法播放」，
                    # 而不是把 'ch:999' 当地址丢给解码器。
                    rows = self._channels()
                    url = ''
                    try:
                        i = int(id[3:] or 0)
                    except Exception:
                        i = -1
                    if 0 <= i < len(rows):
                        us = rows[i].get('urls') or []
                        url = us[0] if us else ''
                else:
                    # 少数客户端会把 id 做一次 base64 再传回来
                    try:
                        j = json.loads(base64.b64decode(url).decode('utf-8'))
                        url = j.get('url') or j.get('playUrl') or url
                    except Exception:
                        pass
        except Exception:
            pass
        # parse=0 表示交给播放器直连，不做嗅探/解析
        return {'parse': 0, 'playUrl': '', 'url': url,
                'header': {'User-Agent': UA}}

    # ---- 直播模式。TVBox 按 class 分栏，按 group 归组。
    def liveContent(self, filter=False, *args, **kw):
        try:
            rows = self._channels()
            lst = [self._item(i, c) for i, c in enumerate(rows)]
            return {'class': self._classes(), 'list': lst,
                    'EPG': EPG, 'epg': EPG}
        except Exception:
            return {'class': [], 'list': []}

    def localProxy(self, url):
        # 直连地址，不需要代理中转
        try:
            return url
        except Exception:
            return None

    def isVideoFormat(self, url):
        # 全部是 m3u8/直播流。这里返回 True 而不是按后缀判断：
        # 有些地址带 query（如 ?id=cctv1hd）没有 .m3u8 后缀，
        # 按后缀判断会把它们误判成非视频，客户端直接不播。
        return True

    def isTextFormat(self, url):
        return False

    def destroy(self):
        try:
            self._rows = None
            self._ts = 0
        except Exception:
            pass


if __name__ == '__main__':
    # 直接用 python CCTV.py 跑一下，确认频道表和接口都正常。
    # 客户端加载时 __name__ 不是 __main__，这段不会执行。
    _sp = Spider()
    _sp.init('')
    _h = _sp.homeContent()
    print('分类:', [c['type_name'] for c in _h['class']])
    for _c in _h['class']:
        _r = _sp.categoryContent(_c['type_id'], 1)
        print('  %-4s %d 个频道' % (_c['type_name'], len(_r['list'])))
    _r = _sp.categoryContent(_h['class'][0]['type_id'], 1)
    for _x in _r['list'][:5]:
        print('  %-16s %s' % (_x['vod_name'], _x['vod_remarks']))
    print('直播模式:', len(_sp.liveContent()['list']), '个频道')
