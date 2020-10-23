import json

from django.http import JsonResponse
from django.shortcuts import render
import hashlib
from user.models import UserProfile
import time


# Create your views here.

def tokens(request):
    """
        创建token == 登录
    :param request:
    :return:
    """
    if not request.method == 'POST':
        result = {'code': 101, 'error': 'Please use method POST'}
        return JsonResponse(result)
    # 获取前端传来数据/生车token
    # 获取-校验密码-生产token
    json_str = request.body.decode()
    if not json_str:
        result = {'code': 102, 'error': 'Without data'}
        return JsonResponse(result)
    json_obj = json.loads(json_str)
    username = json_obj.get('username')
    if not username:
        result = {'code': 103, 'error': 'Please enter the username'}
        return JsonResponse(result)
    password = json_obj.get('password')
    if not password:
        result = {'code': 104, 'error': 'Please enter the password'}
        return JsonResponse(result)
    # 校验用户名和密码

    user = UserProfile.objects.filter(username=username)
    if not user:
        result = {'code': 105, 'error': 'Username or password is wrong!!'}
        return JsonResponse(result)
    user = user[0]
    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        result = {'code': 106, 'error': 'Username or password is wrong!!'}
        return JsonResponse(result)
    # make token
    token = make_token(username).decode()
    result = {'code': 200, 'username': username, 'data': {'token': token}}
    return JsonResponse(result)


def make_token(username, expire=3600 * 24):
    # 官方jwt/自定义jwt
    import jwt
    key = '1234567'
    now = time.time()
    payload = {'username': username, 'exp': int(now + expire)}
    return jwt.encode(payload, key, algorithm='HS256')
