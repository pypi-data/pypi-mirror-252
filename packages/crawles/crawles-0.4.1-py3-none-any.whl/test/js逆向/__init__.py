# coding = utf-8
import requests
import execjs

with open('d1.js', 'r', encoding='utf-8') as f:
    js = execjs.compile(f.read())

url = 'https://webapi.cninfo.com.cn/api/sysapi/p_sysapi1007'

cookies = {
    # 'Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b': '1705384072',
    # 'Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b': '1705327862,1705384033',
    # 'MALLSSID': '4D4B705156364C394A73316F345A4659725470762B70664F39395955456C61566E7053366459434773596D384254363251742F4E55642B6352566C36302F3558',
}

headers = {
    # 'Accept': '*/*',
    'Accept-EncKey': js.call('getResCode'),
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Origin': 'https://webapi.cninfo.com.cn',
    # 'Pragma': 'no-cache',
    'Referer': 'https://webapi.cninfo.com.cn/',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
    # 'X-Requested-With': 'XMLHttpRequest',
    # 'sec-ch-ua': '\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '\"Windows\"',
}

data = {
    'market': 'SZE',
    'tdate': '2024-01-15',
}

# 当前时间戳: 1705384169.8095796
response = requests.post(url, headers=headers, data=data, cookies=cookies)
print(response.text)
