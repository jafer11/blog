from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1/v1/users
    url(r'^$', views.users),
    #APPEND_SLASH 自动不全url后面的斜线
    url(r'^/(?P<username>[\w]{1,11})$', views.users),
    url(r'^/(?P<username>[\w]{1,11}/avatar)$', views.user_avatar),
]
