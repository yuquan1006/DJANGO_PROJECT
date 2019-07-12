from django.db import models

# Create your models here.

class Event(models.Model):
    '''发布会表'''
    id = models.AutoField(primary_key=True)  # 发布会id
    name = models.CharField(max_length=100) # 发布会标题
    limit = models.IntegerField() # 参加人数
    status = models.BooleanField() # 状态
    address = models.CharField(max_length=200) #地址
    start_time = models.DateTimeField('event time') # 发布会时间
    create_time = models.DateTimeField(auto_now=True) #创建时间，自动获取

    def __str__(self):
        return self.name

class Guest(models.Model):
    '''嘉宾表'''
    event = models.ForeignKey(Event,to_field='id',default=1,on_delete=models.CASCADE) # 关联发布会id
    realname = models.CharField(max_length=64) # 姓名
    phone = models.CharField(max_length=16) # 手机号
    email = models.EmailField() #
    sign = models.BooleanField()    # 签到状态
    create_time = models.DateTimeField(auto_now=True) #创建时间，自动获取

    class Meta:
        unique_together=("event","phone")


    def __str__(self):
        return self.realname

    '''
    对于产品发布会来说，显然它是一个事件。那么时间、地点、人物等要素必不可少。数据库表的设计需
要围绕着这些要素进行。
关于发布会表（Event 类）和嘉宾表（Guest 类）的每一个字段，在代码中已经做了注解。有些字段的设
计需要做一下简单的说明。
首先，发布会表和嘉宾表中默认都会生成自增 id，而我们在创建模型时不需要声明该字段。
其次，发布会表中增加了 status 字段用于表示发布会的状态是否开启，用于控制该发布会是否可用。
再次，嘉宾表中通过 event_id 关联发布会表，一条嘉宾信息一定所属于某一场发布会。
最后，对于一场发布会来说，一般会选择手机号作为一位嘉宾的验证信息，所以，对于一场发布会来说，
手机号必须是唯一。除了嘉宾 id 外，这里通过发布会 id +手机号来做为联合主键。
    '''