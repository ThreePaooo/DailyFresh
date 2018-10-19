import datetime

from django.db import models
from django.contrib import admin
from user.models import UserModel

# Create your models here.

class CategoryModel(models.Model):
    """商品分类"""
    category_name = models.CharField(max_length=20,null=False,verbose_name='商品分类名称')
    # 排序
    number = models.IntegerField(default=0,verbose_name='排序字段')
    # 分类的图片
    image = models.CharField(max_length=100,default='/static/images/banner01.jpg',null=False,verbose_name='分类图片')

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'category'
        verbose_name = '商品分类管理'
        verbose_name_plural = verbose_name


@admin.register(CategoryModel)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['category_name','number']


class GoodsModel(models.Model):
    """商品model"""
    # 商品名称
    goods_name = models.CharField(max_length=50,null=False,verbose_name='商品名称')
    # 商品简介
    abstract = models.CharField(max_length=200,null=True,blank=True,verbose_name='商品简介')
    # 价格  max_digits 限制总共多少位     decimal_places 限制小数点后面几位
    price = models.DecimalField(default=0,max_digits=11,decimal_places=2,verbose_name='商品价格')
    # 单位
    unit = models.CharField(max_length=20,null=False,verbose_name='售卖单位')
    # 库存
    stock = models.IntegerField(default=0,verbose_name='商品库存')
    # 详细介绍
    desc = models.TextField(null=True,blank=True,verbose_name='详细介绍')
    # 默认图片
    pic = models.CharField(max_length=100,null=False,default='/static/images/goods/goods003.jpg',verbose_name='商品默认图片')
    # 商品分类外键
    category = models.ForeignKey(CategoryModel,null=False,default='',on_delete=models.CASCADE,verbose_name='商品分类')
    # 人气
    popular = models.IntegerField(default=0,verbose_name='人气指数')

    def __str__(self):
        return self.goods_name

    class Meta:
        # 自定义表名
        db_table = 'goods'
        verbose_name = '商品信息管理'
        verbose_name_plural = verbose_name

@admin.register(GoodsModel)
class GoodsAdminModel(admin.ModelAdmin):
    """商品管理后台注册"""
    list_display = ['goods_name','stock','price']


class CommentModel(models.Model):
    """评论model"""
    # 用户对评论一对多关系
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE,verbose_name='评论用户')
    # 商品跟评论一对多关系
    goods = models.ForeignKey(GoodsModel,on_delete=models.CASCADE,verbose_name='评论商品')
    # 评论内容
    content = models.CharField(max_length=256,null=False,verbose_name='评论内容')
    # 被点赞的次数
    vote_number = models.IntegerField(default=0,verbose_name='点赞次数')
    # 评论时间
    create_time = models.DateTimeField(default=datetime.datetime.now(),verbose_name='评论时间')

    class Meta:
        db_table = 'comment'
        verbose_name = '评论信息管理'
        verbose_name_plural = verbose_name

@admin.register(CommentModel)
class CommentAdminModel(admin.ModelAdmin):
    list_display = ['user_id','goods_id','content','vote_number']


class ImagesModel(models.Model):
    """存储图片与商品的关系"""
    goods = models.ForeignKey(GoodsModel,on_delete=models.CASCADE,verbose_name='商品')
    image_url = models.CharField(max_length=200,verbose_name='图片地址',null=False)

    class Meta:
        db_table = 'images'
        verbose_name = '商品图片管理'
        verbose_name_plural = verbose_name

@admin.register(ImagesModel)
class ImagesAdminModel(admin.ModelAdmin):
    list_display = ['goods','image_url']


class CategoryGoodsModel(models.Model):
    """商品分类和商品之间的关系"""
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE,verbose_name='商品分类')
    goods = models.ForeignKey(GoodsModel,on_delete=models.CASCADE,verbose_name='商品名称')

    class Meta:
        db_table = 'category_goods'
        verbose_name = '商品分类和商品关系'
        verbose_name_plural = verbose_name


@admin.register(CategoryGoodsModel)
class CategoryGoodsAdminModel(admin.ModelAdmin):
    list_display = ['category','goods']


class CommentVoteModel(models.Model):
    """商品的点赞"""
    comment = models.ForeignKey(CommentModel,on_delete=models.CASCADE,verbose_name='评论id')
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE,verbose_name='用户id')

    class Meta:
        db_table = 'comment_vote'
        verbose_name = '商品点赞管理'
        verbose_name_plural = verbose_name