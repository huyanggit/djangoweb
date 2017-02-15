# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from organization.models import CourseOrg

from django.db import models

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name="课程机构",null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name=u"課程名稱")
    desc = models.CharField(max_length=300,verbose_name=u"課程描述")
    detail = models.TextField(verbose_name=u"課程詳情")
    degree = models.CharField(choices=(("cj","初級"),("zj","中級"),("gj","高級")),max_length=10,verbose_name=u"课程难度")
    learn_times = models.IntegerField(default=0,verbose_name=u"學習時常（分鐘數）")
    students = models.IntegerField(default=0,verbose_name=u"學習人數")
    fav_nums = models.IntegerField(default=0,verbose_name=u"收藏數")
    image = models.ImageField(upload_to="image/%Y%m",default="image/",verbose_name=u"封面图",max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course =models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    download = models.FileField(upload_to="course/resource/%Y/%m",verbose_name=u"下载")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/m",verbose_name=u"资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name