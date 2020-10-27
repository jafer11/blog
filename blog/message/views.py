from django.shortcuts import render
from django.http import JsonResponse
from tools.login_check import login_check
import json
from .models import Message
from topic.models import Topic


# Create your views here.
@login_check('POST')
def messages(request, topic_id):
    if request.method != 'POST':
        result = {'code': 401, 'error': 'Please use post method'}
        return JsonResponse(result)
    user = request.user
    # 发表留言/回复
    json_str = request.body.decode()
    if not json_str:
        result = {'code': 402, 'error': 'Without data!'}
        return JsonResponse(result)
    json_obj = json.loads(json_str)
    content = json_obj['content']
    if not content:
        result = {'code': 403, 'error': 'Please enter the content!'}
        return JsonResponse(result)
    parent_id = json_obj.get('parent_id', 0)
    try:
        topic = Topic.objects.get(id=topic_id)
    except Exception as e:
        result = {'code': 404, 'error': 'Without topic!!'}
        return JsonResponse(result)
    # 私有博客只能博主留言
    if topic.limit == 'private':
        # 检查身份
        if user.username != topic.author.username:
            result = {'code': 405, 'error': 'You are not blogger, without jurisdiction!!!'}
            return JsonResponse(result)
    Message.objects.create(content=content, parent_message=parent_id,
                           topic=topic, publisher=user, )
    return JsonResponse({'code': 200, 'data': {}})
