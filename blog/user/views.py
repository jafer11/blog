from django.shortcuts import render
from django.http import JsonResponse
import json


# Create your views here.

def users(request):
    if request.method == 'GET':
        # 获取用户数据
        pass
        return JsonResponse({'code': 200})
    elif request.method == 'POST':
        # request.POST 只能拿表单提交的数据
        dict = json.loads(request.body)
        # 前端注册页面地址 http://127.0.0.1:5000/register
        # 创建用户
        print(11111)
        return JsonResponse({'code': 200,
                             'username': 'jafer',
                             'data': {'token': 'abcdef'}})
    elif request.method == 'PUT':
        # 更新数据
        pass
    else:
        raise
    return JsonResponse({'code': 200})
