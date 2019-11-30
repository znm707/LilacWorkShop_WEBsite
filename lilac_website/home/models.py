# coding: utf-8
from django.db import models
from project.models import HomeProject

# Create your models here.
class HomeItem(models.Model):
    '''
    HomeItem是首页上内容的链接， HomeItem使我们可以轻松的通过admin后台编辑首页显示哪些文章，文章显示的顺序等内容
    '''
    # 文章显示顺序, 默认从0开始
    rank = models.PositiveIntegerField('显示排序', default=0,unique = True)
    # 文章滚动顺序, 默认为空不参与滚动
    roll_rank = models.PositiveIntegerField('滚动顺序', null = True, unique = True, blank = True)
    # 主页项目
    home_project = models.OneToOneField(HomeProject, on_delete=models.CASCADE, null=True)
    class Meta:
        '''
        该类用于自定义在admin页面显示的内容
        '''
        verbose_name = '主页内容'
        verbose_name_plural = '主页内容'
        ordering = ('rank', )
    def __str__(self):
        """
        返回模型的排名字段， 用于优化在admin页面的显示

        Args:
            None

        Returns:
            str: 返回模型的排名字段

        """
        return str(self.rank)
