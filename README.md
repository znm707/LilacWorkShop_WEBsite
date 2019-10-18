# 紫丁香创新工场网站开发说明
![license](https://img.shields.io/badge/license-GPL-blue)   [![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
>  紫丁香创新工场网站, 基于Django+BootStrap编写

## 目录
[TOC]

## 项目介绍
紫丁香微纳卫星创新工场拟定向全校、乃至其他高校的大学生创新团队提供实验场所。因此需要一个在线的管理创新项目的平台。

## 平台功能
### 网页主页
网站主页仅展示一些静态内容，静态内容可通过后台更改，首页也可以选择展示或置顶当前的某个项目

### 用户管理
1. 平台应具有基本的用户管理功能，即自动注册、登录等功能
2. 注册暂时仅面向哈工大在校学生开放
3. 可由管理员管理其他学校用户的管理权限
4. 用户权限分为“超级管理员”、“教师”、“学生”
5. 用户应该有个人详情页

### 项目管理
1. 教师有权限发布项目， 项目应该包含摘要、关键字和详细信息
2. 一个项目只应该有一篇详细信息，该内容允许发布者修改
3. 学生可以报名参加项目
4. 发布者可管理参与项目的学生

## 平台要求
### 数据库设计
### 用户权限
| 权限名称 | 用户增删改 | 项目增删改 | 参与项目 | 评论项目 | 更改项目成员 | 
| ---- |  :----: | :----: | :----: | :----: | :----: |
| 管理员 | ✔ | ✔ | ✔ | ✔ |  ✔ |
| 教师 | ✘  | ✔ | ✔ | ✔ | ✔ |
| 学生 | ✘ | ✘ | ✔ | ✔ | ✘ |

> **注**
教师权限仅针对自己发布的项目
评论项目，只有教师才有权限回复他人的评论

## 开发要求
### 环境要求
| 项目 | 版本 |
| ---- | ----|
| Python | 3.6 |
| Django | 2.2 |
| MySQL | 8.0 |

### 托管平台及合并代码
1. 代码采用GPL 3.0协议， 开源在Github上
2. 任何人应该在框架基础上**新建分支**进行编写
3. 当当每完成后应该申请Pull Request进行代码审查和合并代码
### 语法检查
使用f**lake8**对Python语法进行检查
### 注释要求
> **NOTICE:**采用sphinx自动从注释中生成文档， 因此请大家遵守注释协定
#### Python代码的注释要求
``` Python
class Demo1():
    """类功能 
    """
    def google_style(arg1, arg2):
        """函数功能.

        函数功能说明.

        Args:
            arg1 (int): arg1的参数说明
            arg2 (str): arg2的参数说明

        Returns:
            bool: 返回值说明

        """
        return True
```
#### HTML代码的注释要求
```HTML
<!-- extends表明此页面继承自 base.html 文件 -->
{% extends "base.html" %}
{% load staticfiles %}

<!-- 写入 base.html 中定义的 title -->
{% block title %}
首页
{% endblock title %}

<!-- 写入 base.html 中定义的 content -->
{% block content %}

<!-- 定义放置文章标题的div容器 -->
<div class="container">
    <!-- 新增，搜索栏 -->
    <div class="row">
        <div class="col-auto mr-auto">
        </div>
    </div>
</div>
{% endblock content %}
```