from django.shortcuts import render, HttpResponse
# 认证组件
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm, ProfileRegisterForm


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
            user = authenticate(username=data['username'], password=data['password'])
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
def user_register(request):
    if request.method == 'POST':
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
            print("error")
            print(user_register_form.errors)
            return HttpResponse(user_register_form.errors)
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        profile_register_form = ProfileRegisterForm()
        context = {'form': user_register_form, 'profile_form': profile_register_form}
        return render(request, 'user/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
