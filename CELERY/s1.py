#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from celery import Celery

app = Celery('tasks',borker='redis://127.0.0.1:6379/0',backend='redis://127.0.0.1:6379/0')

@app.task
def x1(x,y):
	return x+y

@app.task
def x2(x,y):
	return x-y