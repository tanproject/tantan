from django.http import JsonResponse
from UserApp.logics import send_vcode
from django.core.cache import cache
from UserApp.models import User


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
            user=User()
            user.phonenum=phonenum
            user.nickname=phonenum
            user.save()
        request.session['user_id']=user.id
        return JsonResponse({'code':0,'data':user.to_dict()})
    else:
        return JsonResponse({'code':1001,'data':'验证码错误'})


def show_profile(request):
    return JsonResponse({'code':0,'data':'测试成功'})