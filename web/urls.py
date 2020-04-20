#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-

from django.conf.urls import url,include
from web.views import account
from django.contrib import admin


urlpatterns = [
    url(r'^register/$',account.Register.as_view(),name='register'),
    url(r'^login/sms/$', account.LoginSms.as_view(), name='login_sms'),
    url(r'^send/sms/$',account.SendSms.as_view(),name='send_sms'),
]