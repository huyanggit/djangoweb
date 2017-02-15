# _*_ coding:utf-8 _*_
__author__ = 'Yxs'
__date__ = '2017/1/8 22:06'
import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc','add_time']
    search_fields =['name', 'desc']
    list_filter = ['name', 'desc','add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc','click_nums','fav_nums','address','city','add_time']
    search_fields = ['name', 'desc','click_nums','fav_nums','address','city']
    list_filter = ['name', 'desc','click_nums','fav_nums','address','city__name','add_time']


class TeacherAdmin(object):
    list_display = ['name', 'work_years','work_company','click_nums','fav_nums','add_time']
    search_fields = ['name', 'work_years','work_company','click_nums','fav_nums']
    list_filter = ['name', 'work_years','work_company','click_nums','fav_nums','add_time']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)

