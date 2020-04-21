#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from web import models

class AuthMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        """如果用户已经登陆"""
        user_id = request.session.get('user_id',0)
        user_pbject = models.UserInfo.objects.filter(id = user_id).first()
        request.tracer = user_pbject