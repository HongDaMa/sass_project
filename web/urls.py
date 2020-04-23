#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-

from django.conf.urls import url,include
from web.views import account,project,manage
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
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.Project_Star.as_view(), name='project_star'),
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.Project_unStar.as_view(), name='project_unstar'),
    url(r'^manage/(?P<project_id>\d+)/', include([
        url(r'^dashboard/$', manage.Dashboard.as_view(), name='dashboard'),
        url(r'^issues/$',manage.Issues.as_view(),name='issues'),
        url(r'^statistics/$', manage.Statistics.as_view(), name='statistics'),
        url(r'^file/$', manage.File.as_view(), name='file'),
        url(r'^wiki/$', manage.Wiki.as_view(), name='wiki'),
        url(r'^setting/$', manage.Setting.as_view(), name='setting'),
    ],None,None))
]