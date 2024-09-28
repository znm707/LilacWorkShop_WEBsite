# coding: utf-8

from django.db import models
# 引入时区支持
from django.utils import timezone
# 引入用户模型
from django.contrib.auth.models import User
# 引入taggit的标签，作为文章关键字
from taggit.managers import TaggableManager
# 引入django-ckeditor 实现富文本编辑器的功能
from ckeditor.fields import RichTextField
# 引入imagekit, 用于自动处理用户上传的图片
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit



# Create your models here.
class ProjectPage(models.Model):
    '''
    该类是一个基础项目模型类，网站中的每个发起的项目，都是填充这个表的内容
    '''
    # 文章标题图, 图片处理的方法仅按照教程中给出，具体的需要具体摸索
    avatar = ProcessedImageField(
        upload_to='project/%Y%m%d',
        processors=[ResizeToFit(width=400)],
        format='JPEG',
        options={'quality': 100},
        blank=True
    )
    # 主页项目
    is_homepage = models.BooleanField('是否在主页可见', default=False)
    # 是否在项目页可见, 因为首页可能有一些紫丁香相关的介绍, 因此需要一些非项目的文章
    # 该字段用于确保非项目的文章在项目页不被显示
    is_project = models.BooleanField('是否在项目页可见', default=True)
    # 文章标题
    title = models.CharField(max_length=100)
    # 摘要, 不超过500字
    abstract = models.CharField(max_length=500)
    # 关键字
    tags = TaggableManager(blank=True)
    # 文章正文， 使用富文本编辑器
    body = RichTextField()
    # 发起者, 一对多， 即一个内容发布者可以发布多个项目， 当内容发起者被删除时，其发布的项目同样被删除
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publisher')
    # 参与者, 多对多， 即一个项目可以有多个参与者， 一个参与者可以参与多个项目
    workers = models.ManyToManyField(User)
    # 申请者, 多对多， 即一个项目可以有多个申请者， 一个申请者可以申请多个项目
    applicants = models.ManyToManyField(User,related_name='applicants',blank = True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 文章更新时间
    updated = models.DateTimeField(auto_now=True)
    # 文章浏览量
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        '''
        该类用于存储模型的别名等项目
        '''
        verbose_name = '项目'
        verbose_name_plural = '项目'
        ordering = ('-created', )  # 默认按创建时间进行排序

    def __str__(self):
        """
        返回模型的标题字段， 用于优化在admin页面的显示

        Args:
            None

        Returns:
            str: 返回模型的标题字段

        """
        return self.title




class HomeProject(models.Model):
    '''
        主页项目类，从基础项目模型类中得出is_homepage
    '''
    # 主页项目 基础项目模型类中 is_homepage == True 的项目
    Home_Project = models.OneToOneField(ProjectPage, on_delete=models.CASCADE, null=True)
    class Meta:
        '''
        该类用于存储模型的别名等项目
        '''
        verbose_name = '主页项目'
        verbose_name_plural = '主页项目'

    def __str__(self):
        """
        返回模型的标题字段， 用于优化在admin页面的显示

        Args:
            None

        Returns:
            str: 返回模型的标题字段

        """
        return self.Home_Project.title