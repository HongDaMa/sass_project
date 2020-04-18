from django.shortcuts import render,HttpResponse
from django.conf import settings
from utils.tencent.sms import send_sms_single
import random
# Create your views here.
def sms(request):
    tpl = request.GET.get('tpl')
    print(tpl)
    print(settings.TENCET_SMS_TEMPLATES)
    template_id = settings.TENCET_SMS_TEMPLATES.get(tpl)
    print(template_id)
    if not template_id:
        return HttpResponse('模板错误')
    code = random.randrange(100000,999999)
    res = send_sms_single('17649803845',template_id,[code,])
    if res['result'] == 0:
        return HttpResponse('成功')
    else:
        return HttpResponse(res['errmsg'])