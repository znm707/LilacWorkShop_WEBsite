# coding: utf-8
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    # 用户退出
    path('logout/', views.user_logout, name='logout'),
    # 用户注册
    path('register/', views.UserRegisterView.as_view(), name='register'),
    # 用户编辑个人信息
    path('edituserinfo/<int:id>/', views.UserInfoChangeView.as_view(), name='userinfo'),
    # 用户信息验证
    path('user-signinup-validate', views.user_signup_in_validate, name='user_signinup_validate'),
]
