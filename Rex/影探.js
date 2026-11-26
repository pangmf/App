/**
 * 影探 —— ForwardWidget 明文模块（WidgetMetadata）
 * ============================================================================
 * 源：http://cms.lyyytv.cn（苹果 CMS 系，vod_play_from / vod_play_url 结构）
 * 由《影探&红果》合集拆分而来，只保留影探部分，可单独导入。
 *
 * 播放模型
 *   详情只给一份分集（episodeItems），线路差异留到起播时由 loadResource 计算，
 *   每个返回值就是播放器里的一条线路（name 即线路名）。
 *   —— 4K 线路的原始地址单独访问是 404，必须过解析接口 parsesId=6 换成签名地址；
 *      网页线路走 parsesId=5，HLS/MPD 直链直接返回。
 *
 * 站点若改版，只改常量区：CMS_BASE / LVDou_KEY / PARSE_API。
 * ============================================================================
 */
WidgetMetadata = {
  id: "forward.yingtan",
  title: "影探",
  version: "3.1.0",
  requiredVersion: "0.0.1",
  description: "影探 CMS：最新电影 / 热播国剧 / 国漫 / 短剧 / 更多分类；详情合并分集，起播按线路解析取流",
  author: "Forward",
  site: "https://github.com/InchStudio/ForwardWidgets",
  icon: "https://cms.lyyytv.cn/favicon.ico",
  detailCacheDuration: 300,
  modules: [
    {
      id: "ytLatest",
      title: "最新电影",
      functionName: "ytLatest",
      cacheDuration: 600,
      params: [
        { name: "page", title: "页码", type: "page" },
        { name: "class", title: "类型", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "喜剧", value: "喜剧" }, { title: "爱情", value: "爱情" }, { title: "恐怖", value: "恐怖" },
          { title: "动作", value: "动作" }, { title: "科幻", value: "科幻" }, { title: "剧情", value: "剧情" },
          { title: "战争", value: "战争" }, { title: "警匪", value: "警匪" }, { title: "犯罪", value: "犯罪" },
          { title: "奇幻", value: "奇幻" }, { title: "武侠", value: "武侠" }, { title: "枪战", value: "枪战" },
          { title: "悬疑", value: "悬疑" }, { title: "惊悚", value: "惊悚" }, { title: "青春", value: "青春" },
          { title: "文艺", value: "文艺" }, { title: "古装", value: "古装" }, { title: "历史", value: "历史" },
          { title: "运动", value: "运动" }, { title: "农村", value: "农村" }
        ] },
        { name: "area", title: "地区", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "大陆", value: "大陆" }, { title: "欧美", value: "欧美" }, { title: "香港", value: "香港" },
          { title: "台湾", value: "台湾" }, { title: "韩国", value: "韩国" }, { title: "日本", value: "日本" },
          { title: "泰国", value: "泰国" }, { title: "印度", value: "印度" }, { title: "其他", value: "其他" }
        ] },
        { name: "year", title: "年份", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "2026", value: "2026" }, { title: "2025", value: "2025" }, { title: "2024", value: "2024" },
          { title: "2023", value: "2023" }, { title: "2022", value: "2022" }, { title: "2021", value: "2021" },
          { title: "2020", value: "2020" }, { title: "2019", value: "2019" }, { title: "2018", value: "2018" },
          { title: "2017", value: "2017" }, { title: "2016", value: "2016" }, { title: "2015", value: "2015" },
          { title: "2014", value: "2014" }, { title: "2013", value: "2013" }, { title: "2012", value: "2012" },
          { title: "2011", value: "2011" }, { title: "2010", value: "2010" }
        ] }
      ]
    },
    {
      id: "ytTv",
      title: "热播国剧",
      functionName: "ytTv",
      cacheDuration: 600,
      params: [
        { name: "page", title: "页码", type: "page" },
        { name: "class", title: "类型", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "都市", value: "都市" }, { title: "古装", value: "古装" }, { title: "战争", value: "战争" },
          { title: "青春偶像", value: "青春偶像" }, { title: "喜剧", value: "喜剧" }, { title: "家庭", value: "家庭" },
          { title: "犯罪", value: "犯罪" }, { title: "动作", value: "动作" }, { title: "奇幻", value: "奇幻" },
          { title: "剧情", value: "剧情" }, { title: "历史", value: "历史" }, { title: "经典", value: "经典" },
          { title: "乡村", value: "乡村" }, { title: "情景", value: "情景" }, { title: "商战", value: "商战" },
          { title: "网剧", value: "网剧" }, { title: "其他", value: "其他" }
        ] },
        { name: "area", title: "地区", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "大陆", value: "大陆" }, { title: "欧美", value: "欧美" }, { title: "香港", value: "香港" },
          { title: "台湾", value: "台湾" }, { title: "韩国", value: "韩国" }, { title: "日本", value: "日本" },
          { title: "泰国", value: "泰国" }, { title: "其他", value: "其他" }
        ] },
        { name: "year", title: "年份", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "2026", value: "2026" }, { title: "2025", value: "2025" }, { title: "2024", value: "2024" },
          { title: "2023", value: "2023" }, { title: "2022", value: "2022" }, { title: "2021", value: "2021" },
          { title: "2020", value: "2020" }, { title: "2019", value: "2019" }, { title: "2018", value: "2018" },
          { title: "2017", value: "2017" }, { title: "2016", value: "2016" }, { title: "2015", value: "2015" },
          { title: "2014", value: "2014" }, { title: "2013", value: "2013" }, { title: "2012", value: "2012" },
          { title: "2011", value: "2011" }, { title: "2010", value: "2010" }
        ] }
      ]
    },
    {
      id: "ytGuoman",
      title: "国漫",
      functionName: "ytGuoman",
      cacheDuration: 600,
      params: [
        { name: "page", title: "页码", type: "page" },
        { name: "class", title: "类型", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "情感", value: "情感" }, { title: "科幻", value: "科幻" }, { title: "热血", value: "热血" },
          { title: "推理", value: "推理" }, { title: "搞笑", value: "搞笑" }, { title: "冒险", value: "冒险" },
          { title: "校园", value: "校园" }, { title: "动作", value: "动作" }, { title: "机战", value: "机战" },
          { title: "战争", value: "战争" }, { title: "少年", value: "少年" }, { title: "少女", value: "少女" },
          { title: "亲子", value: "亲子" }, { title: "励志", value: "励志" }, { title: "其他", value: "其他" }
        ] },
        { name: "area", title: "地区", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "大陆", value: "大陆" }, { title: "欧美", value: "欧美" }, { title: "香港", value: "香港" },
          { title: "台湾", value: "台湾" }, { title: "韩国", value: "韩国" }, { title: "日本", value: "日本" },
          { title: "其他", value: "其他" }
        ] },
        { name: "year", title: "年份", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "2026", value: "2026" }, { title: "2025", value: "2025" }, { title: "2024", value: "2024" },
          { title: "2023", value: "2023" }, { title: "2022", value: "2022" }, { title: "2021", value: "2021" },
          { title: "2020", value: "2020" }, { title: "2019", value: "2019" }, { title: "2018", value: "2018" },
          { title: "2017", value: "2017" }, { title: "2016", value: "2016" }, { title: "2015", value: "2015" }
        ] }
      ]
    },
    {
      id: "ytDuanju",
      title: "短剧",
      functionName: "ytDuanju",
      cacheDuration: 600,
      params: [
        { name: "page", title: "页码", type: "page" },
        { name: "class", title: "类型", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "古装", value: "古装" }, { title: "战争", value: "战争" }, { title: "青春偶像", value: "青春偶像" },
          { title: "喜剧", value: "喜剧" }, { title: "家庭", value: "家庭" }, { title: "犯罪", value: "犯罪" },
          { title: "动作", value: "动作" }, { title: "奇幻", value: "奇幻" }, { title: "剧情", value: "剧情" },
          { title: "历史", value: "历史" }, { title: "经典", value: "经典" }, { title: "乡村", value: "乡村" },
          { title: "其他", value: "其他" }
        ] },
        { name: "year", title: "年份", type: "enumeration", enumOptions: [
          { title: "全部", value: "" },
          { title: "2026", value: "2026" }, { title: "2025", value: "2025" }, { title: "2024", value: "2024" },
          { title: "2023", value: "2023" }, { title: "2022", value: "2022" }, { title: "2021", value: "2021" },
          { title: "2020", value: "2020" }
        ] }
      ]
    },
    {
      id: "ytMore",
      title: "影探·更多分类",
      functionName: "ytMore",
      cacheDuration: 600,
      params: [
        { name: "page", title: "页码", type: "page" },
        { name: "cat", title: "分类", type: "enumeration", enumOptions: [
          { title: "欧美剧", value: "25" }, { title: "韩剧", value: "56" }, { title: "港台剧", value: "28" },
          { title: "国综", value: "24" }, { title: "少儿动画", value: "29" }, { title: "记录片", value: "55" },
          { title: "电影", value: "47" }, { title: "电视剧", value: "48" }, { title: "动漫", value: "49" },
          { title: "综艺", value: "50" }
        ] }
      ]
    },
    {
      id: "loadResource",
      title: "加载资源",
      functionName: "loadResource",
      type: "stream",
      cacheDuration: 0,
      params: []
    }
  ],
  search: {
    title: "搜索",
    functionName: "search",
    params: [
      { name: "keyword", title: "关键词", type: "input" },
      { name: "page", title: "页码", type: "page" }
    ]
  }
};

// ============================================================================
// 常量（与原版 Python 同名同值）
// ============================================================================
var CMS_BASE = "http://cms.lyyytv.cn";
var LVDou_KEY = "wP5bvxoc3yv7FoBQENFZuAF0EUYr4LTy";
var PARSE_API = "http://fys.lyyytv.cn/api/index?appid=10001&videoUrl=";
/* 解析口会不定期调整：parsesId=5 曾用于网页线路，实测已失效；
   当前网页链接用 6、4K 托管（ym4kjx 等）用 8。这里按候选顺序试，
   哪个先成功就把它提到队首，后续同类请求不再试错。 */
var PARSE_PIDS_WEB = [6, 5, 7, 8];
var PARSE_PIDS_4K = [8, 6, 7, 5];
var DEC_PREFIX = "https://baidu.con/"; // 解析接口返回的密文前缀
var CMS_HEADERS = { "User-Agent": "okhttp/4.12.0" };
var PARSE_HEADERS = { "User-Agent": "okhttp/4.12.0", "Accept-Encoding": "identity" };

var YT_LINK = "yt:"; // 影探详情：yt:<vod_id>
var YT_PLAY = "ytp:"; // 影探分集：ytp:<b64url({v:vod_id,i:集索引})>

var PAGE_SIZE = 20;
var YT_DETAIL_TTL = 300000; // 5 分钟
var PLAY_TTL = 120000; // 解析结果 2 分钟（签名地址本身有时效）
var FAIL_TTL = 60000; // 解析失败负缓存 60 秒

var MOVIE_TIDS = { "1": 1, "3": 1, "20": 1, "30": 1, "46": 1, "36": 1, "35": 1, "40": 1, "43": 1, "44": 1, "47": 1 };

// ============================================================================
// 基础工具
// ============================================================================
function s(v) {
  return v === null || v === undefined ? "" : String(v).replace(/^\s+|\s+$/g, "");
}

function toInt(v, def) {
  var m = /^\s*[+-]?\d+/.exec(String(v === null || v === undefined ? "" : v));
  if (!m) return def;
  var n = parseInt(m[0], 10);
  return isNaN(n) ? def : n;
}

function isArray(v) {
  return Object.prototype.toString.call(v) === "[object Array]";
}

function log() {
  try {
    var parts = [];
    for (var i = 0; i < arguments.length; i++) parts.push(String(arguments[i]));
    console.log("[影探红果] " + parts.join(" "));
  } catch (e) {}
}

function jsonParse(text) {
  if (!text) return null;
  if (typeof text === "object") return text;
  try {
    return JSON.parse(text);
  } catch (e) {
    return null;
  }
}

/* 简单的内存 TTL 缓存（模块实例在 App 内常驻，够用） */
var _cache = {};
var _cacheKeys = [];

function cacheGet(key) {
  var it = _cache[key];
  if (!it) return null;
  if (it.exp && it.exp < new Date().getTime()) {
    delete _cache[key];
    return null;
  }
  return it.v;
}

function cacheSet(key, value, ttl) {
  if (!_cache[key]) {
    _cacheKeys.push(key);
    if (_cacheKeys.length > 80) {
      var old = _cacheKeys.shift();
      delete _cache[old];
    }
  }
  _cache[key] = { v: value, exp: new Date().getTime() + (ttl || 60000) };
  return value;
}

/* ---------------- base64 / UTF-8 ---------------- */
var B64C = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var B64MAP = null;

function b64map() {
  if (B64MAP) return B64MAP;
  B64MAP = {};
  for (var i = 0; i < B64C.length; i++) B64MAP[B64C.charAt(i)] = i;
  return B64MAP;
}

function bytesToB64(bytes) {
  var out = "";
  var i = 0;
  while (i < bytes.length) {
    var b0 = bytes[i++] & 0xff;
    var b1 = i < bytes.length ? bytes[i++] & 0xff : NaN;
    var b2 = i < bytes.length ? bytes[i++] & 0xff : NaN;
    var n = (b0 << 16) | ((isNaN(b1) ? 0 : b1) << 8) | (isNaN(b2) ? 0 : b2);
    out += B64C.charAt((n >> 18) & 63);
    out += B64C.charAt((n >> 12) & 63);
    out += isNaN(b1) ? "=" : B64C.charAt((n >> 6) & 63);
    out += isNaN(b2) ? "=" : B64C.charAt(n & 63);
  }
  return out;
}

function b64ToBytes(str) {
  var t = String(str || "").replace(/\s+/g, "").replace(/-/g, "+").replace(/_/g, "/");
  if (!t) return null;
  if (!/^[A-Za-z0-9+/]*={0,2}$/.test(t)) return null;
  while (t.length % 4) t += "=";
  var map = b64map();
  var out = [];
  for (var i = 0; i < t.length; i += 4) {
    var c0 = map[t.charAt(i)];
    var c1 = map[t.charAt(i + 1)];
    var c2 = map[t.charAt(i + 2)];
    var c3 = map[t.charAt(i + 3)];
    if (c0 === undefined || c1 === undefined) return null;
    var n = (c0 << 18) | (c1 << 12) | ((c2 === undefined ? 0 : c2) << 6) | (c3 === undefined ? 0 : c3);
    out.push((n >> 16) & 0xff);
    if (t.charAt(i + 2) !== "=" && c2 !== undefined) out.push((n >> 8) & 0xff);
    if (t.charAt(i + 3) !== "=" && c3 !== undefined) out.push(n & 0xff);
  }
  return out;
}

function utf8Bytes(str) {
  var bytes = [];
  for (var i = 0; i < str.length; i++) {
    var c = str.charCodeAt(i);
    if (c < 0x80) bytes.push(c);
    else if (c < 0x800) {
      bytes.push(0xc0 | (c >> 6), 0x80 | (c & 63));
    } else if (c >= 0xd800 && c <= 0xdbff && i + 1 < str.length) {
      var c2 = str.charCodeAt(i + 1);
      if (c2 >= 0xdc00 && c2 <= 0xdfff) {
        var cp = 0x10000 + ((c - 0xd800) << 10) + (c2 - 0xdc00);
        bytes.push(0xf0 | (cp >> 18), 0x80 | ((cp >> 12) & 63), 0x80 | ((cp >> 6) & 63), 0x80 | (cp & 63));
        i++;
      } else bytes.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
    } else {
      bytes.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
    }
  }
  return bytes;
}

function utf8Decode(bytes) {
  var out = "";
  var i = 0;
  while (i < bytes.length) {
    var b = bytes[i++] & 0xff;
    if (b < 0x80) out += String.fromCharCode(b);
    else if (b >= 0xc0 && b < 0xe0) {
      var b1 = bytes[i++] & 0xff;
      out += String.fromCharCode(((b & 31) << 6) | (b1 & 63));
    } else if (b >= 0xe0 && b < 0xf0) {
      var b2 = bytes[i++] & 0xff;
      var b3 = bytes[i++] & 0xff;
      out += String.fromCharCode(((b & 15) << 12) | ((b2 & 63) << 6) | (b3 & 63));
    } else if (b >= 0xf0) {
      var b4 = bytes[i++] & 0xff;
      var b5 = bytes[i++] & 0xff;
      var b6 = bytes[i++] & 0xff;
      var cp = ((b & 7) << 18) | ((b4 & 63) << 12) | ((b5 & 63) << 6) | (b6 & 63);
      cp -= 0x10000;
      out += String.fromCharCode(0xd800 + (cp >> 10), 0xdc00 + (cp & 1023));
    }
  }
  return out;
}

function b64urlEncode(str) {
  return bytesToB64(utf8Bytes(String(str))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function b64urlDecode(str) {
  var bytes = b64ToBytes(String(str || ""));
  if (!bytes) return "";
  return utf8Decode(bytes);
}

/* ---------------- AES-128-CBC 解密（纯 JS，无依赖） ---------------- */
var AES_SBOX = null;
var AES_INV = null;
var AES_HEX =
  "637c777bf26b6fc53001672bfed7ab76" + "ca82c97dfa5947f0add4a2af9ca472c0" +
  "b7fd9326363ff7cc34a5e5f171d83115" + "04c723c31896059a071280e2eb27b275" +
  "09832c1a1b6e5aa0523bd6b329e32f84" + "53d100ed20fcb15b6acbbe394a4c58cf" +
  "d0efaafb434d338545f9027f503c9fa8" + "51a3408f929d38f5bcb6da2110fff3d2" +
  "cd0c13ec5f974417c4a77e3d645d1973" + "60814fdc222a908846eeb814de5e0bdb" +
  "e0323a0a4906245cc2d3ac629195e479" + "e7c8376d8dd54ea96c56f4ea657aae08" +
  "ba78252e1ca6b4c6e8dd741f4bbd8b8a" + "703eb5664803f60e613557b986c11d9e" +
  "e1f8981169d98e949b1e87e9ce5528df" + "8ca1890dbfe6426841992d0fb054bb16";

function aesInit() {
  if (AES_SBOX) return;
  AES_SBOX = [];
  AES_INV = [];
  for (var i = 0; i < 256; i++) {
    var v = parseInt(AES_HEX.substr(i * 2, 2), 16);
    AES_SBOX.push(v);
    AES_INV[v] = i;
  }
}

function xtime(a) {
  a <<= 1;
  if (a & 0x100) a ^= 0x11b;
  return a & 0xff;
}

function gmul(a, b) {
  var p = 0;
  for (var i = 0; i < 8; i++) {
    if (b & 1) p ^= a;
    var hi = a & 0x80;
    a = (a << 1) & 0xff;
    if (hi) a ^= 0x1b;
    b >>= 1;
  }
  return p;
}

function aesExpandKey(key) {
  var w = [];
  var i;
  for (i = 0; i < 4; i++) w.push([key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]]);
  var rcon = 1;
  for (i = 4; i < 44; i++) {
    var t = w[i - 1].slice(0);
    if (i % 4 === 0) {
      t.push(t.shift());
      for (var j = 0; j < 4; j++) t[j] = AES_SBOX[t[j]];
      t[0] ^= rcon;
      rcon = xtime(rcon);
    }
    w.push([w[i - 4][0] ^ t[0], w[i - 4][1] ^ t[1], w[i - 4][2] ^ t[2], w[i - 4][3] ^ t[3]]);
  }
  return w;
}

function aesAddRoundKey(st, w, round) {
  for (var c = 0; c < 4; c++) {
    var k = w[round * 4 + c];
    st[c * 4] ^= k[0];
    st[c * 4 + 1] ^= k[1];
    st[c * 4 + 2] ^= k[2];
    st[c * 4 + 3] ^= k[3];
  }
}

function aesInvSubBytes(st) {
  for (var i = 0; i < 16; i++) st[i] = AES_INV[st[i]];
}

function aesInvShiftRows(st) {
  var r, c;
  for (r = 1; r < 4; r++) {
    var row = [];
    for (c = 0; c < 4; c++) row.push(st[c * 4 + r]);
    for (c = 0; c < 4; c++) st[c * 4 + r] = row[(c - r + 4) % 4];
  }
}

function aesInvMixColumns(st) {
  for (var c = 0; c < 4; c++) {
    var a0 = st[c * 4], a1 = st[c * 4 + 1], a2 = st[c * 4 + 2], a3 = st[c * 4 + 3];
    st[c * 4] = gmul(a0, 14) ^ gmul(a1, 11) ^ gmul(a2, 13) ^ gmul(a3, 9);
    st[c * 4 + 1] = gmul(a0, 9) ^ gmul(a1, 14) ^ gmul(a2, 11) ^ gmul(a3, 13);
    st[c * 4 + 2] = gmul(a0, 13) ^ gmul(a1, 9) ^ gmul(a2, 14) ^ gmul(a3, 11);
    st[c * 4 + 3] = gmul(a0, 11) ^ gmul(a1, 13) ^ gmul(a2, 9) ^ gmul(a3, 14);
  }
}

function aesDecryptBlock(input, w) {
  var st = input.slice(0);
  aesAddRoundKey(st, w, 10);
  for (var round = 9; round >= 1; round--) {
    aesInvShiftRows(st);
    aesInvSubBytes(st);
    aesAddRoundKey(st, w, round);
    aesInvMixColumns(st);
  }
  aesInvShiftRows(st);
  aesInvSubBytes(st);
  aesAddRoundKey(st, w, 0);
  return st;
}

function aesCbcDecrypt(data, keyBytes, ivBytes) {
  aesInit();
  if (!data || !data.length || data.length % 16) return null;
  if (!keyBytes || keyBytes.length !== 16 || !ivBytes || ivBytes.length !== 16) return null;
  var w = aesExpandKey(keyBytes);
  var prev = ivBytes.slice(0);
  var out = [];
  for (var off = 0; off < data.length; off += 16) {
    var block = data.slice(off, off + 16);
    var dec = aesDecryptBlock(block, w);
    for (var i = 0; i < 16; i++) out.push(dec[i] ^ prev[i]);
    prev = block;
  }
  var pad = out[out.length - 1];
  if (pad >= 1 && pad <= 16) out = out.slice(0, out.length - pad);
  return out;
}

/* ---------------- 地址判定 ---------------- */
function isValidUrl(u) {
  var t = s(u);
  if (!/^https?:\/\/[^\s/]+/i.test(t)) return false;
  if (/^https?:\/\/[^\/]*@/i.test(t)) return false;
  return true;
}

function isDirect(u) {
  if (!isValidUrl(u)) return false;
  var t = s(u);
  if (/^https?:\/\/(?:[^\/]*\.)?(?:baidu\.con|ldmax\.cooom)\//i.test(t)) return false;
  var path = t.replace(/^https?:\/\/[^\/]+/i, "").split("?")[0].split("#")[0];
  return !/\.html?$/i.test(path);
}

function isStream(u) {
  if (!isDirect(u)) return false;
  var path = s(u).replace(/^https?:\/\/[^\/]+/i, "").split("?")[0];
  return /\.(?:m3u8?|mpd)$/i.test(path);
}

var RE_4K_HOST = /(?:^|\.)(?:ym4kjx|hd4kjx|sd4kjx|mm4kjx|mv4kjx|vk4kjx)\.lyyytv\.cn$/i;
var RE_MEDIA_EXT = /\.(?:mp4|flv|avi|mkv|ts|mov|wmv|webm|m4v)$/i;

function is4k(u) {
  var t = s(u);
  var host = (t.replace(/^https?:\/\//i, "").split("/")[0] || "").split(":")[0];
  var path = t.replace(/^https?:\/\/[^\/]+/i, "").split("?")[0].split("#")[0];
  return RE_4K_HOST.test(host) || RE_MEDIA_EXT.test(path);
}

function isLdmax(u) {
  return /^https?:\/\/ldmax\.cooom\//i.test(s(u));
}

/* ---------------- lvdou+ / ldmax 解密链 ---------------- */
function lvdou(t) {
  var r = s(t);
  if (r.indexOf("lvdou+") !== 0) return r;
  try {
    var bytes = b64ToBytes(r.slice(6));
    if (!bytes) return r;
    var k = utf8Bytes(LVDou_KEY.slice(0, 16));
    var iv = utf8Bytes(LVDou_KEY.slice(16, 32));
    var dec = aesCbcDecrypt(bytes, k, iv);
    if (!dec) return r;
    var out = utf8Decode(dec).replace(/^\s+|\s+$/g, "");
    return out.indexOf("http") === 0 ? out : r;
  } catch (e) {
    return r;
  }
}

function ldmaxDecode(t, depth) {
  depth = depth || 0;
  if (depth > 5) return "";
  var r = s(t);
  var wrapped = b64ToBytes(r);
  if (wrapped && wrapped.length) {
    var plain = utf8Decode(wrapped).replace(/\s+/g, "");
    if (plain) r = plain;
  }
  if (!isLdmax(r)) return r;
  var rest = r.replace(/^https?:\/\/ldmax\.cooom\//i, "");
  if (rest.length <= 16) return "";
  try {
    var keyStr = rest.slice(0, 16).split("").reverse().join("");
    var data = b64ToBytes(rest.slice(16));
    if (!data || !data.length || data.length % 16) return "";
    var dec = aesCbcDecrypt(data, utf8Bytes(keyStr), utf8Bytes(keyStr));
    if (!dec) return "";
    var out = utf8Decode(dec).replace(/[\x01-\x10]+$/g, "").replace(/^\s+|\s+$/g, "");
    return isLdmax(out) ? ldmaxDecode(out, depth + 1) : out;
  } catch (e) {
    return "";
  }
}

/* ============================================================================
// HTTP（只用 Widget.http.get，按 skill 要求不依赖 fetch / URLSearchParams）
// ==========================================================================*/
function withTimeout(promise, ms, fallback) {
  if (typeof setTimeout !== "function") return promise;
  return new Promise(function (resolve) {
    var done = false;
    var timer = setTimeout(function () {
      if (done) return;
      done = true;
      resolve(fallback);
    }, ms);
    promise.then(
      function (v) {
        if (done) return;
        done = true;
        try { clearTimeout(timer); } catch (e) {}
        resolve(v);
      },
      function () {
        if (done) return;
        done = true;
        try { clearTimeout(timer); } catch (e) {}
        resolve(fallback);
      }
    );
  });
}

function httpGetText(url, headers, timeoutMs) {
  var p = Widget.http.get(url, { headers: headers || {} }).then(function (res) {
    var data = res && res.data !== undefined ? res.data : res;
    if (data === null || data === undefined) return "";
    if (typeof data === "object") return JSON.stringify(data);
    return String(data);
  });
  return withTimeout(p, timeoutMs || 12000, "");
}

function httpGetJson(url, headers, timeoutMs) {
  return httpGetText(url, headers, timeoutMs).then(function (txt) {
    var obj = jsonParse(txt);
    return obj || null;
  });
}

function buildQuery(params) {
  var parts = [];
  for (var k in params) {
    if (!params.hasOwnProperty(k)) continue;
    var v = params[k];
    if (v === null || v === undefined || v === "") continue;
    parts.push(encodeURIComponent(k) + "=" + encodeURIComponent(String(v)));
  }
  return parts.join("&");
}

/* ============================================================================
// 影探 CMS
// ==========================================================================*/
async function cmsCall(path, params) {
  var q = buildQuery(params || {});
  var url = CMS_BASE + "/api.php/app/" + path + (q ? "?" + q : "");
  var txt = await httpGetText(url, CMS_HEADERS, 12000);
  var data = jsonParse(txt);
  if (!data || typeof data !== "object") throw new Error("影探接口无有效 JSON: " + path);
  if (data.code !== undefined && data.code !== null && data.code !== "") {
    var code = toInt(data.code, -1);
    if (code !== 1 && code !== 200) throw new Error("影探接口返回失败: " + path + " code=" + code);
  }
  return data;
}

/* 详情原始 JSON，5 分钟缓存（详情页与取流共用，避免重复请求） */
async function ytRaw(vid) {
  var id = s(vid).replace(/^yt:/, "");
  if (!id) return null;
  var key = "ytr:" + id;
  var hit = cacheGet(key);
  if (hit) return hit;
  var json = null;
  try {
    json = await cmsCall("video_detail", { id: id });
  } catch (e) {
    log("详情失败", id, e && e.message);
    return null;
  }
  var d = json && json.data;
  if (!d || typeof d !== "object") return null;
  return cacheSet(key, d, YT_DETAIL_TTL);
}

/* vod_url_with_player / vod_play_from+vod_play_url → 线路数组 */
function ytLinesOf(d) {
  var froms = s(d.vod_play_from).split("$$$");
  var out = [];
  var items = d.vod_url_with_player;
  var i;
  if (isArray(items)) {
    for (i = 0; i < items.length; i++) {
      var w = items[i];
      if (!w || typeof w !== "object") continue;
      var url = s(w.url);
      if (!url) continue;
      var name = s(w.name) || s(w.code) || froms[i] || "线路" + (i + 1);
      var code = s(w.code);
      out.push({
        name: name,
        code: code,
        label: code && name.indexOf(code) < 0 ? name + " · " + code : name,
        url: url
      });
    }
  }
  if (!out.length) {
    var urls = s(d.vod_play_url).split("$$$");
    for (i = 0; i < urls.length; i++) {
      if (!s(urls[i])) continue;
      out.push({ name: froms[i] || "线路" + (i + 1), code: "", label: froms[i] || "线路" + (i + 1), url: urls[i] });
    }
  }
  return out;
}

/* 「集名$地址#集名$地址」→ [{name,url}]，url 保持密文，取流时才解 */
function packLine(urlStr) {
  var out = [];
  var parts = s(urlStr).split("#");
  for (var i = 0; i < parts.length; i++) {
    var seg = parts[i];
    var pos = seg.indexOf("$");
    if (pos <= 0) continue;
    var name = s(seg.slice(0, pos)).replace(/[$#]/g, " ") || "正片";
    var url = s(seg.slice(pos + 1));
    if (!url) continue;
    out.push({ name: name, url: url });
  }
  return out;
}

/* ---------------- 解析接口 ---------------- */
function findUrl(obj) {
  if (!obj || typeof obj !== "object") return "";
  if (typeof obj.url === "string" && obj.url) return obj.url;
  if (typeof obj.playUrl === "string" && obj.playUrl) return obj.playUrl;
  if (typeof obj.link === "string" && obj.link) return obj.link;
  if (obj.data && typeof obj.data === "object") return findUrl(obj.data);
  return "";
}

function parseResult(text) {
  var body = s(text);
  if (!body) return "";
  var e = "";
  if (body.charAt(0) === "{") {
    e = findUrl(jsonParse(body));
  } else {
    e = body;
  }
  if (!e) return "";
  var r = s(e);
  if (r.charAt(0) === "{") {
    var inner = findUrl(jsonParse(r));
    if (!inner) return "";
    r = inner;
  }
  if (r.indexOf(DEC_PREFIX) !== 0) return isDirect(r) ? r : "";
  var payload = r.slice(DEC_PREFIX.length);
  if (payload.length <= 16) return "";
  var keyStr = payload.slice(0, 16);
  var cipher = b64ToBytes(payload.slice(16));
  if (!cipher || !cipher.length || cipher.length % 16) return "";
  try {
    var dec = aesCbcDecrypt(cipher, utf8Bytes(keyStr), utf8Bytes(keyStr));
    if (!dec) return "";
    var out = utf8Decode(dec).replace(/^\s+|\s+$/g, "");
    return isDirect(out) ? out : "";
  } catch (e2) {
    return "";
  }
}

/* 调解析接口：parsesId=6 给 4K 线路，parsesId=5 给网页线路。返回可播地址或 "" */
async function parseCall(url, pid) {
  var u = s(url);
  if (!u) return "";
  var quoted = encodeURIComponent(u).replace(/[!'()*]/g, function (c) {
    return "%" + c.charCodeAt(0).toString(16).toUpperCase();
  });
  var api = PARSE_API + quoted + "&parsesId=" + pid;
  var txt = await httpGetText(api, PARSE_HEADERS, 9000);
  return parseResult(txt);
}

/* 候选解析口的当前顺序（成功过的排前面，进程内记忆） */
var PARSE_ORDER = { web: null, k4: null };
function parseOrder(kind) {
  var cur = PARSE_ORDER[kind];
  if (!cur || !cur.length) {
    cur = (kind === "k4" ? PARSE_PIDS_4K : PARSE_PIDS_WEB).slice(0);
    PARSE_ORDER[kind] = cur;
  }
  return cur;
}
function parsePromote(kind, pid) {
  var arr = parseOrder(kind);
  var i = arr.indexOf(pid);
  if (i > 0) {
    arr.splice(i, 1);
    arr.unshift(pid);
  }
}

/* 依次试候选口，返回第一个可播地址；全失败返回 "" */
async function parseAny(url, kind) {
  var arr = parseOrder(kind);
  for (var i = 0; i < arr.length; i++) {
    var real = await parseCall(url, arr[i]);
    if (real) {
      parsePromote(kind, arr[i]);
      return real;
    }
  }
  return "";
}

/* ============================================================================
// 影探：列表 / 详情 / 取流
// ==========================================================================*/
function ytItem(x, mediaType) {
  var vid = s(x && x.vod_id);
  var pic = s(x && x.vod_pic);
  var remarks = s(x && x.vod_remarks);
  var score = s(x && x.vod_score);
  if (score && score !== "0.0") remarks = remarks ? remarks + " " + score : score;
  var item = {
    id: YT_LINK + vid,
    type: "url",
    title: s(x && x.vod_name),
    posterPath: pic,
    backdropPath: pic,
    coverUrl: pic,
    description: remarks,
    mediaType: mediaType || "tv",
    link: YT_LINK + vid
  };
  var rating = Number(score);
  if (rating > 0) item.rating = rating;
  return item;
}

async function ytList(tid, page, filters, mediaType) {
  var params = { tid: String(tid), pg: String(page || 1), limit: String(PAGE_SIZE) };
  if (filters) {
    for (var k in filters) {
      if (!filters.hasOwnProperty(k)) continue;
      var v = s(filters[k]);
      if (v && v !== "all") params[k] = v;
    }
  }
  var d = await cmsCall("video", params);
  var rows = isArray(d.list) ? d.list : [];
  var out = [];
  for (var i = 0; i < rows.length; i++) {
    if (!s(rows[i] && rows[i].vod_id)) continue;
    out.push(ytItem(rows[i], mediaType));
  }
  return out;
}

/* 详情：合并各线路为一份分集，线路留到 loadResource 再算 */
async function ytDetail(link) {
  var vid = s(link).replace(/^yt:/, "");
  if (!vid) return null;
  var key = "ytd:" + vid;
  var hit = cacheGet(key);
  if (hit) return hit;

  var d = await ytRaw(vid);
  if (!d) return null;
  var lines = ytLinesOf(d);
  var maxLen = 0;
  for (var i = 0; i < lines.length; i++) {
    var eps = packLine(lines[i].url);
    if (eps.length > maxLen) maxLen = eps.length;
  }
  var isMovie = maxLen <= 1;

  var episodeItems = [];
  for (var e = 0; e < maxLen; e++) {
    var pid = YT_PLAY + b64urlEncode(JSON.stringify({ v: vid, i: e }));
    episodeItems.push({
      id: pid,
      type: "url",
      title: isMovie ? "正片" : "第" + (e + 1) + "集",
      episode: e + 1,
      mediaType: isMovie ? "movie" : "tv",
      link: pid
    });
  }

  var name = s(d.vod_name);
  var pic = s(d.vod_pic);
  var remarks = s(d.vod_remarks);
  var desc = s(d.vod_content) || s(d.vod_blurb);
  var actors = s(d.vod_actor);
  if (actors) desc = "主演：" + actors + (desc ? "\n" + desc : "");
  var note = "线路 " + lines.length + " 条" + (maxLen > 1 ? " · 共 " + maxLen + " 集" : "");
  desc = (remarks ? remarks + "\n" : "") + note + (desc ? "\n" + desc : "");

  var item = {
    id: YT_LINK + vid,
    type: "url",
    title: name,
    posterPath: pic,
    backdropPath: pic,
    coverUrl: pic,
    description: desc,
    mediaType: isMovie ? "movie" : "tv",
    link: YT_LINK + vid,
    episodeItems: episodeItems
  };
  var rating = Number(s(d.vod_score));
  if (rating > 0) item.rating = rating;
  if (s(d.vod_class)) item.genreTitle = s(d.vod_class).replace(/,/g, " / ");
  if (!episodeItems.length) log("影探详情无可用线路", vid);
  return cacheSet(key, item, YT_DETAIL_TTL);
}

function mkResource(name, desc, url, headers) {
  return {
    name: name,
    description: desc,
    url: url,
    customHeaders: headers || PARSE_HEADERS,
    playerType: "app"
  };
}

/* 网页解析出来的 m3u8 常被上游换成「403 / 反爬 HTML」，这里做一次轻量探活：
 *   2xx 且正文不是 HTML → 收；4xx/5xx 或明显 HTML → 丢；网络未知 → 保留（不误杀）。 */
async function probeHls(url) {
  var path = s(url).replace(/^https?:\/\/[^\/]+/i, "").split("?")[0];
  if (/\.(?:mpd|mp4|mkv|flv|ts|m4v)$/i.test(path)) return true; // 非 HLS，正文本来就是二进制/XML
  var res = await withTimeout(
    Widget.http.get(url, { headers: PARSE_HEADERS }).then(function (r) { return r; }, function () { return null; }),
    6000,
    null
  );
  if (!res) return true;
  var st = toInt(res.status, 0);
  if (st && (st < 200 || st >= 300)) return false;
  var d = typeof res.data === "string" ? res.data : "";
  var isM3u8 = /\.m3u8?$/i.test(path);
  if (isM3u8) return d.indexOf("#EXTM3U") >= 0; // 真 m3u8 必有这个标记
  var head = d.replace(/^\s+/, "").slice(0, 64).toLowerCase();
  if (head.indexOf("<") === 0 || head.indexOf("<!doctype") === 0) return false;
  return true;
}

/* 单条线路 → 可播地址：流直连，4K 走 parsesId=6，网页走 parsesId=5 */
async function ytResolveLine(line, ep) {
  var u = lvdou(ep.url);
  if (isLdmax(u)) u = ldmaxDecode(u);
  if (!isValidUrl(u)) return null;
  if (isStream(u)) {
    return mkResource(line.label, "HLS/MPD 直链 · " + ep.name, u);
  }
  if (is4k(u)) {
    var real4k = await parseAny(u, "k4");
    if (real4k) return mkResource(line.label, "4K 直链（解析）· " + ep.name, real4k);
    return null;
  }
  var realWeb = await parseAny(u, "web");
  if (!realWeb) return null;
  if (realWeb !== u && !(await probeHls(realWeb))) {
    log("网页线路探活失败，已跳过", line.label);
    return null;
  }
  return mkResource(line.label, "网页解析 · " + ep.name, realWeb);
}

/* 取某一集在所有线路的地址（并发解析，结果缓存 2 分钟） */
async function ytResourcesAt(vid, idx) {
  var ck = "p:" + vid + ":" + idx;
  var hit = cacheGet(ck);
  if (hit) return hit;

  var d = await ytRaw(vid);
  if (!d) return [];
  var lines = ytLinesOf(d);
  var jobs = [];
  for (var i = 0; i < lines.length; i++) {
    var eps = packLine(lines[i].url);
    var ep = eps[idx];
    if (!ep) continue;
    jobs.push(ytResolveLine(lines[i], ep));
  }
  var results = await Promise.all(jobs);

  var out = [];
  var seen = {};
  for (var j = 0; j < results.length; j++) {
    var r = results[j];
    if (!r || !r.url || seen[r.url]) continue;
    seen[r.url] = 1;
    out.push(r);
  }
  return cacheSet(ck, out, out.length ? PLAY_TTL : FAIL_TTL);
}

/* ============================================================================
// 模块函数
// ==========================================================================*/
async function ytLatest(params) {
  params = params || {};
  return ytList(1, toInt(params.page, 1), {
    "class": params["class"], area: params.area, year: params.year
  }, "movie");
}

async function ytTv(params) {
  params = params || {};
  return ytList(21, toInt(params.page, 1), {
    "class": params["class"], area: params.area, year: params.year
  }, "tv");
}

async function ytGuoman(params) {
  params = params || {};
  return ytList(23, toInt(params.page, 1), {
    "class": params["class"], area: params.area, year: params.year
  }, "tv");
}

async function ytDuanju(params) {
  params = params || {};
  return ytList(22, toInt(params.page, 1), {
    "class": params["class"], year: params.year
  }, "tv");
}

async function ytMore(params) {
  params = params || {};
  var tid = s(params.cat) || "25";
  var kind = MOVIE_TIDS[tid] ? "movie" : "tv";
  return ytList(tid, toInt(params.page, 1), null, kind);
}

/* 详情入口：App 传 link 字符串 */
async function loadDetail(link) {
  var l = s(link);
  if (!l) return null;
  try {
    if (l.indexOf(YT_LINK) === 0) return await ytDetail(l);
    if (l.indexOf(YT_PLAY) === 0) {
      var res = await loadResource({ link: l });
      if (res && res.length) {
        return {
          id: l, type: "url", title: "播放", mediaType: "tv", link: l,
          videoUrl: res[0].url, customHeaders: res[0].customHeaders || {}
        };
      }
      return null;
    }
    if (isDirect(l)) return { id: l, type: "url", title: "直链", mediaType: "movie", link: l, videoUrl: l };
  } catch (e) {
    log("loadDetail 异常", e && e.message);
  }
  return null;
}

/* 搜索：影探 CMS + 红果官方 XHR 接口 */
async function search(params) {
  params = params || {};
  var kw = s(params.keyword || params.key || params.text);
  var page = toInt(params.page, 1);
  if (!kw) return [];
  var out = [];
  var seen = {};

  try {
    var d = await cmsCall("search", { text: kw, pg: String(page) });
    var rows = isArray(d.list) ? d.list : [];
    for (var i = 0; i < rows.length; i++) {
      var vid = s(rows[i] && rows[i].vod_id);
      if (!vid || seen["yt" + vid]) continue;
      seen["yt" + vid] = 1;
      out.push(ytItem(rows[i], "tv"));
    }
  } catch (e) {
    log("影探搜索失败", kw, e && e.message);
  }

  return out;
}

/* 起播入口：返回 VideoResource[]，每一项就是播放器里的一条线路 */
async function loadResource(params) {
  params = params || {};
  var link = s(params.link || params.videoUrl || params.id || "");
  if (!link && params.item) link = s(params.item.link || params.item.videoUrl || params.item.id);
  if (!link) return [];

  try {
    if (link.indexOf(YT_PLAY) === 0) {
      var payload = jsonParse(b64urlDecode(link.slice(YT_PLAY.length)));
      if (!payload || !s(payload.v)) return [];
      return await ytResourcesAt(s(payload.v), toInt(payload.i, 0));
    }
    if (link.indexOf(YT_LINK) === 0) {
      var det = await ytDetail(link);
      if (det && det.episodeItems && det.episodeItems.length) return await loadResource({ link: det.episodeItems[0].link });
      return [];
    }
    if (isDirect(link)) return [mkResource("直链", "", link, {})];
  } catch (e) {
    log("取流异常", e && e.message);
  }
  return [];
}

/* 导出（部分运行时按 CommonJS 取模块；App 主要读全局） */
if (typeof module !== "undefined" && module && module.exports) {
  module.exports = {
    meta: WidgetMetadata,
    loadDetail: loadDetail,
    loadResource: loadResource,
    search: search
  };
}
