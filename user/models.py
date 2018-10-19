from django.db import models
from django.contrib import admin

# Create your models here.

class UserModel(models.Model):
    """用户model"""

    # 用户名
    username = models.CharField(max_length=50,null=False,verbose_name='用户名')
    # 密码
    password = models.CharField(max_length=256,null=False,verbose_name='密码')
    # 联系方式
    phone = models.CharField(max_length=11,null=False,verbose_name='联系方式')
    # 地址  blank值为True的时候代表后台不用填这个值
    address = models.CharField(max_length=200,null=True,verbose_name='地址',blank=True)
    # 电子邮箱
    email = models.EmailField(null=True,verbose_name='电子邮箱',blank=True)

    def __str__(self):
        return self.username

    class Meta:
        # 修改admin后台显示的名字
        verbose_name = '用户信息管理'
        verbose_name_plural = verbose_name

@admin.register(UserModel)
class UserAdminModel(admin.ModelAdmin):
    list_display = ['username','phone','address']

class CollectGoodsModel(models.Model):
    """收货地址和信息管理"""
    # 属于谁的收货信息
    # 用户对收货信息是一对多的关系
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    # 收件人姓名
    person_name = models.CharField(max_length=30,null=False,verbose_name='收货人')
    # 详细地址
    detail_address = models.CharField(max_length=200,null=False,verbose_name='详细地址')
    # 邮编
    post_code = models.IntegerField(default=000000,verbose_name='邮政编码')
    # 联系方式
    tel = models.CharField(max_length=20,verbose_name='联系方式',null=False)
    # 是否是正在使用的收货地址
    is_used = models.BooleanField(verbose_name='是否正在使用')

    def __str__(self):
        return self.person_name

    class Meta:
        verbose_name = '收货信息管理'
        verbose_name_plural = verbose_name

# 在admin.py中应该这样添加 和装饰器的注册admin只能保留一个
# @admin.site.register(CollectGoodsModel,CollectGoodsAdminModel)
@admin.register(CollectGoodsModel)
class CollectGoodsAdminModel(admin.ModelAdmin):
    list_display = ['person_name','tel','detail_address','is_used']