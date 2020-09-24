import time
import json
from hashlib import md5
import requests
import random

appid = '54897'
appkey = '8ce48d7a312f789cd28575ff881b1c8f'
project = 'WSaOd3'
api = 'https://api.mysubmail.com/message/xsend.json'
vars = json.dumps({'code': str(random.randint(100000,999999))})
to = '15270823532'  # 手机号
timestamp = int(time.time())
sign_type = 'md5'

args = {
    'appid': appid,
    'to': to,
    'project': project,
    'vars': vars,
    'timestamp':timestamp,
    'sign_type':sign_type,
}
# 计算参数的签名
sorted_args = sorted(args.items())  # 提取每一项
args_str = '&'.join([f'{key}={value}' for key, value in sorted_args])  # 对参数排序、组合
sign_str = f'{appid}{appkey}{args_str}{appid}{appkey}'.encode('utf8')  # 拼接成待签名字符串
signature = md5(sign_str).hexdigest()  # 计算签名
args['signature']=signature      #把签名放到args里

'''测试阶段'''
response=requests.post(api,data=args)
print('状态码:',response.status_code)

result=response.json()

print('短信结果:',result)


