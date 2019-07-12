from django.test import TestCase
from django.test import Client
from app_01.models import *
from datetime import datetime
from django.contrib.auth.models import User

# Create your tests here.
class TestModel(TestCase):
    '''测试event创建对象是否成功'''
    def setUp(self):
        Event.objects.create(name='测试发布会',status=True,limit=20,address='上海市',strat_time=datetime(2019,6,15,14,0,0))
        print('创建数据')
    # Django 在执行 setUp()方法中的数据库初始化时，并非真正的向数据库表中插入了数据。所以，数据库并不会因为运行测试而产生测试数据。
    # def tearDown(self):
    #     Event.objects.get(name='测试发布会').delete()
    #     print('删除数据')

    def test_event_models(self):
        result = Event.objects.get(name='测试发布会')
        self.assertEqual(result.address,'上海市')
        self.assertTrue(result.status)
        print('测试通过')

class IndexPageTest(TestCase):
    ''' 测试 index 登录首页 '''
    def test_index_page_renders_index_template(self):
        '''测试index视图'''
        response = self.client.get('/')     # client.get()方法从 TestCase 父类继承而来，用于请求一个路径
        self.assertEqual(response.status_code,2300)
        self.assertTemplateUsed(response,'home.html')  # assertTemplateUsed()断言是否用给定的是 home.html 模版响应。


class LoginActionTest(TestCase):
    '''测试登录动作函数'''
    def setUp(self):
        User.objects.create_user("admin","adminemail@qq.com",'admin123456')  # 用 User.objects.create_user()创建登录用户数据。
        self.c = Client()  # Client()类提供的 get()和 post()方法可以模式 GET/POST请求

    def test_loginAction_null(self):
        '''用户名密码为空'''
        test_data = {'username':'','password':""}
        response = self.c.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'用户名或密码错误！',response.content)      # assertIn()断言在返回的 HTML 中包含“usernameor password error!”提示。

    def test_login_action_success(self):
        ''' 登录成功 '''

        test_data = {'username': 'admin','password': 'admin123456'}
        response = self.c.post(' / login_action / ', data=test_data)
        tesself.assertEqual(response.status_code, 302)
