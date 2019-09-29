# coding: utf-8

from django.views import View
from django.shortcuts import render, HttpResponse
# 用户模型
from django.contrib.auth.models import User
# 认证组件
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
# 自定义表格
from .forms import UserLoginForm, UserRegisterForm, ProfileRegisterForm
from .models import School


# Create your views here.
def user_login(request):
    """
        登录页面的view方法, 自动调用django的认证模块的登录

        Args:
            None

        Returns:
            None
    """
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            if user:
                login(request, user)
                return HttpResponse("TODO: 登录成功")
            else:
                return HttpResponse("账号或密码错误")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'user/login.html', context)
    else:
        return HttpResponse("请使用POST或者GET方法")


def user_logout(request):
    """
        注销页面的view方法, 自动调用django的认证模块的logout

        Args:
            None

        Returns:
            None
    """
    logout(request)
    return HttpResponse("TODO: 登出成功")


# 用户注册
class UserRegisterView(View):
    '''
        用户注册时调用的类视图
    '''
    def get(self, request):
        '''
            返回注册页面
            Args:
                request: 系统请求类, 包含用户必要的信息

            Returns:
                render: 返回渲染的注册页面
        '''
        user_register_form = UserRegisterForm()
        profile_register_form = ProfileRegisterForm()
        context = {
            'form': user_register_form,
            'profile_form': profile_register_form
        }
        return render(request, 'user/register.html', context)

    def post(self, request):
        '''
            处理用户注册表单
            Args:
                request: 系统请求类, 包含用户必要的信息

            Returns:
                render: 注册结果, TODO 如果注册成功, 自动登录, 并自动跳转到某一页面
        '''
        user_register_form = UserRegisterForm(data=request.POST)
        profile_register_form = ProfileRegisterForm(data=request.POST)
        if user_register_form.is_valid() and profile_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            user_register_form_data = user_register_form.cleaned_data
            # 设置密码
            new_user.set_password(user_register_form_data['password'])
            # 设置email
            new_user.email = user_register_form_data['email']
            new_user.save()
            # 保存用户的扩展信息
            new_user_profile = profile_register_form.save(commit=False)
            new_user_profile.user = new_user  # 与用户进行链接
            new_user_profile.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return HttpResponse("TODO: 注册成功")
        else:
            # 这里回返回错误信息, 但是实际的时候使用ajax更改页面禁止提交, 这里只是考虑非法提交绕过ajax时候的情况
            return HttpResponse("填写信息有误, 请重新填写<br>错误信息: <br>" +
                                user_register_form.errors.as_text() +
                                profile_register_form.errors.as_text())


# 验证用户填写的信息
def user_signup_in_validate(request):
    '''
        验证用户登录或者注册时候的信息合法性, 这是暴露给AJAX的接口
        Args:
            request: 系统请求类, 包含AJAX提交的信息

        Returns:
            render: 返回验证的结果
    '''
    data = request.POST  # 拿去post数据
    on_validate_type = data.get('type')

    if on_validate_type == 'login':
        # 以下是登录验证
        username = data.get('username')
        password = data.get('password')
        if User.objects.filter(username__iexact=username).exists():
            user = User.objects.get(username__iexact=username)
            if check_password(password, user.password):
                return HttpResponse('200')
            else:
                # 错误的密码
                return HttpResponse('403')
        else:
            # 找不到的用户名
            return HttpResponse('403')
    # ---------------------以下是注册验证---------------------
    elif on_validate_type == 'username':
        if User.objects.filter(username__iexact=data.get('username')).exists():
            # 用户名存在
            return HttpResponse('403')
        # 用户名可以注册
        return HttpResponse('200')
    elif on_validate_type == 'email':
        user_email = data.get('email')
        # 检查邮箱是否存在
        if User.objects.filter(email__iexact=user_email).exists():
            # 邮箱已经被注册了
            return HttpResponse('403')
        # 检查邮箱是否在可用列表中
        user_email_domin = user_email[(user_email.find('@')+1):]  # 取出用户邮箱域名
        schools = School.objects.all()
        for school in schools:
            if user_email_domin in school.school_emails:
                return HttpResponse('200')
        # 邮箱不在可注册列表中
        return HttpResponse('404')
    # 非法的数据格式
    return HttpResponse('403')
