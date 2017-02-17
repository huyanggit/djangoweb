# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


from .models import CourseOrg,CityDict,Teacher
from forms import UserAskForm
from courses.models import Course
from  operation.models import UserFavorite


class OrgView(View):
    """
    课程机构首页
    """
    def get(self,request):
        #统计课程
        all_orgs = CourseOrg.objects.all()
        # 所有城市
        all_city = CityDict.objects.all()

        #课程排名
        hot_org = all_orgs.order_by("click_nums")[:3]

        #取出筛选城市
        city_id = request.GET.get("city",'')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 筛选类别
        category1 = request.GET.get("ct", '')
        if category1:
                all_orgs = all_orgs.filter(catgory=category1)
        #根据学习人数和课程数进行统计
        sort = request.GET.get("sort",'')
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_num")


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs,2, request=request)

        orgs = p.page(page)
        couser_num = all_orgs.count()
        return render(request,"org-list.html",{
            "all_orgs":orgs,
            "all_city":all_city,
            "couser_num":couser_num,
            "city_id":city_id,
            "category1":category1,
            "hot_org":hot_org,
            "sort":sort,
        })


class AddUserAskView(View):
    """
    用户提交咨询
    """
    def post(self,request):

        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask =userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}',content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"数据错误"}',content_type="application/json")


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current_page = "home"
        coures_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=coures_org.id,fav_type=2):
                has_fav =True
        all_coures = coures_org.course_set.all()
        all_teather = coures_org.teacher_set.all()
        return render(request,'org-detail-homepage.html',{
            "all_coures":all_coures,
            "all_teather":all_teather,
            "coures_org":coures_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class OrgCouresView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        current_page = "course"
        coures_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=coures_org.id, fav_type=2):
                has_fav = True
        all_coures = coures_org.course_set.all()

        return render(request,'org-detail-course.html',{
            "all_coures":all_coures,
            "coures_org":coures_org,
            "current_page":current_page,
            "has_fav": has_fav
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self,request,org_id):
        current_page = "desc"
        coures_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=coures_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',{
            "coures_org":coures_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class OrgTeacherView(View):
    """
    机构教师
    """
    def get(self,request,org_id):
        current_page = "teacher"
        coures_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=coures_org.id, fav_type=2):
                has_fav = True
        all_teather = coures_org.teacher_set.all()

        return render(request,'org-detail-teachers.html',{
            "coures_org":coures_org,
            "current_page":current_page,
            "all_teather": all_teather,
            "has_fav": has_fav
        })


class OrgAddFavView(View):
    """
    用户收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        #判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type="application/json")
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type="application/json")
        else:
            uer_fav = UserFavorite()
            if int(fav_id) and int(fav_type) >0 :
                uer_fav.user = request.user
                uer_fav.fav_id = int(fav_id)
                uer_fav.fav_type = int(fav_type)
                uer_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type="application/json")


class TeacherListView(View):
    #课程讲师列表页
    def get(self,request):
        all_tecaher = Teacher.objects.all()

        return render(request,'teachers-list.html',{
            "all_tecaher":all_tecaher
        })
