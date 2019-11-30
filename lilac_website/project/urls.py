# coding: utf-8
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'project'

urlpatterns = [
    # 项目列表
    path('list/', views.project_view().show_list, name = 'project_list'),
    # 项目详情
    path('detail/<int:id>/', views.project_view().show_detail, name = 'project_detail'),
    # 发布新项目
    path('create/', views.project_view().project_create, name = 'project_create'),
    # 更新项目
    path('update/<int:id>/', views.project_view().project_update, name = 'project_update'),
    # （安全）删除项目
    path('safe_delete/<int:id>/', views.project_view().project_delete, name = 'project_safe_delete'),
    # 添加申请者
    path('apply/<int:id>/', views.project_view().project_apply, name = 'project_apply')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)