from django.http import JsonResponse
from UserApp.logics import send_vcode
from django.core.cache import cache
from UserApp.models import User, Profile
from UserApp.forms import Userform
from UserApp.forms import Profileform


def fetch_vcode(request):
    '''给用户发送验证码'''
    phonenum = request.GET.get('phonenum')  # 获取用户输入的手机号
    '''判断是否为一个合理的手机号'''
    if send_vcode(phonenum):
        return JsonResponse({'code': 0, 'data': None})
    else:
        return JsonResponse({'code': 1000, 'data': '验证码发送失败'})


def submit_vcode(request):
    '''获取用户输入的手机号和验证码'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    '''比对缓存里的验证码'''
    key = f'v_code{phonenum}'
    cache_vcode = cache.get(key)
    if vcode and vcode == cache_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User()
            user.phonenum = phonenum
            user.nickname = phonenum
            user.save()
        request.session['user_id'] = user.id
        return JsonResponse({'code': 0, 'data': user.to_dict()})
    else:
        return JsonResponse({'code': 1001, 'data': '验证码错误'})


def show_profile(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    profile = user.get_profile

    return JsonResponse({'code': 0, 'data': profile.to_dict()})


def update_profile(request):
    '''修改个人资料和交友资料'''
    '''定义form类的对象'''
    user_form = Userform(request.POST)
    profile_form = Profileform(request.POST)
    '''验证这两个数据（类字典）的有效性'''
    if user_form.is_valid() and profile_form.is_valid():
        user_id=request.session.get['user_id']
        User.objects.filter(id=user_id).update(**user_form.cleaned_data)
        Profile.objects.get_or_create(id=user_id,defaults=profile_form.cleaned_data)
        return JsonResponse({'code':0,'data':'修改成功'})
    else:
        err={}
        err.update(user_form.errors)
        err.update(profile_form.errors)
        return JsonResponse({'code':1003,'data':err})


AccessKey='kgtGHMPLUtKBqkMbA75j5Fu_3GHAASVfh6m50TD4'
SecretKey='fb7q_ca7gKwoUayr8ceDd9qrP7--bFEbJoibh54G'
CDN='qhdgby653.hd-bkt.clouddn.com'
space='tantan007'