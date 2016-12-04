# coding: utf-8
from datetime import datetime
from ipware.ip import get_ip
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as Auth_user
from django.conf import settings
from dbmodel.ziben.models import UserInfo, UserBalance, UserOplog, InviteCode
from lib import utils
from lib.pagination import Pagination
from lib.permissions import staff_required
from config import errors
from forms import SearchForm, QuickJumpForm, CreateForm, EditForm


@csrf_exempt
def test(request):
    return utils.NormalResp()


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def home(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')
        email = request.GET.get('email', '')
        status = int(request.GET.get('status', -1))

        q = Auth_user.objects
        q = q.filter(is_superuser=1)
        if status != -1:
            q = q.filter(is_active=status)
        if username:
            q = q.filter(username__icontains=username)

        form_initial = {'status': status,
                        'username': username,
                        'email': email}
        form = SearchForm(initial=form_initial)

        quick_form_initial = {'status': status,
                              'username': username,
                              'email': email,
                              'p': p,
                              'n': n}
        quick_jump_form = QuickJumpForm(initial=quick_form_initial)
        data = {
            'index': 'admin',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'quick_jump_form': quick_jump_form,
            'user_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        users = q.all().order_by('-id')[(p - 1) * n:p * n]
        for u in users:
            try:
                date_joined = utils.dt_field_to_local(u.date_joined) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_joined = ''
            try:
                last_login = utils.dt_field_to_local(u.last_login) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                last_login = ''
            d = {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'last_login': last_login,
                'status': u.is_active,
                'status_name': UserInfo.STATUS[u.is_active],
                'role': u.is_superuser,
                'role_name': UserInfo.ROLE[u.is_superuser],
                'date_joined': date_joined,
                'reg_ip': '',
                'reg_type': '',
                'reg_code': '',
                'invite_code': ''
            }
            try:
                userinfo = UserInfo.objects.get(user_id=u.id)
                d['reg_ip'] = userinfo.reg_ip
                d['reg_code'] = userinfo.reg_code
                d['invite_code'] = userinfo.invite_code
                try:
                    d['reg_type'] = UserInfo.REG_TYPE[userinfo.reg_type]
                except:
                    pass
            except:
                pass
            data['user_list']['data'].append(d)
        return render(request, 'backend/admin/list.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def create(request):
    try:
        data = {
            'msg': '',
            'index': 'admin',
            'form': CreateForm(request.POST)
        }
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            first_name = request.POST.get('first_name', '')
            reg_code = request.POST.get('reg_code', '')
            bank_code = request.POST.get('bank_code', '')
            bank_card = request.POST.get('bank_card', '')
            if not username or not password or not email:
                data['msg'] = '账号及密码、邮箱不能为空'
            elif len(password) < 10:
                data['msg'] = '密码长度至少为10'
            else:

                u_exists = Auth_user.objects.filter(username=username).exists()
                if u_exists:
                    data['msg'] = '账号已存在'
                else:
                    u = Auth_user.objects \
                        .create_user(username, email, password)
                    u.first_name = first_name
                    u.is_superuser = 1
                    u.is_staff = 1
                    u.save()

                    uinfo = UserInfo(
                        user=u,
                        reg_time=datetime.now(),
                        reg_ip=get_ip(request),
                        bank_code=bank_code,
                        bank_card=bank_card
                    )
                    if reg_code:
                        code_exists = InviteCode.objects \
                            .filter(code=reg_code).filter(status=0)
                        if not code_exists:
                            uinfo.reg_code = reg_code
                            uinfo.reg_type = 2
                    else:
                        uinfo.reg_type = 1
                    uinfo.save()
                    data['msg'] = '账号创建成功'
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/admin/create.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def edit(request):
    try:
        user_id = request.GET.get('id', '')
        form = EditForm()
        if user_id:
            try:
                u = Auth_user.objects.get(id=user_id)
                uinfo = UserInfo.objects.get(user=u)
                form_initial = {
                    'username': u.username,
                    'email': u.email,
                    'is_active': 0,
                    'first_name': u.first_name,
                    'bank_code': uinfo.bank_code,
                    'bank_card': uinfo.bank_card
                }
                if u.is_active:
                    form_initial['is_active'] = 1
                form = EditForm(initial=form_initial)
            except:
                pass
        data = {
            'msg': '',
            'index': 'user',
            'form': form,
            'user_id': user_id
        }
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            is_active = int(request.POST.get('is_active', 0))
            first_name = request.POST.get('first_name', '')
            bank_code = request.POST.get('bank_code', '')
            bank_card = request.POST.get('bank_card', '')
            if not username:
                data['msg'] = '账号不能为空'
            elif password and len(password) < 10:
                data['msg'] = '密码长度至少为10'
            else:
                u_exists = Auth_user.objects.filter(username=username).exists()
                if not u_exists:
                    data['msg'] = '用户不存在'
                else:
                    u = Auth_user.objects.get(username=username)
                    u.first_name = first_name
                    u.is_active = is_active
                    if password:
                        u.set_password(password)
                    u.save()

                    uinfo = UserInfo.objects.get(user=u)
                    uinfo.bank_code = bank_code
                    uinfo.bank_card = bank_card
                    uinfo.save()
                    data['msg'] = '账号修改成功'

                    return HttpResponseRedirect('/backend/admin/detail/?id=%s' % user_id)
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/admin/edit.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def detail(request):
    try:
        data = {
            'user_info': {}
        }
        user_id = int(request.GET.get('id', 0))
        u_exists = Auth_user.objects.filter(id=user_id).exists()
        if u_exists:
            u = Auth_user.objects.get(id=user_id)
            date_joined = utils.dt_field_to_local(u.date_joined) \
                .strftime('%Y-%m-%d %H:%M:%S')
            try:
                last_login = utils.dt_field_to_local(u.last_login) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                last_login = ''
            data['user_info'] = {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'first_name': u.first_name,
                'role': UserInfo.ROLE[u.is_superuser],
                'status': UserInfo.STATUS[u.is_active],
                'date_joined': date_joined,
                'last_login': last_login,
                'reg_ip': '',
                'reg_code': '',
                'reg_type': '',
                'bank_code': '',
                'bank_card': '',
                'cash': 0,
                'invite_benifit': 0,
                'total_amount': 0
            }
            try:
                uinfo = UserInfo.objects.get(user=u)
                data['user_info']['reg_ip'] = uinfo.reg_ip
                data['user_info']['reg_code'] = uinfo.reg_code
                data['user_info']['reg_type'] = UserInfo.REG_TYPE[uinfo.reg_type]
                data['user_info']['bank_code'] = uinfo.bank_code
                data['user_info']['bank_card'] = uinfo.bank_card
            except:
                pass
            try:
                ubalance = UserBalance.objects.get(user=u)
                data['user_info']['cash'] = float(ubalance.ubalance)
                data['user_info']['invite_benifit'] = float(ubalance.invite_benifit)
                data['user_info']['total_amount'] = float(ubalance.total)
            except:
                pass
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/admin/detail.html', data)


@csrf_exempt
@staff_required()
def login(request):
    try:
        next_url = request.GET.get('next', '')
        if request.user.is_authenticated():
            if not next_url:
                next_url = settings.BACKEND_INDEX
            return HttpResponseRedirect(next_url)
        data = {
            'error_msg': '',
            'next_url': next_url
        }
        if request.method == 'POST':
            account = request.POST.get('account', '')
            password = request.POST.get('password', '')
            user = authenticate(username=account, password=password)
            if user is not None and user.is_staff and user.is_active:
                auth_login(request, user)
                if not next_url:
                    next_url = settings.BACKEND_INDEX

                log = UserOplog(
                    user_id=user.id,
                    optype=1,
                    content=request.META['HTTP_USER_AGENT'],
                    ip=get_ip(request),
                )
                log.save()
                return HttpResponseRedirect(next_url)
            else:
                data['error_msg'] = '账号或密码错误, 请输新输入'
    except:
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/login.html', data)


@csrf_exempt
@login_required
@staff_required()
def logout(request):
    try:
        next_url = request.GET.get('next', settings.LOGIN_URL)
        auth_logout(request)
        return HttpResponseRedirect(next_url)
    except:
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def change_password(request):
    try:
        data = {
            'error_msg': '',
            'index': 'admin'
        }
        if request.method == 'POST':
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            if not new_password or not confirm_password:
                data['error_msg'] = '请输入新密码及确认密码'
            else:
                if new_password != confirm_password:
                    data['error_msg'] = '两次密码输入不相等, 请重新输入'
                elif len(new_password) < 10:
                    data['error_msg'] = '密码长度需为10'
                else:
                    u = Auth_user.objects.get(username=request.user.username)
                    u.set_password(new_password)
                    u.save()
                    logout(request)
                    return HttpResponseRedirect(settings.LOGIN_URL)
    except:
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/change_password.html', data)
