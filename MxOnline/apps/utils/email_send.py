# _*_ encoding:utf-8 _*_
from django.views.generic.base import View
from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail


from MxOnline.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    e_code = random_str(9)
    email_record.code = e_code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "幕学在线网注册激活链接"
        email_body = "点击一下链接激活http://127.0.0.1:8000/active/{0}".format(e_code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == "forget":

        email_title = "幕学在线网修改密码连接"
        email_body = "点击连接修改密码http://127.0.0.1:8000/reset/{0}".format(e_code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass