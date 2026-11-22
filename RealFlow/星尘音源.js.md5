/*
 * @name 星尘音乐源
 * @description 全平台多源音源 · 星尘自研调度内核，多接口竞速、校验、缓存、打分
 * @version 1.1.0
 * @base 星尘音乐源·终章 1.1.0 (2026-11-15)
 * @note 竞速调度引擎统一接口池 std_* 子源并发择优，自动降级、宿主与后缀校验、体积防伪
 */
const { EVENT_NAMES, request, on, send } = globalThis.lx;
const XINGCHEN_KEY = '199c87dfb00e56ff8fd604c8adadafcece8f08d490a327ba78067bc1a3736663';
const NKI_KEY = 'ed34917b6e3ca97d609a82e73c82599c176a07a4bcad5f5f7ab4ee95b3fa90ba';
const HYW_KEY = '6C1F-53W0-GRKI-EVFG';
const CUNYU_TOKEN= 'mwu4zgfLyMiYmMzIzdm5mZiYnZbLzwm4';
const MIGU_KEY = '60b0413e3e00aecbd56257f60e803e02';
const IKUN_KEY = 'IKM-P18300001-HBtJk8EzMwCBW1v6-t4';
const IKUN_KEY2 = 'IKM-P79900001-787LKHVGzFxOQFIc-vM';
const CACHE_TTL = 20 * 60 * 1000;
const CACHE_MAX = 300;
const INFLIGHT_MAX = 5;
const PENDING_MAX = 6;
const PENDING_MAX_AGE = 120 * 1000;
const STATS_DECAY = 0.99;
const STATS_LIMIT = 200;
const MIN_SAMPLES = 3;
const NO_SOURCE_TTL = 30 * 60 * 1000;
const PLAY_LEVEL = '320k';
const STRICT_LEVELS = ['master', 'jymaster', 'hires', 'flac24bit', 'flac', 'atmos', 'atmos_plus', 'sky', 'jyeffect'];
const PLAY_TOTAL_TIMEOUT = 8000;
const DOWNLOAD_TOTAL_TIMEOUT = 10000;
const SIZE_PROBE_TIMEOUT = 5000;
const LOG_SUBSOURCE = false;
const STRICT_HOST = false;
const STRICT_SUFFIX = true;
const ENABLE_SIZE_CHECK = true;
const LOG_SIZE_CHECK = true;
const SOURCE_STEP_GAP = 0;
const KW_FALLBACK = {
tx: true,
wy: true,
kg: true,
mg: true,
};
const KW_FALLBACK_DELAY = 500;
const ENABLE_MIGU_MAGIC = true;
const MIGU_REVERSE_RULES = {
'hires': [
{ re: /\/歌曲下载\/flac\//i, to: '/歌曲下载/flac_24bit/', ext: '.flac' },
{ re: /\/标清高清\/MP3_(128|320)_16_Stero\//i, to: '/歌曲下载/flac_24bit/', ext: '.flac' },
{ re: /\/歌曲下载\/MP3_(128|320)_16_Stero\//i, to: '/歌曲下载/flac_24bit/', ext: '.flac' },
],
'flac24bit': [
{ re: /\/歌曲下载\/flac\//i, to: '/歌曲下载/flac_24bit/', ext: '.flac' },
{ re: /\/标清高清\/MP3_(128|320)_16_Stero\//i, to: '/歌曲下载/flac_24bit/', ext: '.flac' },
{ re: /\/歌曲下载\/MP3_(128|320)_16_Stero\//i, to: '/歌曲下载/flac_24bit/', ext: '.flac' },
],
'flac': [
{ re: /\/歌曲下载\/flac_24bit\//i, to: '/歌曲下载/flac/', ext: '.flac' },
{ re: /\/标清高清\/MP3_(128|320)_16_Stero\//i, to: '/歌曲下载/flac/', ext: '.flac' },
{ re: /\/歌曲下载\/MP3_(128|320)_16_Stero\//i, to: '/歌曲下载/flac/', ext: '.flac' },
],
'320k': [
{ re: /\/歌曲下载\/flac_24bit\//i, to: '/标清高清/MP3_320_16_Stero/', ext: '.mp3' },
{ re: /\/歌曲下载\/flac\//i, to: '/标清高清/MP3_320_16_Stero/', ext: '.mp3' },
{ re: /\/标清高清\/MP3_128_16_Stero\//i, to: '/标清高清/MP3_320_16_Stero/', ext: '.mp3' },
{ re: /\/歌曲下载\/MP3_(128|320)_16_Stero\//i, to: '/标清高清/MP3_320_16_Stero/', ext: '.mp3' },
],
'128k': [
{ re: /\/歌曲下载\/flac_24bit\//i, to: '/标清高清/MP3_128_16_Stero/', ext: '.mp3' },
{ re: /\/歌曲下载\/flac\//i, to: '/标清高清/MP3_128_16_Stero/', ext: '.mp3' },
{ re: /\/标清高清\/MP3_320_16_Stero\//i, to: '/标清高清/MP3_128_16_Stero/', ext: '.mp3' },
{ re: /\/歌曲下载\/MP3_(128|320)_16_Stero\//i, to: '/标清高清/MP3_128_16_Stero/', ext: '.mp3' },
],
'master': [],
'atmos': [],
'atmos_plus': [],
};
const PLAY_ORDER = {
tx: ['tx_cy', 'tx_ly', 'tx_yx', 'tx_ht', 'tx_ikun', 'tx_nki', 'tx_tang', 'tx_xhs', 'tx_hyw', 'tx_ikun2', 'tx_zddyr', 'tx_anime'],
wy: ['wy_cy', 'wy_ikun', 'wy_ikun_key', 'wy_nx', 'wy_hyw', 'wy_ht', 'wy_ht2', 'wy_ht3', 'wy_zddyr', 'wy_qgg', 'wy_nanorocky', 'wy_bugpk', 'wy_xt', 'wy_xtv2', 'wy_ikun2', 'wy_gdstudio', 'wy_anime', 'wy_cy2'],
kg: ['kg_ht', 'kg_zddyr', 'kg_hyw', 'kg_ikun', 'kg_ikun2', 'kg_anime'],
kw: ['kw_mobi', 'kw_car', 'kw_zx', 'kw_ht', 'kw_ikun', 'kw_ikun2', 'kw_anime'],
mg: ['mg_sy', 'mg_wen', 'mg_zddyr', 'mg_zddyr2'],
};
const DOWNLOAD_ORDER = {
tx: {
master: ['tx_yx', 'tx_ly', 'tx_ht', 'tx_zddyr', 'tx_ikun', 'tx_ikun2', 'tx_anime'],
atmos_plus: ['tx_ly', 'tx_yx', 'tx_ht', 'tx_ikun', 'tx_ikun2'],
atmos: ['tx_ly', 'tx_yx', 'tx_ht', 'tx_ikun', 'tx_ikun2', 'tx_anime', 'tx_tang'],
jyeffect: ['tx_ly'],
sky: ['tx_ly'],
hires: ['tx_ly', 'tx_yx', 'tx_ikun', 'tx_ikun2', 'tx_tang'],
flac24bit: ['tx_ly', 'tx_ht', 'tx_hyw', 'tx_yx', 'tx_ikun', 'tx_ikun2', 'tx_tang'],
flac: ['tx_ly', 'tx_ht', 'tx_hyw', 'tx_yx', 'tx_ikun', 'tx_ikun2', 'tx_cy', 'tx_tang', 'tx_anime'],
},
wy: {
master: ['wy_ikun', 'wy_ikun_key', 'wy_ht', 'wy_ht2', 'wy_ht3', 'wy_nanorocky', 'wy_bugpk', 'wy_ikun2',],
jymaster: ['wy_ikun', 'wy_ikun_key', 'wy_ht', 'wy_ht2', 'wy_ht3', 'wy_nanorocky', 'wy_bugpk', 'wy_ikun2', ],
atmos: ['wy_nx', 'wy_ht', 'wy_ht2', 'wy_ht3', 'wy_ikun', 'wy_ikun_key', 'wy_nanorocky', 'wy_bugpk', 'wy_ikun2', ],
sky: ['wy_nx', 'wy_ht', 'wy_ht2', 'wy_ht3', 'wy_nanorocky', 'wy_bugpk', 'wy_cy2'],
jyeffect: ['wy_nx', 'wy_ht', 'wy_ht2', 'wy_ht3', 'wy_nanorocky', 'wy_bugpk', ],
atmos_plus: ['wy_cy', 'wy_nx', 'wy_ht', 'wy_ht2', 'wy_ht3', 'wy_zddyr', 'wy_nanorocky', 'wy_bugpk', 'wy_ikun', 'wy_ikun_key', 'wy_ikun2', 'wy_cy2'],
hires: ['wy_cy', 'wy_ikun', 'wy_ikun_key', 'wy_nx', 'wy_ht', 'wy_ht2', 'wy_ht3', 'wy_hyw', 'wy_zddyr', 'wy_qgg', 'wy_nanorocky', 'wy_bugpk', 'wy_xt', 'wy_xtv2', 'wy_ikun2', ],
flac24bit: ['wy_cy', 'wy_ikun', 'wy_ikun_key', 'wy_nx', 'wy_ht', 'wy_ht2', 'wy_ht3', 'wy_hyw', 'wy_zddyr', 'wy_qgg', 'wy_nanorocky', 'wy_bugpk', 'wy_xt', 'wy_xtv2', 'wy_ikun2', ],
flac: ['wy_ht', 'wy_ht2', 'wy_ht3', 'wy_nx', 'wy_ikun', 'wy_ikun_key', 'wy_cy', 'wy_hyw', 'wy_zddyr', 'wy_qgg', 'wy_nanorocky', 'wy_bugpk', 'wy_xt', 'wy_xtv2', 'wy_ikun2', 'wy_gdstudio', 'wy_cy2'],
},
kg: {
master: ['kg_ht', 'kg_zddyr', 'kg_ikun', 'kg_ikun2', 'kg_anime'],
hires: ['kg_hyw', 'kg_ht', 'kg_zddyr', 'kg_ikun', 'kg_ikun2'],
atmos: ['kg_ht', 'kg_ikun', 'kg_ikun2'],
flac24bit: ['kg_hyw', 'kg_ht', 'kg_zddyr', 'kg_ikun', 'kg_ikun2'],
flac: ['kg_ht', 'kg_zddyr', 'kg_hyw', 'kg_ikun', 'kg_ikun2', 'kg_anime'],
},
kw: {
master: ['kw_zx', 'kw_mobi', 'kw_ht', 'kw_ikun', 'kw_ikun2'],
atmos_plus: ['kw_zx', 'kw_mobi', 'kw_ht', 'kw_ikun', 'kw_ikun2'],
atmos: ['kw_zx', 'kw_mobi', 'kw_ht', 'kw_ikun', 'kw_ikun2'],
hires: ['kw_car', 'kw_mobi', 'kw_ht', 'kw_ikun', 'kw_ikun2'],
flac24bit: ['kw_car', 'kw_mobi', 'kw_ht', 'kw_ikun', 'kw_ikun2'],
flac: ['kw_car', 'kw_mobi', 'kw_ht', 'kw_ikun', 'kw_ikun2', 'kw_anime'],
},
mg: {
hires: [ 'mg_wen', 'mg_sy','mg_zddyr', 'mg_zddyr2'],
flac24bit: [ 'mg_wen', 'mg_sy','mg_zddyr', 'mg_zddyr2'],
flac: [ 'mg_wen', 'mg_sy','mg_zddyr', 'mg_zddyr2'],
},
};
const PLATFORM_HOSTS = {
tx: ['stream.qqmusic.qq.com', 'qqmusic.qq.com', 'bdycdn.cn', 'bdycdn.com', 'tc.qq.com', 'isure6.ptqqmusic.gitv.tv', 'aqqmusic.tc.qq.com', 'ws.stream.qqmusic.qq.com'],
wy: ['music.126.net', '126.net', 'metingapi.nanorocky.top', 'kuwo.cn', 'kuwo.com', '175.27.166.236'],
kg: ['kugou.com', 'bdycdn.cn', 'bdycdn.com', 'kuwo.cn', 'kuwo.com', '175.27.166.236'],
kw: ['kuwo.cn', 'kuwo.com', '175.27.166.236'],
mg: ['migu.cn', 'freetyst.nf.migu.cn', 'kuwo.cn', 'kuwo.com', '175.27.166.236'],
};
function hostOk(url, platform) {
if (!url || !platform) return false;
const hosts = PLATFORM_HOSTS[platform];
if (!hosts) return true;
const low = String(url).toLowerCase();
for (let i = 0; i < hosts.length; i++) if (low.indexOf(hosts[i]) >= 0) return true;
return false;
}
function suffixOk(url, quality) {
const lowUrl = String(url).toLowerCase();
if (lowUrl.indexOf('.mflac') >= 0 || lowUrl.indexOf('mgg') >= 0) {
return false;
}
const isLossless = STRICT_LEVELS.indexOf(quality) >= 0;
if (!isLossless) return true;
if (quality === 'atmos' || quality === 'atmos_plus') {
if (lowUrl.indexOf('.mp3') >= 0) return false;
return true;
}
if (lowUrl.indexOf('.mp3') >= 0 || lowUrl.indexOf('.m4a') >= 0 || lowUrl.indexOf('m800') >= 0) {
return false;
}
return true;
}
function isTrialUrl(url) {
const low = String(url || '').toLowerCase();
let features = [];
if (/music\.163\.com\/song\/media\/outer\/url/i.test(low)) features.push('网易云外链');
if (/\/outer\/url/i.test(low) || /\/song\/media\/outer/i.test(low)) features.push('外链跳转器');
if (/fcg_pyq_play/i.test(low)) features.push('非音频网页');
if (/\/rs02[0-9a-z]+\.mp3/i.test(low)) features.push('QQ铃声截断(RS02)');
if (/trial|试听|audition|preview|free.?trial/i.test(low)) features.push('trial关键词');
if (/_30\.(mp3|flac|m4a|aac)|30s\.(mp3|flac|m4a|aac)|short\.(mp3|flac|m4a)/i.test(low)) features.push('30s文件');
if (/cdn-img\.gitcode\.com/i.test(low)) features.push('gitcode假试听');
return features.length > 0 ? features.join(', ') : null;
}
function log() {
if (!LOG_SUBSOURCE) return;
try {
const a = Array.prototype.slice.call(arguments);
console.log.apply(console, a);
} catch (e) {}
}
function isValidUrl(u) { return typeof u === 'string' && /^https?:\/\//i.test(u); }
function httpsToHttp(u) { return String(u || '').replace(/^https:\/\//i, 'http://'); }
function b64Encode(str) {
try {
const lxBuf = globalThis.lx && globalThis.lx.utils && globalThis.lx.utils.buffer;
if (lxBuf && lxBuf.from) return lxBuf.bufToString(lxBuf.from(str, 'utf-8'), 'base64');
} catch (e) {}
try {
if (typeof Buffer !== 'undefined') return Buffer.from(str, 'utf-8').toString('base64');
} catch (e) {}
try { return btoa(unescape(encodeURIComponent(str))); } catch (e) { return ''; }
}
function parseSize(s) {
if (!s) return 0;
if (typeof s === 'number') return s > 0 ? s : 0;
const m = String(s).trim().match(/^([\d.]+)\s*([KMGT]?)B?$/i);
if (!m) return 0;
const n = parseFloat(m[1]);
const unit = (m[2] || '').toUpperCase();
const mul = { '': 1, K: 1024, M: 1048576, G: 1073741824, T: 1099511627776 }[unit] || 1;
return n * mul;
}
function fmtMB(n) { return (n / 1048576).toFixed(1) + 'M'; }
function expectedSize(mi, quality) {
if (!mi) return 0;
const aliases = {
'hires': ['hires', 'flac24bit'],
'flac24bit': ['flac24bit', 'hires'],
'master': ['master', 'flac24bit'],
'atmos': ['atmos', 'flac24bit'],
'atmos_plus': ['atmos_plus', 'flac24bit'],
'sky': ['sky', 'flac24bit'],
'jyeffect': ['jyeffect', 'flac24bit']
};
const checkKeys = aliases[quality] || [quality];
if (mi._types) {
for (let i = 0; i < checkKeys.length; i++) {
const k = checkKeys[i];
if (mi._types[k] && mi._types[k].size) {
return parseSize(mi._types[k].size);
}
}
}
if (Array.isArray(mi.types)) {
for (let i = 0; i < checkKeys.length; i++) {
const k = checkKeys[i];
for (let j = 0; j < mi.types.length; j++) {
if (mi.types[j].type === k) return parseSize(mi.types[j].size);
}
}
}
return 0;
}
async function probeUrl(url) {
try {
const finalRes = await httpRequest(url, {
method: 'GET',
headers: { 'Range': 'bytes=0-0', 'User-Agent': 'Mozilla/5.0 (Linux; Android 13)' },
timeout: SIZE_PROBE_TIMEOUT,
});
const h = (finalRes.headers || {});
const cr = String(h['content-range'] || '');
const m = cr.match(/\/(\d+)/);
let size = 0;
if (m) size = parseInt(m[1], 10);
else if (h['content-length']) size = parseInt(h['content-length'], 10) || 0;
return { size: size };
} catch (e) {
return { size: 0 };
}
}
function httpRequest(url, options) {
options = options || { method: 'GET' };
return new Promise(function (resolve, reject) {
request(url, Object.assign({ timeout: 12000 }, options), function (err, res) {
if (err) return reject(new Error('请求错误: ' + err.message));
let body = res && res.body;
if (typeof body === 'string') {
const t = body.trim();
if (t.charAt(0) === '{' || t.charAt(0) === '[') { try { body = JSON.parse(t); } catch (e) {} }
}
resolve({ statusCode: (res && res.statusCode) || 0, headers: (res && res.headers) || {}, body: body });
});
});
}
async function httpGet(url, params, headers) {
let full = url;
if (params) {
const qs = Object.keys(params).filter(function (k) { return params[k] !== undefined && params[k] !== null; })
.map(function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(params[k]); }).join('&');
if (qs) full += (url.indexOf('?') >= 0 ? '&' : '?') + qs;
}
const opts = { method: 'GET' };
if (headers) opts.headers = headers;
const res = await httpRequest(full, opts);
if (res.statusCode >= 400) throw new Error('HTTP ' + res.statusCode);
return res.body;
}
async function httpPost(url, body, headers) {
const opts = { method: 'POST', headers: Object.assign({ 'Content-Type': 'application/json' }, headers || {}), body: JSON.stringify(body) };
const res = await httpRequest(url, opts);
if (res.statusCode >= 400) throw new Error('HTTP ' + res.statusCode);
return res.body;
}
function pickField(obj, paths) {
for (let i = 0; i < paths.length; i++) {
const ks = paths[i].split('.');
let v = obj;
for (let j = 0; j < ks.length; j++) {
if (v == null) { v = undefined; break; }
const k = ks[j];
const m = k.match(/^([^\[]+)\[(\d+)\]$/);
if (m) { const t = v[m[1]]; v = t == null ? undefined : t[parseInt(m[2], 10)]; }
else v = v[k];
}
if (isValidUrl(v)) return httpsToHttp(v);
}
return null;
}
function idOf(mi, platform) {
if (!mi) return '';
let cand = '';
if (platform === 'tx') cand = mi.songmid || mi.mid || mi.id || '';
else if (platform === 'kg') cand = mi.hash || mi.songmid || String(mi.id || '').replace(/^kg_/, '') || '';
else if (platform === 'mg') cand = mi.copyrightId || mi.songmid || mi.id || '';
else cand = mi.songmid || mi.id || '';
return String(cand).replace(/^(kw_|qq_|wy_|kg_|mg_)/, '');
}
function miguCopyrightId(mi) {
if (!mi) return '';
if (mi.copyrightId) return String(mi.copyrightId);
const raw = String(mi.id || mi.songmid || '').replace(/^mg_/, '');
if (raw && /[A-Za-z]/.test(raw)) return raw;
return '';
}
async function miguInternalId(mi) {
const cid = miguCopyrightId(mi);
if (cid) {
try {
const info = await httpGet('http://101.200.224.166/musicfree/index.php',
{ key: MIGU_KEY, action: 'musicInfo', copyright_id: cid });
if (info && info.music && info.music.id) return String(info.music.id);
} catch (e) {}
}
return idOf(mi, 'mg');
}
let xhTk = '', xhTs = 0, xhPrm = null;
async function xhGetTk() {
if (xhTk && Date.now() - xhTs < 240000) return xhTk;
if (xhPrm) return xhPrm;
xhPrm = (async () => {
const r = await httpGet('https://yy.zddyr.top/lx/api/token.php',
{ device_id: 'lx-online-' + Math.random().toString(36).slice(2, 8) + Date.now().toString(36).slice(-4) },
{ 'User-Agent': 'lx-music', 'X-Client': 'XingChenMusicSource/v3.2.17 (Android)' });
if (!r?.data?.token) throw new Error('token.php 无 token');
xhTk = r.data.token; xhTs = Date.now();
return xhTk;
})().finally(() => { xhPrm = null; });
return xhPrm;
}
const urlCache = new Map();
const sidMap = new Map();
const noSourceMap = new Map();
const inflight = {};
const pending = [];
let currentPlayingKey = null;
const stats = { play: {}, download: {} };
function markNoSource(source, mid) {
if (!mid) return;
noSourceMap.set(source + ':' + mid, Date.now() + NO_SOURCE_TTL);
}
function isNoSource(source, mid) {
if (!mid) return false;
const key = source + ':' + mid;
const expire = noSourceMap.get(key);
if (!expire) return false;
if (Date.now() > expire) { noSourceMap.delete(key); return false; }
return true;
}
function scoreKey(sid, quality) { return quality ? (sid + '@' + quality) : sid; }
function recOk(action, key, ms) {
const s = stats[action];
if (!s[key]) s[key] = { ok: 0, fail: 0, ms: 0, n: 0 };
const e = s[key];
if (e.n >= STATS_LIMIT) { e.ok *= .5; e.fail *= .5; e.ms *= .5; e.n *= .5; }
e.ok = e.ok * STATS_DECAY + 1;
e.fail *= STATS_DECAY;
e.ms = e.ms * STATS_DECAY + (ms || 0);
e.n = e.n * STATS_DECAY + 1;
}
function recFail(action, key) {
const s = stats[action];
if (!s[key]) s[key] = { ok: 0, fail: 0, ms: 0, n: 0 };
const e = s[key];
if (e.n >= STATS_LIMIT) { e.ok *= .5; e.fail *= .5; e.ms *= .5; e.n *= .5; }
e.fail = e.fail * STATS_DECAY + 1;
e.ok *= STATS_DECAY;
e.n = e.n * STATS_DECAY + 1;
}
function sortByScore(action, list, quality) {
list.sort(function (a, b) {
const sa = stats[action][scoreKey(a, quality)] || stats[action][a];
const sb = stats[action][scoreKey(b, quality)] || stats[action][b];
if (!sa && !sb) return 0;
if (!sa) return -1;
if (!sb) return 1;
const ra = sa.ok / (sa.ok + sa.fail + 1);
const rb = sb.ok / (sb.ok + sb.fail + 1);
if (Math.abs(ra - rb) > 0.1) return rb - ra;
const msA = sa.n > 0 ? sa.ms / sa.n : Infinity;
const msB = sb.n > 0 ? sb.ms / sb.n : Infinity;
return msA - msB;
});
return list;
}
function buildCacheKey(source, mi, quality) {
let id = '';
if (source === 'kg') id = (mi && (mi.hash || mi.songmid || String(mi.id || '').replace(/^kg_/, ''))) || '';
else if (source === 'mg') id = (mi && (mi.copyrightId || mi.songmid || mi.id)) || '';
else id = (mi && (mi.songmid || mi.id || mi.mid)) || '';
const title = (mi && (mi.title || mi.name)) || '';
const artist = (mi && (mi.artist || mi.singer)) || '';
const fb = title + '|' + artist;
return source + ':' + (id || fb) + ':' + quality;
}
function getCachedUrl(key) {
const item = urlCache.get(key);
if (!item) return null;
if (Date.now() > item.expireAt) {
urlCache.delete(key);
sidMap.delete(String(item.url));
return null;
}
return item.url;
}
function setCachedUrl(key, url) {
if (!isValidUrl(url)) return false;
const isPhp = url.toLowerCase().indexOf('.php') >= 0;
urlCache.set(key, { url: url, expireAt: Date.now() + Math.max(60 * 1000, isPhp ? CACHE_TTL - 15 * 60 * 1000 : CACHE_TTL), ts: Date.now() });
if (urlCache.size > CACHE_MAX) {
const arr = [];
urlCache.forEach(function (v, k) { arr.push([k, v]); });
arr.sort(function (a, b) { return a[1].ts - b[1].ts; });
for (let i = 0; i < arr.length - CACHE_MAX; i++) {
const evicted = urlCache.get(arr[i][0]);
if (evicted) sidMap.delete(String(evicted.url));
urlCache.delete(arr[i][0]);
}
}
return true;
}
function cleanupCache() {
const now = Date.now();
const toDel = [];
urlCache.forEach(function (v, k) { if (now > v.expireAt) toDel.push(k); });
for (let i = 0; i < toDel.length; i++) {
const v = urlCache.get(toDel[i]);
if (v) sidMap.delete(String(v.url));
urlCache.delete(toDel[i]);
}
noSourceMap.forEach(function (expire, key) {
if (now > expire) noSourceMap.delete(key);
});
}
function isPendingExpired(e) { return Date.now() - e.pendingTs >= PENDING_MAX_AGE; }
function cleanupExpiredPending() {
for (let i = pending.length - 1; i >= 0; i--) {
if (isPendingExpired(pending[i])) {
const e = pending.splice(i, 1)[0];
if (e.reject) e.reject(new Error('pending timeout'));
}
}
}
function pumpPendingToInflight() {
cleanupExpiredPending();
while (Object.keys(inflight).length < INFLIGHT_MAX && pending.length > 0) {
const e = pending.shift();
if (isPendingExpired(e)) { if (e.reject) e.reject(new Error('pending timeout')); continue; }
startInflight(e);
}
}
function startInflight(entry) {
entry.ts = Date.now();
inflight[entry.id] = entry;
(async function () {
let url = null;
try { url = await fetchUrlBySource(entry.source, entry.musicInfo, entry.quality); }
catch (e) { log(' ⛔ 获取失败 | ' + entry.id + ' | ' + e.message); }
if (isValidUrl(url)) {
setCachedUrl(entry.key, url);
log(' ✅ 获取成功 | ' + entry.id);
if (entry.resolve) entry.resolve(url);
} else {
if (entry.reject) entry.reject(new Error('音源返回了无效的播放地址'));
}
if (inflight[entry.id] === entry) delete inflight[entry.id];
pumpPendingToInflight();
})();
}
function evictOldestInflight(protectId) {
while (Object.keys(inflight).length >= INFLIGHT_MAX) {
let oid = null, ots = Infinity;
for (const id in inflight) {
if (id === protectId || id === currentPlayingKey) continue;
if (inflight[id].ts < ots) { ots = inflight[id].ts; oid = id; }
}
if (!oid) break;
const e = inflight[oid]; e.pendingTs = Date.now(); delete inflight[oid];
if (pending.length >= PENDING_MAX) { const d = pending.shift(); if (d.reject) d.reject(new Error('pending overflow')); }
pending.push(e);
}
}
async function getOrFetchUrl(source, mi, quality) {
const key = buildCacheKey(source, mi, quality);
currentPlayingKey = key;
const c = getCachedUrl(key);
if (c) {
log(' 💾 命中缓存 | ' + key);
return Promise.resolve({ _url: c, _fromCache: true });
}
for (const id in inflight) {
if (inflight[id].key === key) {
return inflight[id].promise.then(function (u) { return { _url: u, _fromCache: false }; });
}
}
for (let i = 0; i < pending.length; i++) {
if (pending[i].key === key) {
const e = pending.splice(i, 1)[0];
if (isPendingExpired(e)) { if (e.reject) e.reject(new Error('pending timeout')); break; }
if (Object.keys(inflight).length >= INFLIGHT_MAX) evictOldestInflight(key);
startInflight(e);
return e.promise.then(function (u) { return { _url: u, _fromCache: false }; });
}
}
cleanupExpiredPending();
let rp, rf;
const promise = new Promise(function (res, rej) { rp = res; rf = rej; });
const entry = { id: key, key: key, source: source, musicInfo: mi, quality: quality, promise: promise, resolve: rp, reject: rf, ts: 0, pendingTs: 0 };
if (Object.keys(inflight).length >= INFLIGHT_MAX) evictOldestInflight(key);
startInflight(entry);
return promise.then(function (u) { return { _url: u, _fromCache: false }; });
}
async function ikun_common(mi, source, q, useKey) {
const id = idOf(mi, source);
const headers = { 'User-Agent': 'lx-music-desktop/2.10.1' };
if (useKey) headers['X-Api-Key'] = IKUN_KEY;
const r = await httpPost('https://c.wwwweb.top/music/url', { source: source, musicId: id, quality: q }, headers);
if (!r || r.code !== 200) throw new Error('ikun获取URL失败');
if (!isValidUrl(r.url)) throw new Error('ikun无URL');
return httpsToHttp(r.url);
}
async function tx_ikun(mi, q) { return ikun_common(mi, 'tx', q, true); }
async function wy_ikun(mi, q) { return ikun_common(mi, 'wy', q, false); }
async function wy_ikun_key(mi, q) { return ikun_common(mi, 'wy', q, true); }
async function kg_ikun(mi, q) { return ikun_common(mi, 'kg', q, true); }
async function kw_ikun(mi, q) { return ikun_common(mi, 'kw', q, true); }
const IKUN2_QUALITY = {
tx: ['128k', '320k', 'flac', 'flac24bit', 'hires', 'atmos', 'atmos_plus', 'master'],
wy: ['128k', '320k', 'flac', 'flac24bit', 'hires', 'atmos', 'atmos_plus', 'master', 'jymaster'],
kg: ['128k', '320k', 'flac', 'flac24bit', 'hires', 'atmos', 'master'],
kw: ['128k', '320k', 'flac', 'flac24bit', 'hires'],
};
async function ikun2_common(mi, source, q) {
const supported = IKUN2_QUALITY[source];
if (!supported || supported.indexOf(q) < 0) throw new Error('ikun2不支持 ' + q);
const id = idOf(mi, source);
if (!id) throw new Error('ikun2缺ID');
const r = await httpPost('https://c.wwwweb.top/music/url',
{ source: source, musicId: id, quality: q },
{ 'User-Agent': 'lx-music-desktop/2.10.1', 'X-Api-Key': IKUN_KEY2 });
if (!r || r.code !== 200) throw new Error('ikun2获取URL失败');
if (!isValidUrl(r.url)) throw new Error('ikun2无URL');
return httpsToHttp(r.url);
}
async function tx_ikun2(mi, q) { return ikun2_common(mi, 'tx', q); }
async function wy_ikun2(mi, q) { return ikun2_common(mi, 'wy', q); }
async function kg_ikun2(mi, q) { return ikun2_common(mi, 'kg', q); }
async function kw_ikun2(mi, q) { return ikun2_common(mi, 'kw', q); }
async function tx_anime(mi, q) {
const mid = idOf(mi, 'tx');
if (!mid) throw new Error('anime缺mid');
const map = { '128k': '128k', '320k': '192k', 'flac': 'flac', 'master': 'master', 'atmos': '320k' };
const r = await httpPost('https://animemusic.bzxhkj.com/v1/index.php/music/url?key=', { source: 'tx', musicId: mid, quality: map[q] || q }, { 'User-Agent': 'lx-music-desktop/2.10.1', 'X-Api-Key': '' });
if (!r || r.code !== 200) throw new Error('anime获取URL失败');
if (!isValidUrl(r.url)) throw new Error('anime无URL');
return httpsToHttp(r.url);
}
async function wy_anime(mi, q) {
const id = idOf(mi, 'wy');
if (!id) throw new Error('anime缺id');
const map = { '128k': '128k' };
const r = await httpPost('https://animemusic.bzxhkj.com/v1/index.php/music/url?key=', { source: 'wy', musicId: id, quality: map[q] || q }, { 'User-Agent': 'lx-music-desktop/2.10.1', 'X-Api-Key': '' });
if (!r || r.code !== 200) throw new Error('anime获取URL失败');
if (!isValidUrl(r.url)) throw new Error('anime无URL');
return httpsToHttp(r.url);
}
async function kg_anime(mi, q) {
const hash = idOf(mi, 'kg');
if (!hash) throw new Error('anime缺hash');
const map = { '128k': '128k', '320k': '320k', 'flac': 'flac', 'master': 'master' };
const r = await httpPost('https://animemusic.bzxhkj.com/v1/index.php/music/url?key=', { source: 'kg', musicId: hash, quality: map[q] || q }, { 'User-Agent': 'lx-music-desktop/2.10.1', 'X-Api-Key': '' });
if (!r || r.code !== 200) throw new Error('anime获取URL失败');
if (!isValidUrl(r.url)) throw new Error('anime无URL');
return httpsToHttp(r.url);
}
async function kw_anime(mi, q) {
const rid = idOf(mi, 'kw');
if (!rid) throw new Error('anime缺rid');
const map = { '128k': '128k', '320k': '192k', 'flac': 'flac' };
const r = await httpPost('https://animemusic.bzxhkj.com/v1/index.php/music/url?key=', { source: 'kw', musicId: rid, quality: map[q] || q }, { 'User-Agent': 'lx-music-desktop/2.10.1', 'X-Api-Key': '' });
if (!r || r.code !== 200) throw new Error('anime获取URL失败');
if (!isValidUrl(r.url)) throw new Error('anime无URL');
return httpsToHttp(r.url);
}
async function qq_cy(mi, q) {
const mid = idOf(mi, 'tx');
if (isNoSource('tx_cy', mid)) throw new Error('迟言已标记无源');
const map = { '128k': 'm4a', '320k': '320k', 'flac': 'flac', 'flac24bit': 'flac' };
const r = await httpGet('https://cyapi.top/API/qq_music.php', { apikey: XINGCHEN_KEY, type: 'json', mid: mid, quality: map[q] || '320k' });
if (!r || !isValidUrl(r.url)) {
markNoSource('tx_cy', mid);
throw new Error('迟言无URL');
}
if (!/stream\.qqmusic\.qq\.com/i.test(r.url)) {
markNoSource('tx_cy', mid);
throw new Error('迟言假链接');
}
return httpsToHttp(r.url);
}
async function qq_xhs(mi) {
const mid = idOf(mi, 'tx');
const r = await httpGet('https://api.xunhuisi.store/API/QQMusic/Song.php', { id: mid, quality: 'high', type: 'json' });
if (!r || !isValidUrl(r.music_url)) throw new Error('巡回寺无URL');
return httpsToHttp(r.music_url);
}
async function qq_hyw(mi, q) {
const mid = idOf(mi, 'tx');
const r = await httpGet('http://103.79.184.97/api/music/url', { source: 'tx', songId: mid, quality: q, key: HYW_KEY }, { 'User-Agent': 'Mozilla/5.0', 'X-Card-Key': HYW_KEY });
const u = pickField(r, ['url', 'data.url']);
if (!u) throw new Error('HYW无URL');
return u;
}
async function qq_tang(mi, q) {
const mid = idOf(mi, 'tx');
const r = await httpGet('https://tang.api.s01s.cn/music_open_api.php', { mid: mid });
if (!r || typeof r !== 'object') throw new Error('tang无响应');
const map = {
'master': 'song_play_url_sq',
'jymaster': 'song_play_url_sq',
'atmos_plus': 'song_play_url_pq',
'atmos': 'song_play_url_pq',
'jyeffect': 'song_play_url_pq',
'sky': 'song_play_url_pq',
'flac24bit': 'song_play_url_sq',
'hires': 'song_play_url_sq',
'flac': 'song_play_url_sq',
'320k': 'song_play_url_hq',
'128k': 'song_play_url_standard'
};
const field = map.hasOwnProperty(q) ? map[q] : 'song_play_url_sq';
if (r[field] && typeof r[field] === 'string' && r[field].trim()) {
return httpsToHttp(r[field].trim());
}
throw new Error('tang无 ' + q + ' 链接');
}
async function qq_ht(mi, q) {
const mid = idOf(mi, 'tx');
const map = { master: 'jymaster', atmos_plus: '2999', atmos: 'jyeffect', flac: 'lossless', flac24bit: 'lossless', '320k': 'exhigh', '128k': 'standard' };
const r = await httpPost('https://musicserver.haitangw.cc/v1/music/resolve-url', { source: 'tx', rid: mid, level: map[q] || 'exhigh' }, { 'User-Agent': 'Mozilla/5.0' });
const u = pickField(r, ['data.url']);
if (!u) throw new Error('长青海棠无URL');
return u;
}
async function qq_nki(mi) {
const mid = idOf(mi, 'tx');
const kw = (mi && mi.title) || mid;
const r = await httpGet('https://api.nki.pw/API/music_open_api.php', { apikey: NKI_KEY, msg: kw, mid: mid, n: 1, json: 1 });
const u = pickField(r, ['song_play_url_sq','song_play_url_pq','song_play_url_hq','song_play_url_standard','song_play_url_fq']);
if (!u) throw new Error('西瓜糖无URL');
return u;
}
async function qq_yx(mi, q) {
const title = (mi && (mi.title || mi.name)) || '';
if (!title) throw new Error('云汐缺歌名');
const wantMid = idOf(mi, 'tx');
const singer = (mi && (mi.artist || mi.singer)) || '';
const mainSinger = singer.split(/[\/&、,，]/)[0].trim();
const kw = mainSinger ? (title + ' ' + mainSinger) : title;
const map = {
'128k': '1', '192k': '1', '320k': '1',
'flac': '4', 'flac24bit': '4',
'master': '5', 'jymaster': '5', 'hires': '5',
'atmos_plus': '7', 'atmos': '1'
};
const type = map[q] || '1';
log(' [yx] ▶ 云汐双路并发 | 目标 mid=' + wantMid + ' | kw="' + kw + '" | type=' + type);
const pFast = httpGet('https://a.aa.cab/qq.music', {
msg: kw, num: 1, n: 1, type: type, html: 'true'
}).catch(e => { throw new Error('极速失败: ' + e.message); });
const pList = httpGet('https://a.aa.cab/qq.music', {
msg: kw, num: 10, type: type, html: 'true'
}).catch(e => { throw new Error('列表失败: ' + e.message); });
function isMatch(item) {
if (!item) return false;
const rTitle = String(item.song || '').trim().toLowerCase();
const rSinger = String(item.singer || '').trim().toLowerCase();
const wTitle = title.trim().toLowerCase();
const wSinger = mainSinger.toLowerCase();
const titleMatch = (rTitle === wTitle);
const singerMatch = !wSinger || rSinger.indexOf(wSinger) >= 0 || wSinger.indexOf(rSinger) >= 0;
return titleMatch && singerMatch;
}
let fallbackUrl = null;
try {
const r1 = await pFast;
const item = r1 && r1.data && (Array.isArray(r1.data) ? r1.data[0] : r1.data);
if (item) {
const u = pickField(r1, ['data.music', 'data.data.music', 'music', 'playUrl', 'url', 'data.url']);
if (u) fallbackUrl = u;
if (isMatch(item)) {
log(' [yx] 🎯 极速命中 | ' + item.song + ' - ' + item.singer);
if (fallbackUrl) return fallbackUrl;
}
}
} catch (e) { log(' [yx] ⚠️ 极速错误: ' + e.message); }
let list = [];
try {
const r2 = await pList;
if (r2 && Array.isArray(r2.data)) list = r2.data;
else if (r2 && r2.data && r2.data.mid) list = [r2.data];
else if (r2 && Array.isArray(r2.data.list)) list = r2.data.list;
} catch (e) { log(' [yx] ⚠️ 列表错误: ' + e.message); }
let hit = null;
if (list.length > 0) {
if (wantMid) {
for (let i = 0; i < list.length; i++) {
if (String(list[i].mid) === String(wantMid)) {
hit = list[i];
log(' [yx] 🎯 列表命中 MID | n=' + hit.num);
break;
}
}
}
if (!hit) {
for (let i = 0; i < list.length; i++) {
if (isMatch(list[i])) {
hit = list[i];
log(' [yx] 🎯 列表模糊命中 | ' + hit.song + ' | n=' + hit.num);
break;
}
}
}
if (!hit) {
hit = list[0];
log(' [yx] ⚠️ 强行兜底取第 1 首 | ' + hit.song + ' | n=' + hit.num);
}
}
if (hit) {
try {
const targetNum = hit.num;
const r3 = await httpGet('https://a.aa.cab/qq.music', {
msg: kw, num: targetNum, n: targetNum, type: type, html: 'true'
});
const u = pickField(r3, ['data.music', 'data.data.music', 'music', 'playUrl', 'url', 'data.url']);
if (u) {
log(' [yx] ✅ 列表取链成功 (num=' + targetNum + ', n=' + targetNum + ')');
return u;
}
} catch (e) { log(' [yx] ⚠️ 列表取链失败: ' + e.message); }
}
if (fallbackUrl) {
log(' [yx] 🚑 兜底使用极速备用链接');
return fallbackUrl;
}
throw new Error('云汐彻底无源');
}
async function qq_zddyr(mi, q) {
const mid = idOf(mi, 'tx');
const map = { master: 'master', hires: 'hires', flac: 'flac', '320k': '320k', '128k': '128k' };
const quality = map[q] || '320k';
const token = await xhGetTk();
const r = await httpGet('https://yy.zddyr.top/lx/api/',
{ source: 'tx', songmid: mid, quality: quality },
{ 'X-Token': token, 'X-Client': 'XingChenMusicSource/v3.2.17 (Android)', 'User-Agent': 'lx-music' });
const u = pickField(r, ['url', 'data.url']);
if (!u) throw new Error('星尘(tx)无URL: ' + ((r && r.msg) || ''));
return u;
}
async function tx_ly(mi, q) {
const mid = idOf(mi, 'tx');
const map = { '128k': '4', '320k': '8', flac: '10', flac24bit: '16', hires: '16', atmos: '12', master: '16' };
const quality = map[q] || '8';
const url = `https://api.vkeys.cn/v2/music/tencent/geturl?mid=${mid}&quality=${quality}`;
const r = await httpGet(url);
if (!r || r.code !== 200 || !r.data || !r.data.url) {
throw new Error('落月无URL');
}
const qualityStr = r.data.quality || '';
if (qualityStr.indexOf('试听') >= 0) {
throw new Error('落月返回了试听片段');
}
return httpsToHttp(r.data.url);
}
async function wy_cy(mi, q) {
const id = idOf(mi, 'wy');
const map = {
master: 'jymaster',
jymaster: 'jymaster',
atmos: 'hires',
atmos_plus: 'lossless',
sky: 'lossless',
jyeffect: 'lossless',
hires: 'hires',
flac24bit: 'hires',
flac: 'lossless',
'320k': 'exhigh',
'128k': 'standard'
};
const r = await httpGet('https://www.cunyuapi.top/163music_play', { id: id, quality: map[q] || 'exhigh', api_token: CUNYU_TOKEN });
const u = r && r.song_file_url;
if (!isValidUrl(u)) throw new Error('存雨无URL');
return httpsToHttp(u);
}
async function wy_xt(mi, q) {
const id = idOf(mi, 'wy');
if (!id || !/^\d+$/.test(id)) throw new Error('xt: 缺少有效数字 ID');
const map = {
'128k': 1,
'320k': 2,
'flac': 3,
'flac24bit': 4,
'hires': 4,
'atmos': 5,
'atmos_plus': 5,
'master': 7,
'jymaster': 7
};
const yz = map[q] || 7;
const url = `https://api.s0o1.com/API/wyy_music/?id=${id}&yz=${yz}`;
const res = await httpGet(url);
if (!res || !res.data || !res.data.url) {
throw new Error('xt 接口未返回 URL');
}
return res.data.url.replace(/^https:\/\//i, 'http://');
}
async function wy_xtv2(mi, q) {
const id = idOf(mi, 'wy');
if (!id || !/^\d+$/.test(id)) throw new Error('xtv2: 缺少有效数字 ID');
const map = {
'128k': 'standard',
'320k': 'exhigh',
'flac': 'lossless',
'flac24bit': 'hires',
'hires': 'hires',
'atmos': 'jyeffect',
'atmos_plus': 'jyeffect',
'master': 'jymaster',
'jymaster': 'jymaster'
};
const level = map[q] || 'lossless';
const url = `https://api.s0o1.com/API/wyy_v2/?action=song&url=${id}&level=${level}&type=json`;
const res = await httpGet(url);
if (!res || res.status !== 200 || !res.data || !res.data.url) {
throw new Error('xtv2 接口未返回 URL');
}
return res.data.url.replace(/^https:\/\//i, 'http://');
}
async function wy_nx(mi, q) {
const id = idOf(mi, 'wy');
const map = {
master: 'jymaster',
jymaster: 'jymaster',
atmos: 'jyeffect',
atmos_plus: 'lossless',
sky: 'lossless',
jyeffect: 'lossless',
hires: 'hires',
flac24bit: 'hires',
flac: 'lossless',
'320k': 'exhigh',
'128k': 'standard'
};
const r = await httpGet('https://mcp.nianxinxz.com/share/ceshi/wy.php', { id: id, level: map[q] || 'exhigh' });
if (!r || r.code !== 200) throw new Error('念心无数据');
if (!isValidUrl(r.url)) throw new Error('念心无URL');
return httpsToHttp(r.url);
}
async function wy_cy2(mi, q) {
const id = idOf(mi, 'wy');
if (!id) throw new Error('迟言缺ID');
const songName = (mi && (mi.title || mi.name)) || '';
const singerName = (mi && (mi.artist || mi.singer)) || '';
const msg = `${songName} ${singerName}`.trim();
if (!msg) throw new Error('迟言缺搜索词');
const searchData = await httpGet('https://cyapi.top/API/netease.php', {
apikey: XINGCHEN_KEY, msg: msg, type: 'json'
});
const list = searchData && searchData.list ? searchData.list : [];
if (!list.length) throw new Error('迟言搜索无结果');
let targetN = 1;
let idIndex = list.findIndex(item => String(item.id) === String(id));
if (idIndex !== -1) {
targetN = idIndex + 1;
} else {
for (let i = 0; i < list.length; i++) {
if ((list[i].name || '').includes(songName) && (list[i].artists || '').includes(singerName)) {
targetN = i + 1; break;
}
}
}
const data = await httpGet('https://cyapi.top/API/netease.php', {
apikey: XINGCHEN_KEY, msg: msg, n: String(targetN), type: 'json'
});
if (!data || !isValidUrl(data.url)) {
throw new Error('迟言无URL');
}
return httpsToHttp(data.url);
}
async function wy_ht(mi, q) {
const id = idOf(mi, 'wy');
const map = {
master: 'jymaster',
jymaster: 'jymaster',
atmos: 'jyeffect',
atmos_plus: 'lossless',
sky: 'lossless',
jyeffect: 'lossless',
hires: 'hires',
flac24bit: 'hires',
flac: 'lossless',
'320k': 'exhigh',
'128k': 'standard'
};
const r = await httpPost('https://musicserver.haitangw.cc/v1/music/resolve-url', { source: 'wy', rid: id, level: map[q] || 'exhigh' }, { 'User-Agent': 'Mozilla/5.0' });
const u = pickField(r, ['data.url']);
if (!u) throw new Error('长青海棠无URL');
return u;
}
async function wy_ht2(mi, q) {
const id = idOf(mi, 'wy');
const map = {
'master': 'jymaster',
'jymaster': 'jymaster',
'atmos': 'sky',
'atmos_plus': 'lossless',
'sky': 'sky',
'jyeffect': 'jyeffect',
'hires': 'hires',
'flac24bit': 'hires',
'flac': 'lossless',
'320k': 'exhigh',
'128k': 'standard'
};
const level = map[q];
if (!level) throw new Error('海棠(net)不支持 ' + q);
const r = await httpGet('https://musicapi.haitangw.net/music/wy_song_kw.php',
{ type: 'json', id: id, level: level });
const u = r?.data?.url;
if (!isValidUrl(u)) throw new Error('海棠(net)无URL');
return httpsToHttp(u);
}
async function wy_ht3(mi, q) {
const id = idOf(mi, 'wy');
const map = {
'master': 'jymaster',
'jymaster': 'jymaster',
'atmos': 'sky',
'atmos_plus': 'lossless',
'sky': 'sky',
'jyeffect': 'jyeffect',
'hires': 'hires',
'flac24bit': 'hires',
'flac': 'lossless',
'320k': 'exhigh',
'128k': 'standard'
};
const level = map[q];
if (!level) throw new Error('海棠(cc)不支持 ' + q);
const r = await httpGet('https://music.haitangw.cc/music/wy_song_kw.php',
{ type: 'json', id: id, level: level });
const u = r?.data?.url;
if (!isValidUrl(u)) throw new Error('海棠(cc)无URL');
return httpsToHttp(u);
}
async function wy_hyw(mi, q) {
const id = idOf(mi, 'wy');
const r = await httpGet('http://103.79.184.97/api/music/url', { platform: 'wy', songId: id, quality: q, key: HYW_KEY }, { 'User-Agent': 'lx-music-mobile/2.0.0', 'X-Card-Key': HYW_KEY });
const u = pickField(r, ['url', 'data.url', 'data']);
if (!u) throw new Error('HYW无URL');
return u;
}
async function wy_zddyr(mi, q) {
const id = idOf(mi, 'wy');
const map = { hires: 'hires', flac: 'flac', '320k': '320k', '128k': '128k' };
const quality = map[q];
if (!quality) throw new Error('星尘(wy)不支持 ' + q);
const token = await xhGetTk();
const r = await httpGet('https://yy.zddyr.top/lx/api/',
{ source: 'wy', songmid: id, quality: quality },
{ 'X-Token': token, 'X-Client': 'XingChenMusicSource/v3.2.17 (Android)', 'User-Agent': 'lx-music' });
const u = pickField(r, ['url', 'data.url']);
if (!u) throw new Error('星尘(wy)无URL');
return u;
}
async function wy_qgg(mi, q) {
const id = idOf(mi, 'wy');
const map = { '128k': 'standard', '320k': 'exhigh', flac: 'lossless', flac24bit: 'hires' };
const level = map[q];
if (!level) throw new Error('芩鬼鬼不支持 ' + q);
const r = await httpGet('https://api.cenguigui.cn/api/netease/music_v1.php',
{ id: id, type: 'json', level: level });
const u = pickField(r, ['data.url']);
if (!u) throw new Error('芩鬼鬼无URL');
return u;
}
async function wy_nanorocky(mi, q) {
const id = idOf(mi, 'wy');
const map = {
'128k': '128', '320k': '320', flac: '999', flac24bit: '999',
hires: '1999', atmos: '2999', master: '9999'
};
const br = map[q] || '320';
const url = `https://metingapi.nanorocky.top/?server=netease&type=url&br=${br}&id=${id}`;
return new Promise((resolve, reject) => {
httpRequest(url, {
method: 'GET', timeout: 8000,
headers: { 'Range': 'bytes=0-10', 'User-Agent': 'Mozilla/5.0' }
}, (err, res) => {
if (err) return resolve(url);
if (res.statusCode === 200 || res.statusCode === 206) return resolve(url);
reject(new Error('nanorocky状态码异常: ' + res.statusCode));
});
});
}
async function wy_bugpk(mi, q) {
const id = idOf(mi, 'wy');
const map = {
master: 'jymaster',
atmos: 'sky',
hires: 'hires',
flac24bit: 'lossless',
flac: 'lossless',
'320k': 'exhigh',
'128k': 'standard'
};
const level = map[q] || 'standard';
const res = await httpRequest(`https://api.bugpk.com/api/163_music?type=json&ids=${id}&level=${level}`, {
method: 'GET',
timeout: 15000
});
if (res.body && res.body.status === 200 && res.body.url) {
return httpsToHttp(res.body.url);
}
throw new Error('BugPk无有效URL');
}
async function wy_gdstudio(mi, q) {
const id = idOf(mi, 'wy');
if (!id) throw new Error('gdstudio缺ID');
const map = {
'128k': 128,
'320k': 320,
flac: 1411,
};
const br = map[q] || 1411;
const base = {
use_xbridge3: 'true', loader_name: 'forest', need_sec_link: '1',
sec_link_scene: 'im', theme: 'light',
types: 'url', source: 'netease', id: id
};
const API = 'https://music-api.gdstudio.xyz/api.php';
async function call(b) {
const r = await httpGet(API, Object.assign({ br: b }, base));
if (!r || !isValidUrl(r.url)) throw new Error('gdstudio无URL');
return r.url;
}
try { return await call(br); } catch (e) {
await new Promise(function (res) { setTimeout(res, 1200); });
try { return await call(br); } catch (e2) {
if (br !== 320) { try { return await call(320); } catch (e3) {} }
if (br !== 128) { try { return await call(128); } catch (e4) {} }
throw new Error('gdstudio失败');
}
}
}
async function kg_ht(mi, q) {
const hash = idOf(mi, 'kg');
const map = { master: 'master', jymaster: 'jymaster', hires: 'hires', atmos: 'atmos', flac24bit: 'flac24bit', flac: 'lossless', '320k': '320k', '128k': '128k' };
const level = map[q] || '320k';
const r = await httpPost('https://musicserver.haitangw.cc/v1/music/resolve-url',
{ source: 'kg', rid: hash, level: level },
{ 'User-Agent': 'Mozilla/5.0' });
const u = pickField(r, ['data.url']);
if (!u) throw new Error('长青海棠无URL');
return u;
}
async function kg_zddyr(mi, q) {
const hash = idOf(mi, 'kg');
const map = { master: 'master', hires: 'hires', flac24bit: 'hires', flac: 'flac', '320k': '320k', '128k': '128k' };
const quality = map[q] || '320k';
const token = await xhGetTk();
const r = await httpGet('https://yy.zddyr.top/lx/api/',
{ source: 'kg', mainHash: hash, quality: quality },
{ 'X-Token': token, 'X-Client': 'XingChenMusicSource/v3.2.17 (Android)', 'User-Agent': 'lx-music' });
if (!r || !isValidUrl(r.url)) throw new Error('星尘无URL');
return httpsToHttp(r.url);
}
async function kg_hyw(mi, q) {
const hash = idOf(mi, 'kg');
const map = { master: 'master', hires: 'hires', flac24bit: 'hires', flac: 'flac', '320k': '320k', '128k': '128k' };
const quality = map[q] || '320k';
const url = 'http://103.79.184.97/api/music/url?source=kg&songId=' + encodeURIComponent(hash) + '&quality=' + encodeURIComponent(quality) + '&key=' + encodeURIComponent(HYW_KEY);
const res = await httpRequest(url, { method: 'GET', headers: { 'User-Agent': 'Mozilla/5.0', 'X-Card-Key': HYW_KEY }, timeout: 3000 });
const u = pickField(res.body, ['url', 'data.url']);
if (!u) throw new Error('HYW无URL');
return u;
}
async function sync_kw(mi, q) {
if (mi.source === 'kw') throw new Error('同平台无需兜底');
await new Promise(resolve => setTimeout(resolve, KW_FALLBACK_DELAY));
if (mi.__is_resolved) throw new Error('静默退出');
let expectedDuration = 0;
if (mi.interval) {
if (typeof mi.interval === 'string' && mi.interval.indexOf(':') > -1) {
const parts = mi.interval.split(':');
if (parts.length === 2) expectedDuration = (parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10)) * 1000;
} else {
expectedDuration = Number(mi.interval || 0);
if (expectedDuration > 0 && expectedDuration < 10000) expectedDuration *= 1000;
}
}
const mainArtist = String(mi.artist || mi.singer || '').split(/[\/&、,，]/)[0].trim();
const title = mi.title || mi.name || '';
const keywordArr = [];
if (title && mainArtist) keywordArr.push(title + ' ' + mainArtist);
if (title) keywordArr.push(title);
let list = [];
for (const keyword of keywordArr) {
const url = 'http://search.kuwo.cn/r.s?client=kt&all=' + encodeURIComponent(keyword) +
'&pn=0&rn=30&uid=794762570&ver=kwplayer_ar_9.2.2.1&vipver=1' +
'&show_copyright_off=1&newver=1&ft=music&cluster=0&strategy=2012' +
'&encoding=utf8&rformat=json&vermerge=1&mobi=1&issubtitle=1&_=' + Date.now();
try {
let res = await httpGet(url, null, { 'User-Agent': 'Mozilla/5.0' });
if (typeof res === 'string') {
let s = res.trim();
if (s.charAt(0) === '(') s = s.slice(1);
if (s.charAt(s.length - 1) === ')') s = s.slice(0, -1);
try { res = JSON.parse(s); } catch (e) { try { res = JSON.parse(s.replace(/'/g, '"')); } catch (e2) {} } } if (res && res.abslist && res.abslist.length > 0) { list = res.abslist; break; } } catch(e) {} } if (!list.length) throw new Error('搜索无结果'); let rid = ''; const stripHtml = (s) => String(s || '').replace(/&nbsp;/g, ' ').replace(/<[^>]+>/g, '').trim(); const wT = stripHtml(mi.title || mi.name || '').toLowerCase(); const wA = stripHtml(mainArtist).toLowerCase(); const wTNoSp = wT.replace(/\s+/g, ''); const wANoSp = wA.replace(/\s+/g, ''); let exactMatch = null, durationMatch = null; let closestDurationItem = null; let minDiff = Infinity; for (const o of list) { const curRid = o.MUSICRID ? String(o.MUSICRID).replace(/^MUSIC_/, '') : (o.DC_TARGETID || o.rid || ''); if (!curRid) continue; const rTitle = stripHtml(o.SONGNAME || o.NAME || '').toLowerCase(); const rArtist = stripHtml(o.ARTIST || o.FARTIST || '').toLowerCase(); const rDuration = Number(o.DURATION || 0) * 1000; const rTitleNoSp = rTitle.replace(/\s+/g, ''); const rArtistNoSp = rArtist.replace(/\s+/g, ''); if (expectedDuration && rDuration) { const diff = Math.abs(rDuration - expectedDuration); if (diff < minDiff) { minDiff = diff; closestDurationItem = { rid: curRid, duration: rDuration }; } } let titleOk = false; if (rTitle === wT || rTitle.indexOf(wT) >= 0) { titleOk = true; } else if (rTitleNoSp === wTNoSp || rTitleNoSp.indexOf(wTNoSp) >= 0) { titleOk = true; } else if (wTNoSp.indexOf(rTitleNoSp) >= 0) { if (rTitleNoSp.length >= 2 && rTitleNoSp.length >= wTNoSp.length * 0.5) { titleOk = true; } } let artistOk = false; if (!wA || rArtist.indexOf(wA) >= 0 || wA.indexOf(rArtist) >= 0) { artistOk = true; } else if (wANoSp && (rArtistNoSp.indexOf(wANoSp) >= 0 || wANoSp.indexOf(rArtistNoSp) >= 0)) { artistOk = true; } if (titleOk && artistOk) { const item = { rid: curRid, duration: rDuration }; if (!exactMatch) exactMatch = item; if (expectedDuration && item.duration && Math.abs(item.duration - expectedDuration) < 5000) { durationMatch = item; break; } } } rid = (durationMatch || exactMatch)?.rid; const isLossless = STRICT_LEVELS.indexOf(q) >= 0; if (!rid && !isLossless) { if (closestDurationItem) { rid = closestDurationItem.rid; } else { const firstValid = list.find(o => o.MUSICRID || o.DC_TARGETID || o.rid); if (firstValid) { rid = firstValid.MUSICRID ? String(firstValid.MUSICRID).replace(/^MUSIC_/, '') : (firstValid.DC_TARGETID || firstValid.rid); } } } if (!rid) throw new Error('未匹配到合适音源'); if (mi.__is_resolved) throw new Error('静默退出'); const kwMi = Object.assign({}, mi, { rid: rid, songmid: rid, id: 'kw_' + rid }); return await kw_mobi(kwMi, q); } async function kw_mobi(mi, q) { const rid = idOf(mi, 'kw'); const map = { master: '20900kmflac', atmos_plus: '20501kmflac', atmos: '20201kmflac', hires: '2000kflac', flac24bit: '2000kflac', flac: '2000kflac', '320k': '320kmp3', '128k': '128kmp3' }; const r = await httpGet('http://nmobi.kuwo.cn/mobi.s', { f: 'web', user: 0, source: 'kwplayerhd_ar_6.6.6.6_tianbao_T1A_qirui.apk', type: 'convert_url_with_sign', rid: rid, br: map[q] || '320kmp3' }, { 'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36' }); const u = pickField(r, ['data.url']); if (!u) throw new Error('酷我手机无URL'); return u; } async function kw_car(mi, q) { const rid = idOf(mi, 'kw'); const map = { '128k': '128kmp3', '320k': '320kmp3', flac: '2000kflac', flac24bit: '2000kflac', hires: '2000kflac' }; const r = await httpGet('http://mobi.kuwo.cn/mobi.s', { f: 'web', user: 0, source: 'kwplayercar_ar_6.0.0.9_B_jiakong_vh.apk', type: 'convert_url_with_sign', br: map[q] || '320kmp3', sig: 0, rid: rid }, { 'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36' }); const u = pickField(r, ['data.url']); if (!u) throw new Error('酷我车机无URL'); return u; } async function kw_zx(mi, q) { const rid = idOf(mi, 'kw'); const map = { master: 'master', atmos_plus: 'atmos_plus', atmos: 'atmos' }; const level = map[q]; if (!level) throw new Error('酷我专线不支持 ' + q); return 'http://175.27.166.236:8928/kwstream?id=' + encodeURIComponent(rid) + '&level=' + encodeURIComponent(level) + '&stream=1'; } async function kw_ht(mi, q) { const rid = idOf(mi, 'kw'); const map = { master: 'master', atmos_plus: 'atmos_plus', atmos: 'atmos' }; const level = map[q]; if (!level) throw new Error('长青海棠(kw)不支持 ' + q); const r = await httpPost('https://musicserver.haitangw.cc/v1/music/resolve-url', { source: 'kw', rid: rid, level: level }, { 'User-Agent': 'Mozilla/5.0' }); const u = pickField(r, ['data.url']); if (!u) throw new Error('长青海棠(kw)无URL'); return u; } async function mg_wen(mi, q) { const map = { '128k': 'PQ', '320k': 'HQ', flac: 'SQ', flac24bit: 'SQ', hires: 'SQ', master: 'SQ', atmos: 'SQ', atmos_plus: 'SQ' }; const quality = map[q] || 'HQ'; const realId = await miguInternalId(mi); const r = await httpGet('http://101.200.224.166/musicfree/index.php', { key: MIGU_KEY, action: 'musicSource', id: realId, quality: quality }); if (!r || !isValidUrl(r.url)) throw new Error('温部署无URL'); return httpsToHttp(r.url); } async function mg_sy(mi, q) { const rawTitle = (mi && (mi.title || mi.name)) || ''; const rawArtist = (mi && (mi.artist || mi.singer)) || ''; const title = String(rawTitle) .replace(/[（(][^）)]*[）)]/g, '') .replace(/[-—]\s*/g, ' ') .replace(/\s+/g, ' ') .trim(); const kw = [title, rawArtist].filter(Boolean).join(' ').trim(); const map = { '128k': 'PQ', '320k': 'HQ', flac: 'SQ', flac24bit: 'ZQ24', hires: 'ZQ24', master: 'ZQ32', atmos: 'ZQ24', atmos_plus: 'ZQ32', }; const br = map[q] || 'HQ'; if (!kw) throw new Error('星尘溯音缺关键词(' + br + ')'); const r = await httpGet('https://oiapi.net/api/MiGu_Music', { msg: kw, br: br, n: 1 }); if (!r || r.code !== 1 || !r.data || !r.data.url) { throw new Error('星尘溯音无URL(' + br + ') code=' + (r && r.code) + ' kw="' + kw + '"'); } return r.data.url; } async function mg_zddyr(mi, q) { const map = { '128k': '128k', '320k': '320k', flac: 'flac', flac24bit: 'flac', hires: 'flac' }; const quality = map[q] || '320k'; const realId = await miguInternalId(mi); const token = await xhGetTk(); const name = (mi && (mi.title || mi.name)) || ''; const singer = (mi && (mi.artist || mi.singer)) || ''; const url = 'https://yy.zddyr.top/lx/api/?source=migu' + '&name=' + encodeURIComponent(name) + '&singer=' + encodeURIComponent(singer) + '&songmid=' + encodeURIComponent(realId) + '&quality=' + encodeURIComponent(quality); const r = await httpGet(url, null, { 'X-Token': token, 'X-Client': 'XingChenMusicSource/v3.2.17 (Android)', 'User-Agent': 'lx-music', }); if (!r || !isValidUrl(r.url)) throw new Error('星尘无URL'); return httpsToHttp(r.url); } async function mg_zddyr2(mi, q) { const map = { '128k': '128k', '320k': '320k', flac: 'flac', flac24bit: 'flac', hires: 'flac' }; const quality = map[q] || '320k'; const realId = await miguInternalId(mi); const url = 'https://yy.zddyr.top/lx/api/?source=migu' + '&songmid=' + encodeURIComponent(realId) + '&quality=' + encodeURIComponent(quality); const r = await httpGet(url); if (!r || !isValidUrl(r.url)) throw new Error('星尘2无URL'); return httpsToHttp(r.url); } async function serialTry(candidates, mi, q, platform, action, totalTimeoutMs) { if (candidates.length === 0) throw new Error('无候选源'); const startTs = Date.now(); const isLossless = STRICT_LEVELS.indexOf(q) >= 0; const expSize = isLossless ? expectedSize(mi, q) : 0; return new Promise(function (resolve, reject) { let done = false; let activeCount = 0; let firedCount = 0; const totalCount = candidates.length; const errors = []; const timers = []; timers.push(setTimeout(function () { if (done) return; done = true; clearTimers(); reject(new Error(platform + (action === 'download' ? '严格模式' : '播放') + '全部失败: ' + errors.join(' | '))); }, totalTimeoutMs)); function clearTimers() { for (let i = 0; i < timers.length; i++) clearTimeout(timers[i]); timers.length = 0; } function recordFail(cand, reason) { if (done) return; errors.push(cand.sid + ':' + reason); recFail(action, scoreKey(cand.sid, q)); } function checkAllFailed() { if (!done && firedCount === totalCount && activeCount === 0) { done = true; clearTimers(); reject(new Error(platform + (action === 'download' ? '严格模式' : '播放') + '全部失败: ' + errors.join(' | '))); } } function fireAll() { if (done) return; for (let i = 0; i < candidates.length; i++) { const cand = candidates[i]; timers.push(setTimeout(function () { if (done) { firedCount++; checkAllFailed(); return; } firedCount++; activeCount++; handleCandidate(cand).finally(() => { activeCount--; checkAllFailed(); }); }, i * SOURCE_STEP_GAP)); } } async function handleCandidate(cand) { const elapsed = Date.now() - startTs; const left = totalTimeoutMs - elapsed; if (left <= 800) { recordFail(cand, '总超时'); return; } const perTimeout = left; if (!done) log(' 🔄 [' + cand.sid + '] 尝试 | ' + q + ' | 剩余总超时 ' + perTimeout + 'ms'); const t0 = Date.now(); let url; try { url = await Promise.race([ cand.fn(mi, q), new Promise(function (_, rej) { setTimeout(function () { rej(new Error('总超时')); }, perTimeout); }), ]); } catch (e) { if (done) return; recordFail(cand, e.message); log(' ❌ [' + cand.sid + '] 失败 | ' + e.message); return; } if (done) return; if (!isValidUrl(url)) { recordFail(cand, '无效URL'); log(' ❌ [' + cand.sid + '] 无效URL'); return; } let isMiguFixed = false; if (platform === 'mg' && ENABLE_MIGU_MAGIC) { const rules = MIGU_REVERSE_RULES[q] || []; if (rules.length > 0) { let decoded = decodeURIComponent(url); for (let i = 0; i < rules.length; i++) { const rule = rules[i]; if (rule.re.test(decoded)) { decoded = decoded.replace(rule.re, rule.to); decoded = decoded.replace(/\.(mp3|m4a|flac|wav)(?=\?|$)/i, rule.ext); url = encodeURI(decoded); isMiguFixed = true; log(` 🔄 [${cand.sid}] 反推命中: ${q}`); break; } } } } if (STRICT_HOST && !hostOk(url, platform)) { recordFail(cand, '串台'); log(' ❌ [' + cand.sid + '] 串台 | ' + url.slice(0, 80)); return; } if (STRICT_SUFFIX && !suffixOk(url, q)) { recordFail(cand, '格式不符'); let suffix = 'unknown'; const lowUrl = url.toLowerCase(); if (lowUrl.includes('.mflac')) suffix = 'mflac'; else if (lowUrl.includes('mgg')) suffix = 'mgg'; else if (lowUrl.includes('.mp3')) suffix = 'mp3'; else if (lowUrl.includes('.m4a')) suffix = 'm4a'; else if (lowUrl.includes('m800')) suffix = 'm800'; else { const match = lowUrl.match(/\.([a-z0-9]+)(?:\?|$)/); if (match) suffix = match[1]; } log(' 🚫 [' + cand.sid + '] 格式不符 ' + q + ' → ' + suffix); return; } const trialFeature = isTrialUrl(url); if (trialFeature) { recordFail(cand, trialFeature); log(' 🚫 [' + cand.sid + '] 拦截: ' + trialFeature + ' → ' + url.slice(0, 80)); return; } if (ENABLE_SIZE_CHECK && isLossless) { let finalProbe = await probeUrl(url); if (finalProbe.size === 0) { recordFail(cand, '测不出体积'); if (LOG_SIZE_CHECK) log(' 📉 [' + cand.sid + '] 测不出体积 判定为假货/外链 直接踢掉'); return; } if (expSize > 0) { const actualMB = finalProbe.size / 1048576; const expMB = expSize / 1048576; const minRule1 = Math.max(0, expMB - 5); const maxRule1 = expMB + 5; const baseTen = Math.floor(expMB / 10) * 10; const minRule2 = baseTen === 0 ? 0 : baseTen; const maxRule2 = baseTen + 10; const minMB = Math.min(minRule1, minRule2); const maxMB = Math.max(maxRule1, maxRule2); if (actualMB < minMB || actualMB > maxMB) { recordFail(cand, '体积不符'); if (LOG_SIZE_CHECK) log(' 🚫 [' + cand.sid + '] 体积异常 | 实际: ' + actualMB.toFixed(1) + 'MB | 预期: ' + expMB.toFixed(1) + 'MB | 合法区间: ' + minMB.toFixed(1) + '~' + maxMB.toFixed(1) + 'MB | 直接踢掉'); return; } else { if (LOG_SIZE_CHECK) log(' 🎯 [' + cand.sid + '] 体积通过 | 实际: ' + actualMB.toFixed(1) + 'MB | 落在 ' + minMB.toFixed(1) + '~' + maxMB.toFixed(1) + 'MB'); } } else { const actualMB = finalProbe.size / 1048576; const lowUrl = url.toLowerCase(); let isInvalid = false; if (q === 'atmos' || q === 'atmos_plus') { if (lowUrl.includes('.mp3')) { recordFail(cand, '假全景声(MP3)'); if (LOG_SIZE_CHECK) log(' 🚫 [' + cand.sid + '] 体积校验失败: 请求全景声却返回了 MP3'); isInvalid = true; } else if (actualMB < 5) { recordFail(cand, '体积过小(盲测)'); if (LOG_SIZE_CHECK) log(' 🚫 [' + cand.sid + '] 未知预期体积 但实际只有 ' + actualMB.toFixed(1) + 'MB 直接踢掉'); isInvalid = true; } else if (actualMB > 250) { recordFail(cand, '体积过大(盲测)'); if (LOG_SIZE_CHECK) log(' 🚫 [' + cand.sid + '] 未知预期体积 但实际高达 ' + actualMB.toFixed(1) + 'MB 直接踢掉'); isInvalid = true; } } else { if (lowUrl.includes('.mp3') || lowUrl.includes('.m4a')) { recordFail(cand, '假无损(MP3/M4A)'); if (LOG_SIZE_CHECK) log(' 🚫 [' + cand.sid + '] 体积校验失败: 请求无损却返回了 MP3/M4A'); isInvalid = true; } else if (actualMB < 10) { recordFail(cand, '体积过小(盲测)'); if (LOG_SIZE_CHECK) log(' 🚫 [' + cand.sid + '] 未知预期体积 但实际只有 ' + actualMB.toFixed(1) + 'MB 直接踢掉'); isInvalid = true; } else if (actualMB > 600) { recordFail(cand, '体积过大(盲测)'); if (LOG_SIZE_CHECK) log(' 🚫 [' + cand.sid + '] 未知预期体积 但实际高达 ' + actualMB.toFixed(1) + 'MB 直接踢掉'); isInvalid = true; } } if (isInvalid) return; if (LOG_SIZE_CHECK) log(' 🎯 [' + cand.sid + '] 盲测通过 | 实际: ' + actualMB.toFixed(1) + 'MB (未知预期)'); } } if (done) return; const ms = Date.now() - t0; recOk(action, scoreKey(cand.sid, q), ms); log(' ✅ [' + cand.sid + '] 成功 | ' + q + ' | ' + ms + 'ms | ' + url.slice(0, 120)); sidMap.set(String(url), cand.sid); done = true; mi.__is_resolved = true; clearTimers(); resolve(url); } fireAll(); }); } async function txGetUrl(mi, quality) { const isStrict = STRICT_LEVELS.indexOf(quality) >= 0; const q = isStrict ? quality : PLAY_LEVEL; const action = isStrict ? 'download' : 'play'; const FN_MAP = { tx_cy: qq_cy, tx_xhs: qq_xhs, tx_hyw: qq_hyw, tx_tang: qq_tang, tx_ht: qq_ht, tx_nki: qq_nki, tx_yx: qq_yx, tx_zddyr: qq_zddyr, tx_ly: tx_ly, tx_ikun: tx_ikun, tx_ikun2: tx_ikun2, tx_anime: tx_anime, sync_kw: sync_kw }; xcCandidates('tx', q).forEach(function (_c) { FN_MAP[_c.sid] = _c.fn; }); let list = isStrict ? (DOWNLOAD_ORDER.tx[q] || DOWNLOAD_ORDER.tx.flac || []).slice() : PLAY_ORDER.tx.slice(); list = sortByScore(action, list, q); var _own = {}; for (var _i = 0; _i < list.length; _i++) _own[list[_i]] = 1; list = list.concat(xcCandidates('tx', q, _own).map(function (c) { return c.sid; })); if (KW_FALLBACK.tx) list.push('sync_kw'); const candidates = []; for (let i = 0; i < list.length; i++) if (FN_MAP[list[i]]) candidates.push({ sid: list[i], fn: FN_MAP[list[i]] }); const timeout = isStrict ? DOWNLOAD_TOTAL_TIMEOUT : PLAY_TOTAL_TIMEOUT; return await serialTry(candidates, mi, q, 'tx', action, timeout); } async function wyGetUrl(mi, quality) { const isStrict = STRICT_LEVELS.indexOf(quality) >= 0; const q = isStrict ? quality : PLAY_LEVEL; const action = isStrict ? 'download' : 'play'; const FN_MAP = { wy_cy: wy_cy, wy_cy2: wy_cy2, wy_ikun: wy_ikun, wy_ikun_key: wy_ikun_key, wy_nx: wy_nx, wy_ht: wy_ht, wy_ht2: wy_ht2, wy_ht3: wy_ht3, wy_hyw: wy_hyw, wy_zddyr: wy_zddyr, wy_qgg: wy_qgg, wy_nanorocky: wy_nanorocky, wy_bugpk: wy_bugpk, wy_xt: wy_xt, wy_xtv2: wy_xtv2, wy_ikun2: wy_ikun2, wy_gdstudio: wy_gdstudio, wy_anime: wy_anime, sync_kw: sync_kw }; xcCandidates('wy', q).forEach(function (_c) { FN_MAP[_c.sid] = _c.fn; }); let list = isStrict ? (DOWNLOAD_ORDER.wy[q] || DOWNLOAD_ORDER.wy.flac || []).slice() : PLAY_ORDER.wy.slice(); list = sortByScore(action, list, q); var _own = {}; for (var _i = 0; _i < list.length; _i++) _own[list[_i]] = 1; list = list.concat(xcCandidates('wy', q, _own).map(function (c) { return c.sid; })); if (KW_FALLBACK.wy) list.push('sync_kw'); const candidates = []; for (let i = 0; i < list.length; i++) { if (FN_MAP[list[i]]) candidates.push({ sid: list[i], fn: FN_MAP[list[i]] }); } const timeout = isStrict ? DOWNLOAD_TOTAL_TIMEOUT : PLAY_TOTAL_TIMEOUT; return await serialTry(candidates, mi, q, 'wy', action, timeout); } async function kgGetUrl(mi, quality) { const isStrict = STRICT_LEVELS.indexOf(quality) >= 0; const q = isStrict ? quality : PLAY_LEVEL; const action = isStrict ? 'download' : 'play'; const FN_MAP = { kg_ht: kg_ht, kg_zddyr: kg_zddyr, kg_hyw: kg_hyw, kg_ikun: kg_ikun, kg_ikun2: kg_ikun2, kg_anime: kg_anime, sync_kw: sync_kw }; xcCandidates('kg', q).forEach(function (_c) { FN_MAP[_c.sid] = _c.fn; }); let list = isStrict ? (DOWNLOAD_ORDER.kg[q] || DOWNLOAD_ORDER.kg.flac || []).slice() : PLAY_ORDER.kg.slice(); list = sortByScore(action, list, q); var _own = {}; for (var _i = 0; _i < list.length; _i++) _own[list[_i]] = 1; list = list.concat(xcCandidates('kg', q, _own).map(function (c) { return c.sid; })); if (KW_FALLBACK.kg) list.push('sync_kw'); const candidates = []; for (let i = 0; i < list.length; i++) if (FN_MAP[list[i]]) candidates.push({ sid: list[i], fn: FN_MAP[list[i]] }); const timeout = isStrict ? DOWNLOAD_TOTAL_TIMEOUT : PLAY_TOTAL_TIMEOUT; return await serialTry(candidates, mi, q, 'kg', action, timeout); } async function kwGetUrl(mi, quality) { const isStrict = STRICT_LEVELS.indexOf(quality) >= 0; const q = isStrict ? quality : PLAY_LEVEL; const action = isStrict ? 'download' : 'play'; const FN_MAP = { kw_mobi: kw_mobi, kw_car: kw_car, kw_zx: kw_zx, kw_ht: kw_ht, kw_ikun: kw_ikun, kw_ikun2: kw_ikun2, kw_anime: kw_anime }; xcCandidates('kw', q).forEach(function (_c) { FN_MAP[_c.sid] = _c.fn; }); let list = isStrict ? (DOWNLOAD_ORDER.kw[q] || DOWNLOAD_ORDER.kw.flac || []).slice() : PLAY_ORDER.kw.slice(); list = sortByScore(action, list, q); var _own = {}; for (var _i = 0; _i < list.length; _i++) _own[list[_i]] = 1; list = list.concat(xcCandidates('kw', q, _own).map(function (c) { return c.sid; })); const candidates = []; for (let i = 0; i < list.length; i++) if (FN_MAP[list[i]]) candidates.push({ sid: list[i], fn: FN_MAP[list[i]] }); const timeout = isStrict ? DOWNLOAD_TOTAL_TIMEOUT : PLAY_TOTAL_TIMEOUT; return await serialTry(candidates, mi, q, 'kw', action, timeout); } async function mgGetUrl(mi, quality) { const isStrict = STRICT_LEVELS.indexOf(quality) >= 0; const q = isStrict ? quality : PLAY_LEVEL; const action = isStrict ? 'download' : 'play'; const FN_MAP = { mg_sy: mg_sy, mg_wen: mg_wen, mg_zddyr: mg_zddyr, mg_zddyr2: mg_zddyr2, sync_kw: sync_kw }; xcCandidates('mg', q).forEach(function (_c) { FN_MAP[_c.sid] = _c.fn; }); let list = isStrict ? (DOWNLOAD_ORDER.mg[q] || DOWNLOAD_ORDER.mg.flac || []).slice() : PLAY_ORDER.mg.slice(); list = sortByScore(action, list, q); var _own = {}; for (var _i = 0; _i < list.length; _i++) _own[list[_i]] = 1; list = list.concat(xcCandidates('mg', q, _own).map(function (c) { return c.sid; })); if (KW_FALLBACK.mg) list.push('sync_kw'); const candidates = []; for (let i = 0; i < list.length; i++) if (FN_MAP[list[i]]) candidates.push({ sid: list[i], fn: FN_MAP[list[i]] }); const timeout = isStrict ? DOWNLOAD_TOTAL_TIMEOUT : PLAY_TOTAL_TIMEOUT; return await serialTry(candidates, mi, q, 'mg', action, timeout); } const SOURCE_GETTERS = { tx: txGetUrl, wy: wyGetUrl, kg: kgGetUrl, kw: kwGetUrl, mg: mgGetUrl, }; async function fetchUrlBySource(source, mi, quality) { const getter = SOURCE_GETTERS[source]; if (!getter) throw new Error('未知音源: ' + source); return await getter(mi, quality); } function cleanupCache() { const now = Date.now(); if (urlCache.size > CACHE_MAX) { const keys = Array.from(urlCache.keys()); for (let i = 0; i < keys.length && urlCache.size > CACHE_MAX; i++) { const v = urlCache.get(keys[i]); if (!v || (v.expire || 0) < now) urlCache.delete(keys[i]); } } const ks = Array.from(noSourceMap.keys()); for (let i = 0; i < ks.length; i++) { const v = noSourceMap.get(ks[i]); if (v && v.expire && v.expire < now) noSourceMap.delete(ks[i]); } } const XC_CONFIG = { kw: { name: '酷我音乐', apis: [ { api: 'https://musicserver.haitangw.cc/v1/music/resolve-url', idField: ['hash', 'rid', 'songId', 'songmid', 'id'], method: 'POST', headers: { 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0' }, body: { source: 'kw', rid: '{id}', level: '{quality}' }, urlField: ['data.url'], quality: { atmos: 'atmos', atmos_plus: 'atmos_plus', master: 'master' } }, { api: 'http://nmobi.kuwo.cn/mobi.s?f=web&user=0&source=kwplayerhd_ar_6.6.6.6_tianbao_T1A_qirui.apk&type=convert_url_with_sign&rid={id}&br={quality}', idField: ['rid', 'hash', 'songId', 'id', 'songmid'], urlField: ['data.url'], quality: { '128k': '128kmp3', '320k': '320kmp3', flac: '2000kflac', flac24bit: '4000kflac', hires: '4000kflac', atmos: '20201kmflac', atmos_plus: '20501kmflac', master: '20900kmflac' }, headers: { 'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36' } } ] }, kg: { name: '酷狗音乐', apis: [ { api: 'http://103.79.184.97/api/music/url?source=kg&songId={id}&quality={quality}&key=6C1F-53W0-GRKI-EVFG', idField: ['hash', 'songmid', 'id', 'rid'], headers: { 'User-Agent': 'Mozilla/5.0', 'X-Card-Key': '6C1F-53W0-GRKI-EVFG' }, urlField: ['url', 'data.url'], quality: { '128k': '128k', '320k': '320k', flac: 'flac' } }, { api: 'https://yy.zddyr.top/lx/api/?source=kg&quality={quality}&mainHash={id}', idField: ['hash', 'songmid', 'id', 'rid'], urlField: ['url'], quality: { '128k': '128k', '320k': '320k', flac: 'flac', hires: 'hires' } }, { api: 'https://musicserver.haitangw.cc/v1/music/resolve-url', idField: ['hash', 'songmid', 'id', 'rid'], method: 'POST', headers: { 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0' }, body: { source: 'kg', rid: '{id}', level: '{quality}' }, urlField: ['data.url'], quality: { '128k': 'standard', '320k': 'exhigh', flac: 'lossless', hires: 'hires', atmos: 'atmos', master: 'clear' } } ] }, tx: { name: 'QQ音乐', apis: [ { api: 'http://103.79.184.97/api/music/url?source=tx&songId={id}&quality={quality}&key=6C1F-53W0-GRKI-EVFG', idField: ['songmid', 'id', 'hash'], headers: { 'User-Agent': 'Mozilla/5.0', 'X-Card-Key': '6C1F-53W0-GRKI-EVFG' }, urlField: ['url', 'data.url'], quality: { '128k': '128k', '320k': '320k', flac: 'flac', flac24bit: 'flac24bit' } }, { api: 'https://yy.zddyr.top/lx/api/?source=tx&songmid={id}&quality={quality}', idField: ['songmid', 'id', 'hash'], urlField: ['url'], quality: { '128k': '128k', '320k': '320k', flac: 'flac', hires: 'hires' } }, { api: 'https://tang.api.s01s.cn/music_open_api.php?mid={id}', idField: ['songmid', 'id', 'hash'], urlField: ['song_play_url_pq', 'song_play_url_sq', 'song_play_url_hq', 'song_play_url_standard', 'song_play_url', 'song_play_url_fq'], quality: { '128k': 'song_play_url_standard', '320k': 'song_play_url_hq', flac: 'song_play_url_sq', flac24bit: 'song_play_url_pq', atmos: 'song_play_url_pq' }, after: (data) => { if (!data) throw new Error('tang 无响应'); const fields = ['song_play_url_pq', 'song_play_url_sq', 'song_play_url_hq', 'song_play_url_standard', 'song_play_url', 'song_play_url_fq']; for (const f of fields) { if (typeof data[f] === 'string' && data[f].trim()) return data[f].trim(); } throw new Error('tang 无链接'); } }, { api: 'https://musicserver.haitangw.cc/v1/music/resolve-url', idField: ['songmid', 'id', 'hash'], method: 'POST', headers: { 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0' }, body: { source: 'tx', rid: '{id}', level: '{quality}' }, urlField: ['data.url'], quality: { '128k': 'standard', '320k': 'exhigh', flac: 'lossless', flac24bit: 'hires', hires: 'hires', atmos: '1999', atmos_plus: '2999', master: 'jymaster' } }, { api: 'https://a.aa.cab/qq.music?msg={keyword}&n=1&type={quality}', idField: ['songmid', 'id', 'hash'], urlField: ['data.music', 'playUrl', 'url', 'data.url'], quality: { '128k': '0', '320k': '1', flac: '4', master: '5' } } ] }, wy: { name: '网易云音乐', apis: [ { api: 'https://c.wwwweb.top/music/url', idField: ['hash', 'songmid'], urlField: ['url'], method: 'POST', headers: { 'Content-Type': 'application/json', 'User-Agent': 'lx-music-desktop/2.10.1' }, body: { source: 'wy', musicId: '{id}', quality: '{quality}' }, quality: { '128k': '128k', '320k': '320k', flac: 'flac', flac24bit: 'flac24bit', hires: 'hires', atmos: 'atmos', master: 'master' }, after: (data) => { if (data && data.code === 200 && data.url) return data.url; throw new Error((data && data.message) || '无数据'); } }, { api: 'https://musicserver.haitangw.cc/v1/music/resolve-url', idField: ['songmid', 'id', 'hash'], method: 'POST', headers: { 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0' }, body: { source: 'wy', rid: '{id}', level: '{quality}' }, urlField: ['data.url'], quality: { '128k': 'standard', '320k': 'exhigh', flac: 'lossless', flac24bit: 'hires', hires: 'hires', atmos: 'jyeffect', master: 'jymaster' } }, { api: 'https://yy.zddyr.top/lx/api/?source=wy&songmid={id}&quality={quality}', idField: ['hash', 'songmid', 'id'], urlField: ['url', 'data.url'], quality: { '128k': '128k', '320k': '320k', flac: 'flac', hires: 'hires' } }, { api: 'https://mcp.nianxinxz.com/share/ceshi/wy.php?id={id}&level={quality}', idField: ['hash', 'songmid', 'id'], urlField: ['url'], quality: { '128k': 'standard', '320k': 'exhigh', flac: 'lossless', flac24bit: 'hires', hires: 'hires', master: 'jymaster', atmos: 'jyeffect' }, after: (data) => { if (data && data.code === 200 && data.url) return data.url; throw new Error((data && data.message) || 'mcp 无数据'); } }, { api: 'http://103.79.184.97/api/music/url?platform=wy&songId={id}&quality={quality}&key=6C1F-53W0-GRKI-EVFG', idField: ['songmid', 'songId', 'id', 'hash'], urlField: ['url', 'data.url', 'data'], quality: { '128k': '128k', '320k': '320k', flac: 'flac', flac24bit: 'flac24bit', hires: 'hires' }, headers: { 'User-Agent': 'lx-music-mobile/2.0.0', 'X-Card-Key': '6C1F-53W0-GRKI-EVFG' } } ] }, mg: { name: '咪咕音乐', apis: [ { api: 'https://yy.zddyr.top/lx/api/?source=migu&songmid={id}&quality={quality}', idField: ['songmid', 'id', 'hash'], urlField: ['url', 'data.url'], quality: { '128k': '128k', '320k': '320k', flac: 'flac', hires: 'hires' } }, { api: 'https://oiapi.net/api/MiGu_Music?msg={keyword}&br={quality}&n=1', idField: ['songmid', 'id', 'hash'], urlField: ['data.url', 'url'], quality: { '128k': 'LQ', '320k': 'HQ', flac: 'SQ', hires: 'SQ' } } ] } }; const XC_CHAIN = { master: ['master', 'atmos_plus', 'atmos'], jymaster: ['master', 'atmos_plus', 'atmos', 'jymaster'], atmos_plus: ['atmos_plus', 'atmos'], atmos: ['atmos'], sky: ['atmos_plus', 'atmos'], jyeffect: ['atmos'], hires: ['hires', 'flac24bit', 'flac'], flac24bit: ['flac24bit', 'flac'], flac: ['flac'], '320k': ['320k'], '128k': ['128k'] }; const xcSubst = (val, map) => typeof val === 'string' ? val.replace(/\{(id|quality|keyword)\}/g, (_, k) => map[k] ?? '') : Array.isArray(val) ? val.map(v => xcSubst(v, map)) : (val && typeof val === 'object') ? Object.fromEntries(Object.entries(val).map(([k, v]) => [k, xcSubst(v, map)])) : val; const xcHas = (api, name) => [api.api, api.body, api.headers].some(v => v && JSON.stringify(v).includes('{' + name + '}')); function xcMakeFn(platform, api, levelMap) { return async function xcApi(mi, q) { const level = levelMap[q]; if (!level) throw new Error('不支持 ' + q); const needId = xcHas(api, 'id'); const needKw = xcHas(api, 'keyword'); const id = needId ? idOf(mi, platform) : ''; if (needId && !id) throw new Error('缺少ID'); const kw = needKw ? encodeURIComponent(mi.name || mi.title || mi.songname || '') : ''; if (needKw && !kw) throw new Error('缺少歌曲名'); const map = { id: id, keyword: kw, quality: api.quality[level] }; const url = xcSubst(api.api, map); const headers = api.headers ? xcSubst(api.headers, map) : { 'User-Agent': 'Mozilla/5.0' }; let data; if ((api.method || 'GET') === 'POST') { data = await httpPost(url, api.body ? xcSubst(api.body, map) : {}, headers); } else { data = await httpGet(url, null, headers); } let out = null; if (typeof api.after === 'function') { const parsed = api.after(data); out = typeof parsed === 'string' ? parsed : pickField(parsed, api.urlField || ['url']); } else { out = pickField(data, api.urlField || ['url', 'data.url']); } if (!out) throw new Error('无URL'); return httpsToHttp(out); }; } const XC_SOURCES = (function compile() { const out = {}; Object.keys(XC_CONFIG).forEach(function (p) { const byLevel = {}; XC_CONFIG[p].apis.forEach(function (api, i) { const sid = 'std_' + p + '_' + (api.method === 'POST' ? 'p' : 'g') + i; const declared = Object.keys(api.quality || {}); const levelMap = {}; Object.keys(XC_CHAIN).forEach(function (want) { for (let i = 0; i < XC_CHAIN[want].length; i++) { const lv = XC_CHAIN[want][i]; if (declared.indexOf(lv) >= 0) { levelMap[want] = lv; break; } } }); if (!Object.keys(levelMap).length) return; const fn = xcMakeFn(p, api, levelMap); Object.keys(levelMap).forEach(function (lv) { (byLevel[lv] = byLevel[lv] || []).push({ sid: sid, fn: fn }); }); }); out[p] = byLevel; }); return out; })(); function xcCandidates(platform, q, existingSids) { const arr = (XC_SOURCES[platform] || {})[q] || []; const seen = {}, list = []; for (let i = 0; i < arr.length; i++) { if (seen[arr[i].sid]) continue; if (existingSids && existingSids[arr[i].sid]) continue; seen[arr[i].sid] = 1; list.push(arr[i]); } return list; } function syncQualityTable() { const ORDER = ['128k', '320k', 'flac', 'flac24bit', 'hires', 'atmos', 'atmos_plus', 'master', 'jymaster', 'sky', 'jyeffect']; Object.keys(XC_SOURCES).forEach(function (p) { if (!sourceConfig[p]) return; const set = {}; sourceConfig[p].qualitys.forEach(function (q) { set[q] = 1; }); Object.keys(XC_SOURCES[p]).forEach(function (lv) { if ((XC_SOURCES[p][lv] || []).length) set[lv] = 1; }); sourceConfig[p].qualitys = ORDER.filter(function (q) { return set[q]; }); }); } const sourceConfig = { tx: { name: 'QQ音乐', type: 'music', actions: ['musicUrl'], qualitys: ['128k', '320k', 'flac', 'flac24bit', 'hires', 'atmos', 'atmos_plus', 'master', 'jyeffect', 'sky', 'jymaster'] }, wy: { name: '网易云', type: 'music', actions: ['musicUrl'], qualitys: ['128k', '320k', 'flac', 'flac24bit', 'hires', 'atmos', 'atmos_plus', 'master', 'jymaster', 'sky', 'jyeffect'] }, kg: { name: '酷狗', type: 'music', actions: ['musicUrl'], qualitys: ['128k', '320k', 'flac', 'flac24bit', 'hires', 'atmos', 'master', 'jymaster', 'sky'] }, kw: { name: '酷我', type: 'music', actions: ['musicUrl'], qualitys: ['128k', '320k', 'flac', 'flac24bit', 'hires', 'atmos', 'atmos_plus', 'master'] }, mg: { name: '咪咕', type: 'music', actions: ['musicUrl'], qualitys: ['128k', '320k', 'flac', 'flac24bit', 'hires', 'atmos', 'atmos_plus', 'master'] }, }; syncQualityTable(); const handleGetMusicUrl = async (source, musicInfo, quality) => { const songId = musicInfo.hash ?? musicInfo.songmid ?? musicInfo.id; if (!songId) throw new Error('无法获取歌曲ID'); const title = musicInfo.title || musicInfo.name || '未知歌曲'; const singer = musicInfo.artist || musicInfo.singer || '未知歌手'; const t0 = Date.now(); const supported = sourceConfig[source] ? sourceConfig[source].qualitys : ['128k']; const targetQuality = supported.indexOf(quality) >= 0 ? quality : (supported[supported.length - 1] || '128k'); const hostSize = expectedSize(musicInfo, targetQuality); const expLog = hostSize > 0 ? (hostSize / 1048576).toFixed(2) + 'mb' : '未知'; log('--- 开始 | ' + source + ' | ' + targetQuality + ' | ' + title + ' - ' + singer + ' | id=' + songId + ' | ' + expLog); try { const pack = await getOrFetchUrl(source, musicInfo, targetQuality); const url = pack._url; const fromCache = pack._fromCache; const cost = Date.now() - t0; const sid = sidMap.get(String(url)) || (fromCache ? '缓存' : '未知'); log('--- 结束 | ' + (fromCache ? '命中缓存' : '成功') + ' | ' + cost + 'ms | 最终使用源: ' + sid + (fromCache ? ' | ' + String(url) : '')); return url; } catch (e) { log('--- 结束 | 失败 | ' + (Date.now() - t0) + 'ms | ' + (e && e.message ? e.message : String(e)).slice(0, 160)); throw e; } }; on(EVENT_NAMES.request, function (payload) { const action = payload.action, source = payload.source, info = payload.info; if (action !== 'musicUrl') return Promise.reject(new Error('action not support')); if (!info || !info.musicInfo) return Promise.reject(new Error('请求参数不完整'));
cleanupCache();
const q = info.type || PLAY_LEVEL;
return handleGetMusicUrl(source, info.musicInfo, q);
});
send(EVENT_NAMES.inited, {
openDevTools: false,
sources: sourceConfig,
});
