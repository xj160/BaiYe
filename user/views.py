from time import time
from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from . import  until
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm
import json
import random
import os
from BaiYe import settings
@csrf_exempt
def register(request):
    ip = until.get_ip(request)
    ver_code_path=os.path.join(settings.STATIC_ROOT, ip + '.json')
    if request.method == 'GET':
        if os.path.exists(ver_code_path):
            os.remove(ver_code_path)
        obj = RegisterForm()
        return render(request,'user/register.html',{'obj':obj})
    elif request.method == 'POST':
        ret_json = dict({'status':200})
        # return render(request, 'error.html')

        rform = RegisterForm(request.POST, ver_path=ver_code_path)
        if rform.is_valid():
            nick_name = request.POST.get('nick_name')
            # user = UserProfile.objects.get(nick_name=nick_name)
            passwd = request.POST.get('password')
            phone = request.POST.get('phone')
            username = until.get_username(UserProfile,passwd)
            user = UserProfile.objects.create(
                username = username,
                nick_name = nick_name,
                password=passwd,
                phone = phone,
                register_ip = ip
            )
            user.set_password(passwd)
            user.save()
            auth.login(request,user)
            return HttpResponse(json.dumps(ret_json), content_type="application/json")
        else:
            err_msg = rform.errors
            ret_json = {'status':404}
            ret_json.update(err_msg)
            return HttpResponse(json.dumps(ret_json), content_type="application/json")
    else:
        return render(request,'error.html')

@csrf_exempt
def check_phone(request):
    if request.method == 'POST':
        request_data = request.body
        request_dict = json.loads(request_data.decode('utf-8'))
        phone = request_dict.get('phone')
        # print(phone)
        err = until.phone_filter(phone, UserProfile)
        if err is not None:
            return HttpResponse(err)
        return HttpResponse('')
    else:
        return render(request, 'error.html')

@csrf_exempt
def ver_code(request):
    if request.method == 'POST':
        ver_code = str(random.randint(100000, 999999))
        until.send_ver_code(ver_code)
        t = time()
        ip = until.get_ip(request)
        jsonStr = json.dumps({
          'time':t,
          'ver_code':ver_code
        })
        with open(os.path.join(settings.STATIC_ROOT, ip+'.json'),'w') as f:
            f.write(jsonStr)
        return HttpResponse('')
    return render(request, 'error.html')

