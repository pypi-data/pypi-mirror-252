# coding = utf-8
import crawles

url = 'https://webapi.cninfo.com.cn/api/sysapi/p_sysapi1007'

cookies = { 
    'Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b': '1705384855',
    'Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b': '1705384843',
    'MALLSSID': '6F5867575A6F7041634656746679754874587370646454593769483255494A6843784E7851764761767A44634446735A4877794433346F475A676C637464434B',
    'b-user-id': 'fc0eee2b-e1cf-27f5-a47d-c32de2433f53',
}

headers = { 
    'Accept': '*/*',
    'Accept-EncKey': '8hn2ufcSvlJqagSk4HXk1Q==',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://webapi.cninfo.com.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://webapi.cninfo.com.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
}

data = { 
    'market': 'SZE',
    'tdate': '2024-01-14',
}


# 当前时间戳: 1705388770.0042071
response = crawles.post(url, headers=headers, data=data, cookies=cookies)
print(response.text)

