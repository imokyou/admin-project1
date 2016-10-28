# coding=utf-8
from django import forms
from redactor.widgets import RedactorEditor
from dbmodel.ziben.models import NewsCategory


STATUS = [
    (1, '正常'),
    (2, '删除')
]

category_queryset = NewsCategory.objects.filter(status=1).all()
formcontrol = {'class': 'form-control'}


class CateSearchForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (1, '正常'),
        (2, '已删除')
    ]
    name = forms.CharField(label="",
                           required=False,
                           widget=forms.TextInput(attrs=formcontrol))
    status = forms.ChoiceField(label="",
                               choices=CHOICES,
                               widget=forms.Select(attrs=formcontrol),
                               required=False)


class CateCreateForm(forms.Form):
    name = forms.CharField(label="",
                           widget=forms.TextInput(attrs=formcontrol))
    status = forms.ChoiceField(label="",
                               choices=STATUS,
                               widget=forms.Select(attrs=formcontrol),
                               required=False)


class CateEditForm(forms.Form):
    id = forms.CharField(label="",
                         widget=forms.HiddenInput(),
                         required=False)
    name = forms.CharField(label="",
                           widget=forms.TextInput(attrs=formcontrol),
                           required=False)
    status = forms.ChoiceField(label="",
                               choices=STATUS,
                               widget=forms.Select(attrs=formcontrol),
                               required=False)


class SearchForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (1, '正常'),
        (2, '已删除')
    ]
    title = forms.CharField(label="",
                            widget=forms.TextInput(attrs=formcontrol),
                            required=False)
    category = forms.ModelChoiceField(label="",
                                      queryset=category_queryset,
                                      widget=forms.Select(attrs=formcontrol),
                                      required=False)
    status = forms.ChoiceField(label="",
                               choices=CHOICES,
                               widget=forms.Select(attrs=formcontrol),
                               required=False)


class CreateForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (1, '正常'),
        (2, '已删除')
    ]
    title = forms.CharField(label="",
                            widget=forms.TextInput(attrs=formcontrol),
                            required=False)
    category = forms.ModelChoiceField(label="",
                                      queryset=category_queryset,
                                      widget=forms.Select(attrs=formcontrol),
                                      required=False)
    content = forms.CharField(label="",
                              widget=RedactorEditor(),
                              required=False)


class EditForm(forms.Form):
    CHOICES = [
        (1, '正常'),
        (2, '已删除')
    ]
    id = forms.CharField(label="",
                         required=False,
                         widget=forms.HiddenInput())
    title = forms.CharField(label="",
                            required=False,
                            widget=forms.TextInput(attrs=formcontrol))
    category = forms.ModelChoiceField(label="",
                                      required=False,
                                      queryset=category_queryset,
                                      widget=forms.Select(attrs=formcontrol))
    content = forms.CharField(label="",
                              widget=RedactorEditor(),
                              required=False)
    status = forms.ChoiceField(label="",
                               choices=CHOICES,
                               widget=forms.Select(attrs=formcontrol),
                               required=False)
