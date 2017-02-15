# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
# Create your views here.

from .forms import LoginForm,RegisterForm,ForgetForm,ResetForm
from .models import UserProfile,EmailVerifyRecord
from utils.email_send import send_register_email


class ForgetPwdView(View):
    def get(self,request):
        forgetform = ForgetForm(request.POST)
        return render(request,"forgetpwd.html",{"forgetform": forgetform})

    def post(self,request):
        forgetform = ForgetForm(request.POST)
        if forgetform.is_valid():
            email = request.POST.get("email","")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forgetform": forgetform})

#找回密码
class ResetView(View):
    def get(self,request,active_code):
        all_recodes = EmailVerifyRecord.objects.filter(code=active_code)
        if all_recodes:
            for recodes in all_recodes:
                email = recodes.email
                return render(request, "password_reset.html",{"email":email})
        else:
            return render(request, "bejing.html")
        return render(request,"login.html")


# 找回密码
class ModifyPwdView(View):
    def post(self,request):
        resetform = ResetForm(request.POST)
        if resetform.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pwd1 !=pwd2:
                return render(request, "password_reset.html", {"email": email,"msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.check_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "resetform":resetform})



class Retrievepassword(View):
    def get(self,request,active_code):
        all_recodes = EmailVerifyRecord.objects.filter(code=active_code)
        if all_recodes:
            for recodes in all_recodes:
                email = recodes.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "bejing.html")
        return render(request,"login.html")

class RegisterViwe(View):
    def get(self,request):
        return render(request,"register.html",{})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            try:
                if UserProfile.objects.get(email=user_name):
                    return render(request, "register.html", {"msg":"用户名已经存在" })
            except UserProfile.DoesNotExist:
                user_password = request.POST.get("password", "")
                user_register = UserProfile()
                user_register.username = 'yxs'
                user_register.email = user_name
                user_register.password = make_password(user_password)
                user_register.save()
                send_register_email(user_name,"register")
                return render(request, "login.html")

        else:
            return render(request, "register.html", {"register_for": register_form})


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username))
            user.check_password(password)
            if user is not None:
                return user
        except EOFError as e:
            return None


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request,"index.html")
                else:
                    return render(request, "login.html",{"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request,"login.html", {"Login_Form": login_form})

