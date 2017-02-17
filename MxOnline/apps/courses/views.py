# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from  operation.models import UserFavorite,CourseComments,UserCourse
from courses.models import CourseResource
from  utils.mixi_utils import LoginRequiredMixin

# Create your views here.


from .models import Course,Video


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


class CourseInfoView(LoginRequiredMixin,View):
    #课程章节页面
    def get(self,request,coures_id):
        couse_it = Course.objects.get(id=int(coures_id))
        couse_it.students +=1
        couse_it.save()
        #查询用户是否已经学习过该课程
        user_course = UserCourse.objects.filter(user=request.user,course=couse_it)
        if not user_course:
            user_course = UserCourse(user=request.user,course=couse_it)
            user_course.save()


        #1、怎么找学过该课程的同学
        user_cousers = UserCourse.objects.filter(course=couse_it)

        #取到所有的学生
        user_ids = [user_course.user.id for user_course in user_cousers]

        #查找所有所有学生学过的课程
        #filter(user_id),是因为user是UserCours的外键
        #filter(user_id__in)是django model的用法

        all_user_couses = UserCourse.objects.filter(user_id__in=user_ids)

        #取出课程所有id
        coures_ids = [user_course.course.id for user_course in all_user_couses]

        #取出课程
        relate_couses = Course.objects.filter(id__in=coures_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=couse_it)
        return render(request,"course-video.html",{
            "couse_it":couse_it,
            "all_resources":all_resources,
            "relate_couses":relate_couses,

        })


class CommentView(LoginRequiredMixin,View):
    #所有的评论
   def get(self,request,coures_id):
       couse_it = Course.objects.get(id=int(coures_id))
       # 1、怎么找学过该课程的同学
       user_cousers = UserCourse.objects.filter(course=couse_it)

       # 取到所有的学生
       user_ids = [user_course.user.id for user_course in user_cousers]

       # 查找所有所有学生学过的课程
       # filter(user_id),是因为user是UserCours的外键
       # filter(user_id__in)是django model的用法

       all_user_couses = UserCourse.objects.filter(user_id__in=user_ids)

       # 取出课程所有id
       coures_ids = [user_course.course.id for user_course in all_user_couses]

       # 取出课程
       relate_couses = Course.objects.filter(id__in=coures_ids).order_by('-click_nums')[:5]
       all_resources = CourseResource.objects.filter(course=couse_it)
       all_comment = CourseComments.objects.all()

       return render(request, "course-comment.html", {
           "all_comment": all_comment,
           "couse_it": couse_it,
           "all_resources": all_resources,
           "relate_couses":relate_couses,


       })


class AddComentsView(View):
    """
    用户提交课程评论
    """
    def post(self,request):

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type="application/json")

        comment = request.POST.get("comments", '')
        coures_id = request.POST.get('course_id', 0)

        if coures_id > 0 and comment:
            user_comment = CourseComments()
            coures = Course.objects.get(id=int(coures_id))
            user_comment.user = request.user
            user_comment.course = coures
            user_comment.comments = comment
            user_comment.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type="application/json")


class ViedoPly(View):
    # 视频播放页面
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        couse_it = video.lesson.course
        couse_it.students += 1
        couse_it.save()
        # 查询用户是否已经学习过该课程
        user_course = UserCourse.objects.filter(user=request.user, course=couse_it)
        if not user_course:
            user_course = UserCourse(user=request.user, course=couse_it)
            user_course.save()

        # 1、怎么找学过该课程的同学
        user_cousers = UserCourse.objects.filter(course=couse_it)

        # 取到所有的学生
        user_ids = [user_course.user.id for user_course in user_cousers]

        # 查找所有所有学生学过的课程
        # filter(user_id),是因为user是UserCours的外键
        # filter(user_id__in)是django model的用法

        all_user_couses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出课程所有id
        coures_ids = [user_course.course.id for user_course in all_user_couses]

        # 取出课程
        relate_couses = Course.objects.filter(id__in=coures_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=couse_it)
        return render(request, "course-play.html", {
            "couse_it": couse_it,
            "all_resources": all_resources,
            "relate_couses": relate_couses,
            "video":video,

        })

