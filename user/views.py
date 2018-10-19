from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import Paginator

# Create your views here.
from user.models import UserModel,CollectGoodsModel
from user.forms import UserRegistModelForm,UserLoginModelForm
from user.utils import login_required
from goods.models import GoodsModel
from order.models import OrderModel


# 只接受POST请求
def regist_post(request):
    if request.method == 'POST':
        user = UserLoginModelForm(request.POST)
        if not user.is_valid():
            return JsonResponse(user.errors.get_json_data(),safe=False)
    user = UserLoginModelForm()
    return render(request,'user/regist_post.html',{'form':user})

def regist(request):
    """注册接口"""
    cookie = request.COOKIES
    print(cookie)

    if request.method == 'POST':
        # 格式验证在前端
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address','')
        email = request.POST.get('email','')

        # 保存到数据库
        user = UserModel()
        user.username = username
        # 密码加密后存储
        user.password = make_password(password)
        user.phone = phone
        user.address = address
        user.email = email
        user.save()
        return JsonResponse({'user':'success'})

    return render(request,'user/regist.html')

def login(request):
    """登录接口"""
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        # 当复选框选中的时候值为1 没有为0
        jizhu = request.POST.get('jizhu',0)

        # 根据用户名查找对象
        user = UserModel.objects.filter(username=username)

        # 判断 如果没有查找到 说明用户名错误 如果查到判断密码是否正确
        # 密码错误 返回登录页面 并且提示密码错误
        if user:
            user = user[0]
            is_password = check_password(password,user.password)
            if not is_password:
                # 密码错误
                return render(request,'user/login.html',{'username':username,'password_error':True})
            else:
                # 密码正确
                # 先实例化一个response对象
                next_url = request.COOKIES.get('next_url','/goods/index/')
                response = HttpResponseRedirect(next_url)
                # 记住用户名
                # 设置cookie
                if jizhu != 0:
                    response.set_cookie('username',username)
                else:
                    response.set_cookie('username','',max_age=-1) # max_age=-1 立即过期
                # 把用户id和用户名放入session中
                request.session['user_id'] = user.id
                request.session['username'] = username
                return response
                # return render(request,'user/index.html',{'username':username})
        else:
            return render(request,'user/login.html',{'username':username,'user_error':True})

    # 查看cookie
    username = request.COOKIES.get('username','')
    if username != '':
        return render(request,'user/login.html',{'username':username})
    else:

        return render(request,'user/login.html')

def logout(request):
    del request.session['user_id']
    del request.session['username']
    return redirect('/account/login/')

@login_required
def info(request):
    """用户个人信息"""
    user_id = request.session['user_id']
    user = UserModel.objects.get(id=user_id)
    user_info = {
        'username':user.username,
        'phone':user.phone,
        'address':user.address
    }
    # 最近的浏览记录
    goods_id_list = request.session.get(str(user_id),[])
    print(goods_id_list)
    goods_list = []
    for goods_id in goods_id_list:
        goods_list.append(GoodsModel.objects.get(id=goods_id))
    if len(goods_list) > 5:
        goods_list.pop(-1)

    context = {'user_info':user_info,
               'goods_list':goods_list,
               'title':'用户中心',
               'active':'info'
               }
    return render(request,'user/user_center_info.html',context)


@login_required
def all_order(request,page_num):
    """全部订单"""
    # 查询当前登录用户所有订单信息
    user_id = request.session.get('user_id')
    all_order = OrderModel.objects.filter(user_id=user_id)
    # 每一页展示两个
    paginator = Paginator(all_order,2)
    page = paginator.page(page_num)

    context = {
        'title':'全部订单',
        'page':page,
        'page_num':page_num,
        'active':'all_order'
    }

    return render(request,'user/user_center_order.html',context)


def site(request):
    """收货地址"""
    user_id =request.session.get('user_id')

    user = UserModel.objects.get(id=user_id)
    all_sites = CollectGoodsModel.objects.filter(user_id=user_id)
    used_site = CollectGoodsModel.objects.filter(user_id=user_id,is_used=True)

    context = {
        'user':user,
        'all_sites':all_sites,
        'used_site':used_site
    }

    return render(request,'user/user_center_site.html',context)


def upload(request):
    """上传接口"""
    myfile = request.FILES.get('myfile')
    if request.method == 'GET':
        return render(request,'upload.html')
    if request.method == 'POST':
        ext = myfile.name.split('.')[-1]
        print(ext)
        filename = 'test.' + ext
        with open(filename,'wb',)as f:
            for chunk in myfile.chunks():
                f.write(chunk)
        return JsonResponse({'result':'success'})