# coding: utf-8
from django.shortcuts import render
from .models import HomeItem
from django.db.models import Q
# Create your views here.
def show_home(request):
    HomeItems = HomeItem.objects.all()
    # 查找滚动项目
    RollItems = HomeItem.objects.filter(~Q(roll_rank = None))
    # 滚动项目按照顺序排序
    RollItems = RollItems.order_by("roll_rank")
    # num为有滚动顺序的主页项目总数
    num = HomeItem.objects.all().count() - HomeItem.objects.filter(roll_rank = None).count()
    # 最小滚动顺序
    min_rollindex = -1
    for item in HomeItems:
        if min_rollindex < 0:
            min_rollindex = item.roll_rank
        else:
            if min_rollindex > item.roll_rank:
                min_rollindex = item.roll_rank
    roll_num = []
    for i in range(0,num):
        roll_num.append(i)
    return render(request,
                  'home/homepage.html',
                  {'HomeItems':HomeItems,
                   'roll_num':roll_num,
                   'min_rollindex':min_rollindex,
                   'RollItems':RollItems})