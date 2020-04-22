#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from rest_framework.views import APIView

class Project_List(APIView):
    """项目列表"""
    def get(self,request,*args,**kwargs):
        return render(request,'project_list.html')
    def post(self,request,*args,**kwargs):
        pass