from libs.http import render_json



def rcmd_users(request):
    '''获取推荐用户'''
    return render_json()

def like(request):
    '''喜欢（右滑）'''
    return render_json()

def superlike(request):
    '''超级喜欢（上滑）'''
    return render_json()

def dislike(request):
    '''不喜欢（左滑）'''
    return render_json()

def rewind(request):
    '''返回（单独按钮）'''
    return render_json()

def show_fans(request):
    '''查看喜欢过我的人'''
    return render_json()


