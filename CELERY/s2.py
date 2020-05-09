#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from CELERY.s1 import x1

result =x1.delay(4,4)
print(result.id)