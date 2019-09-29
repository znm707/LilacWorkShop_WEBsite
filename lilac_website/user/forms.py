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
        '''
            定义元数据, 使用User模型, 设置默认需要填写的内容
        '''
        model = User
        fields = ('username', 'first_name', 'last_name')

    def clean_password2(self):
        '''
            对两次输入的密码是否一致进行检查

            Args:
                None

            Returns:
                返回匹配的密码, 或者返回错误信息
        '''
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")

    def clean_email(self):
        '''
            对输入的email进行检查是否为可注册邮箱, 验证邮箱是否唯一
            Args:
                None

            Returns:
                返回匹配的email
                或者返回错误信息
        '''
        data = self.cleaned_data
        user_email = data.get('email')
        username = data.get('username')
        # 检查邮箱是否存在
        if user_email and User.objects.filter(email=user_email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')

        user_email_domin = user_email[(user_email.find('@')+1):]  # 取出用户邮箱域名
        schools = School.objects.all()
        for school in schools:
            if user_email_domin in school.school_emails:
                return data.get('email')
        raise forms.ValidationError("该邮箱暂不支持")


class ProfileRegisterForm(forms.ModelForm):
    '''
    定义注册时, 用户的扩展表单
    '''
    class Meta:
        '''
            定义元数据, 使用Profile模型, 必须填写school 和 phone字段
        '''
        model = Profile
        fields = ('school', 'phone')
