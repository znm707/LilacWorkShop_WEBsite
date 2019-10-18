#-*-coding:GBK -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
# messageģ��
from .models import ProjectPage
from .forms import ProjectForm
from user.models import Profile
from django.core.paginator import Paginator
# ��ҳģ��
from django.contrib.auth.models import User
# �û�ģ��
# Create your views here.
class project_view(View):
    '''
        �û�ע��ʱ���õ�����ͼ
    '''
    def show_list(self,request):
        '''
            ������Ŀ�б�
            Args:
                self: ��ʵ��������
                request: ϵͳ������, �����û���Ҫ����Ϣ
            Returns:
                render: ������Ŀ�б�ҳ��
        '''
        project_list = ProjectPage.objects.all()
        # ÿҳ��ʾ 9 ƪ����
        paginator = Paginator(project_list, 9)
        # ��ȡҳ��
        page = request.GET.get('page')
        # ������������Ӧ��ҳ�����ݷ��ظ� projects
        projects = paginator.get_page(page)
        return render(request, 'project/project_list.html',{'projects':projects})

    def show_detail(self,request,id):
        '''
            ��������ҳ��
            Args:
                self: ��ʵ��������
                request: ϵͳ������, �����û���Ҫ����Ϣ
                id:��Ӧ��Ŀid
            Returns:
                render: ������Ŀ����ҳ��
        '''
        project = ProjectPage.objects.get(id = id)
        if (project.publisher == request.user)or(request.user.is_superuser == True):
            # ����Ƿ����߻��߳�������Ա�����Ӧҳ��
            return render(request, 'project/project_detail_self.html',{'project':project})
        else:
            # ������ͨҳ��
            # �����+1
            project.total_views += 1
            project.save(update_fields=['total_views'])
            return render(request, 'project/project_detail_other.html',{'project':project})

    def project_create(self,request):
        '''
            ���ط�������Ŀҳ��
            Args:
                self: ��ʵ��������
                request: ϵͳ������, �����û���Ҫ����Ϣ
            Returns:
                render: ���ط�������Ŀҳ��
        '''
        if request.user.is_authenticated == False:
            # ���û�е�¼
            messages.success(request, "���¼")
            return redirect("project:project_list")
        else:
            # ��ȡ��ǰ�û�����֤��Ϣ
            profiles = Profile.objects.all()
            for a in profiles:
                if a.user == request.user:
                    profile = a

            #��֤�Ƿ��з���Ȩ��
            if  (request.user.is_superuser == False)and(profile.role == "ST"):
                # ������ǳ�������Ա����ѧ��
                messages.success(request,"û�ʸ�")
                return redirect("project:project_list")
            else:
                if request.method == "POST":
                    # ���ύ�����ݸ�ֵ����ʵ����
                    project_form = ProjectForm(data=request.POST,files=request.FILES)
                    # �ж��ύ�������Ƿ�����ģ�͵�Ҫ��
                    if project_form.is_valid():
                    # ��������
                        new_project = project_form.save(commit=False)
                        new_project.publisher = request.user
                        project_cd = project_form.cleaned_data
                        # ����ͼƬ
                        if 'avatar' in request.FILES:
                            new_project.avatar = project_cd["avatar"]

                        # �������±��浽���ݿ���
                        new_project.save()
                        project_form.save_m2m()
                        new_project.workers.add(request.user)

                        return redirect("project:project_list")
                    # ������ݲ��Ϸ������ش�����Ϣ
                    else:
                        return HttpResponse("������������������д��")

                else:
                    context = {'project_form': ProjectForm()}
                    return render(request, 'project/project_create.html', context)

    def project_delete(self,request,id):
        '''
            ������Ŀɾ��ҳ��
            Args:
                self: ��ʵ��������
                request: ϵͳ������, �����û���Ҫ����Ϣ
                id: ��Ӧ����Ŀid
            Returns:
                render: ������Ŀɾ��ҳ��
        '''
        if request.method == 'POST':
            project = ProjectPage.objects.get(id = id)
            project.delete()
            return redirect("project:project_list")
        else:
            return HttpResponse("������post����")

    def project_update(self,request,id):
        '''
            ������Ŀ����ҳ��
            Args:
                self: ��ʵ��������
                request: ϵͳ������, �����û���Ҫ����Ϣ
                id: ��Ӧ����Ŀid
            Returns:
                render: ������Ŀ����ҳ��
        '''
        project = ProjectPage.objects.get(id=id)
        if request.method == "POST":
            # ���ύ�����ݸ�ֵ����ʵ����
            project_form = ProjectForm(data=request.POST,files=request.FILES)
            # �ж��ύ�������Ƿ�����ģ�͵�Ҫ��
            if project_form.is_valid():
                # ������д���project���ݲ�����
                project.title = request.POST['title']
                project.abstract = request.POST['abstract']
                project.body = request.POST['body']
                project.tags.set(request.POST['tags'], clear=True)
                project_cd = project_form.cleaned_data
                # workers���ͨ���ı�����,applicantsɾ��ͨ����
                all_applicants = request.POST['applicants_add']
                flag = 0
                for i in range(len(all_applicants)):
                    if all_applicants[i] == " ":
                        applicant_name = all_applicants[flag:i]
                        add_worker = User.objects.get_by_natural_key(applicant_name)
                        project.workers.add(add_worker)
                        project.applicants.remove(add_worker)
                        flag = i + 1
                # applicantsɾ����ͨ���ı�����
                applicants_delete = request.POST['applicants_delete']
                flag = 0
                for i in range(len(applicants_delete)):
                    if applicants_delete[i] == " ":
                        applicant_name = applicants_delete[flag:i]
                        delete_applicant = User.objects.get_by_natural_key(applicant_name)
                        project.applicants.remove(delete_applicant)
                        flag = i + 1

                # workersɾ��Ҫɾ���Ĳ�����
                workers_delete = request.POST['workers_delete']
                flag = 0
                for i in range(len(workers_delete)):
                    if workers_delete[i] == " ":
                        delete_worker_name = workers_delete[flag:i]
                        delete_worker = User.objects.get_by_natural_key(delete_worker_name)
                        project.workers.remove(delete_worker)
                        flag = i + 1

                # �����ͼƬ�ļ�����ӻ��滻ԭ�ļ�
                if 'avatar' in request.FILES:
                    project.avatar = project_cd["avatar"]
                project.save()
                # ��ɺ󷵻ص��޸ĺ�������С��贫�����µ� id ֵ
                return redirect("project:project_detail", id=id)
            # ������ݲ��Ϸ������ش�����Ϣ
            else:
                return HttpResponse("������������������д��")

            # ����û� GET �����ȡ����
        else:
            # ��������ʵ��
            ini = {'body': project.body}
            project_form = ProjectForm(initial = ini)
            context = {'project': project, 'project_form': project_form}
            # ����Ӧ���ص�ģ����
            return render(request, 'project/project_update.html', context)

    def project_apply(self,request,id):
        '''
            ����URL֮�����������
            Args:
                self: ��ʵ��������
                request: ϵͳ������, �����û���Ҫ����Ϣ
                id: ��Ӧ����Ŀid
            Returns:
                render: ����ԭ������Ŀ����ҳ��
        '''
        project = ProjectPage.objects.get(id=id)
        project.applicants.add(request.user)
        return render(request, 'project/project_detail_other.html',{'project':project})
