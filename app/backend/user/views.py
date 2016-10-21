# coding: utf-8
from datetime import datetime
from ipware.ip import get_ip
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User as Auth_user
from django.conf import settings
from dbmodel.ziben.models import UserInfo, UserBalance, UserOplog, UserRevenue, UserPayment, UserConnection, InviteCode, Bank
from lib import utils
from lib.pagination import Pagination
from config import errors
from forms import SearchForm, QuickJumpForm, CreateForm, EditForm, OplogSearchForm, RevenueSearchForm, PaymentSearchForm, RelationSearchForm
import services


@csrf_exempt
def test(request):
    return utils.NormalResp()


@csrf_exempt
@login_required
def home(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')
        email = request.GET.get('email', '')
        status = int(request.GET.get('status', -1))

        q = Auth_user.objects
        q = q.filter(is_superuser=0)
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
            'index': 'user',
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
        return render(request, 'backend/user/list.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required
def create(request):
    try:
        data = {
            'msg': '',
            'index': 'user',
            'form': CreateForm(request.POST)
        }
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            is_superuser = int(request.POST.get('is_superuser', 0))
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
                    u.is_superuser = is_superuser
                    if is_superuser:
                        u.is_staff = is_superuser
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
    return render(request, 'backend/user/create.html', data)


@csrf_exempt
@login_required
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

                    return HttpResponseRedirect('/backend/user/detail/?id=%s' % user_id)
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/user/edit.html', data)


@csrf_exempt
@login_required
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
    return render(request, 'backend/user/detail.html', data)

@csrf_exempt
@login_required
def oplog(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')
        optype = request.GET.get('optype', -1)

        q = UserOplog.objects
        if optype != -1:
            q = q.filter(optype=optype)
        if username:
            try:
                u = Auth_user.objects.get(username=username)
                q = q.filter(user_id=u.id)
            except:
                pass

        form_initial = {'optype': optype,
                        'username': username}
        form = OplogSearchForm(initial=form_initial)

        data = {
            'index': 'user',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'oplog_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        oplogs = q.all().order_by('-id')[(p - 1) * n:p * n]
        for o in oplogs:
            try:
                optime = utils.dt_field_to_local(o.create_time) \
                .strftime('%Y-%m-%d %H:%M:%S')
            except:
                optime = ''
            d = {
                'id': o.id,
                'user_id': o.user.id,
                'username': o.username,
                'optype': UserOplog.OPTYPE[o.optype],
                'content': o.content,
                'create_time': optime,
                'ip': o.ip
            }
            data['user_list']['data'].append(d)
        return render(request, 'backend/user/oplog.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required
def revenue(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')
        revenue_type = request.GET.get('revenue_type', -1)

        q = UserRevenue.objects
        if revenue_type != -1:
            q = q.filter(revenue_type=revenue_type)
        if username:
            try:
                u = Auth_user.objects.get(username=username)
                q = q.filter(user_id=u.id)
            except:
                pass

        form_initial = {'revenue_type': revenue_type,
                        'username': username}
        form = RevenueSearchForm(initial=form_initial)

        data = {
            'index': 'user',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'revenue_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        revenues = q.all().order_by('-id')[(p - 1) * n:p * n]
        for r in revenues:
            try:
                create_time = utils.dt_field_to_local(r.create_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                create_time = ''
            d = {
                'id': r.id,
                'user_id': r.user.id,
                'username': r.user.username,
                'revenue_type': UserRevenue.REVENUE_TYPE[r.revenue_type],
                'revenue': r.revenue,
                'create_time': create_time
            }
            data['user_list']['data'].append(d)
        return render(request, 'backend/user/revenue_records.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required
def payment(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')
        pay_type = request.GET.get('pay_type', -1)

        q = UserPayment.objects
        if pay_type != -1:
            q = q.filter(pay_type=pay_type)
        if username:
            try:
                u = Auth_user.objects.get(username=username)
                q = q.filter(user_id=u.id)
            except:
                pass

        form_initial = {'pay_type': pay_type,
                        'username': username}
        form = PaymentSearchForm(initial=form_initial)

        data = {
            'index': 'user',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'payment_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        payments = q.all().order_by('-id')[(p - 1) * n:p * n]
        for p in payments:
            try:
                create_time = utils.dt_field_to_local(p.create_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                create_time = ''
            d = {
                'id': p.id,
                'user_id': p.user.id,
                'username': p.user.username,
                'payout': float(p.payout),
                'bank_name': '',
                'bank_code': '',
                'bank_card': p.bank_card,
                'account': p.account,
                'pay_type': UserPayment.PAY_TYPE[p.pay_type],
                'create_time': create_time,
                'ip': p.ip
            }
            try:
                bank = Bank.objects.get(id=p.bank_id)
                d['bank_name'] = bank.name
                d['bank_code'] = bank.code
            except:
                pass
            data['user_list']['data'].append(d)
        return render(request, 'backend/user/payment.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required
def relation(request):
    try:
        user_id = int(request.GET.get('id', 0))
        username = request.GET.get('username', '')
        u_exists = Auth_user.objects \
            .filter(Q(id=user_id) | Q(username=username)).exists()

        searchform = PaymentSearchForm(initial={'username': username})
        data = {
            'user_info': {},
            'parent_info': {},
            'children_info': [],
            'searchform': searchform
        }
        if u_exists:
            u = Auth_user.objects.get(Q(id=user_id) | Q(username=username))
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
                'date_joined': date_joined,
                'last_login': last_login,
                'reg_ip': '',
                'cash': 0,
                'invite_benifit': 0,
                'total_amount': 0
            }
            try:
                uinfo = UserInfo.objects.get(user=u)
                data['user_info']['reg_ip'] = uinfo.reg_ip
            except:
                pass
            try:
                ubalance = UserBalance.objects.get(user=u)
                data['user_info']['cash'] = float(ubalance.ubalance)
                data['user_info']['invite_benifit'] = float(ubalance.invite_benifit)
                data['user_info']['total_amount'] = float(ubalance.total)
            except:
                pass
            data['parent_info'] = services._get_parent_info(u.id)
            data['children_info'] = services._get_childs(u.id)
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/user/relation.html', data)
