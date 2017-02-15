# _*_ coding:utf-8 _*_
from django import forms
from operation.models import UserAsk
import re


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    def clean_mobile(self):
        mobie = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p =re.compile(REGEX_MOBILE)
        if p.match(mobie):
            return mobie
        else:
            raise forms.ValidationError(u"手机号码错误",code="mobie_invalid")