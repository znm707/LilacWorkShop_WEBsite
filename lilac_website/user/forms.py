# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from .models import School, Profile


class UserLoginForm(forms.Form):
    '''
    用于定义用户登录时要填写的表格内容
    '''
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    '''
        定义用户注册表单
        其中复写了password字段
    '''
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()
    # 复写email字段
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        print('in clean_password2')
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")

    def clean_email(self):
        '''
            对输入的email进行检查是否为可注册邮箱
        '''
        print('in clean_email')
        data = self.cleaned_data
        user_email = data.get('email')
        user_email_domin = user_email[(user_email.find('@')+1):]  # 取出用户邮箱域名
        print(user_email_domin)
        schools = School.objects.all()
        for school in schools:
            if user_email_domin in school.school_emails:
                print('mail check OK')
                return data.get('email')
        raise forms.ValidationError("该邮箱暂不支持")


class ProfileRegisterForm(forms.ModelForm):
    '''
    定义注册时, 用户的扩展表单
    '''
    class Meta:
        model = Profile
        fields = ('school', 'phone')
