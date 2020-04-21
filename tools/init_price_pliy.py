#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from tools import base
from web import models

def run():
    exists = models.PricePoliy.objects.filter(category=1,title='个人免费版').exists()
    if not exists:
        models.PricePoliy.objects.create(
        category=1 ,
        title ='个人免费版' ,
        price = 0 ,
        project_num = 3,
        project_member = 2,
        project_max_memory = 20,
        single_file = 5 ,
        )

if __name__ == '__main__':
    run()