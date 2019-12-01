# coding: utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
# message模块
from django.contrib import messages
# 数据模型
from .models import ProjectPage,HomeProject
# 表单
from .forms import ProjectForm
# 用户认证
from user.models import Profile
# 分页模块
from django.core.paginator import Paginator
# 用户模型
from django.contrib.auth.models import User
# model保存信号
from django.db.models.signals import post_save
# Create your views here.

# 信号接收器，增加主页项目
def add_homeproject(sender, instance, **kwargs):
    '''
        sender：信号发送器
        instance:类实例
        **kwargs：信号参数
    '''
    flag = False;
    if instance.is_homepage == True:
        for i in HomeProject.objects.all():
            if  i.Home_Project == instance:
                flag = True
                break
    else:
        for i in HomeProject.objects.all():
            if i.Home_Project == instance:
                i.delete()
                break
    if flag == False:
        HomeProject.objects.create(Home_Project=instance)

# 信号连接
post_save.connect(add_homeproject, sender = ProjectPage, dispatch_uid = None)

class project_view(View):
    '''
        项目管理视图类
    '''
    def show_list(self,request):
        '''
            返回项目列表
            Args:
                self: 类实例对象本身
                request: 系统请求类, 包含用户必要的信息
            Returns:
                render: 返回项目列表页面
        '''
        project_list = ProjectPage.objects.all()
        # 每页显示 9 篇文章
        paginator = Paginator(project_list, 9)
        # 获取页码
        page = request.GET.get('page')
        # 将导航对象相应的页码内容返回给 projects
        projects = paginator.get_page(page)
        return render(request, 'project/project_list.html',{'projects':projects})

    def show_detail(self,request,id):
        '''
            返回详情页面
            Args:
                self: 类实例对象本身
                request: 系统请求类, 包含用户必要的信息
                id:对应项目id
            Returns:
                render: 返回项目详情页面
        '''
        project = ProjectPage.objects.get(id = id)
        if (project.publisher == request.user)or(request.user.is_superuser == True):
            # 如果是发布者或者超级管理员进入对应页面
            return render(request, 'project/project_detail_self.html',{'project':project})
        else:
            # 进入普通页面
            # 浏览量+1
            project.total_views += 1
            project.save(update_fields=['total_views'])
            return render(request, 'project/project_detail_other.html',{'project':project})

    def project_create(self,request):
        '''
            返回发布新项目页面
            Args:
                self: 类实例对象本身
                request: 系统请求类, 包含用户必要的信息
            Returns:
                render: 返回发布新项目页面
        '''
        if request.user.is_authenticated == False:
            # 如果没有登录
            messages.success(request, "请登录")
            return redirect("project:project_list")
        else:
            # 获取当前用户的验证信息
            profiles = Profile.objects.all()
            for a in profiles:
                if a.user == request.user:
                    profile = a

            #验证是否有发布权限
            if  (request.user.is_superuser == False)and(profile.role == "ST"):
                # 如果不是超级管理员且是学生
                messages.success(request,"没资格")
                return redirect("project:project_list")
            else:
                if request.method == "POST":
                    # 将提交的数据赋值到表单实例中
                    project_form = ProjectForm(data=request.POST,files=request.FILES)
                    # 判断提交的数据是否满足模型的要求
                    if project_form.is_valid():
                    # 保存数据
                        new_project = project_form.save(commit=False)
                        new_project.publisher = request.user
                        project_cd = project_form.cleaned_data
                        # 保存图片
                        if 'avatar' in request.FILES:
                            new_project.avatar = project_cd["avatar"]

                        # 将新文章保存到数据库中
                        new_project.save()
                        project_form.save_m2m()
                        new_project.workers.add(request.user)

                        return redirect("project:project_list")
                    # 如果数据不合法，返回错误信息
                    else:
                        return HttpResponse("表单内容有误，请重新填写。")
                else:
                    context = {'project_form': ProjectForm()}
                    return render(request, 'project/project_create.html', context)

    def project_delete(self,request,id):
        '''
            返回项目删除页面
            Args:
                self: 类实例对象本身
                request: 系统请求类, 包含用户必要的信息
                id: 对应的项目id
            Returns:
                render: 返回项目删除页面
        '''
        if request.method == 'POST':
            project = ProjectPage.objects.get(id = id)
            project.delete()
            return redirect("project:project_list")
        else:
            return HttpResponse("仅允许post请求")

    def project_update(self,request,id):
        '''
            返回项目更新页面
            Args:
                self: 类实例对象本身
                request: 系统请求类, 包含用户必要的信息
                id: 对应的项目id
            Returns:
                render: 返回项目更新页面
        '''
        project = ProjectPage.objects.get(id=id)
        if request.method == "POST":
            # 将提交的数据赋值到表单实例中
            project_form = ProjectForm(data=request.POST,files=request.FILES)
            # 判断提交的数据是否满足模型的要求
            if project_form.is_valid():
                # 保存新写入的project数据并保存
                project.title = request.POST['title']
                project.abstract = request.POST['abstract']
                project.body = request.POST['body']
                project.tags.set(request.POST['tags'], clear=True)
                project_cd = project_form.cleaned_data
                # workers添加通过的报名者,applicants删除通过者
                all_applicants = request.POST['applicants_add']
                flag = 0
                for i in range(len(all_applicants)):
                    if all_applicants[i] == " ":
                        applicant_name = all_applicants[flag:i]
                        add_worker = User.objects.get_by_natural_key(applicant_name)
                        project.workers.add(add_worker)
                        project.applicants.remove(add_worker)
                        flag = i + 1
                # applicants删除不通过的报名者
                applicants_delete = request.POST['applicants_delete']
                flag = 0
                for i in range(len(applicants_delete)):
                    if applicants_delete[i] == " ":
                        applicant_name = applicants_delete[flag:i]
                        delete_applicant = User.objects.get_by_natural_key(applicant_name)
                        project.applicants.remove(delete_applicant)
                        flag = i + 1

                # workers删除要删除的参与者
                workers_delete = request.POST['workers_delete']
                flag = 0
                for i in range(len(workers_delete)):
                    if workers_delete[i] == " ":
                        delete_worker_name = workers_delete[flag:i]
                        delete_worker = User.objects.get_by_natural_key(delete_worker_name)
                        project.workers.remove(delete_worker)
                        flag = i + 1

                # 如果有图片文件，添加或替换原文件
                if 'avatar' in request.FILES:
                    project.avatar = project_cd["avatar"]
                project.save()
                # 完成后返回到修改后的文章中。需传入文章的 id 值
                return redirect("project:project_detail", id=id)
            # 如果数据不合法，返回错误信息
            else:
                return HttpResponse("表单内容有误，请重新填写。")

            # 如果用户 GET 请求获取数据
        else:
            # 创建表单类实例
            ini = {'body': project.body}
            project_form = ProjectForm(initial = ini)
            context = {'project': project, 'project_form': project_form}
            # 将响应返回到模板中
            return render(request, 'project/project_update.html', context)

    def project_apply(self,request,id):
        '''
            调用URL之后添加申请者
            Args:
                self: 类实例对象本身
                request: 系统请求类, 包含用户必要的信息
                id: 对应的项目id
            Returns:
                render: 返回原来的项目详情页面
        '''
        project = ProjectPage.objects.get(id=id)
        project.applicants.add(request.user)
        return render(request, 'project/project_detail_other.html',{'project':project})
