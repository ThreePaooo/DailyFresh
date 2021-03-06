from django.shortcuts import render,redirect
import datetime
from django.http import JsonResponse

# Create your views here.
from user.models import UserModel
from cart.models import CartModel
from order.models import OrderModel,OrderGoodsModel
from user.utils import login_required


@login_required
def order(request):
    """订单页面"""
    user_id = request.session.get('user_id')
    user = UserModel.objects.get(id=user_id)

    cart_id_list = request.GET.getlist('cart_id_list')
    if cart_id_list == []:
        return redirect('/goods/index/')

    # 根据购物车的id查询出对应的商品
    cart_info_list = []
    for cart_id in cart_id_list:
        cart = CartModel.objects.get(id=cart_id)
        cart_info_list.append(cart)

    context = {
        'title':'订单页面',
        'user':user,
        'cart_info_list':cart_info_list,
    }

    return render(request,'order/order.html',context)


@login_required
def add_order(request):
    """添加订单到数据库"""
    cart_list = request.POST.getlist('cart_list')

    total_price = request.POST.get('shifu')
    print(request.POST)
    user_id = request.session.get('user_id')

    order = OrderModel()
    order.user_id = user_id
    order.create_time = datetime.datetime.now()
    order.total_price = total_price
    order.is_pay = False
    order.save()

    for cart_id in cart_list:
        cart = CartModel.objects.get(id=cart_id)

        order_goods = OrderGoodsModel()
        order_goods.goods_id = cart.goods.id
        order_goods.order_id = order.id
        order_goods.number = cart.count

        order_goods.save()
        cart.delete()

    return JsonResponse({'result':'success'})