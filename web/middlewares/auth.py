#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from django.shortcuts import redirect
from web import models

import datetime

class Tracer(object):
    """用户信息类"""
    def __init__(self):
        #登录的用户数据
        self.user =None
        #价格策略
        self.price_poliy =None
        #项目
        self.project = None

class AuthMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        request.tracer = Tracer()
        """如果用户已经登陆"""
        user_id = request.session.get('user_id',0)
        user_pbject = models.UserInfo.objects.filter(id = user_id).first()
        request.tracer.user = user_pbject

        #白名单：没有登录都有可以访问的URL
        """
        1.获取用户访问当前的URL
        2.检查URL是否在白名单中，如果存在则可以访问，如果不存在则判断用户是否已经登录
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        #检查用户是否已经登录,已登录继续往后走，未登录则返回登录页面
        if not request.tracer.user:
            return redirect('login')

        #登录成功之后，访问后台管理时，获取当前用户所拥有的额度
        #方式一：免费额度在交易记录中存储
        #获取当前用户ID最大值（最近交易记录）
        _object = models.Transaction.objects.filter(user=user_pbject,status=2).order_by('-id').first()
        #判断是否已经过期
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime:
            _object = models.Transaction.objects.filter(user=user_pbject, status=2,price_poliy__category=1).first()
        request.tracer.price_poliy = _object.price_poliy

    def process_view(self, request,view,args,kwargs):
        #判断url是否是以manage开头的,如果不是则return
        if not request.path_info.startswith('/manage/'):
            return
        project_id = kwargs.get('project_id')

        #是否是我创建的
        project_object = models.Project.objects.filter(id=project_id,creator=request.tracer.user).first()
        if project_object:
            request.tracer.project = project_object
            return

        #是否是我参与的
        project_user_object = models.ProjectUser.objects.filter(project_id=project_id,user=request.tracer.user).first()
        if project_object:
            request.tracer.project = project_user_object.project
            return

        return redirect('project_list')