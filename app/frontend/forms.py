# coding=utf8
from django import forms
from django.contrib.auth.models import User as Auth_user
from django.contrib.auth import authenticate


class RegForm(forms.Form):
    first_name = forms.CharField(max_length=64, required=True)
    last_name = forms.CharField(max_length=64, required=True)
    username = forms.CharField(max_length=25, min_length=4, required=True)
    password = forms.CharField(max_length=16,
                               min_length=6,
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=16,
                                       min_length=6,
                                       widget=forms.PasswordInput())
    email = forms.CharField(max_length=64, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address1 = forms.CharField(max_length=64, required=False)
    address2 = forms.CharField(max_length=64, required=False)
    city = forms.CharField(max_length=64, required=False)
    provincy = forms.CharField(max_length=64, required=False)
    country = forms.CharField(max_length=64, required=False)
    zip_code = forms.CharField(max_length=64, required=False)
    sexal = forms.CharField(max_length=64, required=False)
    age = forms.CharField(max_length=64, required=False)
    # network_type = forms.CharField(max_length=64)
    is_info_real = forms.BooleanField()
    recommend_user = forms.CharField(max_length=64,
                                     required=False,
                                     widget=forms.TextInput(
                                        attrs={'readonly': 'readonly'}))
    is_agree = forms.BooleanField()

    def clean(self):
        cleaned_data = super(RegForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            msg = "两次密码输入不一致"
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if Auth_user.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if "@" not in email:
            raise forms.ValidationError("邮件格式不合法")
        if Auth_user.objects.filter(email=email).exists():
            raise forms.ValidationError("邮件已存在")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, min_length=4)
    password = forms.CharField(max_length=16,
                               min_length=6,
                               widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        user = authenticate(username=cleaned_data['username'],
                            password=cleaned_data['password'])
        if user is None or not user.is_active:
            self.add_error('username', '用户名或密码不正确')
        return cleaned_data


class FeedbackForm(forms.Form):
    CHOICES = [
        (1, '类型一')
    ]
    ctype = forms.ChoiceField(label="",
                              choices=CHOICES,
                              widget=forms.Select())
    title = forms.CharField(max_length=256,
                            error_messages={'required': '标题不能为空'})
    content = forms.CharField(max_length=1024,
                              widget=forms.Textarea(attrs={'rows': 6}),
                              error_messages={'required': '内容不能为空'})
