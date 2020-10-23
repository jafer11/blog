from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
import hashlib
import random
import time
from blog_token.views import make_token


# Create your views here.

def users(request):
    if request.method == 'GET':
        # 获取用户数据
        pass
        return JsonResponse({'code': 200})
    elif request.method == 'POST':
        # request.POST 只能拿表单提交的数据
        dict = json.loads(request.body.decode())
        # 前端注册页面地址 http://127.0.0.1:5000/register
        json_str = request.body
        if not json_str:
            result = {'code': 201, 'error': 'Without data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        username = json_obj.get('username')
        if not username:
            result = {'code': 202, 'error': 'Please enter the username'}
            return JsonResponse(result)
        email = json_obj.get('email')
        if not email:
            result = {'code': 203, 'error': 'Please enter the email'}
            return JsonResponse(result)
        password_1 = json_obj.get('password_1')
        password_2 = json_obj.get('password_2')
        if not password_1 or not password_2:
            result = {'code': 204, 'error': 'Please enter the password'}
            return JsonResponse(result)
        if password_1 != password_2:
            result = {'code': 205, 'error': 'The passwords you entered do not match'}
            return result
        # 优先查询当前用户名是否已存在
        old_users = UserProfile.objects.filter(username=username)
        if old_users:
            result = {'code': 206, 'error': 'Username has already existed'}
        # 密码处理 md5哈希/散列
        m = hashlib.md5()
        m.update(password_1.encode())
        # Charfield 进来避免使用 null=True
        # info = ['我来到你的城市，熟悉的那一条街', '摔倒了，要抱抱才能起来', '我奋力追，即使拖毁这身躯']
        # sigh = random.choice(info)
        sign = info = ''
        try:
            UserProfile.objects.create(username=username, nickname=username, email=email, password=m.hexdigest(),
                                       sign=sign, info=info)
        except Exception as e:
            # 数据库down，用户名已存在
            result = {'code': 207, 'error': 'Server is busy'}
            return JsonResponse(result)
        # make token
        token = make_token(username).decode()
        # 正常返回给前端
        result = {'code': 200, 'username': username, 'data': {'token': token}}
        return JsonResponse(result)

    elif request.method == 'PUT':
        # 更新数据
        pass
    else:
        raise
    return JsonResponse({'code': 200})
