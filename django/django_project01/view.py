#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 15:55
# @Author  : Yuquan
# @Site    : 
# @File    : view.py
# @Software: PyWCharm
'''
每个view函数的第一个参数是一个HttpRequest对象
HttpRequest对象包含当前请求URL的一些信息：
path         请求页面的全路径
method       请求中使用的HTTP方法的字符串表示
GET         包含所有HTTP GET参数的类字典对象
POST        包含所有HTTP POST参数的类字典对象
COOKIES     包含所有cookies的标准Python字典对象。Keys和values都是字符串
META        包含所有可用HTTP头部信息的字典
FILES       包含所有上传文件的类字典对象。FILES中的每个Key都是<input type="file" name="" />标签中name属性的值. FILES中的每个value 同时也是一个标准Python字典对象，包含下面三个Keys:
            filename: 传文件名,用Python字符串表示
            content-type: 上传文件的Content type
            content: 上传文件的原始内容

HttpRequest对象的方法
has_key()	检查request.GET or request.POST中是否包含参数指定的Key。
get_full_path()	    返回包含查询字符串的请求路径。例如， "/music/bands/the_beatles/?print=true"
is_secure()	        发出的是HTTPS请求
'''
import time,datetime

from django.http import HttpResponse
from django.shortcuts import render

r_data = {"username":'yuquan'}

def index(request):
    if request.method == 'post':
        username = request.POST.get("username", None)
        passwd = request.POST.get("passwd", None)
        print(username, passwd)
        print(request.POST.path)
    return render(request, "index.html",r_data)

def hello(request):
    context ={}
    context['hello'] = "hell world!"
    return render(request,'hello.html',context)

def current_time(request):
    '''返回当前时间'''
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    html = "<html><body><H1>It is now %s.</H1></body></html>"% now
    return HttpResponse(html)

def hours_ahead(request,offset):
    '''计算当前几个小时前时间'''
    try:
        offset = int(offset)    # offset是从urls中地址中获取的参数
    except ValueError:
        raise Http404()

    dt = datetime.datetime.now()-datetime.timedelta(hours=offset)
    html ="<html><body><H1>It is now %s.</H1></body></html>"% dt
    return HttpResponse(html)