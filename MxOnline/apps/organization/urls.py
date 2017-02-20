# _*_ coding:utf-8 _*_
from django.conf.urls import url,include
from .views import OrgView,AddUserAskView,OrgHomeView,OrgCouresView,OrgDescView,OrgTeacherView,OrgAddFavView,TeacherListView
from .views import TeacherDetilView
urlpatterns = [
    #课程机构首页
    url(r'^list/$',OrgView.as_view(),name='orgliste'),
    url(r'^add_ask/$',AddUserAskView.as_view(),name='add_ask1'),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$',OrgCouresView.as_view(),name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name='org_teacher'),
    #机构收藏
    url(r'^add_fav/$',OrgAddFavView.as_view(),name='add_fav'),
    #讲师
    url(r'^teacher/$', TeacherListView.as_view(), name='teacherlist'),
    # 讲师相关 URL 配置
    url(r'^techaer/detei(?P<teacher_id>.*)/$', TeacherDetilView.as_view(), name="techaerdetai"),

]