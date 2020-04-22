#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-

from django.conf.urls import url,include
from web.views import account
from web.views import project
from django.contrib import admin


urlpatterns = [
    url(r'^register/$',account.Register.as_view(),name='register'),
    url(r'^login/sms/$', account.LoginSms.as_view(), name='login_sms'),
    url(r'^login/$', account.Login.as_view(), name='login'),
    url(r'^send/sms/$',account.SendSms.as_view(),name='send_sms'),
    url(r'^send/sms/$',account.SendSms.as_view(),name='send_sms'),
    url(r'^image/code/$', account.ImageCode.as_view(), name='image_code'),
    url(r'^index/$', account.Index.as_view(), name='index'),
    url(r'^logout/$', account.Logout.as_view(), name='logout'),
    url(r'^project/list/$', project.Project_List.as_view(), name='project_list'),
]