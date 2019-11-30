#-*-coding:GBK -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
# message妯″潡
from django.contrib import messages
# 鏁版嵁妯″瀷
from .models import ProjectPage,HomeProject
# 琛ㄥ崟
from .forms import ProjectForm
# 鐢ㄦ埛璁よ瘉
from user.models import Profile
# 鍒嗛〉妯″潡
from django.core.paginator import Paginator
# 鐢ㄦ埛妯″瀷
from django.contrib.auth.models import User
# model淇濆瓨淇″彿
from django.db.models.signals import post_save
# Create your views here.

# 淇″彿鎺ユ敹鍣紝澧炲姞涓婚〉椤圭洰
def add_homeproject(sender, instance, **kwargs):
    '''
        sender锛氫俊鍙峰彂閫佸櫒
        instance:绫诲疄渚�
        **kwargs锛氫俊鍙峰弬鏁�
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

# 淇″彿杩炴帴
post_save.connect(add_homeproject, sender = ProjectPage, dispatch_uid = None)

class project_view(View):
    '''
        椤圭洰绠＄悊瑙嗗浘绫�
    '''
    def show_list(self,request):
        '''
            杩斿洖椤圭洰鍒楄〃
            Args:
                self: 绫诲疄渚嬪璞℃湰韬�
                request: 绯荤粺璇锋眰绫�, 鍖呭惈鐢ㄦ埛蹇呰鐨勪俊鎭�
            Returns:
                render: 杩斿洖椤圭洰鍒楄〃椤甸潰
        '''
        project_list = ProjectPage.objects.all()
        # 姣忛〉鏄剧ず 9 绡囨枃绔�
        paginator = Paginator(project_list, 9)
        # 鑾峰彇椤电爜
        page = request.GET.get('page')
        # 灏嗗鑸璞＄浉搴旂殑椤电爜鍐呭杩斿洖缁� projects
        projects = paginator.get_page(page)
        return render(request, 'project/project_list.html',{'projects':projects})

    def show_detail(self,request,id):
        '''
            杩斿洖璇︽儏椤甸潰
            Args:
                self: 绫诲疄渚嬪璞℃湰韬�
                request: 绯荤粺璇锋眰绫�, 鍖呭惈鐢ㄦ埛蹇呰鐨勪俊鎭�
                id:瀵瑰簲椤圭洰id
            Returns:
                render: 杩斿洖椤圭洰璇︽儏椤甸潰
        '''
        project = ProjectPage.objects.get(id = id)
        if (project.publisher == request.user)or(request.user.is_superuser == True):
            # 濡傛灉鏄彂甯冭�呮垨鑰呰秴绾х鐞嗗憳杩涘叆瀵瑰簲椤甸潰
            return render(request, 'project/project_detail_self.html',{'project':project})
        else:
            # 杩涘叆鏅�氶〉闈�
            # 娴忚閲�+1
            project.total_views += 1
            project.save(update_fields=['total_views'])
            return render(request, 'project/project_detail_other.html',{'project':project})

    def project_create(self,request):
        '''
            杩斿洖鍙戝竷鏂伴」鐩〉闈�
            Args:
                self: 绫诲疄渚嬪璞℃湰韬�
                request: 绯荤粺璇锋眰绫�, 鍖呭惈鐢ㄦ埛蹇呰鐨勪俊鎭�
            Returns:
                render: 杩斿洖鍙戝竷鏂伴」鐩〉闈�
        '''
        if request.user.is_authenticated == False:
            # 濡傛灉娌℃湁鐧诲綍
            messages.success(request, "璇风櫥褰�")
            return redirect("project:project_list")
        else:
            # 鑾峰彇褰撳墠鐢ㄦ埛鐨勯獙璇佷俊鎭�
            profiles = Profile.objects.all()
            for a in profiles:
                if a.user == request.user:
                    profile = a

            #楠岃瘉鏄惁鏈夊彂甯冩潈闄�
            if  (request.user.is_superuser == False)and(profile.role == "ST"):
                # 濡傛灉涓嶆槸瓒呯骇绠＄悊鍛樹笖鏄鐢�
                messages.success(request,"娌¤祫鏍�")
                return redirect("project:project_list")
            else:
                if request.method == "POST":
                    # 灏嗘彁浜ょ殑鏁版嵁璧嬪�煎埌琛ㄥ崟瀹炰緥涓�
                    project_form = ProjectForm(data=request.POST,files=request.FILES)
                    # 鍒ゆ柇鎻愪氦鐨勬暟鎹槸鍚︽弧瓒虫ā鍨嬬殑瑕佹眰
                    if project_form.is_valid():
                    # 淇濆瓨鏁版嵁
                        new_project = project_form.save(commit=False)
                        new_project.publisher = request.user
                        project_cd = project_form.cleaned_data
                        # 淇濆瓨鍥剧墖
                        if 'avatar' in request.FILES:
                            new_project.avatar = project_cd["avatar"]

                        # 灏嗘柊鏂囩珷淇濆瓨鍒版暟鎹簱涓�
                        new_project.save()
                        project_form.save_m2m()
                        new_project.workers.add(request.user)

                        return redirect("project:project_list")
                    # 濡傛灉鏁版嵁涓嶅悎娉曪紝杩斿洖閿欒淇℃伅
                    else:
                        return HttpResponse("琛ㄥ崟鍐呭鏈夎锛岃閲嶆柊濉啓銆�")
                else:
                    context = {'project_form': ProjectForm()}
                    return render(request, 'project/project_create.html', context)

    def project_delete(self,request,id):
        '''
            杩斿洖椤圭洰鍒犻櫎椤甸潰
            Args:
                self: 绫诲疄渚嬪璞℃湰韬�
                request: 绯荤粺璇锋眰绫�, 鍖呭惈鐢ㄦ埛蹇呰鐨勪俊鎭�
                id: 瀵瑰簲鐨勯」鐩甶d
            Returns:
                render: 杩斿洖椤圭洰鍒犻櫎椤甸潰
        '''
        if request.method == 'POST':
            project = ProjectPage.objects.get(id = id)
            project.delete()
            return redirect("project:project_list")
        else:
            return HttpResponse("浠呭厑璁竝ost璇锋眰")

    def project_update(self,request,id):
        '''
            杩斿洖椤圭洰鏇存柊椤甸潰
            Args:
                self: 绫诲疄渚嬪璞℃湰韬�
                request: 绯荤粺璇锋眰绫�, 鍖呭惈鐢ㄦ埛蹇呰鐨勪俊鎭�
                id: 瀵瑰簲鐨勯」鐩甶d
            Returns:
                render: 杩斿洖椤圭洰鏇存柊椤甸潰
        '''
        project = ProjectPage.objects.get(id=id)
        if request.method == "POST":
            # 灏嗘彁浜ょ殑鏁版嵁璧嬪�煎埌琛ㄥ崟瀹炰緥涓�
            project_form = ProjectForm(data=request.POST,files=request.FILES)
            # 鍒ゆ柇鎻愪氦鐨勬暟鎹槸鍚︽弧瓒虫ā鍨嬬殑瑕佹眰
            if project_form.is_valid():
                # 淇濆瓨鏂板啓鍏ョ殑project鏁版嵁骞朵繚瀛�
                project.title = request.POST['title']
                project.abstract = request.POST['abstract']
                project.body = request.POST['body']
                project.tags.set(request.POST['tags'], clear=True)
                project_cd = project_form.cleaned_data
                # workers娣诲姞閫氳繃鐨勬姤鍚嶈��,applicants鍒犻櫎閫氳繃鑰�
                all_applicants = request.POST['applicants_add']
                flag = 0
                for i in range(len(all_applicants)):
                    if all_applicants[i] == " ":
                        applicant_name = all_applicants[flag:i]
                        add_worker = User.objects.get_by_natural_key(applicant_name)
                        project.workers.add(add_worker)
                        project.applicants.remove(add_worker)
                        flag = i + 1
                # applicants鍒犻櫎涓嶉�氳繃鐨勬姤鍚嶈��
                applicants_delete = request.POST['applicants_delete']
                flag = 0
                for i in range(len(applicants_delete)):
                    if applicants_delete[i] == " ":
                        applicant_name = applicants_delete[flag:i]
                        delete_applicant = User.objects.get_by_natural_key(applicant_name)
                        project.applicants.remove(delete_applicant)
                        flag = i + 1

                # workers鍒犻櫎瑕佸垹闄ょ殑鍙備笌鑰�
                workers_delete = request.POST['workers_delete']
                flag = 0
                for i in range(len(workers_delete)):
                    if workers_delete[i] == " ":
                        delete_worker_name = workers_delete[flag:i]
                        delete_worker = User.objects.get_by_natural_key(delete_worker_name)
                        project.workers.remove(delete_worker)
                        flag = i + 1

                # 濡傛灉鏈夊浘鐗囨枃浠讹紝娣诲姞鎴栨浛鎹㈠師鏂囦欢
                if 'avatar' in request.FILES:
                    project.avatar = project_cd["avatar"]
                project.save()
                # 瀹屾垚鍚庤繑鍥炲埌淇敼鍚庣殑鏂囩珷涓�傞渶浼犲叆鏂囩珷鐨� id 鍊�
                return redirect("project:project_detail", id=id)
            # 濡傛灉鏁版嵁涓嶅悎娉曪紝杩斿洖閿欒淇℃伅
            else:
                return HttpResponse("琛ㄥ崟鍐呭鏈夎锛岃閲嶆柊濉啓銆�")

            # 濡傛灉鐢ㄦ埛 GET 璇锋眰鑾峰彇鏁版嵁
        else:
            # 鍒涘缓琛ㄥ崟绫诲疄渚�
            ini = {'body': project.body}
            project_form = ProjectForm(initial = ini)
            context = {'project': project, 'project_form': project_form}
            # 灏嗗搷搴旇繑鍥炲埌妯℃澘涓�
            return render(request, 'project/project_update.html', context)

    def project_apply(self,request,id):
        '''
            璋冪敤URL涔嬪悗娣诲姞鐢宠鑰�
            Args:
                self: 绫诲疄渚嬪璞℃湰韬�
                request: 绯荤粺璇锋眰绫�, 鍖呭惈鐢ㄦ埛蹇呰鐨勪俊鎭�
                id: 瀵瑰簲鐨勯」鐩甶d
            Returns:
                render: 杩斿洖鍘熸潵鐨勯」鐩鎯呴〉闈�
        '''
        project = ProjectPage.objects.get(id=id)
        project.applicants.add(request.user)
        return render(request, 'project/project_detail_other.html',{'project':project})
