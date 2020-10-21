from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1/v1/users
    url(r'^$', views.users),
]
