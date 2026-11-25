/**
 * cctv.live — 央视 / 卫视精选 56 台（多线路备份）
 * Rex 明文模块  v1.0.0
 * 更新: 2026-11-25 14:55:47  |  频道: 56  线路: 163
 *
 * 设计要点:
 *   列表只出 56 条主条目，刷不出 "CCTV-1 #2 #3" 这类重复项；
 *   点开某台后，episodeItems 里放该台 2~3 条备用线路，Rex 播放器可逐条切换。
 *
 * 数据源: guovin 每日输出 / BigBigGrandG / aptv / vbskycn / ZBDS / iptv-org
 */

var WidgetMetadata = {
  id: "cctv.live",
  title: "cctv.live 电视直播",
  version: "1.0.0",
  requiredVersion: "0.0.1",
  description: "央视 + 卫视精选 56 台，每台 2~3 条备用线路自动换线（来源：guovin / BigBigGrandG / aptv / vbskycn / ZBDS / iptv-org）",
  author: "cctv.live",
  detailCacheDuration: 300,
  modules: [
    { id: "loadCCTV", title: "央视", functionName: "loadCCTV", cacheDuration: 3600 },
    { id: "loadWeishi", title: "卫视", functionName: "loadWeishi", cacheDuration: 3600 },
    { id: "loadFeature", title: "特色", functionName: "loadFeature", cacheDuration: 3600 },
    { id: "loadAll", title: "全部频道", functionName: "loadAll", cacheDuration: 3600 }
  ],
  search: { title: "搜频道", functionName: "searchChannels" }
};

var UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36";

var CHANNELS = [
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
];

/* ------------------------------------------------------------ 工具 */
function playHeaders(url) {
  var i = url.lastIndexOf("/");
  var base = i > 0 ? url.substring(0, i + 1) : url;
  return { "User-Agent": UA, "Referer": base };
}

function toItem(ch) {
  return {
    id: ch.id,
    type: "detail",
    title: ch.name,
    link: ch.id,
    coverUrl: ch.logo || "",
    posterPath: ch.logo || "",
    mediaType: "tv",
    genreTitle: ch.group,
    description: ch.name + " · " + ch.lines.length + " 条备用线路",
    durationText: "",
    releaseDate: ""
  };
}

function matchGroup(group) {
  var out = [];
  for (var i = 0; i < CHANNELS.length; i++) {
    if (!group || CHANNELS[i].group === group) out.push(toItem(CHANNELS[i]));
  }
  return out;
}

/* ------------------------------------------------------------ 列表 */
async function loadCCTV(params) {
  return matchGroup("央视");
}

async function loadWeishi(params) {
  return matchGroup("卫视");
}

async function loadFeature(params) {
  return matchGroup("特色");
}

async function loadAll(params) {
  return matchGroup("");
}

/* ------------------------------------------------------------ 搜索 */
async function searchChannels(params) {
  var kw = String((params && params.keyword) || "").toLowerCase().replace(/\s/g, "");
  if (!kw) return [];
  var out = [];
  for (var i = 0; i < CHANNELS.length; i++) {
    var c = CHANNELS[i];
    if (c.name.toLowerCase().indexOf(kw) > -1 || c.id.indexOf(kw) > -1) out.push(toItem(c));
  }
  return out;
}

/* ------------------------------------------------------------ 详情：展开全部备用线路 */
async function loadDetail(link) {
  var id = String(link || "").split("|")[0];
  var ch = null;
  for (var i = 0; i < CHANNELS.length; i++) {
    if (CHANNELS[i].id === id) { ch = CHANNELS[i]; break; }
  }
  if (!ch) return null;

  var eps = [];
  for (var j = 0; j < ch.lines.length; j++) {
    var ln = ch.lines[j];
    eps.push({
      id: ch.id + "_" + (j + 1),
      type: "url",
      mediaType: "tv",
      title: "线路 " + (j + 1),
      episodeName: "线路 " + (j + 1) + " · " + ln.src,
      videoUrl: ln.url,
      customHeaders: playHeaders(ln.url),
      episode: j + 1,
      description: "来源 " + ln.src
    });
  }

  return {
    id: ch.id,
    type: "detail",
    mediaType: "tv",
    title: ch.name,
    coverUrl: ch.logo || "",
    posterPath: ch.logo || "",
    genreTitle: ch.group,
    description: ch.name + " 共 " + eps.length + " 条备用线路，播放失败可切下一条。",
    link: ch.id,
    episodeItems: eps,
    episode: 1
  };
}

/* ------------------------------------------------------------ 播放（兜底直取） */
async function loadResource(params) {
  params = params || {};
  var url = params.videoUrl || "";
  if (!url && params.link) {
    var id = String(params.link).split("|")[0];
    for (var i = 0; i < CHANNELS.length; i++) {
      var c = CHANNELS[i];
      if (c.id !== id) continue;
      var idx = parseInt(params.episode || "1", 10) - 1;
      if (idx < 0 || idx >= c.lines.length) idx = 0;
      url = c.lines[idx].url;
      break;
    }
  }
  if (!url) return [];
  return [{
    name: "cctv.live",
    description: params.title || "",
    url: url,
    customHeaders: playHeaders(url),
    playerType: "app"
  }];
}
