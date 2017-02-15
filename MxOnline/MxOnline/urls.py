# _*_ coding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import LoginView,RegisterViwe,Retrievepassword,ForgetPwdView,ResetView,ModifyPwdView
import xadmin
from organization.views import OrgView
from settings import MEDIA_ROOT



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',TemplateView.as_view(template_name="index.html"),name="index"),
    url(r'^login/$', LoginView.as_view(), name="userlogin"),
    url(r'^register/$', RegisterViwe.as_view(), name="registe"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',Retrievepassword.as_view(),name="retrievepassword"),
    url(r'^forget/$',ForgetPwdView.as_view(),name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name="resetview"),
    url(r'^modifypwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    #课程机构首页
    url(r'^org/',include('organization.urls',namespace='org_list')),
    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)/$',serve,{"document_root":MEDIA_ROOT}),

    #课程相关的url配置
    url(r'^course/',include('courses.urls',namespace='course')),




]
