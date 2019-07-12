#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11 9:36
# @Author  : Yuquan
# @Site    : 
# @File    : search02.py
# @Software: PyCharm
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import csrf


def search_post(requests):
    ctx = {}
    ctx.update(csrf(requests))
    if requests.POST:
        ctx['rlt'] = requests.POST['q']
    return render(requests,"post.html",ctx)
