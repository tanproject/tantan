from libs.http import render_json
from SocialApp import logics
from VipApp.logics import perm_required
from my_tt import config


def rcmd_users(request):
    '''获取推荐用户'''
    users = logics.rcmd(request.uid)
    users_list = [user.to_dict(exclude=['phonenum']) for user in users]
    return render_json(data=users_list)


def like(request):
    '''喜欢（右滑）'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.uid, sid)
    return render_json(data={'is_match': is_matched})


@perm_required('superlike')
def superlike(request):
    '''超级喜欢（上滑）'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.uid, sid)
    return render_json(data={'is_match': is_matched})


def dislike(request):
    '''不喜欢（左滑）'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.uid, sid)
    return render_json()


@perm_required('rewind')
def rewind(request):
    '''反悔（单独按钮）'''
    logics.rewind_last_swiped(request.uid)
    return render_json()


@perm_required('show_fans')
def show_fans(request):
    '''查看喜欢过我的人'''
    fans = logics.show_like_me(request.uid)
    fans_data = [fan.to_dict(exclude=['phonenum']) for fan in fans]
    return render_json(data=fans_data)


def show_friends(request):
    uid = request.uid
    all_friends = logics.show_my_friend(uid)
    friends_list = [f.to_dict() for f in all_friends]
    return render_json(data=friends_list)


def ranking_list(request):
    rank_date=logics.get_rank_list(config.RANK_NUM)
    return render_json(data=rank_date)