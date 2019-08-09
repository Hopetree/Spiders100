# -*- coding:utf-8 -*-
import requests
import json
import time
dstr = int(time.time()*1000)
headers = {
    'Referer': 'https://vdisk.weibo.com/s/tg6IJ27yoga8g?category_id=0&parents_ref=,tg6IJ27yogat5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
}

url = 'https://vdisk.weibo.com/api/weipan/fileopsStatCount?link=tg6IJ27yoga8d&ops=download&wpSign=666882e7754bbbe55e13970be7b093ac.1565341348&_={}'.format(dstr)
req = requests.get(url,headers=headers)
res = json.loads(req.text)


print(res)
