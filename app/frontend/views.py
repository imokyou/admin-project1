# coding: utf-8
from ipware.ip import get_ip
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from lib import utils
from dbmodel.ziben.models import Statics, UserInfo, UserOplog, UserFeedback
from forms import RegForm, LoginForm, FeedbackForm
import services


@csrf_exempt
def test(request):
    return utils.NormalResp()


def home(request):
    data = {
        'index': 'home'
    }
    statics_info = Statics.objects.order_by('-id').first()
    data['statics_info'] = statics_info
    return render(request, 'frontend/index.html', data)


def about_us(request):
    data = {
        'index': 'about_us'
    }
    return render(request, 'frontend/about_us.html', data)


def register(request):
    invite_code = request.GET.get('invite_code', '')
    recommend_user = ''
    if invite_code:
        try:
            uinfo = UserInfo.objects.filter(invite_code=invite_code).first()
            recommend_user = uinfo.user.username
        except:
            pass

    data = {
        'index': 'register',
        'form': RegForm(initial={'recommend_user': recommend_user}),
        'errmsg': ''
    }
    statics_info = Statics.objects.order_by('-id').first()
    data['statics_info'] = statics_info

    if request.method == 'POST':
        data['form'] = RegForm(request.POST)
        if data['form'].is_valid():
            services.reg(data['form'], request)
            return HttpResponseRedirect('/login/')
    return render(request, 'frontend/register.html', data)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/member/')
    data = {
        'index': 'login',
        'statics_info': Statics.objects.order_by('-id').first(),
        'form': LoginForm(),
        'errmsg': ''
    }

    if request.method == 'POST':
        data['form'] = LoginForm(request.POST)
        if data['form'].is_valid():
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            if user is not None and user.is_active:
                auth_login(request, user)

                log = UserOplog(
                    user_id=user.id,
                    optype=1,
                    content=request.META['HTTP_USER_AGENT'],
                    ip=get_ip(request),
                )
                log.save()

                return HttpResponseRedirect('/member/')
    return render(request, 'frontend/login.html', data)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


def video(request):
    data = {
        'index': 'video'
    }
    return render(request, 'frontend/video.html', data)


def faq(request):
    data = {
        'index': 'faq'
    }
    statics_info = Statics.objects.order_by('-id').first()
    data['statics_info'] = statics_info
    return render(request, 'frontend/faq.html', data)


def support(request):
    data = {
        'index': 'support',
        'statics_info': Statics.objects.order_by('-id').first(),
        'form': FeedbackForm(),
        'data': []
    }
    result = UserFeedback.objects \
        .filter(user_id=request.user.id) \
        .order_by('-id')[0:5]
    for r in result:
        data['data'].append({
            'id': r.id,
            'username': r.user.username,
            'title': r.title,
            'create_time': r.create_time.strftime('Y-m-d'),
            'status': UserFeedback.STATUS[r.status]
        })

    if request.method == 'POST':
        data['form'] = FeedbackForm(request.POST)
        if data['form'].is_valid():
            fb = UserFeedback(
                user=request.user,
                ctype=request.POST.get('ctype'),
                title=request.POST.get('title'),
                content=request.POST.get('content')
            )
            fb.save()
            return HttpResponseRedirect('/support/')

    return render(request, 'frontend/support.html', data)
