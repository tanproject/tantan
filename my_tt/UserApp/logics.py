import re
import random
import json
from libs.Redis import rds

from libs.message import send_msg

from django.core.cache import cache

def is_phonenum(phonenum):
    '''验证是否是一个正确的手机号'''
    if re.match(r'1[3-9]\d{9}$', phonenum):
        return True
    else:
        return False




def send_vcode(phonenum):
    if is_phonenum(phonenum) is False:
        return False
    else:
        key = f'v_code{phonenum}'  # 将手机号设置为key，为了便于区分这是验证码的key，加上前缀
        '''检查缓存里是否有验证码，防止用户频繁申请验证码'''
        if rds.get(key):
            return True
        else:
            vcode = str(random.randint(100000, 999999))
            '''需要将上面的验证码添加到缓存，并且多给些时间'''
            cache.set(key,vcode,600)
            return send_msg(phonenum,vcode)