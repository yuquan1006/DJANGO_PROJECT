"""old_01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from app_01 import views

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^$', views.index, name='home'),
    re_path('^index/$', views.index, name='home'),
    re_path('^register/$', views.register),
    re_path('^register_action/$', views.register_action),
    re_path('^logout/$', views.logout),
    re_path('^add_event/$', views.add_event),
    re_path('^add_event_action/$', views.add_event_action),
    re_path('^get_event_list/$', views.get_event_list),
    re_path('^add_guest/$', views.add_guest),
    re_path('^logout/$', views.logout),
    re_path('^accounts/login/$', views.index),
    re_path(r'^login_action/$', views.login_action),
    re_path(r'^event_manage/$', views.event_manage),
    re_path(r'^search_name/$', views.search_name),
    re_path(r'^guest_manage/$', views.guest_manage),
    re_path(r'^search_guestName/$', views.search_guestName),
    re_path(r'^sign_index/(?P<event_id>[0-9]+)/$', views.sign_index),     # 配置二级目录，发布会 id，要求必须为数字。而且匹配的数字，将会作为 sign_index()视图函数的参数。
    re_path(r'^sign_index_action/(?P<event_id>[0-9]+)/$', views.sign_index_action),     # 配置二级目录，发布会 id，要求必须为数字。而且匹配的数字，将会作为 sign_index()视图函数的参数。
    re_path(r'^index1/$', views.index2),
    re_path(r'^bye/$', views.bye),
    re_path(r'^apis/$', views.apis),
]
