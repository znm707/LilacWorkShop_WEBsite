# coding: utf-8

from django.db import models
# 引入django原生user类
from django.contrib.auth.models import User
# 引入django-ckeditor 实现富文本编辑器的功能
from ckeditor.fields import RichTextField


# Create your models here.
class School(models.Model):
    '''
    学校类， 这里用于创建可选学校
    '''
    # 学校名称
    school_name = models.CharField(max_length=50)
    # 学校域名列表, 采用JSON格式存储
    school_emails = models.CharField(max_length=500)

    class Meta:
        '''
        该类用于存储模型的别名等项目
        '''
        verbose_name = '参与学校'
        verbose_name_plural = '参与学校'

    def __str__(self):
        """
        返回模型的校名字段， 用于优化在admin页面的显示

        Args:
            None

        Returns:
            str: 返回模型的校名字段

        """
        return self.school_name


class Profile(models.Model):
    '''
    采用扩展django原生User类， 这样原生的User类用于处理登录等功能， 这里扩展了用户的信息
    '''
    # 与 User 模型构成一对一关系, 其中on_delete=models.CASCADE 表示user删除时 同时自动删除profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 学校 构成一对多的模式， 即一个学校可以拥有多个学生， 当学校删除时， 用户也一并删除
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school')
    # 用户手机号
    phone = models.CharField(max_length=20, blank=True)
    # 用户角色（权限） 用户可以使‘项目发布者’， ‘项目参与者’
    # 枚举列表
    TEACHER = 'TE'  # 项目发布者
    STUDENT = 'ST'  # 项目参与者
    ROLE_CHOICES = (
        (TEACHER, '项目发布者'),
        (STUDENT, '项目参与者'),
    )
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=STUDENT,
    )
    # 用户头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 个人介绍, 使用富文本编辑器
    body = RichTextField()

    class Meta:
        '''
        该类用于存储模型的别名等项目
        '''
        verbose_name = '用户详情'
        verbose_name_plural = '用户详情'

    def __str__(self):
        """
        返回模型的所属用户的用户名， 用于优化在admin页面的显示

        Args:
            None

        Returns:
            str: 返回模型的所属用户的用户名

        """
        return self.user.username
