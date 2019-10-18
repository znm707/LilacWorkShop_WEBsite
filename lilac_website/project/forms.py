from django import forms
# 引入文章模型
from .models import ProjectPage

# 写文章的表单类
class ProjectForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ProjectPage
        # 定义表单包含的字段
        fields = ('title', 'abstract', 'tags', 'body', 'avatar')