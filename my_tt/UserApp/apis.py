import logging

from UserApp.logics import send_vcode
from libs.redis_cache import rds
from UserApp.models import User, Profile
from UserApp.forms import Userform
from UserApp.forms import Profileform
from libs.qiniu_cloud import gen_token
from libs.qiniu_cloud import get_res_url
from libs.http import render_json
from common import errors,keys

info_log=logging.getLogger('inf')


def fetch_vcode(request):
    '''给用户发送验证码'''
    phonenum = request.GET.get('phonenum')  # 获取用户输入的手机号
    send_vcode.delay(phonenum)
    return render_json()
    # '''判断是否为一个合理的手机号'''
    # if send_vcode(phonenum):
    #     pass
    # else:
    #     # return JsonResponse({'code': 1000, 'data': '验证码发送失败'})
    #     return render_json(data='验证码发送失败', code=errors.VCODE_FAILED)


def submit_vcode(request):
    '''获取用户输入的手机号和验证码'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    '''比对缓存里的验证码'''
    key = keys.VCODE_K % (phonenum)
    cache_vcode = rds.get(key)
    if vcode and vcode == cache_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
            info_log.info(f'user login:{user.id}-{user.phonenum}')
        except User.DoesNotExist:
            user = User()
            user.phonenum = phonenum
            user.nickname = phonenum
            user.save()
            info_log.info(f'user register:{user.id}-{user.phonenum}')
        request.session['user_id'] = user.id
        # return JsonResponse({'code': 0, 'data': user.to_dict()})
        return render_json(data=user.to_dict())
    else:
        raise errors.VcodeErr()
        # return render_json(data='验证码错误', code=errors.VCODE_ERR)


def show_profile(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    profile = user.get_profile

    return render_json(data=profile.to_dict())
    # return JsonResponse({'code': 0, 'data': profile.to_dict()})


def update_profile(request):
    '''修改个人资料和交友资料'''
    '''定义form类的对象'''
    user_form = Userform(request.POST)
    profile_form = Profileform(request.POST)
    '''验证这两个数据（类字典）的有效性'''
    if user_form.is_valid() and profile_form.is_valid():
        user_id = request.session.get('user_id')
        User.objects.filter(id=user_id).update(**user_form.cleaned_data)
        Profile.objects.update_or_create(id=user_id, defaults=profile_form.cleaned_data)
        return render_json()
    else:
        err = {}
        err.update(user_form.errors)
        err.update(profile_form.errors)
        raise errors.ProfileErr(data=err)
        # return render_json(data=err, code=errors.PROFILE_ERR)
        # return JsonResponse({'code':1003,'data':err})


def qn_token(request):
    user_id = request.session.get('user_id')
    filename = f'Avatar-{user_id}'
    token = gen_token(user_id, filename)
    return render_json(data={'token': token, 'key': filename})


def qn_callback(request):
    uid = request.POST.get('uid')
    key = request.POST.get('key')
    avatar_url = get_res_url(key)
    '''将保存在七牛云上头像地址，保存到数据库'''
    User.objects.filter(id=uid).update(avatar=avatar_url)
    return render_json(data=avatar_url)
    # return JsonResponse({'code':0,'data':avatar_url})
