# -*- coding: utf-8 -*-
import random
import string
import json
from urlparse import urlparse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url


# 响应相关
def HttpJSONResponse(data):
    """
    输出一个json
    """
    return HttpResponse(json.dumps(data),
                        content_type='application/json')


def NormalResp(d={}):
    """
    请求正常的响应
    """
    data = {'c': 0, 'm': '', 'd': d}
    return HttpJSONResponse(data)


def ExcepResp(e, c=-1024):
    """
    请求异常的响应
    """
    return HttpJSONResponse({'c': c,
                             'm': e.message})


def ErrResp(error):
    """
    请求出错的响应
    """
    return HttpJSONResponse({'c': error[0],
                             'm': error[1]})


def redirect_to_previous(request):
    currentUrl = urlparse(request.get_full_path())
    next = request.META.get('HTTP_REFERER')  # next 有可能为 None

    if not is_safe_url(url=next, host=request.get_host()):
        next = '/'

    nextUrl = urlparse(next)
    # 避免重定向循环
    if currentUrl.path == nextUrl.path and currentUrl.query == nextUrl.query:
        next = '/'
    response = HttpResponseRedirect(next)
    return response


def redirect_to(request, next=None):
    if next:
        return HttpResponseRedirect(next)
    return redirect_to_previous(request)


def activation_code(id, length=10):
    prefix = hex(int(id))[2:] + 'L'
    length = length - len(prefix)
    chars = string.ascii_letters + string.digits
    return prefix + ''.join([random.choice(chars) for i in range(length)])
