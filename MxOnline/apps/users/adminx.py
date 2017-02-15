# _*_ coding:utf-8 _*_
__author__ = 'Yxs'
__date__ = '2017/1/8 19:29'
import xadmin
from xadmin import views


from .models import UserProfile
from .models import EmailVerifyRecord,Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "慕学后台管理"
    site_footer = "慕学在线网"
    menu_style = "accordion"

class UserProfileAdmin(object):
    list_display = ['nick_name', 'gender', 'address', 'mobile']
    search_fields = ['nick_name', 'gender', 'address', 'mobile']
    list_filter = ['nick_name', 'gender', 'address', 'mobile', ]


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)