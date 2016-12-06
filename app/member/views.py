# coding=utf8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User as Auth_user
from dbmodel.ziben.models import UserOplog, News, UserMessage, UserPromoteRank
from lib import utils
from lib.pagination import Pagination
from forms import ChatForm
import services


def test(request):
    return utils.NormalResp()


@login_required(login_url='/login/')
def home(request):
    data = {
        'index': 'member',
        'sub_index': 'home'
    }
    data['statics'] = services.get_statics(request.user.id)
    return render(request, 'frontend/member/index.html', data)


@login_required(login_url='/login/')
def log(request, logtype):
    data = {
        'index': 'member',
        'sub_index': 'log',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }

    n = 20
    p = request.GET.get('p', 1)
    q = UserOplog.objects \
        .filter(optype=UserOplog.OPTYPE_CODES[logtype]) \
        .filter(user_id=request.user.id)

    data['loglist'] = {
        'paging': Pagination(request, q.count()),
        'data': q.all().order_by('-id')[(p - 1) * n:p * n]
    }

    return render(request, 'frontend/member/log_%s.html' % logtype, data)


@login_required(login_url='/login/')
def news(request):
    data = {
        'index': 'member',
        'sub_index': 'log',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }

    n = 20
    p = request.GET.get('p', 1)
    q = News.objects

    data['news'] = {
        'paging': Pagination(request, q.count()),
        'data': q.all().order_by('-id')[(p - 1) * n:p * n]
    }

    return render(request, 'frontend/member/news.html', data)


@login_required(login_url='/login/')
def chat(request):
    data = {
        'index': 'member_chat',
        'sub_index': 'log',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'form': ChatForm()
    }
    if request.method == 'POST':
        data['form'] = ChatForm(request.POST)
        if data['form'].is_valid():
            to_user = Auth_user.objects \
                .get(username=request.POST.get('username'))
            m = UserMessage(
                to_user_id=to_user.id,
                from_user_id=request.user.id,
                title=request.POST.get('title'),
                content=request.POST.get('message'),
                create_time=timezone.now(),
                status=0
            )
            m.save()
            return HttpResponseRedirect('/member/chat/')

    return render(request, 'frontend/member/chat.html', data)


@login_required(login_url='/login/')
def mailbox(request, ctype):
    data = {
        'index': 'member_mailbox',
        'sub_index': 'log',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'ctype': ctype
    }

    n = 20
    p = request.GET.get('p', 1)
    q = UserMessage.objects
    if ctype == 'sended':
        q = q.filter(from_user_id=request.user.id)
    elif ctype == 'received':
        q = q.filter(to_user_id=request.user.id)

    data['maillist'] = {
        'tot': q.count(),
        'paging': Pagination(request, q.count()),
        'data': q.all().order_by('-id')[(p - 1) * n:p * n]
    }

    return render(request, 'frontend/member/mailbox.html', data)


@login_required(login_url='/login/')
def rank(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }

    n = 20
    p = request.GET.get('p', 1)
    q = UserPromoteRank.objects
    data['ranklist'] = {
        'tot': q.count(),
        'paging': Pagination(request, q.count()),
        'data': q.all().order_by('-id')[(p - 1) * n:p * n]
    }

    return render(request, 'frontend/member/rank.html', data)


@login_required(login_url='/login/')
def seller(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }

    return render(request, 'frontend/member/seller.html', data)

