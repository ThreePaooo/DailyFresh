from django.urls import path

from .views import index,list,detail,comment,add_comment,vote_comment

app_name = 'goods'
urlpatterns = [
    path('index/',index,name='index'),
    path('list/<int:category_id>/<str:sort>/<int:page_num>/',list,name='list'),
    path('detail/<int:goods_id>/',detail,name='detail'),
    path('comment/<int:goods_id>/',comment,name='comment'),
    path('add_comment/<int:goods_id>/',add_comment,name='add_comment'),
    path('vote_comment/<int:comment_id>/',vote_comment,name='vote_comment')
]