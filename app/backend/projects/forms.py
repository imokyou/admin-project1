# coding=utf-8
from django import forms

STATUS = [
    (1, '正常'),
    (2, '已删除')
]


class SearchForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (1, '正常'),
        (2, '已删除')
    ]
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    status = forms.ChoiceField(label="", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)


class CreateForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    total = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))


class EditForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    price = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    total = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(label="", choices=STATUS, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
