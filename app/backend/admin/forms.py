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

    username = forms.CharField(label="",
                               required=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    email = forms.CharField(label="",
                            required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    status = forms.ChoiceField(label="",
                               choices=CHOICES,
                               required=False,
                               widget=forms.Select(
                                   attrs={'class': 'form-control'}))



class QuickJumpForm(SearchForm):
    username = forms.CharField(label="",
                               required=False,
                               widget=forms.HiddenInput())
    email = forms.CharField(label="",
                            required=False,
                            widget=forms.HiddenInput())
    status = forms.CharField(label="",
                             required=False,
                             widget=forms.HiddenInput())
    is_superuser = forms.CharField(label="",
                                   required=False,
                                   widget=forms.HiddenInput())
    n = forms.CharField(label="",
                        required=False,
                        widget=forms.HiddenInput())
    p = forms.ChoiceField(label="",
                          required=False,
                          widget=forms.TextInput(attrs={'size': 4}))


class CreateForm(forms.Form):
    username = forms.CharField(label="",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    email = forms.CharField(label="",
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    password = forms.CharField(label="",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="",
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    reg_code = forms.CharField(label="",
                               required=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    bank_code = forms.ChoiceField(label="",
                                  required=False,
                                  choices=BANK_CODE,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control'}))
    bank_card = forms.CharField(label="",
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))


class EditForm(forms.Form):
    username = forms.CharField(label="",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'readonly': 'readonly'}))
    email = forms.CharField(label="",
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'readonly': 'readonly'}))
    password = forms.CharField(label="",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="",
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    bank_code = forms.ChoiceField(label="",
                                  choices=BANK_CODE,
                                  required=False,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control'}))
    bank_card = forms.CharField(label="",
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))
    is_active = forms.ChoiceField(label="",
                                  choices=STATUS,
                                  required=False,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control'}))

