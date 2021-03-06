import logging
import re
import random
import json
from libs.redis_cache import rds
from libs.message import send_msg
from common import keys
from tasks import celery_app
info_log=logging.getLogger('inf')



def is_phonenum(phonenum):
    '''验证是否是一个正确的手机号'''
    if re.match(r'1[3-9]\d{9}$', phonenum):
        return True
    else:
        return False



@celery_app.task
def send_vcode(phonenum):
    if is_phonenum(phonenum) is False:
        return False
    else:
        key = keys.VCODE_K % phonenum  # 将手机号设置为key，为了便于区分这是验证码的key，加上前缀
        '''检查缓存里是否有验证码，防止用户频繁申请验证码'''
        if rds.get(key):
            return True
        else:
            vcode = str(random.randint(100000, 999999))
            '''需要将上面的验证码添加到缓存，并且多给些时间'''
            rds.set(key,vcode,600)
            info_log.info(f'已向手机号是{phonenum}的用户，发送了验证码：{vcode}')
            return send_msg(phonenum,vcode)