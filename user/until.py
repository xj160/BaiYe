import hashlib
from time import time
import random
import re
from . import errors
# 在自己脚本中使用django model
import os, sys
import json
from BaiYe import settings
# import django
# BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 定位到你的django根目录
# sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_tasks.settings")



# from .models import UserProfile
def toMD5(code):
    return hashlib.md5(code.encode('utf-8')).hexdigest()

def uuid(passwd):
    seed = hex(int(time() * 10000))[-10:]
    return passwd[:2] + seed + passwd[-3:]

def send_verification_code():
    code = random.randint(100000, 999999)
    print(code)
    return code

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]#所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')#这里获得代理ip
    return ip


def name_filter(s):
    if len(s) == 0:
        raise errors.naneNullError()

    if len(s) > 15:
        return errors.lengthError(message='昵称不能超过15个字符！',code=1001)

    patt = r'[\\\\/:*?\"<>|]'
    if re.search(patt,s):
        return False

    return True


def phone_filter(num,userModel):
    if not re.search(r'^1[3456789]\d{9}$',num):
        return '手机号码有误！'
    if userModel.objects.filter(phone=num):
        return '此号码已被注册！'
    return None
def pwd_filter(s):
    length = len(s)
    return length >= 6 and length <= 16


# def fields_filter(*args, **kwargs):
#     filters = {
#         'phone':phone_filter,
#         'pwd':pwd_filter,
#         'uname':name_filter
#     }
#     if len(args) == 0 and len(kwargs) == 0:
#         return False
#     ret = True
#     for k,v in kwargs.items():
#         ret &= filters[k](v)
#     return ret

def get_username(UserProfile,pwd):
    pwd = toMD5(pwd)
    username = uuid(pwd)
    while UserProfile.objects.filter(username=username) == []:
        username = uuid(pwd)
    return username

def check_verification(code,fpath):
    if os.path.exists(fpath):
        with open(fpath,'r') as f:
            jsorStr = '\n'.join(f.readlines())
        verDict = json.loads(jsorStr)
        t = time()
        if t - verDict['time'] > 180:
            return '验证码超时，请重新获取！'
        if verDict['ver_code'] != code:
            return '验证码错误！'
        return None
    return '尚未获取验证码，请获取验证码！'

def send_ver_code(code):
    print(code)

def get_icon_name(cachePath,iconType):
    icon_name = toMD5(str(time())) + iconType
    while True:
        if not os.path.exists(os.path.join(cachePath,icon_name)):
            break
        icon_name = toMD5(str(time())) + iconType


    return icon_name

def get_icon_path(cache_icon_path,username):
    iconType = os.path.splitext(cache_icon_path)[1]
    usersPath = cache_icon_path.split('icon_cache/')[0]
    userPath = usersPath + username + '/'
    if not os.path.exists(userPath):
        os.mkdir(userPath)

def save_image(image_file,icon_url,name):
    if icon_url not in name:
        image_file.seek(0)
        real_path = os.path.join(settings.MEDIA_ROOT, icon_url)
        if not os.path.exists(real_path):
            os.makedirs(real_path)
        ext = os.path.splitext(name)[1]
        icon_name = get_icon_name(real_path, ext)
        # self.icon.file
        with open(os.path.join(real_path, icon_name), 'wb') as f:
            f.writelines(image_file.readlines())
        image_file.close()
        ret_url = os.path.join(icon_url, icon_name)
        return ret_url
    return None