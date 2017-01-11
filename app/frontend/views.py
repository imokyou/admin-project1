# coding: utf-8
from ipware.ip import get_ip
from captcha.models import CaptchaStore  
from captcha.helpers import captcha_image_url
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User as Auth_user
from lib import utils
from dbmodel.ziben.models import Statics, UserInfo, UserOplog, UserFeedback
from forms import RegForm, LoginForm, FeedbackForm
from config import errors
import services



@csrf_exempt
def test(request):
    return utils.NormalResp()


def home(request):
    data = {
        'index': 'home',
        'statics_info': Statics.objects.order_by('-id').first(),
        'chatlist': UserFeedback.objects.order_by('-id')[0:10],
    }

    return render(request, 'frontend/index.html', data)


def about_us(request):
    data = {
        'index': 'about_us'
    }
    return render(request, 'frontend/about_us.html', data)


@csrf_exempt
def register(request):
    hashkey = CaptchaStore.generate_key()  
    captcha_url = captcha_image_url(hashkey)

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
        'statics_info': Statics.objects.order_by('-id').first(),
        'chatlist': UserFeedback.objects.order_by('-id')[0:10],
        'form': RegForm(initial={'recommend_user': recommend_user}),
        'ages': range(18, 61),
        'hashkey': hashkey,
        'captcha_url': captcha_url,
        'errmsg': ''
    }

    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        username_exists = Auth_user.objects.filter(username=username).exists()
        if username_exists:
            return utils.ErrResp(errors.UserExists)
        if len(username) < 6:
            return utils.ErrResp(errors.UsernameInvalid)
        email_exists = Auth_user.objects.filter(email=email).exists()
        if email_exists:
            return utils.ErrResp(errors.EmailExists)
        if len(request.POST.get('password', '')) < 8  or len(request.POST.get('password', '')) > 16:
            return utils.ErrResp(errors.PasswordInvalid)

        captcha_code = request.POST.get('captcha_code', '')
        captcha_code_key = request.POST.get('captcha_code_key', '')
        cs = CaptchaStore.objects.filter(hashkey=captcha_code_key)
        true_key = cs[0].response
        print true_key, captcha_code.lower()
        if captcha_code.lower() != true_key:
            return utils.ErrResp(errors.CaptchCodeInvalid)
        CaptchaStore.objects.filter(hashkey=captcha_code_key).delete()
        
        services.reg(request)
        return utils.NormalResp()
    else:
        return render(request, 'frontend/register.html', data)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/member/')
    data = {
        'index': 'login',
        'statics_info': Statics.objects.order_by('-id').first(),
        'chatlist': UserFeedback.objects.order_by('-id')[0:10],
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
        'index': 'faq',
        'chatlist': UserFeedback.objects.order_by('-id')[0:10],
    }
    statics_info = Statics.objects.order_by('-id').first()
    data['statics_info'] = statics_info
    return render(request, 'frontend/faq.html', data)


def support(request):
    data = {
        'index': 'support',
        'statics_info': Statics.objects.order_by('-id').first(),
        'chatlist': UserFeedback.objects.order_by('-id')[0:10],
        'form': FeedbackForm(),
        'data': [],
        'errmsg': ''
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
        if not request.user.is_authenticated():
            data['errmsg'] = '请先登陆'
        else:
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


def risk_disclosure(request):
    data = {}
    return render(request, 'frontend/risk_disclosure.html', data)


def privacy(request):
    data = {}
    return render(request, 'frontend/privacy.html', data)


def contract(request):
    data = {}
    return render(request, 'frontend/contract.html', data)


def copyright(request):
    data = {}
    return render(request, 'frontend/copyright.html', data)
