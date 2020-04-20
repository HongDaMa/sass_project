#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
"""
账户相关功能：注册，短信，登录，注销
"""

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from web.forms.account import RegisterModelForm,SendsmsForm

# Create your views here.

#注册模块
class Register(APIView):
    def get(self,request,*args,**kwargs):
        form = RegisterModelForm()
        return render(request, 'register.html', {'form':form})
    def post(self,request,*args,**kwargs):
        form = RegisterModelForm(data=request.POST)
        if form.is_valid():
            #验证通过，写入数据库，（密码应该是密文）
            instance = form.save()
            return JsonResponse({'status':True,'data':'/login/'})
        else:
            return JsonResponse({'status':False,'error':form.errors})

#注册发送短信模块
class SendSms(APIView):
    def get(self,request,*args,**kwargs):
        print(request.GET)
        form = SendsmsForm(data=request.GET,request=request)
        #校验手机号，不能为空，格式是否正确
        if form.is_valid():
            #验证通过，写入数据库
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False,'error':form.errors})
