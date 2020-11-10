from django.db.models import query
from django.db.models import base
from django.db import models
import datetime

from libs.cache import rds
from common.keys import MODEL_K


def get(self, *args, **kwargs):
    """
    Perform the query and return a single object matching the given
    keyword arguments.
   """
    cls_name = self.model.__name__
    pk = kwargs.get('pk') or kwargs.get('id')
    if pk:
        '''说明已经有了缓存，直接从缓存获取数据'''
        key = MODEL_K % (cls_name, pk)
        model_obj = rds.get(key)
        if isinstance(model_obj, self.model):
            print('数据来自缓存')
            return model_obj

    '''主键不在，说明缓存里没有，只能从数据库里取'''
    model_obj = self._get(*args, **kwargs)
    print('数据来自数据库')
    '''将这次取出的对象加入缓存中'''
    key = MODEL_K % (cls_name, model_obj.pk)
    rds.set(key, model_obj)
    return model_obj


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    """
    Save the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    """
    '''调用原来的save正常将对象保存进数据库里'''
    self._save(force_insert=False, force_update=False, using=None,
               update_fields=None)
    '''将刚刚保存的对象加入到缓存'''
    print('数据保存好了')
    key = MODEL_K % (self.__class__.__name__, self.pk)
    rds.set(key, self)
    print('数据保存好了，我把对象加到缓存里')


def to_dict(self, exclude=()):
    '''将对象属性添加到字典里'''
    attr_data = {}

    '''找到对象身上所有的字段名称'''
    for f in self._meta.fields:
        if f.attname in exclude:  # 判断字段是否需要排除
            continue
        value = getattr(self, f.attname)  # 找到字段名对应的值
        '''由于datetime类型的值无法json序列化，因此要将它强转为字符串'''
        if isinstance(value, (datetime.datetime, datetime.date)):
            value = str(value)
        attr_data[f.attname] = value
    return attr_data


def path_orm():
    '''通过猴子补丁的方式为ORM增加缓存处理'''
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    # base.Model._save = base.Model.save
    # base.Model.save = save
    models.Model._save = models.Model.save
    models.Model.save = save

    models.Model.to_dict = to_dict
