from django.db import models, IntegrityError


# Create your models here.
from common import errors


class Swiped(models.Model):
    '''滑动记录表'''
    STYPES = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢'),
    )
    user_id = models.IntegerField(verbose_name='当前用户id')
    sid = models.IntegerField(verbose_name='被滑的用户id')
    stype = models.CharField(max_length=9, choices=STYPES, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动的时间')
    '''为避免服务器出现bug，所以不能再次滑动曾经出现过的用户,
        意味着这条滑动记录只能出现一次'''

    class Meta:
        db_table = 'slide_record'
        unique_together = ['user_id', 'sid']

    @classmethod
    def is_liked(cls, user_id, sid):
        '''检查对方是否喜欢过自己'''
        swiped = Swiped.objects.filter(user_id=sid, sid=user_id).first()
        if not swiped:
            return None  # 说明没滑过
        elif swiped.stype in ['like', 'superlike']:
            return True  # 喜欢过
        else:
            return False  # 不喜欢

    @classmethod
    def swpied(cls, user_id, sid, stype):
        try:
            cls.objects.create(user_id=user_id, sid=sid, stype=stype)
        except IntegrityError:
            raise errors.RepeatSwipeErr


class Friend(models.Model):
    '''好友关系表'''
    user_id1 = models.IntegerField()
    user_id2 = models.IntegerField()

    class Meta:
        unique_together = ['user_id1', 'user_id2']

    @classmethod
    def make_friends(cls, user_id1, user_id2):
        user_id1, user_id2 = (user_id1, user_id2) if user_id1 < user_id2 else (user_id2, user_id1)
        Friend.objects.create(user_id1=user_id1, user_id2=user_id2)

    @classmethod
    def remove_relation(cls,user_id1,user_id2):
        user_id1, user_id2 = (user_id1, user_id2) if user_id1 < user_id2 else (user_id2, user_id1)
        cls.objects.filter(user_id1=user_id1,user_id2=user_id2).delete()
