from django.shortcuts import render,redirect
from django.http import JsonResponse

# Create your views here.
from user.utils import login_required
from cart.models import CartModel
from common.common import cart_count_goods

@login_required
def cart(request):
    """购物车"""
    user_id = request.session.get('user_id')
    carts = CartModel.objects.filter(user_id=user_id)

    return render(request,'cart/cart.html',{'carts':carts})

@login_required
def add(request,goods_id,count):
    """添加到购物车视图 接收两个参数 商品id和商品数量"""
    user_id = request.session['user_id']

    # 查询购物车中是否已经有这个商品在这个人的名下 如果有 数量增加  如果没有 在购物车中添加
    carts = CartModel.objects.filter(user_id=user_id,goods_id=goods_id)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartModel()
        cart.user_id = user_id
        cart.goods_id = goods_id
        cart.count = count
    cart.save()

    # 如果是ajax请求 则返回一个json 否则重定向
    if request.is_ajax():
        cart_count = cart_count_goods(request)
        return JsonResponse({'cart_count':cart_count})

    return redirect('/cart/')


@login_required
def delete(request,cart_id):
    """删除购物车中的商品"""
    cart = CartModel.objects.get(id=cart_id)
    cart.delete()
    # 后端尽量不传给前端bool类型 后端也不接收前端传来的bool类型
    return JsonResponse({'success':1})


@login_required
def update(request,cart_id,count):
    """更新购物车内商品的数量"""
    cart = CartModel.objects.get(id=cart_id)
    cart.count = count
    cart.save()
    return JsonResponse({'success':1})
