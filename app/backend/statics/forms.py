# coding=utf8
from django import forms
from django.forms import TextInput, Select
from dbmodel.ziben.models import Statics, SiteSetting

BONUS_SWITCH = (
    (0, '关闭'),
    (1, '开启')
)


class EditForm(forms.ModelForm):
    class Meta:
        model = Statics
        fields = ['members',
                  'online',
                  'hits',
                  'total_paid',
                  'offers',
                  'pts_value',
                  'ptc_value']
        widgets = {
            'members': TextInput(attrs={'class': 'form-control'}),
            'online': TextInput(attrs={'class': 'form-control'}),
            'hits': TextInput(attrs={'class': 'form-control'}),
            'total_paid': TextInput(attrs={'class': 'form-control'}),
            'offers': TextInput(attrs={'class': 'form-control'}),
            'pts_value': TextInput(attrs={'class': 'form-control'}),
            'ptc_value': TextInput(attrs={'class': 'form-control'}),
        }


class SsetingEditForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = ['user_buy_price']
        widgets = {
            'user_buy_price': TextInput(attrs={'class': 'form-control'})
        }
