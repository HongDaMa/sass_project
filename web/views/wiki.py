#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.urls import reverse
from web.forms.wiki import Wiki_Model_Form
from rest_framework.views import APIView
from rest_framework import serializers
from web import models

class MySerializers2(serializers.ModelSerializer):

    class Meta:
        model = models.Wiki
        fields = "__all__"


class Wiki(APIView):
    def get(self,request,project_id):
        wiki_id = request.GET.get('wiki_id')
        if not wiki_id or not wiki_id.isdecimal():
            return render(request, 'wiki.html')
        wiki_project = models.Wiki.objects.filter(id=wiki_id,project=request.tracer.project).first()
        print(wiki_project.content)
        return render(request,'wiki.html',{'wiki_project':wiki_project})

    def post(self,request,project_id):
        pass

class Wiki_Add(APIView):
    """ 添加文章 """

    def get(self,request,project_id):
        form = Wiki_Model_Form(request)
        return render(request, 'wiki_form.html', {'form':form})

    def post(self,request,project_id):
        form = Wiki_Model_Form(request,data = request.POST)
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

class Wiki_Edit(APIView):
    """ 更新文章 """

    def get(self,request,project_id,wiki_id):
        if not wiki_id:
            url = reverse('wiki',kwargs={'project_id':project_id})
            return redirect(url)
        wiki_object = models.Wiki.objects.filter(id=wiki_id,project=request.tracer.project).first()
        form = Wiki_Model_Form(request,instance=wiki_object)
        return render(request, 'wiki_form.html', {'form':form,'wiki_object':wiki_object})

    def post(self,request,project_id,wiki_id):
        wiki_object = models.Wiki.objects.filter(id=wiki_id, project=request.tracer.project).first()
        form = Wiki_Model_Form(request,data = request.POST,instance = wiki_object )
        if form.is_valid():
            #判断是否有父文章：
            #如果有，找到该文章的深度+1
            if form.instance.parent:
                form.instance.depth = form.instance.parent.depth + 1
            else:
                form.instance.project = request.tracer.project
            form.save()
            WIKI = reverse('wiki',kwargs={'project_id':project_id})
            url = WIKI+'?wiki_id='+str(wiki_id)

        return redirect(url)

class Wiki_Detele(APIView):
    """ 删除文章 """

    def get(self,request,project_id,wiki_id):
        models.Wiki.objects.filter(project_id=project_id,id=wiki_id).delete()
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)

class Wiki_Catalog(APIView):
    """ wiki目录 """

    #获取现有目录
    def get(self,request,project_id):

        catalog_data_list = models.Wiki.objects.filter( project_id = project_id ).order_by('depth','id')
        #将QuerySet类型数据序列化
        ser = MySerializers2(instance=catalog_data_list,many=True)

        return JsonResponse({'status': True, 'data': ser.data},safe=False)