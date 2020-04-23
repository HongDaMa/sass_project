#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from web.forms.project import ProjectModelForm
from web import models

class Dashboard(APIView):
    def get(self,request,project_id):
        return render(request,'dashboard.html')

class Issues(APIView):
    def get(self,request,project_id):
        return render(request,'issues.html')

class Statistics(APIView):
    def get(self,request,project_id):
        return render(request,'statistics.html')

class File(APIView):
    def get(self,request,project_id):
        return render(request,'file.html')

class Wiki(APIView):
    def get(self,request,project_id):
        return render(request,'wiki.html')

class Setting(APIView):
    def get(self,request,project_id):
        return render(request,'setting.html')
