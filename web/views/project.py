#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from web.forms.project import ProjectModelForm
from utils.tencent import cos
from web import models
import time

class Project_List(APIView):
    """项目列表"""
    def get(self,request,*args,**kwargs):
        form = ProjectModelForm(request)
        project_dict = {'my':[],'join':[],'star':[]}
        """
        1.我创建的所有项目：星标，未星标
        2.我参与的所有项目：星标，未星标
        """
        my_project_list = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append({'value':row,'type':'my'})
            else:
                project_dict['my'].append(row)
        my_join_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in my_join_list:
            if item.star:
                project_dict['star'].append({'value':item.project,'type':'join'})
            else:
                project_dict['join'].append(item.project)

        return render(request,'project_list.html',{'form':form,'project_dict':project_dict})

    def post(self,request,*args,**kwargs):
        form = ProjectModelForm(request,data=request.POST)
        if form.is_valid():
            #验证通过
            form.instance.creator = request.tracer.user
            # 1.为项目创建一个桶
            bucket = "{}-{}-1258040712".format(request.tracer.user.mobile_phone,int(time.time()))
            region = 'ap-nanjing'
            cos.create_bucket(bucket,region)
            # 2. 把桶和区域写进数据库
            form.instance.bucket = bucket
            form.instance.region = region
            #讲项目保存到数据库
            form.save()
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False,'error':form.errors})

class Project_Star(APIView):
    def get(self,request,project_type, project_id):
        if project_type == 'my':
            models.Project.objects.filter(id=project_id,creator=request.tracer.user).update(star = True)
            return redirect('project_list')
        elif project_type == 'join':
            models.ProjectUser.objects.filter(project_id=project_id,user=request.tracer.user).update(star = True)
            return redirect('project_list')

class Project_unStar(APIView):
    def get(self,request,project_type, project_id):
        if project_type == 'my':
            models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
            return redirect('project_list')
        elif project_type == 'join':
            models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
            return redirect('project_list')