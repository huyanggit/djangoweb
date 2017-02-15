# _*_ coding:utf-8 _*_
__author__ = 'Yxs'
__date__ = '2017/2/13 0:51'

from django.conf.urls import url,include
from .views import CourseListView,CourseDetailView


urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    url(r'^detail/(?P<coures_id>\d+)$',CourseDetailView.as_view(),name='course_detail'),

        ]