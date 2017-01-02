# coding=utf8
from django import forms
from django.forms import TextInput, Select
from dbmodel.ziben.models import SiteSetting

BONUS_SWITCH = (
    (0, '关闭'),
    (1, '开启')
)


class BonusForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = ['bonus_switch', 'bonus_50', 'bonus_100', 'bonus_200', 'bonus_400', 'bonus_600', 'bonus_800', 'bonus_1000', 'bonus_2000']
        widgets = {
            'bonus_switch': Select(choices=BONUS_SWITCH, attrs={'class': 'form-control'}),
            'bonus_50': TextInput(attrs={'class': 'form-control'}),
            'bonus_100': TextInput(attrs={'class': 'form-control'}),
            'bonus_200': TextInput(attrs={'class': 'form-control'}),
            'bonus_400': TextInput(attrs={'class': 'form-control'}),
            'bonus_600': TextInput(attrs={'class': 'form-control'}),
            'bonus_800': TextInput(attrs={'class': 'form-control'}),
            'bonus_1000': TextInput(attrs={'class': 'form-control'}),
            'bonus_2000': TextInput(attrs={'class': 'form-control'})
        }


class InitForm(forms.Form):
    price = forms.CharField(label="",
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    total = forms.CharField(label="",
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}))


class UserOrderSellSearchForm(forms.Form):
    CHOICES = [
        (-1, '所有'),
        (0, '挂单中'),
        (1, '已结单')
    ]
    seller = forms.CharField(label="",
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control'}),
                             required=False)
    buyer = forms.CharField(label="",
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}),
                            required=False)
    status = forms.ChoiceField(label="",
                               choices=CHOICES,
                               widget=forms.Select(
                                   attrs={'class': 'form-control'}),
                               required=False)
