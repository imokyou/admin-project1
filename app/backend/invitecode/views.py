# coding: utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from lib import utils


@csrf_exempt
def home(request):
    data = {
        'index': 'admin'
    }
    return render(request, 'backend/invite_code.html', data)


@csrf_exempt
def test(request):
    return utils.NormalResp()
