# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from  operation.models import UserFavorite,CourseComments
from courses.models import CourseResource

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
        couse_it = Course.objects.get(id=int(coures_id))
        couse_it.click_nums += 1
        couse_it.save()
        tag = couse_it.tag

        if tag:
            relate_courses = Course.objects.filter(tag=tag)

        else:
            relate_courses = []

        #课程收藏和机构收藏
        has_fav_course =False
        has_fav_org = False
        # 判断用户登录状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=couse_it.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=couse_it.course_org_id, fav_type=2):
                has_fav_org = True
        return render(request,'course-detail.html',{
            "couse_it":couse_it,
            "relate_courses":relate_courses,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org,
        })


class CourseInfoView(View):
    #课程章节页面
    def get(self,request,coures_id):
        couse_it = Course.objects.get(id=int(coures_id))
        all_resources = CourseResource.objects.filter(course=couse_it)
        return render(request,"course-video.html",{
            "couse_it":couse_it,
            "all_resources":all_resources,

        })

class CommentView(View):
    #课程评论页面
   def get(self,request,coures_id):
       couse_it = Course.objects.get(id=int(coures_id))
       all_resources = CourseResource.objects.filter(course=couse_it)
       all_comment = CourseComments.objects.all()

       return render(request, "course-comment.html", {
           "all_comment": all_comment,
           "couse_it": couse_it,
           "all_resources": all_resources,

       })


class AddComentsView(View):
    pass