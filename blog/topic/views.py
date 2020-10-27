from django.shortcuts import render
from django.http import JsonResponse

from message.models import Message
from tools.login_check import login_check, get_user_by_request
import json
from .models import Topic
from user.models import UserProfile


# Create your views here.
@login_check('POST', 'DELETE')
def topics(request, author_id):
    if request.method == 'GET':
        # 获取用户数据
        # author 博主
        authors = UserProfile.objects.filter(username=author_id)
        if not authors:
            result = {'code': 308, 'error': 'no author'}
            return JsonResponse(result)
        # 取出结果中的博主
        author = authors[0]

        # visitor
        visitor = get_user_by_request(request)
        visitor_name = None
        if visitor:
            visitor_name = visitor.username
        t_id = request.GET.get('t_id')
        if t_id:
            # 当前是否为博主自己访问自己
            is_self = False
            # 获取文章详情页
            t_id = int(t_id)
            if author_id == visitor_name:
                is_self = True
                # 博主访问自己的博客
                try:
                    author_topic = Topic.objects.get(id=t_id)
                except Exception as e:
                    result = {'code': 312, 'error': 'Without this topic'}
                    return JsonResponse(result)
            else:
                # 访客访问博主博客
                try:
                    author_topic = Topic.objects.get(id=t_id, limit='public')
                except Exception as e:
                    result = {'code': 313, 'error': 'Without this topic!'}
                    return JsonResponse(result)
            res = make_topic_res(author, author_topic, is_self)
            # print('-------------------------------------')
            # print(res)
            # print(type(res))
            return JsonResponse(res)
        else:
            # h获取文章列表
            category = request.GET.get('category')
            if category in ['tec', 'no-tec']:
                # v1/topics/<author_id>?category=[tec | no-tec]
                if author_id == visitor_name:
                    # 当前博主访问自己的博客 获取全部博客数据

                    topics = Topic.objects.filter(author_id=author_id, category=category)
                else:
                    # 非博主
                    topics = Topic.objects.filter(author_id=author_id, limit='public', category=category)
            else:
                # v1/topics/<author_id> 用户全量数据
                if author_id == visitor_name:
                    # 当前博主访问自己的博客 获取全部博客数据

                    topics = Topic.objects.filter(author_id=author_id)
                else:
                    # 非博主
                    topics = Topic.objects.filter(author_id=author_id, limit='public')
            res = make_topics_res(author, topics)
            return JsonResponse(res)
    elif request.method == 'POST':
        # 创建用户博客数据
        # request.POST只能那表单数据，而django提交过来的不是表单提交
        # 只能用request.body来拿传过来的参数
        json_str = request.body.decode()
        if not json_str:
            result = {'code': 301, 'error': 'Without json data'}
            return JsonResponse(result)
        json_boj = json.loads(json_str)
        title = json_boj.get('title')
        # xss注入 将input输入框的含有JS脚本的语义转为文本
        import html
        title = html.escape(title)
        if not title:
            result = {'code': 302, 'error': 'Please enter title'}
            return JsonResponse(result)
        content = json_boj.get('content')
        if not content:
            result = {'code': 303, 'error': 'Please enter the eontent'}
            return JsonResponse(result)
        # 获取纯文本内容， 用于切割文章简介
        content_text = json_boj.get('content_text')
        if not content_text:
            result = {'code': 304, 'error': 'Please enter content_text'}
            return JsonResponse(result)
        # 切割简介
        introduce = content_text[:30]
        limit = json_boj.get('limit')
        if limit not in ['public', 'private']:
            result = {'code': 305, 'error': 'Your limit is wrong'}
            return JsonResponse(result)
        category = json_boj.get('category')
        if category not in ['tec', 'no-tec']:
            result = {'code': 303, 'error': 'Please choose category'}
            return JsonResponse(result)

        # 创建数据
        Topic.objects.create(title=title, category=category,
                             limit=limit, content=content,
                             introduce=introduce,
                             author=request.user)
        result = {'code': 200, 'username': request.user.username}
        return JsonResponse(result)
    elif request.method == 'DELETE':
        # 先获取传过来的参数
        # token存储的用户
        author = request.user
        token_author_id = author.username
        # url 床过来的_id 必须与token中欧给你的用户名相等
        if author_id != token_author_id:
            result = {'code': 309, 'error': "You can't delete it"}
            return JsonResponse(result)
        topic_id = request.GET.get('topic_id')
        try:
            topic = Topic.objects.get(id=topic_id)
        except:
            result = {'code': 310, 'error': 'You can not delete it!'}
            return JsonResponse(result)
        #  先检查再删除
        if topic.author.username != author_id:
            result = {'code': 311, 'error': "You can't delete it!!"}
            return JsonResponse(result)
        topic.delete()
        res = {'code': 200}
        return JsonResponse(res)


def make_topics_res(author, topics):
    res = {'code': 200, 'data': {}}
    data = {}
    data['nickname'] = author.nickname
    topics_list = []
    for topic in topics:
        d = {}
        d['id'] = topic.id
        d['title'] = topic.title
        d['category'] = topic.category
        d['introduce'] = topic.introduce
        d['author'] = author.nickname
        d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
        topics_list.append(d)
    data['topics'] = topics_list
    res['data'] = data
    return res


def make_topic_res(author, author_topic, is_self):
    """
    拼接详情页 返回数据
    :param author:
    :param author_topic:
    :param is_self:
    :return:
    """
    if is_self:
        # 博主访问自己博客
        # 下一篇文章，取出ID大于当前博客ID的第一个，且author为当前作者的
        next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author).first()
        # 上一篇文章 ， 取出ID小于当前博客ID的最后一个，且author为当前作者的
        last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author).last()
    else:
        # 访客访问博主的
        # 下一篇
        next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author, limit='public').first()
        # 上一篇
        last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author, limit='public').last()

    if next_topic:
        next_id = next_topic.id
        next_title = next_topic.title
    else:
        next_id = None
        next_title = None
    if last_topic:
        last_id = last_topic.id
        last_title = last_topic.title
    else:
        last_id = None
        last_title = None

    all_messages = Message.objects.filter(topic=author_topic).order_by('-created_time')
    # 所有的留言
    msg_list = []
    # 留言&回复的映射字典
    msg_count = 0
    reply_dict = {}
    for msg in all_messages:
        msg_count += 1
        if msg.parent_message == 0:
            # parent_message=0 当前是留言
            msg_list.append({'id': msg.id, 'content': msg.content,
                             'publisher': msg.publisher.nickname,
                             'publisher_avatar': str(msg.publisher.avatar),
                             'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                             'reply': []
                             })
        else:
            # 当前是回复
            reply_dict.setdefault(msg.parent_message, [])
            reply_dict[msg.parent_message].append({
                'msg_id': msg.id, 'content': msg.content,
                'publisher': msg.publisher.nickname,
                'publisher_avatar': str(msg.publisher.avatar),
                'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            })
    # 合并 msg_list 和 reply_dict
    for _msg in msg_list:
        if _msg['id'] in reply_dict:
            _msg['reply'] = reply_dict[_msg['id']]

    res = {'code': 200, 'data': {}}
    res['data']['nickname'] = author.nickname
    res['data']['title'] = author_topic.title
    res['data']['category'] = author_topic.category
    res['data']['created_time'] = author_topic.created_time.strftime('%Y-h%-%d %H:%M:%S')
    res['data']['content'] = author_topic.content
    res['data']['introduce'] = author_topic.introduce
    res['data']['author'] = author.nickname
    res['data']['next_id'] = next_id
    res['data']['next_title'] = next_title
    res['data']['last_id'] = last_id
    res['data']['last_title'] = last_title
    # messages 暂时为假数据
    res['data']['messages'] = msg_list
    res['data']['messages_count'] = msg_count

    return res
