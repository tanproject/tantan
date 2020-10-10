'''程序逻辑配置，及第三方平台配置'''

'''赛迪云通信所需参数'''
sd_appid = '54897'
sd_appkey = '8ce48d7a312f789cd28575ff881b1c8f'
sd_project = 'q1nuH3'  # 'WSaOd3'
sd_api = 'https://api.mysubmail.com/message/xsend.json'
sd_sign_type = 'md5'

'''七牛云配置'''
QN_DOMAIN = 'qhdgby653.hd-bkt.clouddn.com'
QN_BUCKET = 'tantan007'
QN_ACCESS_KEY = 'kgtGHMPLUtKBqkMbA75j5Fu_3GHAASVfh6m50TD4'
QN_SECRET_KEY = 'fb7q_ca7gKwoUayr8ceDd9qrP7--bFEbJoibh54G'
QN_CALLBACK_URL = '49.234.220.221:8000/qiniu/callback'
QN_CALLBACK_DOMAIN = '49.234.220.221:8000'

'''Redis 配置'''
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 2,
}

'''反悔条件配置'''
REWIND_TIMES = 3  # 每日反悔次数
REWIND_TIMEOUT = 5 * 60  # 反悔超时时间
