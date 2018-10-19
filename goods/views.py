from django.shortcuts import render,redirect
from django.core.paginator import Paginator
import datetime
from django.http import JsonResponse

# Create your views here.
from haystack.views import SearchView
from .models import CategoryModel,CategoryGoodsModel,GoodsModel,CommentModel,CommentVoteModel
from cart.models import CartModel
from order.models import OrderModel,OrderGoodsModel
from common.common import cart_count_goods


def index(request):
    """主页"""
    # 拿出所有的分类
    category_list = CategoryModel.objects.all()
    # 分别取出每个分类下最新的商品
    new_goods_dict = {}  # 存储每个分类下的最新商品
    for category in category_list:
        goods_list = GoodsModel.objects.filter(category_id=category.id).order_by('-id')[:4]
        new_goods_dict[category] = goods_list

        # goods_list = CategoryGoodsModel.objects.filter(category_id=category.id).order_by('-goods_id')[:4]
        # # 拿到查询出的所有的goods的id
        # goods_ids = [goods.goods_id for goods in goods_list]
        # goods_info_list = GoodsModel.objects.filter(id__in=goods_ids)
        # new_goods_dict[category] = goods_info_list

    cart_count = cart_count_goods(request)

    context = {
        'new_goods_dict':new_goods_dict,
        'cart_count':cart_count
    }

    return render(request,'goods/index.html',context)


def list(request,category_id,sort,page_num):
    """商品列表视图"""
    """category_id 分类id    
        sort 排序字段(默认：default 价格：price 人气：popular)
        page_num 获取当前页的页码"""

    category = CategoryModel.objects.get(id=category_id)
    # 取出该类型中最新的两个商品
    news = GoodsModel.objects.filter(category_id=category_id).order_by('-id')[:2]
    # 使用外键查找
    # news = category.goodsmodel_set.order_by('-id')[:2]

    goods_list = []
    if sort == 'default':
        goods_list = GoodsModel.objects.filter(category_id=category_id).order_by('id')
    elif sort == 'price':
        goods_list = GoodsModel.objects.filter(category_id=category_id).order_by('price')
    elif sort == 'popular':
        goods_list = GoodsModel.objects.filter(category_id=category_id).order_by('-popular')

    cart_count = cart_count_goods(request)

    # 根据商品的列表goods_list进行分页
    paginator = Paginator(goods_list,2)
    page = paginator.page(page_num)

    context = {
        'category':category, # 商品的分类对象
        'news':news,  # 新品推荐
        'goods_list':goods_list, # 排序后的商品列表
        'sort':sort,  # 排序的条件
        'cart_count':cart_count,  # 购物车中的商品数量
        'page':page,  # 分页信息
        'page_num':page_num  # 当前页码
    }

    return render(request,'goods/list.html',context)


def detail(request,goods_id):
    """商品详细信息"""
    goods = GoodsModel.objects.get(id=goods_id)
    goods.popular = goods.popular + 1  # 增加商品的人气值
    goods.save()
    # 利用orm外键的特性
    news = goods.category.goodsmodel_set.order_by('-id')[:2]
    cart_count = cart_count_goods(request)

    # 记录用户最近的浏览记录
    # 判断是否有用户登录
    if request.session.has_key('user_id'):
        user_id = str(request.session.get('user_id'))
        goods_id_list = request.session.get(user_id,[])
        if not goods_id_list:
            goods_id_list.append(goods.id)
        else:
            # 判断之前是否存在该商品的记录
            if goods_id in goods_id_list:
                goods_id_list.remove(goods_id)
            goods_id_list.insert(0,goods_id)
            if len(goods_id_list) > 6:  # 如果超过5个浏览记录 删除最后一个
                del goods_id_list[-1]
        # 把最近的浏览记录存储到session中 以user_id为key
        request.session[user_id] = goods_id_list

    return render(request,'goods/detail.html',{'goods':goods,'news':news,'cart_count':cart_count})


def comment(request,goods_id):
    """商品评论"""
    user_id = request.session.get('user_id')
    comments = CommentModel.objects.filter(goods_id=goods_id)
    goods = GoodsModel.objects.get(id=goods_id)

    # 查找用户所有的订单id
    user_orders_id = OrderModel.objects.filter(user_id=user_id,is_pay=True)

    goods_id_list = []
    for order_id in user_orders_id:
        order_goods = OrderGoodsModel.objects.filter(order_id=order_id)
        for order in order_goods:
            goods_id_list.append(order.goods_id)

    if goods_id in goods_id_list:
        add_comment = True
    else:
        add_comment = False

    if comments:
        return render(request,'goods/comment.html',{'comments':comments,'goods':goods,'add_comment':add_comment})
    else:
        return render(request,'goods/comment.html',{'null':'还没有人评论~','goods':goods,'add_comment':add_comment})


def add_comment(request,goods_id):
    """添加评论"""
    user_id = request.session.get('user_id')
    content = request.GET.get('content')

    comment = CommentModel()
    comment.content = content
    comment.vote_number = 0
    comment.create_time = datetime.datetime.now()
    comment.goods_id = goods_id
    comment.user_id = user_id
    comment.save()

    return redirect('/goods/comment/{}'.format(goods_id))


def vote_comment(request,comment_id):
    """评论点赞"""

    user_id = request.session.get('user_id')

    vote_record = CommentVoteModel.objects.filter(comment_id=comment_id,user_id=user_id)

    if request.is_ajax():
        if vote_record:
            return JsonResponse({'msg':'只能点一次赞哦~'})
        else:
            # 添加用户点赞记录
            vote = CommentVoteModel()
            vote.comment_id = comment_id
            vote.user_id = user_id
            vote.save()

            # 评论点赞数+1
            comment = CommentModel.objects.get(id=comment_id)
            comment.vote_number = comment.vote_number + 1
            comment.save()

            return JsonResponse({'vote_number':comment.vote_number})




