import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from common import errors
from libs.http import render_json

err_log=logging.getLogger('err')

'''登录需求中间件'''


class LoginRequiredMiddleware(MiddlewareMixin):
    '''访问白名单里的接口无需登录'''
    white_list = [
        '/api/user/vcode/fetch',
        '/api/user/vcode/submit',
        '/qiniu/callback',
        '/',
        'api/social/rank',
    ]

    def process_request(self, request):
        '''检查当前访问接口是否在白名单里'''
        if request.path in self.white_list:
            '''如果不在直接返回，停止执行此函数'''
            return
        else:
            '''获取并检查session的user_id'''
            user_id = int(request.session.get('user_id'))
            if not user_id:
                return JsonResponse({'code': 1002, 'data': "用户未登录！"})
            else:
                request.uid=user_id



class LogicErrMiddleware(MiddlewareMixin):
    '''逻辑异常处理中间件'''
    def process_exception(self, request, exception):
        if isinstance(exception, errors.LogicErr):
            err_log.error(f'逻辑异常:{exception.code}-{exception.data}')
            return render_json(data=exception.data, code=exception.code)
