from django import forms
# ��������ģ��
from .models import ProjectPage

# д���µı���
class ProjectForm(forms.ModelForm):
    class Meta:
        # ָ������ģ����Դ
        model = ProjectPage
        # ������������ֶ�
        fields = ('title', 'abstract', 'tags', 'body', 'avatar')