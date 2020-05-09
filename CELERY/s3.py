#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from celery.result import AsyncResult
from CELERY.s1 import app

result_object = AsyncResult(id="xxxxxxxx",app=app)
print(result_object.status)