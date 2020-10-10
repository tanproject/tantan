import datetime

from my_tt import config
from UserApp.models import User, Profile
from SocialApp.models import Swiped, Friend
from libs.cache import rds
from common import keys, errors

from django.db.transaction import atomic
from django.db.models import Q


def rcmd_from_list(user_id):
    '''从优先推荐列表取出滑动用户'''
    uid_list = rds.lrange(keys.PRIOR_RCMD_LIST % user_id, 0, 19)
    uid_list = [int(uid) for uid in uid_list]  # 将bytes类型强转为int类型
    users = User.objects.filter(id__in=uid_list)
    return users


def rcmd_from_db(user_id, num=20):
    '''从数据库里取出滑动用户'''
    user_profile = Profile.objects.get(id=user_id)
    today = datetime.date.today()
    '''计算最大和最小交友年龄对应的出生日期'''
    earliest_birthday = today - \
                        datetime.timedelta(user_profile.max_dating_age * 365)
    latest_birthday = today - \
                      datetime.timedelta(user_profile.min_dating_age * 365)

    '''找出自己所以滑过的用户'''
    slide_list = Swiped.objects.filter(user_id=user_id).values_list('sid', flat=True)

    # 排除已经滑过的人
    users = User.objects.filter(
        gender=user_profile.dating_gender,
        location=user_profile.dating_location,
        birthday__range=[earliest_birthday, latest_birthday]
    ).exclude(id__in=slide_list)[:num]
    # (懒加载)只取前20个，users即便有了切片依然是queryset对象因为这包含多个对象。

    return users


def rcmd(user_id):
    '''推荐滑动用户'''
    first_users = rcmd_from_list(user_id)
    lack = 20 - len(first_users)  # 计算离20个还差几个
    if lack == 0:
        return first_users
    else:
        second_users = rcmd_from_db(user_id, lack)
        return set(first_users) | set(second_users)


@atomic
def like_someone(user_id, sid):
    '''添加滑动记录'''
    Swiped.swpied(user_id, sid, 'like')

    '''在自己的优先推荐列表里删除对方id'''
    rds.lrem(keys.PRIOR_RCMD_LIST % user_id, value=sid)

    '''检查对方是否上滑（superlike）或右滑（like）过你'''
    liked = Swiped.is_liked(user_id, sid)
    if liked is True:
        '''如果对方也喜欢过你，将你们匹配为好友'''
        Friend.make_friends(user_id, sid)

        return True
    else:
        return False


@atomic
def superlike_someone(user_id, sid):
    '''超级喜欢某人'''
    '''添加滑动记录'''
    Swiped.swpied(user_id, sid, 'superlike')

    '''在自己的优先推荐列表里删除对方id'''
    rds.lrem(keys.PRIOR_RCMD_LIST % user_id, value=sid)

    '''检查对方是否上滑（superlike）或右滑（like）过你'''
    liked = Swiped.is_liked(user_id, sid)
    if liked is True:  # 对方喜欢你
        '''如果对方也喜欢过你，将你们匹配为好友'''
        Friend.make_friends(user_id, sid)
        return True

    elif liked is False:  # 对方不喜欢你
        return False

    else:  # 对方没有滑过你，将你的id给到对方的优先推荐列表
        rds.rpush(keys.PRIOR_RCMD_LIST % sid, user_id)
        return False


@atomic
def dislike_someone(user_id, sid):
    '''添加滑动记录'''
    Swiped.objects.create(user_id=user_id, sid=sid, stype='dislike')

    '''删除自己Redis缓存的优先推荐列表里，对方的id'''
    rds.lrem(keys.PRIOR_RCMD_LIST % user_id, value=sid)


def rewind_last_swiped(user_id):
    ''' 撤销最后⼀次滑动,每天允许反悔三次，反悔时间距上一次滑动时间不超过5分钟'''
    now = datetime.datetime.now()
    rewind_key = keys.REWIND_TIMES_K % (now.date(), user_id)
    # 1检查今天的反悔次数是否超过三次
    rewind_times = rds.get(rewind_key, 0)
    if rewind_times > config.REWIND_TIMES:
        raise errors.RewindLimit()

    # 2找到最后一次滑动
    last_swpied = Swiped.objects.filter(user_id=user_id).latest('stime')

    # 3检查最后一次滑动时间距离现在是否在5分钟内
    past_time = (now - last_swpied.stime).total_seconds()
    if past_time > config.REWIND_TIMEOUT:
        raise errors.RewindTimeout()

    with atomic():
        # 4删除好友关系（只要上一次滑动类型是喜欢或超级喜欢，都有可能匹配为好友）
        if last_swpied.stype in ['like', 'superlike']:
            Friend.remove_relation(user_id, last_swpied.sid)
            # 5如果最后一次滑动是超级喜欢删除自己在对方的优先推荐列表
            if last_swpied.stype == 'superlike':
                rds.lrem(keys.PRIOR_RCMD_LIST % last_swpied.sid, value=user_id)

        # 6删除滑动记录
        last_swpied.delete()
        # 今日反悔次数加一
        rds.set(rewind_key, rewind_times + 1, 86500)  # 缓存过期时间为一天零100秒


def show_like_me(user_id):
    '''找出自己滑过的人'''
    sid_list = Swiped.objects.filter(user_id=user_id).values_list('sid', flat=True)

    '''找出喜欢或超级喜欢我的人，附加条件：排除那些我划过的人'''
    fans_id_list = Swiped.objects.filter(sid=user_id, stype__in=['like', 'superlike']) \
        .exclude(user_id__in=sid_list) \
        .values_list('user_id', flat=True)
    fans = User.objects.filter(id__in=fans_id_list)
    return fans


def show_my_friend(uid):
    '''查找自己所有好友的ID'''
    condition = Q(user_id1=uid) | Q(user_id2=uid)
    friends_id_list = []
    for friend in Friend.objects.filter(condition):
        if friend.user_id1 == uid:
            friends_id_list.append(friend.user_id2)
        else:
            friends_id_list.append(friend.user_id1)

    all_friends=User.objects.filter(id__in=friends_id_list)

    return all_friends