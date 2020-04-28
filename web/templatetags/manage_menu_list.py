#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.template import Library
from django.urls import reverse
register = Library()

@register.inclusion_tag('inclusion/manage_menu_list.html')
def manage_menu_list(request):
    data_list = [
        {'title': '概览','url':reverse('dashboard',kwargs={'project_id':request.tracer.project.id})},
        {'title': '问题', 'url': reverse('issues', kwargs={'project_id': request.tracer.project.id})},
        {'title': '统计', 'url': reverse('statistics', kwargs={'project_id': request.tracer.project.id})},
        {'title': 'wiki', 'url': reverse('wiki', kwargs={'project_id': request.tracer.project.id})},
        {'title': '文件', 'url': reverse('file', kwargs={'project_id': request.tracer.project.id})},
        {'title': '配置', 'url': reverse('setting', kwargs={'project_id': request.tracer.project.id})},
    ]
    for item in data_list:
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'
    return {'data_list':data_list}