# coding: utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from lib import utils


@csrf_exempt
@login_required
def home(request):
    data = {
        'msg': 'Hello World!',
        'index': 'dashboard'
    }
    return render(request, 'backend/index.html', data)


@csrf_exempt
def test(request):
    return utils.NormalResp()
