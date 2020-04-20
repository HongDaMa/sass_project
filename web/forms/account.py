#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django import forms
from web import models
from django.core.validators import RegexValidator,ValidationError
from django.core.exceptions import ValidationError
from django.conf import settings
from django_redis import get_redis_connection
from utils import encrypt
from utils.tencent.sms import send_sms_single
import random

class RegisterModelForm(forms.ModelForm):

    mobile_phone = forms.CharField(
        label='手机号',
        required = True,
        validators=[RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$")],
        error_messages={'required':'手机号不能为空。'}
    )
    email = forms.EmailField(
        label='邮箱',
        required=True,
        error_messages={'required':'邮箱不能为空。'}
    )
    password = forms.CharField(
        label='密码',
        required = True,
        widget=forms.PasswordInput(),
        error_messages={'required':'密码不能为空。'}
    )
    confirm_password = forms.CharField(
        label='重复密码',
        required = True,
        widget=forms.PasswordInput(),
        error_messages={'required':'请输入重复密码。'}
    )
    code = forms.CharField(
        label='验证码',
        required = True,
        error_messages={'required':'验证码不能为空。'}
    )

    class Meta:
        model = models.UserInfo
        fields = ['username','email','password','confirm_password','mobile_phone','code']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s'%(field.label)

    def clean_username(self):
        """
        username 的钩子函数
        :return: 用户名
        """
        username = self.cleaned_data.get('username')
        exists = models.UserInfo.objects.filter(username= username).exists()
        if exists:
            raise ValidationError('用户名已存在，请重新输入!')
        else:
            return username

    def clean_email(self):
        """
        email 的钩子函数
        :return: 邮箱地址
        """
        email = self.cleaned_data.get('email')
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在，请重新输入!')
        else:
            return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        #加密&返回
        return encrypt.md5(password)

    def clean_confirm_password(self):
        """
        confirm_password 的钩子函数
        :return: confirm_password重复密码
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != encrypt.md5(confirm_password):
            raise ValidationError('两次输入密码不一致')
        else:
            return confirm_password
    def clean_code(self):
        """
        code 的钩子函数
        :return: 正确的验证码
        """
        mobile_phone = self.cleaned_data.get('mobile_phone')
        code = self.cleaned_data.get('code')
        conn = get_redis_connection("default")
        # 将验证码写入redis
        value = conn.get(mobile_phone)
        #将返回的二进制字符串转化成字符串
        if value != None:
            value = str(value,encoding='utf-8')
            print(value)
        if value == None:
            raise ValidationError('验证码不存在或者已过期！')
        elif value != None and value != code:
            raise ValidationError('验证码错误，请重新输入！')
        else:
            return code

class SendsmsForm(forms.Form):

    mobile_phone = forms.CharField(
        label='手机号',
        required=True,
        validators=[RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$")],
        error_messages={'required': '手机号不能为空'}
    )

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean_mobile_phone(self):
        """手机号验证的钩子函数"""
        mobile_phone = self.cleaned_data['mobile_phone']

        #校验短信模板是否有问题
        tpl = self.request.GET.get('tpl')

        #校验数据库中是否已经有手机号
        template_id = settings.TENCET_SMS_TEMPLATES.get(tpl)
        print(template_id)
        if not template_id:
            raise ValidationError('短信模板错误')
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已存在')

        code = random.randrange(1000,9999)
        # 利用腾讯sdk发送短信
        sms = send_sms_single(mobile_phone,template_id,[code,])
        if sms['result'] != 0:
            raise ValidationError("短信发送失败，{}".format(sms['errmsg']))
        # 去连接池中获取一个连接
        conn = get_redis_connection("default")
        #将验证码写入redis
        conn.set(mobile_phone, code, ex=180)
        value = conn.get(mobile_phone)
        print(value)

        return mobile_phone
