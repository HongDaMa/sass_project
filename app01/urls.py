#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.conf.urls import url
from app01 import views
urlpatterns = [
    url(r'^register/',views.Register.as_view()),
]
