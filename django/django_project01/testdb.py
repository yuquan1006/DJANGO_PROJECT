#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/10 15:10
# @Author  : Yuquan
# @Site    : 
# @File    : testdb.py
# @Software: PyCharm
from django.http import HttpResponse
from TestModel.models import Test

# 数据库操作


# 1 新增
def testdb_insert(request):
    test1 = Test(name="w3cschool.cn")
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")

# 2 查询
def testdb_select(request):
    response = ''
    response_01 = ''
    # # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    # list = Test.objects.all()
    # for var in list:
    #     response += str(var.id) + " "  # 获取Test表中全部name字段然后拼接
    #     response_01 += var.name + " "

    # 获取单个对象  单个对象即可通过 a.字段获取单个字段值
    # response2 = Test.objects.get(id=3)

    #
    # # filter相当于SQL中的WHERE，可设置条件过滤结果
    # response1 = Test.objects.filter(id=3).get(id=3)
    #
    # # 数据排序
    # response3 = Test.objects.order_by("id").get(id=2)
    #
    #  # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    # response4 = Test.objects.order_by('id')[0:1].first()
    #
    # #  # 上面的方法可以连锁使用
    response5 = Test.objects.filter(id=3).order_by("id")[0:1].first()


    return HttpResponse("<p>查询数据：%s</p>"% response5.name)

# 更新数据
def testdb_update(request):
    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    # test1 = Test.objects.get(id=2)
    # test1.name = 'update——'
    # test1.save()

    # 第二种
    Test.objects.filter(id=1).update(name='update_02')

    # 修改所有的列
    # Test.objects.all().update(name='w3cschoolW3Cschool教程')
    return HttpResponse("修改数据成功！")

def testdb_delete(request):
    # 删除id=1的数据
    test1 = Test.objects.get(id=4)
    test1.delete()
    # 另外一种方式
    # Test.objects.filter(id=1).delete()
    # 删除所有数据
    # Test.objects.all().delete()

    return HttpResponse("删除数据成功")