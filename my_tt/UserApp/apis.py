from django.http import JsonResponse
from UserApp.logics import send_vcode

def fetch_vcode(request):
    '''给用户发送验证码'''
    phonenum=request.Get.get('phonenum')#获取用户输入的手机号
    '''判断是否为一个合理的手机号'''
    if send_vcode(phonenum):
        return JsonResponse({'code':0,'data':None})
    else:
        return JsonResponse({'code':1000,'data':'验证码发送失败'})