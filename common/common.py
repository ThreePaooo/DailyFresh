from cart.models import CartModel

def cart_count_goods(request):
    # 从session中拿到user_id
    user_id = request.session.get('user_id',0)
    cart_list = CartModel.objects.filter(user_id=user_id)
    # 统计出购物车中所有的商品数量
    cart_count = 0
    for cart in cart_list:
        cart_count += cart.count
    return cart_count