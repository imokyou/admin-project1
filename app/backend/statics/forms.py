# coding=utf8
from django import forms
from django.forms import TextInput
from dbmodel.ziben.models import Statics, SiteSetting


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
        fields = ['user_buy_price', 'bonus_50', 'bonus_100', 'bonus_200', 'bonus_400', 'bonus_600', 'bonus_800', 'bonus_1000', 'bonus_2000', 'bonus_times']
        widgets = {
            'user_buy_price': TextInput(attrs={'class': 'form-control'}),
            'bonus_50': TextInput(attrs={'class': 'form-control'}),
            'bonus_100': TextInput(attrs={'class': 'form-control'}),
            'bonus_200': TextInput(attrs={'class': 'form-control'}),
            'bonus_400': TextInput(attrs={'class': 'form-control'}),
            'bonus_600': TextInput(attrs={'class': 'form-control'}),
            'bonus_800': TextInput(attrs={'class': 'form-control'}),
            'bonus_1000': TextInput(attrs={'class': 'form-control'}),
            'bonus_2000': TextInput(attrs={'class': 'form-control'}),
            'bonus_times': TextInput(attrs={'class': 'form-control'})
        }
