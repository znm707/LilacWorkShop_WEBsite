# coding: utf-8

from django import forms


class UserLoginForm(forms.Form):
    '''
    用于定义用户登录时要填写的表格内容
    '''
    username = forms.CharField()
    password = forms.CharField()
