#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from web.forms.file import CreateFolderForm,FileModelForm
from rest_framework.views import APIView
from web import models
from utils.tencent.cos import credential,delete_file,delete_file_list
from django.urls import reverse
import requests
import json

class File(APIView):

    def get(self,request,project_id):
        parent_object = None
        """
        获取所有的文件和文件夹对象
        :param request:
        :param project_id:
        :return:
        """
        folder_id= request.GET.get("folder_id","")
        dir_list = []
        form = CreateFolderForm(request,parent_object)
        #判断URL是否有folder_id参数
        #如果没有则访问根目录
        #如果有则访问对应ID的目录
        if not folder_id:
            folder_object = None
            file_object_list = models.FileRepository.objects.filter(parent=None).order_by('-file_type')
        else:
            parent_object = models.FileRepository.objects.filter(id=folder_id,file_type=2).first()
            file_object_list = models.FileRepository.objects.filter(parent=parent_object)
            folder_object = parent_object
            row_object = parent_object
            while row_object:
                dir_list.insert(0,row_object)
                row_object = row_object.parent
        return render(request,'file.html',
                      {
                          'form':form,
                          'file_object_list':file_object_list,
                          'folder_object':folder_object,
                          'dir_list':dir_list
                      })

    def post(self,request,project_id):
        parent_object = None
        fid = request.POST.get('fid', '')
        if fid.isdecimal():
            edit_object = models.FileRepository.objects.filter(id=int(fid), file_type=2,
                                                               project=request.tracer.project).first()
        if edit_object:
            form = CreateFolderForm(request, parent_object, data=request.POST, instance=edit_object)
        else:
            form = CreateFolderForm(request,data=request.POST)
        parent_object = None
        folder_id = request.GET.get('folder_id')
        print(folder_id)
        if folder_id:
            parent_object = models.FileRepository.objects.filter(id=folder_id,file_type=2,project=request.tracer.project).first()
        if form.is_valid():
            form.instance.project = request.tracer.project
            form.instance.file_type=2
            form.instance.update_user=request.tracer.user
            form.instance.parent= parent_object
            form.save()
            return JsonResponse({'status':True,'error':None})
        else:
            return JsonResponse({'status':False,'error':form.errors})

    def delete(self,request,project_id):
        """ 删除文件 """
        fid = request.data.get('fid')

        # 删除数据库中的 文件 & 文件夹 （级联删除）
        delete_object = models.FileRepository.objects.filter(id=fid, project=request.tracer.project).first()
        if delete_object.file_type == 1:
            # 删除文件，将容量还给当前项目的已使用空间
            request.tracer.project.use_space -= delete_object.file_size
            request.tracer.project.save()

            # cos中删除文件
            delete_file(request.tracer.project.bucket, request.tracer.project.region, delete_object.key)

            # 在数据库中删除当前文件
            delete_object.delete()

            return JsonResponse({'status': True})

        # 删除文件夹（找到文件夹下所有的文件->数据库文件删除、cos文件删除、项目已使用空间容量还回去）
        # delete_object
        # 找他下面的 文件和文件夹
        # models.FileRepository.objects.filter(parent=delete_object) # 文件 删除；文件夹 继续向里差

        total_size = 0
        key_list = []

        folder_list = [delete_object, ]
        for folder in folder_list:
            child_list = models.FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by(
                '-file_type')
            for child in child_list:
                if child.file_type == 2:
                    folder_list.append(child)
                else:
                    # 文件大小汇总
                    total_size += child.file_size

                    # 删除文件
                    key_list.append({"Key": child.key})

        # cos 批量删除文件
        if key_list:
            delete_file_list(request.tracer.project.bucket, request.tracer.project.region, key_list)

        # 归还容量
        if total_size:
            request.tracer.project.use_space -= total_size
            request.tracer.project.save()

        # 删除数据库中的文件
        delete_object.delete()
        return JsonResponse({'status': True})

class File_Post(APIView):

    def post(self,request,project_id):
        """ 已上传成功的文件写入到数据 """
        """
        name: fileName,
        key: key,
        file_size: fileSize,
        parent: CURRENT_FOLDER_ID,
        # etag: data.ETag,
        file_path: data.Location
        """

        # 根据key再去cos获取文件Etag和"db7c0d83e50474f934fd4ddf059406e5"

        print(request.POST)
        # 把获取到的数据写入数据库即可
        form = FileModelForm(request, data=request.POST)
        if form.is_valid():
            # 通过ModelForm.save存储到数据库中的数据返回的isntance对象，无法通过get_xx_display获取choice的中文
            # form.instance.file_type = 1
            # form.update_user = request.tracer.user
            # instance = form.save() # 添加成功之后，获取到新添加的那个对象（instance.id,instance.name,instance.file_type,instace.get_file_type_display()

            # 校验通过：数据写入到数据库
            data_dict = form.cleaned_data
            data_dict.pop('etag')
            data_dict.update({'project': request.tracer.project, 'file_type': 1, 'update_user': request.tracer.user})
            instance = models.FileRepository.objects.create(**data_dict)
            # 项目的已使用空间：更新 (data_dict['file_size'])
            request.tracer.project.use_space += data_dict['file_size']
            request.tracer.project.save()
            print(instance.update_time)
            result = {
                'id': instance.id,
                'name': instance.name,
                'file_size': instance.file_size,
                'username': instance.update_user.username,
                'datetime': instance.update_time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒'),
                'download_url': reverse('file_download', kwargs={"project_id": project_id, 'file_id': instance.id})
                # 'file_type': instance.get_file_type_display()
            }
            return JsonResponse({'status': True, 'data': result})
        print(form.errors)
        return JsonResponse({'status': False, 'data': "文件错误"})

class File_Download(APIView):
    def get(self,request,project_id,file_id):
        file_object = models.FileRepository.objects.filter(id=file_id, project_id=project_id).first()
        res = requests.get(file_object.file_path)

        # 文件分块处理（适用于大文件）     @孙歆尧
        data = res.iter_content()

        # 设置content_type=application/octet-stream 用于提示下载框        @孙歆尧
        response = HttpResponse(data, content_type="application/octet-stream")
        from django.utils.encoding import escape_uri_path

        # 设置响应头：中文件文件名转义      @王洋
        response['Content-Disposition'] = "attachment; filename={};".format(escape_uri_path(file_object.name))
        return response


class Cos_Credential(APIView):
    def get(self,requwst,project_id):
        pass

    def post(self, request, project_id):
        """ 获取cos上传临时凭证 """
        per_file_limit = request.tracer.price_poliy.per_file_size * 1024 * 1024
        total_file_limit = request.tracer.price_poliy.project_space * 1024 * 1024 * 1024

        total_size = 0
        file_list = json.loads(request.body.decode('utf-8'))
        for item in file_list:
            # 文件的字节大小 item['size'] = B
            # 单文件限制的大小 M
            # 超出限制
            if item['size'] > per_file_limit:
                msg = "单文件超出限制（最大{}M），文件：{}，请升级套餐。".format(request.tracer.price_policy.per_file_size, item['name'])
                return JsonResponse({'status': False, 'error': msg})
            total_size += item['size']

            # 做容量限制：单文件 & 总容量

        # 总容量进行限制
        # request.tracer.price_poliy.project_space  # 项目的允许的空间
        # request.tracer.project.use_space # 项目已使用的空间
        if request.tracer.project.use_space + total_size > total_file_limit:
            return JsonResponse({'status': False, 'error': "容量超过限制，请升级套餐。"})

        data_dict = credential(request.tracer.project.bucket, request.tracer.project.region)
        return JsonResponse({'status': True, 'data': data_dict})
