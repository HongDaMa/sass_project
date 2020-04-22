#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django import forms
from web import models
from django.core.validators import RegexValidator,ValidationError
from django.core.exceptions import ValidationError
from web.forms.account import BootStrapForm

class ProjectModelForm(BootStrapForm,forms.ModelForm):
    """新建项目表单"""
    class Meta:
        model = models.Project
        fields = ['name','color','desc']
        widgets = {
            'desc':forms.Textarea()
        }

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean_name(self):
        """ 新建项目校验 """
        name = self.cleaned_data['name']

        #1.校验该项目名称是否已经存在
        exists = models.Project.objects.filter(name=name,creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError('该项目已存在')

        #2.当前用户是否还有额度创建项目
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()
        if count >= self.request.tracer.price_poliy.project_num:
            raise ValidationError('当前项目个数超限，请更换套餐')

        return name