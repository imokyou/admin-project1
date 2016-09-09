# coding: utf-8
from django.views.decorators.csrf import csrf_exempt
from lib import utils


@csrf_exempt
def test(request):
    return utils.NormalResp()
