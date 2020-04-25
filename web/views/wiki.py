#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.urls import reverse
from web.forms.wiki import Wiki_Add_Form
from rest_framework.views import APIView
from rest_framework import serializers
from web import models

class MySerializers2(serializers.ModelSerializer):

    class Meta:
        model = models.Wiki
        fields = "__all__"


class Wiki(APIView):
    def get(self,request,project_id):
        return render(request,'wiki.html')

    def post(self,request,project_id):
        pass

class Wiki_Add(APIView):
    """ 添加文章 """

    def get(self,request,project_id):
        form = Wiki_Add_Form(request)
        return render(request,'wiki_add.html',{'form':form})

    def post(self,request,project_id):
        form = Wiki_Add_Form(request,data = request.POST)
        if form.is_valid():
            #判断是否有父文章：
            #如果有，找到该文章的深度+1
            if form.instance.parent:
                form.instance.depth = form.instance.parent.depth + 1
            else:
                form.instance.project = request.tracer.project
            form.save()
            url = reverse('wiki',kwargs={'project_id':project_id})

        return redirect(url)

class Wiki_Catalog(APIView):
    """ wiki目录 """

    #获取现有目录
    def get(self,request,project_id):

        catalog_data_list = models.Wiki.objects.filter( project_id = project_id ).order_by('depth','id')
        #将QuerySet类型数据序列化
        ser = MySerializers2(instance=catalog_data_list,many=True)

        return JsonResponse(ser.data,safe=False)