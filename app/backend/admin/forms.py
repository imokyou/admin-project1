# coding=utf-8
from django import forms

STATUS = [
    (0, '删除'),
    (1, '正常')
]

YES_NO = [
    (-1, '请选择'),
    (1, '是'),
    (0, '否')
]

BANK_CODE = [
    ('', '请选择'),
    ('ICBC', '工商银行'),
    ('CCTV', 'xx银行')
]


class SearchForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (0, '已删除'),
        (1, '正常')
    ]

    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    email = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    status = forms.ChoiceField(label="", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)



class QuickJumpForm(SearchForm):
    username = forms.CharField(label="", widget=forms.HiddenInput(attrs={}), required=False)
    email = forms.CharField(label="", widget=forms.HiddenInput(attrs={}), required=False)
    status = forms.CharField(label="", widget=forms.HiddenInput(attrs={}), required=False)
    is_superuser = forms.CharField(label="", widget=forms.HiddenInput(attrs={}), required=False)
    n = forms.CharField(label="", widget=forms.HiddenInput(attrs={}), required=False)
    p = forms.ChoiceField(label="", widget=forms.TextInput(attrs={'size': 4}), required=False)


class CreateForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    reg_code = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    bank_code = forms.ChoiceField(label="", choices=BANK_CODE, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    bank_card = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)


class EditForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    email = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    password = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))
    bank_code = forms.ChoiceField(label="", choices=BANK_CODE, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    bank_card = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    is_active = forms.ChoiceField(label="", choices=STATUS, widget=forms.Select(attrs={'class': 'form-control'}), required=False)