# coding=utf8
from functools import wraps
from django.utils.decorators import available_attrs
from django.http.response import HttpResponseRedirect


def staff_required(redirect_to='/'):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def wrapper(request, *args, **kwargs):
            # 已登录
            if request.user.is_authenticated():
                # 超管
                if request.user.is_staff:
                    return view_func(request, *args, **kwargs)

                return HttpResponseRedirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
