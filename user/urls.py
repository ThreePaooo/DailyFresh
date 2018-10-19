from django.urls import path
from .views import regist,regist_post,login,logout,info,all_order,site,upload

# 命名空间
app_name = 'user'
urlpatterns = [
    path('regist/',regist,name='regist'),
    path('regist_post/',regist_post,name='regist_post'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('info/',info,name='info'),
    path('all_order/<int:page_num>/',all_order,name='all_order'),
    path('site/',site,name='site'),
    path('upload/',upload,name='upload')
]