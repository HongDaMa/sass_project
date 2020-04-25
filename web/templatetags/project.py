#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.template import Library
from web import models
register = Library()

@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    """
    1。获取我创建的所有项目
    2.获取我参与的所有项目
    :return:
    """
    my_project_list = models.Project.objects.filter(creator=request.tracer.user)
    print(my_project_list)
    join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)

    return {'my':my_project_list,'join':join_project_list,'request':request}