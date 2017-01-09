# -*- coding: utf-8 -*-
import pytz
import traceback
import random
import string
import json
import datetime
import calendar
from urlparse import urlparse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.utils import timezone


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
    traceback.print_exc()
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


def page_url(request):
    url = request.get_full_path
    return url


def dt_field_to_local(dt):  # 数据库中字段转成本地
    utcdt = dt.replace(tzinfo=pytz.utc)
    current_timezone = timezone.get_current_timezone()
    localdt = utcdt.astimezone(current_timezone)
    return localdt


def getMonthFirstDayAndLastDay(year=None, month=None):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 当月的第一天，datetime.date类型
              lastDay: 当月的最后一天，datetime.date类型
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    # 获取当月的第一天
    firstDay = datetime.date(year=year, month=month, day=1)
    lastDay = datetime.date(year=year, month=month, day=monthRange)

    return firstDay, lastDay


def debug():
    traceback.print_exc()
