"""django_project01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path

from . import view
from django_project01.testdb import *
from django_project01.search import *
from django_project01.search02 import *
# 路由配置

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^index/$', view.index),
    re_path(r'^[A-Z]hello/$', view.hello),
    re_path(r'^time/$', view.current_time),
    re_path(r'^time/(\d{1,2})/$', view.hours_ahead),        # ()正则表达式也是用圆括号来从文本里提取数据的
    re_path(r'^testdb_insert/$',testdb_insert),
    re_path(r'^testdb_select/$',testdb_select),
    re_path(r'^testdb_update/$',testdb_update),
    re_path(r'^testdb_delete/$',testdb_delete),
    re_path(r'^search/$',search),
    re_path(r'^search_form/$',search_form),
    re_path(r'^search_post/$',search_post),
]
