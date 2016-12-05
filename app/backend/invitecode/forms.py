# coding=utf-8
from django import forms


class SearchForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (0, '未使用'),
        (1, '已使用')
    ]
    code = forms.CharField(label="",
                           required=False,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    status = forms.ChoiceField(label="",
                               choices=CHOICES,
                               required=False,
                               widget=forms.Select(
                                   attrs={'class': 'form-control'}))


class QuickJumpForm(SearchForm):
    code = forms.CharField(label="",
                           required=False,
                           widget=forms.HiddenInput(attrs={}))
    status = forms.CharField(label="",
                             required=False,
                             widget=forms.HiddenInput(attrs={}))
    n = forms.CharField(label="",
                        required=False,
                        widget=forms.HiddenInput(attrs={}))
    p = forms.ChoiceField(label="",
                          required=False,
                          widget=forms.TextInput(attrs={'size': 4}))
