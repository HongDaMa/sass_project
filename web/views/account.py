#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
"""
账户相关功能：注册，短信，登录，注销
"""

from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from web.forms.account import RegisterModelForm,Login_SmsForm,SendsmsForm,LoginForm
from web import models
import uuid
import datetime

# Create your views here.


class Register(APIView):
    """ 注册模块 """
    def get(self,request,*args,**kwargs):
        form = RegisterModelForm()
        return render(request, 'register.html', {'form':form})
    def post(self,request,*args,**kwargs):
        form = RegisterModelForm(data=request.POST)
        if form.is_valid():
            #验证通过，写入数据库，（密码应该是密文）
            instance = form.save()
            """  在交易记录表生成对应的交易信息  """
            price_object = models.PricePoliy.objects.filter(category=1,title='个人免费版').first()
            models.Transaction.objects.create(
                status=2,
                order= uuid.uuid4(),#根据当前时间和当前计算机的网卡计算的随机字符串
                user=instance,
                price_poliy=price_object,
                count=0,
                price=0,
                start_datetime=datetime.datetime.now(),
            )
            return JsonResponse({'status':True,'url':'/login/'})
        else:
            return JsonResponse({'status':False,'error':form.errors})


class LoginSms(APIView):
    """ 短信登录模块 """
    def get(self,request,*args,**kwargs):
        form = Login_SmsForm()
        return render(request,'login_sms.html',{'form':form})
    def post(selfself,request,*args,**kwargs):
        form = Login_SmsForm(data=request.POST)
        if form.is_valid():
            #验证成功，将用户ID写入session中
            mobile_phone = form.cleaned_data.get('mobile_phone')
            user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return JsonResponse({'status': True, 'url': '/index/'})
        else:
            return JsonResponse({'status':False,'error':form.errors})


class Login(APIView):
    """ 用户名密码登录模块 """
    def get(self,request,*args,**kwargs):
        form = LoginForm(request)
        return render(request,'login.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            from django.db.models import Q
            # 验证成功，将用户ID写入session中
            user_object = models.UserInfo.objects.filter(Q(mobile_phone = username)|Q(email=username)).filter(password=password).first()
            if user_object:
                request.session['user_id'] = user_object.id
                request.session.set_expiry(60*60*24*14)
                return redirect('index')
            else:
                form.add_error(username,'用户名或者密码错误')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request,'login.html',{'form':form})



class ImageCode(APIView):
    """ 生成写入内存验证码并返回 """
    def get(self,request,*args,**kwargs):
        from utils.image_code import check_code
        image_code_obj ,code = check_code()
        from io import BytesIO
        stream = BytesIO()
        image_code_obj.save(stream, 'png')
        #讲验证码存入session中
        request.session['image_code'] = code
        #设置session过期时间为60s
        request.session.set_expiry(60)
        return HttpResponse(stream.getvalue())

class SendSms(APIView):
    """ 注册发送短信模块 """
    def get(self,request,*args,**kwargs):
        print(request.GET)
        form = SendsmsForm(data=request.GET,request=request)
        #校验手机号，不能为空，格式是否正确
        if form.is_valid():
            #验证通过，写入数据库
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False,'error':form.errors})

class Logout(APIView):
    """ 注销登录 """
    def get(self,request,*args,**kwargs):
        #清空session数据
        request.session.flush()
        return redirect('login')

class Index(APIView):
    def get(self,request,*args,**kwargs):
        return render(request,'index.html')