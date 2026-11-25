# cctv.live

央视 + 卫视精选 **56 台**，每台挂 **2~3 条备用线路**。

列表页只出 56 条干净条目，不会出现 `CCTV-1 #2 #3` 这种重复项；
点开某个台后，才把它的备用线路全部展开，播放失败能直接切下一条。

---

## 文件

| 文件 | 用途 | 说明 | 条目数 |
|---|---|---|---|
| `cctv.txt` | 通用 TXT 源 | `名称,url` + `#genre#` 分组，几乎所有播放器都吃 | 163 行 |
| `cctv.m3u` | M3U 播放列表（全线路） | 带 `tvg-id` / `tvg-logo` / `group-title`，已配 EPG | 163 |
| `cctv.lite.m3u` | M3U 播放列表（**精简版**） | 每台只留 1 条主线路，频道列表干净不重复 | **56** |
| `cctv.rex.js` | Rex 模块（明文） | 导入 Rex 直接用，列表 56 条、详情页出备用线路 | 列表 56 |
| `cctv.py` | Python spider | 标准 spider 接口，可接 TVBox 类框架或自行调用 | 56 / 163 |

当前规模：**56 频道 / 163 线路**（央视 32 · 卫视 18 · 特色 6）。

### 全线路版 vs 精简版怎么选

M3U 格式里，一条 `#EXTINF` 只能挂一个 URL。所以「一个台 3 条备用线路」必然写成 3 条 EXTINF，
在播放器里就显示成 `CCTV-1 综合`、`CCTV-1 综合 (2)`、`CCTV-1 综合 (3)` —— 这是格式决定的，不是文件出错。

| 你的播放器 | 用哪个 |
|---|---|
| 支持按 `group-title` 分组折叠（TiviMate、部分盒子） | `cctv.m3u`，分组后视觉上就干净 |
| 平铺显示所有条目（VLC 默认、多数轻量播放器） | `cctv.lite.m3u`，56 条无重复 |
| Rex | `cctv.rex.js`，真正做到「列表 56 条 + 点开展开线路」 |

**精简版的取舍**：每个台只留质量分最高的 1 条线路，没有备份。某条挂了要等下次更新，或者手动去全线路版里找替代。

---

## 数据来源

六个自动测速源，全部取每日构建产物：

| 源 | 地址 | 原始条目 |
|---|---|---|
| guovin 每日输出 | `Guovin/iptv-api` → `output/result.txt` | ~1600 |
| BigBigGrandG | `BigBigGrandG/IPTV-URL` → `Gather.m3u` | ~1950 |
| aptv | `Kimentanm/aptv` → `m3u/iptv.m3u` | ~120 |
| vbskycn | `vbskycn/iptv` → `tv/iptv4.m3u` | ~350 |
| ZBDS | `live.zbds.top/tv/iptv4.txt` | ~470 |
| iptv-org | `iptv-org.github.io/iptv/countries/cn.m3u` | ~155 |

合计约 4600 条原始条目，归并后剩 56 条主条目、163 条线路。

**注意**：ZBDS 的 `iptv4.m3u` 与 vbskycn 那份字节级完全一致（ZBDS 是镜像），
所以 ZBDS 这一路必须取它的 **txt**，否则六个源实际只有五路。

---

## 频道清单

**央视 32**：CCTV-1~17、CCTV-5+、CCTV-4K、怀旧剧场、第一剧场、风云音乐、风云足球、
风云剧场、文化精品、女性时尚、CGTN 英语/法语/西语/阿语/俄语/纪录

**卫视 18**：湖南、浙江、江苏、东方、北京、深圳、广东、安徽、山东、天津、湖北、
河南、河北、四川、重庆、辽宁、江西、东南

**特色 6**：卡酷少儿、金鹰纪实、金鹰卡通、纪实人文、星空卫视、优漫卡通

---

## 每种版本怎么用

### cctv.txt

丢进 Perfect Player / 电视盒子 / 任何支持 TXT 源的播放器。
主线路用台名，备用线路是 `台名 #2`、`台名 #3`，播放器若按名归组会自动合并。

### cctv.m3u

```
#EXTM3U x-tvg-url="https://epg.112114.xyz/pp.xml"
```
VLC / PotPlayer / Kodi 直接打开。备用线路的 `tvg-id` 是 `cctv1_2` 这种，
`tvg-name` 保持一致，所以 EPG 仍能对上。

### cctv.rex.js（Rex 模块）

1. Rex → 模块 → 导入本地模块，选 `cctv.rex.js`
2. 首页加一行，选「cctv.live 电视直播」，四个模块任选：
   - **央视**（32 条）
   - **卫视**（18 条）
   - **特色**（6 条）
   - **全部频道**（56 条）

点开某个台 → 详情页的线路列表就是该台全部备用线路，逐条切着试。

模块结构：`WidgetMetadata` + 四个 list handler + `searchChannels` + `loadDetail` + `loadResource`，
全部是顶层 `async function`，符合 Rex 的 `functionName` 约定。明文无双引号包裹，可直接改。

### cctv.py（spider）

```python
from cctv import Spider
s = Spider()
s.home()                  # {'class': [央视/卫视/特色], 'filters': {}}
s.category('cctv')        # 央视 32 条
s.detail('cctv1')         # 该台全部线路，vod_play_url 用 # 连接
s.play('cctv.live', url)  # 带 UA / Referer 的播放信息
s.search('东方')          # 搜台
```
自测：`python3 cctv.py`

---

## 线路为什么是这几条

每条台最多留 3 条，选线逻辑：

1. **先按源分散**：第一轮每台最多从同一个源取 1 条 —— 保证 3 条线路来自 3 个不同源，
   某一家源整体挂掉时不会三条一起死。
2. **再补同源**：只有跨源凑不满 3 条时，才允许同一源出第 2 条。
3. **质量排序**：1080p > 720p > HD > 标清；`[Not 24/7]` 降权，
   `[Geo-blocked]` 大幅降权；https 微加分。
4. **IPv6 降权但不删**：`http://[2409:...]` 这类直连地址在纯 IPv4 网络下播不了，
   但移动宽带用户反而更依赖，所以只扣分不排除。
5. **URL 去重**：同一个 url 不会在一台里出现两次。

---

## ⚠️ 关于测活

`probe.py` 会并发拉每条线路的 m3u8 头做存活判断。但这台机器有出口白名单策略，
普通 IPTV 源地址大多连不上，实测只跑通 14/163，而且全是 cgtn/cztv 这类官方 CDN。

**这个数字不代表源真的死了。** 所以：

- 在这台机器上更新请加 `--no-probe`，别让测活结果去裁剪线路
- 想真正测活，丢到能访问国内运营商网络的机器上跑 `python3 scripts/probe.py`
- `probe.py` 有保护：某台存活线路数低于 `--min-lines`（默认 1）时保留原线路，
  防止网络策略导致全军覆没

---

## 更新

```bash
python3 scripts/update.py                          # 全流程，出到 ./cctv.live/
python3 scripts/update.py -o ~/Desktop/cctv        # 指定输出目录
python3 scripts/update.py --no-probe               # 跳过测活（本机推荐）
python3 scripts/update.py --total 60               # 改名单条数
python3 scripts/update.py --fresh                  # 强制重下源（默认 6 小时内复用缓存）
```

分步跑：

```bash
python3 scripts/build_cctv.py --data ./data --total 56   # 合并 → data/cctv_list.json
python3 scripts/probe.py --data ./data/cctv_list.json    # 测活（可选）
python3 scripts/export.py --data ./data --out ./out      # 导出四版
```

改频道表就编辑 `scripts/build_cctv.py` 顶部那一串 `C(...)` 调用：
`C(标准id, 显示名, 分组, [别名正则...])`。想加台，照抄一行改正则即可。

---

## 已知限制

- 源本身随时会失效，公开 IPTV 源没有长期保证，定期重跑 `update.py` 是唯一办法
- 部分源在特定运营商网络下才有速度，同一份名单在不同网络表现差异很大
- 直播源不含任何视频内容，仅是地址索引
