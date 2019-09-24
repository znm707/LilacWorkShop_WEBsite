# coding: utf-8
from django.db import models


# Create your models here.
class HomeItem(models.Model):
    '''
    HomeItem是首页上内容的链接， HomeItem使我们可以轻松的通过admin后台编辑首页显示哪些文章，文章显示的顺序等内容
    '''
    # 文章显示顺序, 默认从0开始
    rank = models.IntegerField('显示排序', default=0)

    class Meta:
        '''
        该类用于自定义在admin页面显示的内容
        '''
        verbose_name = '主页内容'
        verbose_name_plural = '主页内容'

    def __str__(self):
        """
        返回模型的排名字段， 用于优化在admin页面的显示

        Args:
            None

        Returns:
            str: 返回模型的排名字段

        """
        return self.rank
