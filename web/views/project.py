#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from web.forms.project import ProjectModelForm

class Project_List(APIView):
    """项目列表"""
    def get(self,request,*args,**kwargs):
        form = ProjectModelForm(request)
        return render(request,'project_list.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form = ProjectModelForm(request,data=request.POST)
        if form.is_valid():
            #验证通过
            form.instance.creator = request.tracer.user
            #讲项目保存到数据库
            form.save()
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False,'error':form.errors})