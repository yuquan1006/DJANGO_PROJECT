#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from app_01.models import Event,Guest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.urls import reverse
from datetime import datetime
import time
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request):
    '''首页'''
    return render(request,"app_01/home.html") # 返回html页面

def register(request):
    '''注册页面'''
    return render(request,'app_01/register.html')
def register_action(request):
    '''注册动作'''
    try:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            user = User.objects.create_user(username=username, password=password, email=email)
            if user:
                print('注册成功！')
                return render(request,'app_01/register_sucess.html',{'username':username})
            else:
                print('注册失败！', e)
                return render(request,'app_01/register.html',{'hint':'注册失败，请重新尝试'})
    except BaseException as e:
        print('注册失败',e)
        return render(request, 'app_01/register.html', {'hint': '注册失败，请重新尝试'})


def login_action(request):
    '''登录动作'''
    # print(request.method)
    if request.method=='POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password) #authenticate()函数认证给出的用户名和密码。正确返回一个 user 对象，不正确返回None
        if user is not None:
            auth.login(request,user) # 登录
            response = HttpResponseRedirect('/event_manage/')
            request.session['user']=username # 将session信息记录到浏览器
            return response
        # if username=='admin' and password=='123456':
        #     print('登录成功！')
        #     # return render(request,"event_manage.html",{'username':username})
        #     # return HttpResponseRedirect('/event_manage/')
        #     response = HttpResponseRedirect('/event_manage/')
        #     # response.set_cookie('user',username,3600) # 添加浏览器cookie
        #     request.session['user']=username # 将session信息记录到浏览器
        #     return response
        else:
            print('登录失败！')
            return render(request,'app_01/home.html',{'error':'用户名或密码错误！'})
    return render(request, 'app_01/home.html', {'error': '请求方法错误！'})

@login_required # 限制某个视图函数必须登录才能访问，只需要在这个函数的前面加上@login_required 即可。
def event_manage(request):
    '''登录成功页面'''
    # username = request.COOKIES.get('user') # 读取浏览器cookie
    username = request.session.get('user') # 读取浏览器session
    # 查询全部发布会信息
    eventList = Event.objects.all()

    return render(request,'app_01/event_manage.html',{'username':username,'events':eventList})

@login_required()
def search_name(request):
    '''发布会搜索页面'''
    username = request.session.get('user')
    search_name = request.GET.get('name')
    event_list = Event.objects.filter(name__contains=search_name)
    return  render(request,'app_01/event_manage.html',{'username':username,'events':event_list})

@login_required()
def add_event(request):
    return render(request,'app_01/add_event.html')
@login_required()
def add_event_action(request):
    '''添加发布会接口'''
    eid = request.POST.get('id')
    name = request.POST.get('name')
    limit = request.POST.get('limit')
    address = request.POST.get('address')
    status = request.POST.get('status')
    start_time = request.POST.get('start_time')
    # 检查必填字段是否为空
    if eid== '' or name=='' or limit=='' or address==''  or start_time=='':
        return JsonResponse({'status':10021,'message':'parametererror'})    # JsonResponse 它可以直接将字典转化成Json格式返回到客户端

    # 检查eid,name是否已经存在
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status':10022,'message':'eventid alreadyexists'})
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status':10023,'message':'eventname alreadyexists'})
    if status==None:
        status=1
    try:
        Event.objects.create(id=eid,name=name,limit=int(limit),address=address,status=status,start_time=start_time)
    except ValidationError as e:
        error='start_timeformaterror.ItmustbeinYYYY-MM-DDHH:MM:SSformat.'
        return JsonResponse({'status':10024,'message':error})
    except ValueError as e:
        print(e)
        return JsonResponse({'status':10021,'message':'parametererror'})
    except BaseException as e:
        print(e)
        return JsonResponse({'status':10021,'message':'parametererror'})
    return JsonResponse({"status":"200",'message':'success'})

# @login_required()
def get_event_list(request):
    '''查询发布会接口 id，name 非必填'''
    # 查询参数
    eid = request.GET.get('id','')     # 发布会id
    name = request.GET.get('name','') # 发布会名
    if eid =='' and name =='':
        return JsonResponse({'status':10021,"message":'parametererror'})
    if eid != '':
        event={}
        try:
            print(eid)
            result = Event.objects.get(id=eid)
            print(result.limit)
        except ObjectDoesNotExist as e:
            return JsonResponse({'status':10022,'message':'queryresultisempty'})
        else:
            event['id'] = result.id
            event['name'] = result.name
            event['limit'] = result.limit
            event['address'] = result.address
            event['status'] = result.status
            event['start_time'] = result.start_time
            return JsonResponse({'status':200,'message':'success','data':event})
    if name != '':
        datas=[]
        results = Event.objects.filter(name__contains=name)
        if results:
            for result in results:
                event={}
                event['name'] = result.name
                event['limit'] = result.limit
                event['address'] = result.address
                event['status'] = result.status
                event['start_time'] = result.start_time
                datas.append(event)
            return JsonResponse({'status':200,'message':'success','data':datas})
        else:
            return JsonResponse({'status':10022,'message':'queryresultisempty'})

# @login_required()
@csrf_exempt    # 取消csrf认证
def add_guest(request):
    '''添加嘉宾'''
    # 获取请求参数
    event_id = request.POST.get('event_id','')
    realname = request.POST.get('realname','')
    phone = request.POST.get('phone','')
    email = request.POST.get('email','')
    sign = request.POST.get('sign','')
    # 检查必填参数
    if event_id =='' or realname=='' or phone=='' or email=='' or sign=='':
        return JsonResponse({'status': 10021, "message": 'parametererror'})
    # 检查event_id是否存在及发布会状态
    result = Event.objects.filter(id=event_id)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event_id 关联不到发布会'})
    result = Event.objects.get(id=event_id).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not true'})
    # 检查发布会人数是否已满
    event_limit = Event.objects.get(id=event_id).limit # 发布会限制人数
    guest_limit = len(Guest.objects.filter(event_id=event_id)) # 发布会已添加人数
    print(guest_limit,event_limit)
    if guest_limit>=int(event_limit):
        return JsonResponse({'status': 10024, 'message': 'eventnumberisfull'})
    # 检查发布会时间
    event_time = Event.objects.get(id=event_id).start_time
    print(event_time)
    # #转化为数组
    timeArray = time.strptime(str(event_time),"%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    e_time = int(time.mktime(timeArray)) # 1524822540
    # 获取当前时间戳
    now_time=str(time.time()) # 1560928025.8670208
    # 去掉后部分
    now_time = now_time.split('.')[0]  # 1560928025
    n_time = int(now_time)
    if n_time>e_time:
        return JsonResponse({'status': 10024, 'message': 'eventhasstarted'})
    try:
        Guest.objects.create(event_id=event_id,realname=realname,sign=sign,phone=phone,email=email)
    except IntegrityError:  # 发布会的手机号重复则抛IntegrityError异常
        return JsonResponse({'status':'the event guest phonenumber repeat'})
    return JsonResponse({"status":200,"message":"add guest success"})

@login_required()
def guest_manage(request):
    '''嘉宾管理'''
    username = request.session.get('user')
    guest_list=Guest.objects.all().order_by('event_id')
    paginator = Paginator(guest_list,4) # 把查询出来的所有嘉宾列表 guest_list 放到 Paginator 类中，划分每页显示 2 条数据。
    page = request.GET.get('page')          # 通过 GET 请求得到当前要显示第几页的数据。
    try:
        contacts = paginator.page(page) # 获取第 page 页的数据（对象列表）
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.# If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages) # 返回最后一页面的数据。
    return render(request,"app_01/guest_manage.html",{'username':username,'guests':contacts})

@login_required()
def search_guestName(request):
    '''嘉宾搜索页面'''
    username = request.session.get('user')
    search_guestName = request.GET.get('name')
    print(search_guestName)
    guest_list = Guest.objects.filter(realname__contains=search_guestName).order_by('event_id')
    paginator = Paginator(guest_list, 4)
    page = request.GET.get('page')          # 通过 GET 请求得到当前要显示第几页的数据。
    try:
        contacts = paginator.page(page)  # 获取第 page 页的数据（对象列表）
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.# If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  # 返回最后一页面的数据。

    return  render(request,'app_01/guest_manage.html',{'username':username,'guests':contacts,'search_guestName':search_guestName})

@login_required
def sign_index(request,event_id):
    '''签到页面'''
    event = get_object_or_404(Event, id=event_id) # 默认的调用django 的get方法， 如果查询的对象不存在的话，会抛出一个Http404的异常
    return render(request, 'app_01/sign_index.html', {'event': event})

@login_required()
def sign_index_action(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    phone = request.POST.get('phone')
    result = Guest.objects.filter(phone=phone)  # 查询 Guest 表判断用户输入的手机号是否存在，如果不存在将提示用户“手机号为空或不存在”。
    if not result:
        return render(request,'app_01/sign_index.html',{'event':event,'hint':'phone error'})
    result =Guest.objects.filter(event_id=event_id,phone=phone)     #通过手机和发布会 id 两个条件来查询 Guest 表，如果结果为空将提示用户“该用户未参加此次发布会
    if not result:
        return render(request,'app_01/sign_index.html',{'event':event,'hint':'event id or phone error'})
    result =Guest.objects.get(event_id=event_id,phone=phone)    # 再通过手机号查询 Guest 表，判断该手机号的签到状态是否为 1，如果为 1，表示已经签过到了，返回用户“已签到”，否则，将提示用户“签到成功！”，并返回签到用户的信息
    if result.sign:
        return render(request,'app_01/sign_index.html',{'event':event,'hint':'user has sign in'})
    else:
        result.sign = True
        result.save()
        return render(request,'app_01/sign_index.html',{'event':event,'hint':'sign sucessful!','guests':result})

def logout(request):
    auth.logout(request) #退出登录
    # response = HttpResponseRedirect('/index/')
    response = HttpResponseRedirect(reverse('home'))    # urls.py中的name参数应用
    return response
def index2(request):
    print(Event.objects.create())
    return HttpResponse("返回字符串数据")  # 返回字符串

def bye(request):
    return render(request,"app_01/bye.html")


@csrf_exempt    # 取消csrf认证
def apis(request):
    print("hello input") # p={"word":"data"}
    # #查看客户端发来的请求,前端的数据
    print(request.POST)
    print("request.body={}".format(request.body))
    print(type(json.loads(request.body.decode())))
    # #返回给客户端的数据
    result="success"
    if request.method=="POST":
        print(request.POST)
    return JsonResponse({"status": 200, "msg": "OK","data": result})
