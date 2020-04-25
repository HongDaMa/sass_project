#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django import forms
from web import models
from django.core.validators import RegexValidator,ValidationError
from django.core.exceptions import ValidationError
from web.forms.account import BootStrapForm

class Wiki_Model_Form(BootStrapForm,forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ['project','depth']

    #找到想要的字段把他绑定显示的数据重置
    # 数据 = 去数据库中获取 当前项目所有的wiki标题
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        total_data_list = [("","请选择")]
        data_list = models.Wiki.objects.filter(project=request.tracer.project).values_list('id','title')
        total_data_list.extend(data_list)

        self.fields['parent'].choices = total_data_list

