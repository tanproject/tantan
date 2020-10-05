from django.db import models


# Create your models here.
class User(models.Model):
    genders = (
        ('male', '男'),
        ('female', '女'),
        ('unknow', '未知'),
    )
<<<<<<< HEAD
    LOCATIONS = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('成都', '成都'),
        ('西安', '西安'),
        ("武汉", "武汉"),
        ("沈阳", "沈阳")
    )
=======
>>>>>>> 1842f83a6a852b5e182b58d487f57075cc926635
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=20, db_index=True, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=genders, default='male', verbose_name='性别')
    birthday = models.DateField(default='2002-01-01', verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=10, default='上海', verbose_name='常居地')

    class Meta:
        db_table = 'user'

    @property  #使实例方法成为类属性，实例对象也可调用类方法
    def get_profile(self):
        '''判断self身上是否有这个属性，如果没有说明是第一次，正常查询数据库，如果有就不必再次查询数据库，直接在属性例获取'''
        if not hasattr(self,'profile'):
            '''将这行这整行数据挂到self身上，这行数据成了self的属性,例：self.profile.dating_gender'''
            self.profile,_=Profile.objects.get_or_create(id=self.id)
        return self.profile

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'birthday': str(self.birthday),
            'avatar': self.avatar,
            'location': self.location,
        }


class Profile(models.Model):
    '''用户的交友资料'''
    dating_location = models.CharField(max_length=10, default='上海',
                                       verbose_name='目标城市')
    dating_gender = models.CharField(max_length=10, choices=User.genders,
                                     default='female', verbose_name='匹配的性别')

    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=50, verbose_name='最大查找范围')

    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')

    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='不让陌生人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    class Meta:
        db_table = 'profile'

    def to_dict(self):
        return {
            'id': self.id,
            'dating_location': self.dating_location,
            'dating_gender': self.dating_gender,
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'min_dating_age': self.min_dating_age,
            'max_dating_age': self.max_dating_age,
            'vibration': self.vibration,
            'only_matched': self.only_matched,
            'auto_play': self.auto_play,
        }
