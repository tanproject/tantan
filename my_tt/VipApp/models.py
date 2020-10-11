from django.db import models


# Create your models here.

class Vip(models.Model):
    name = models.CharField(max_length=32, verbose_name='会员名称')
    level = models.IntegerField(verbose_name='会员等级')
    duration = models.IntegerField(verbose_name='会员时长/天数')
    price = models.FloatField(verbose_name='价格')

    class Meta:
        db_table = 'vip'

    def has_perm(self,perm_name):
        '''检查当前vip是否拥有某权限'''
        perm=Permission.objects.get(name=perm_name)
        return Vip_Permission_Relation.objects.filter(perm_id=perm.id,vip_level=self.level).exists()




class Permission(models.Model):
    name = models.CharField(max_length=32, verbose_name='权限名称')
    description = models.TextField(verbose_name='权限描述')

    class Meta:
        db_table = 'permission'


class Vip_Permission_Relation(models.Model):
    vip_level = models.IntegerField(verbose_name='会员等级')
    perm_id = models.IntegerField(verbose_name='对应的权限')

    class Meta:
        db_table = 'vip_permission_relation'
