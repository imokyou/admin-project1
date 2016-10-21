# coding=utf-8
from django import forms


class SearchForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (0, '未使用'),
        (1, '已使用')
    ]
    code = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    status = forms.ChoiceField(label="", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)


class QuickJumpForm(SearchForm):
    code = forms.CharField(label="", widget=forms.HiddenInput(attrs={}), required=False)
    status = forms.CharField(label="", widget=forms.HiddenInput(attrs={}), required=False)
    n = forms.CharField(label="", widget=forms.HiddenInput(attrs={}), required=False)
    p = forms.ChoiceField(label="", widget=forms.TextInput(attrs={'size': 4}), required=False)