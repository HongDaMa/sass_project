from django.shortcuts import render,HttpResponse
from django.conf import settings
from utils.tencent.sms import send_sms_single
from rest_framework.views import APIView
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from app01 import models
# Create your views here.

class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号',validators=[RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$")])
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码',widget=forms.PasswordInput())
    code = forms.CharField(label='验证码')
    class Meta:
        model = models.UserInfo
        fields = ['username','email','password','confirm_password','mobile_phone','code']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s'%(field.label)

class Register(APIView):
    def get(self,request,*args,**kwargs):
        form = RegisterModelForm()
        return render(request,'register.html',{'form':form})
    def post(self,request,*args,**kwargs):
        pass