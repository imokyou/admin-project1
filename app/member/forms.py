# coding=utf8
from django import forms
from django.forms import TextInput, Textarea
from django.contrib.auth.models import User as Auth_user
from captcha.fields import CaptchaField  


class ChatForm(forms.Form):
    username = forms.CharField(max_length=64,
                               min_length=4,
                               required=True,
                               widget=TextInput(
                                   attrs={'placeholder': 'username...'}),
                               error_messages={'required': '收件人不能为空'})
    title = forms.CharField(max_length=256,
                            required=True,
                            widget=TextInput(
                                attrs={'placeholder': 'title...'}),
                            error_messages={'required': '标题不能为空'})
    message = forms.CharField(required=True,
                              widget=Textarea(
                                attrs={'placeholder': 'message...'}),
                              error_messages={'required': '内容不能为空'})

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != 'company':
            u = Auth_user.objects.filter(username=username).first()
            if not u:
                raise forms.ValidationError("用户不存在")
        return username


class EnChatForm(forms.Form):
    username = forms.CharField(max_length=64,
                               min_length=4,
                               required=True,
                               widget=TextInput(
                                   attrs={'placeholder': 'username...'}))
    title = forms.CharField(max_length=256,
                            required=True,
                            widget=TextInput(
                                attrs={'placeholder': 'title...'}))
    message = forms.CharField(required=True,
                              widget=Textarea(
                                attrs={'placeholder': 'message...'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        u = Auth_user.objects.filter(username=username).first()
        if not u:
            raise forms.ValidationError("username not exists")


class ChangeRecommendForm(forms.Form):
    username = forms.CharField(max_length=64,
                               min_length=4,
                               required=True,
                               error_messages={'required': '用户名不能为空'},
                               widget=TextInput(
                                   attrs={'placeholder': '请输入用户名...'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        u = Auth_user.objects.filter(username=username).first()
        if not u:
            raise forms.ValidationError("用户不存在")
        return username


class ChangePwdForm(forms.Form):
    password = forms.CharField(max_length=64,
                               min_length=4,
                               required=True,
                               widget=forms.PasswordInput(),
                               error_messages={'required': '旧密码不能为空'})
    new_password = forms.CharField(max_length=64,
                                   min_length=4,
                                   required=True,
                                   widget=forms.PasswordInput(),
                                   error_messages={'required': '新密码不能为空'})
    cnew_password = forms.CharField(max_length=64,
                                    min_length=4,
                                    required=True,
                                    widget=forms.PasswordInput(),
                                    error_messages={'required': '确认密码不能为空'})

class EnChangePwdForm(forms.Form):
    password = forms.CharField(max_length=64,
                               min_length=4,
                               required=True,
                               widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=64,
                                   min_length=4,
                                   required=True,
                                   widget=forms.PasswordInput())
    cnew_password = forms.CharField(max_length=64,
                                    min_length=4,
                                    required=True,
                                    widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(EnChangePwdForm, self).clean()
        new_password = cleaned_data.get("new_password")
        cnew_password = cleaned_data.get("cnew_password")

        if new_password != cnew_password:
            msg = "两次密码输入不一致"
            self.add_error('new_password', msg)
            self.add_error('cnew_password', msg)
        return cleaned_data


class ChangeUserInfoForm(forms.Form):
    pass


class WithDrawForm(forms.Form):
    PAY_TYPE = [
      ('CSPAY', '银联'),
      ('BITCOIN', '比特币'),
      ('PM', '完美货币'),
      ('VISA', '万事达卡'),
    ]
    cash = forms.CharField(max_length=64,
                           min_length=4,
                           required=False,
                           widget=TextInput(
                               attrs={'readonly': 'readonly'}))
    amount = forms.CharField(max_length=6,
                             min_length=1,
                             required=True,
                             widget=TextInput(attrs={'type': 'number'}),
                             error_messages={'required': '提款金额不能为空'})
    pay_type = forms.ChoiceField(label="",
                                 choices=PAY_TYPE,
                                 required=False,
                                 widget=forms.Select(attrs={'readonly': 'readonly'}))
    bank_code = forms.CharField(max_length=64,
                                min_length=4,
                                required=True,
                                widget=TextInput(),
                                error_messages={'required': '收款银行不能为空'})
    pay_account = forms.CharField(max_length=64,
                                  min_length=4,
                                  required=True,
                                  widget=TextInput(),
                                  error_messages={'required': '收款账号不能为空'})
    password = forms.CharField(max_length=64,
                               min_length=4,
                               required=True,
                               widget=forms.PasswordInput(
                                   attrs={"placeholder": "你的登陆密码"}),
                               error_messages={'required': '密码不能为空'})

