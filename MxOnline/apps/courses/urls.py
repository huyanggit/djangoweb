# _*_ coding:utf-8 _*_
__author__ = 'Yxs'
__date__ = '2017/2/13 0:51'

from django.conf.urls import url,include
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentView


urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    #课程详情页
    url(r'^detail/(?P<coures_id>\d+)$',CourseDetailView.as_view(),name='course_detail'),
    #课程视频列表
    url(r'^video/(?P<coures_id>\d+)$',CourseInfoView.as_view(),name='course_info'),
    #课程视频列表
    url(r'^comment/(?P<coures_id>\d+)$',CommentView.as_view(),name='course_comment'),
        ]