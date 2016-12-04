# coding=utf8
from django import forms
from django.forms import TextInput, Textarea
from django.contrib.auth.models import User as Auth_user


class ChatForm(forms.Form):
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
            raise forms.ValidationError("用户不存在")
        return username
