# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from organization.models import CourseOrg,Teacher

from django.db import models

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name="课程机构",null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name=u"課程名稱")
    category =models.CharField(default=u"后端开发",max_length=20,verbose_name=u"课程类别")
    desc = models.CharField(max_length=300,verbose_name=u"課程描述")
    detail = models.TextField(verbose_name=u"課程詳情")
    teacher = models.ForeignKey(Teacher, verbose_name=u"关联教师", null=True, blank=True)
    degree = models.CharField(choices=(("cj","初級"),("zj","中級"),("gj","高級")),max_length=10,verbose_name=u"课程难度")
    learn_times = models.IntegerField(default=0,verbose_name=u"學習時常（分鐘數）")
    students = models.IntegerField(default=0,verbose_name=u"學習人數")
    fav_nums = models.IntegerField(default=0,verbose_name=u"收藏數")
    image = models.ImageField(upload_to="image/%Y%m",default="image/",verbose_name=u"封面图",max_length=100)
    tag = models.CharField(default="",verbose_name=u"关键词",max_length=20)
    click_nums = models.IntegerField(default=0,verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")
    course_need = models.CharField(default='',verbose_name=u"课程须知",max_length=200,null=True,blank=True)
    teacher_tell = models.CharField(default='', verbose_name=u"老师告诉", max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = u"课程表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_zj_nums(self):
        #获取章节数
        return self.lesson_set.all().count()
    def get_learn_user(self):
        #取出学习用户
        return self.usercourse_set.all()[:5]
    def get_course_lesson(self):
        #获取章节数量
        return self.lesson_set.all()

    def get_course_teacher(self):
        # 获取章节数量
        return self.tea.all()


class Lesson(models.Model):
    course =models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def get_leeson_viedo(self):
        # 获取章节视频
        return self.video_set.all()

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(max_length=200,default='',verbose_name=u"下载地址")
    learn_times = models.IntegerField(default=0, verbose_name=u"學習時常（分鐘數）")
    download = models.FileField(upload_to="course/resource/%Y/%m",verbose_name=u"下载")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/m",verbose_name=u"资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name