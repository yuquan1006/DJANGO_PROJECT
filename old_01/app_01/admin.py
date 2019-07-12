from django.contrib import admin
from app_01.models import Event,Guest

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['id','name','status','limit','address','start_time']  # 自定义显示字段
    search_fields = ['name','status']   # 搜索栏
    list_filter = ['status'] # 过滤器

class GuestAdmin(admin.ModelAdmin):
    list_display = ['event','realname','phone','email','sign']


admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)  # s这些代码通知 admin 管理工具为这些模块逐一提供界面。