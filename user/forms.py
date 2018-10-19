from django import forms
from user.models import UserModel

# 用户注册表单验证
# class UserRegistForm(forms.Form):
#     username = forms.CharField(max_length=10,error_messages={'error':'不能为空'})
#     password = forms.CharField(max_length=10,error_messages={'error':'不能为空'})
#     email = forms.EmailField(error_messages={'error':'不能为空'})

class UserRegistModelForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'

class UserLoginModelForm(forms.ModelForm):
    class Meta:
        model = UserModel
        # 限制显示的字段
        fields = ['username','password']