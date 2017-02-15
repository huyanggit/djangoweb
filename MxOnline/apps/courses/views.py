# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


from .models import Course

class CourseListView(View):
    def get(self,request):
        all_course = Course.objects.all()
        #热门课程推荐
        hot_course = all_course.order_by("click_nums")[:3]

        # 课程排序
        sort = request.GET.get("sort", '')
        if sort == "students":
            all_course = all_course.order_by("-students")
        elif sort == "hot":
            all_course = all_course.order_by("-click_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_course,3, request=request)

        couses = p.page(page)

        return render(request,'course-list.html',{
            "all_course":couses,
            "sort":sort,
            "hot_course":hot_course,


        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self,request,coures_id):

        return render(request,'course-detail.html',{})