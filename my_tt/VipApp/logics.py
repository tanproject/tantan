from VipApp.models import Vip
from UserApp.models import User
from common import errors

def perm_required(perm_name):
    '''检查当前用户的vip是否拥有某权限'''
    def outer(view_func):
        def inner(request,*args,**kwargs):
            user=User.objects.get(id=request.uid)
            if user.vip.has_perm(perm_name):
                return view_func(request,*args,**kwargs)
            else:
                raise errors.PermissionErr
        return inner
    return outer