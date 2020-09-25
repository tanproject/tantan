import time
import json
from hashlib import md5
import requests
import random

import os
import sys

from my_tt import config


# v_code = str(random.randint(100000, 999999))




def send_msg(phonenum,v_code):
    vars = json.dumps({'code': v_code}) #验证码需要处理
    timestamp = int(time.time())    #需要用到模块不宜放在cnfig下
    args = {
        'appid': config.sd_appid,
        'to': phonenum,
        'project': config.sd_project,
        'vars': vars,
        'timestamp': timestamp,
        'sign_type': config.sd_sign_type,
    }
    # 计算参数的签名
    sorted_args = sorted(args.items())  # 提取每一项
    print(sorted_args)
    print([f'{key}={value}' for key, value in sorted_args])
    args_str = '&'.join([f'{key}={value}' for key, value in sorted_args])  # 对参数排序、组合
    sign_str = f'{config.sd_appid}{config.sd_appkey}{args_str}{config.sd_appid}{config.sd_appkey}'.encode(
        'utf8')  # 拼接成待签名字符串
    signature = md5(sign_str).hexdigest()  # 计算签名
    args['signature'] = signature  # 把签名放到args里

    response = requests.post(config.sd_api, data=args)
    if response.status_code == 200:
        result = response.json()
        print('短信结果：', result)
        if result.get('status') == 'success':
            return True
    return False
