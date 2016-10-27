# coding=utf-8
from django import forms
from ckeditor.widgets import CKEditorWidget
from dbmodel.ziben.models import NewsCategory


STATUS = [
    (1, '正常'),
    (2, '删除')
]

category_queryset = NewsCategory.objects.filter(status=1).all()

class CateSearchForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (1, '正常'),
        (2, '已删除')
    ]
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    status = forms.ChoiceField(label="", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)


class CateCreateForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(label="", choices=STATUS, widget=forms.Select(attrs={'class': 'form-control'}), required=False)

class CateEditForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), required=False)
    status = forms.ChoiceField(label="", choices=STATUS, widget=forms.Select(attrs={'class': 'form-control'}), required=False)


class SearchForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (1, '正常'),
        (2, '已删除')
    ]
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    category = forms.ModelChoiceField(label="", queryset=category_queryset, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    status = forms.ChoiceField(label="", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)


class CreateForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (1, '正常'),
        (2, '已删除')
    ]
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    category = forms.ModelChoiceField(label="", queryset=category_queryset, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    content = forms.CharField(label="", widget=CKEditorWidget(), required=False)
