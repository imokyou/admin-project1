# coding: utf-8
import traceback
import requests
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
from django.utils import timezone
from dbmodel.ziben.models import UserInfo, UserBalance, UserOplog, UserRevenue, UserPayment, UserConnection, InviteCode, Bank, UserMessage, UserFeedback, UserWithDraw, UserVisaApply
from lib import utils
from lib.pagination import Pagination
from lib.permissions import staff_required
from config import errors
from forms import *
import services


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
                'date_joined': date_joined,
                'reg_ip': '',
                'reg_type': '',
                'reg_code': '',
                'invite_code': '',
                'invite_url': '',
                'first_name': u.first_name,
                'last_name': u.last_name,
            }
            try:
                userinfo = UserInfo.objects.get(user_id=u.id)
                d['reg_ip'] = userinfo.reg_ip
                d['reg_code'] = userinfo.reg_code
                d['invite_code'] = userinfo.invite_code
                d['invite_url'] = '%sregister/?invite_code=%s' % \
                    (settings.SITE_URL, userinfo.invite_code)
                d['country'] = userinfo.country
                d['provincy'] = userinfo.provincy
                d['city'] = userinfo.city
                d['address1'] = userinfo.address1
                d['address2'] = userinfo.address2
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
@login_required(login_url='/backend/login/')
@staff_required()
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
@login_required(login_url='/backend/login/')
@staff_required()
def edit(request):
    try:
        user_id = request.GET.get('id', '')
        form_initial = {}
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
            except:
                pass
            try:
                ubalance = UserBalance.objects.get(user_id=user_id)
                form_initial['cash'] = float(ubalance.cash)
            except:
                form_initial['cash'] = 0

        data = {
            'msg': '',
            'index': 'user',
            'form': EditForm(initial=form_initial),
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
                    if password:
                        uinfo.pwd = password
                    uinfo.save()

                    try:
                        ub = UserBalance.objects.get(user=u)
                        ub.cash = float(request.POST.get('cash'))
                    except:
                        ub = UserBalance(
                            user=u,
                            cash=float(request.POST.get('cash')),
                            invite_benifit=0,
                            total=0,
                            point=0,
                        )
                    finally:
                        ub.save()
                    data['msg'] = '账号修改成功'

                    return HttpResponseRedirect('/backend/user/detail/?id=%s' % user_id)
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/user/edit.html', data)


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
                'last_name': u.last_name,
                'role': UserInfo.ROLE[u.is_superuser],
                'status': UserInfo.STATUS[u.is_active],
                'date_joined': date_joined,
                'last_login': last_login,
                'reg_ip': '',
                'reg_code': '',
                'reg_type': '',
                'invite_code': '',
                'bank_code': '',
                'bank_card': '',
                'cash': 0,
                'invite_benifit': 0,
                'total_amount': 0
            }
            try:
                uinfo = UserInfo.objects.get(user=u)
                data['user_info']['pwd'] = uinfo.pwd
                data['user_info']['reg_ip'] = uinfo.reg_ip
                data['user_info']['reg_code'] = uinfo.reg_code
                data['user_info']['reg_type'] = UserInfo.REG_TYPE[uinfo.reg_type]
                data['user_info']['bank_code'] = uinfo.bank_code
                data['user_info']['bank_card'] = uinfo.bank_card
                data['user_info']['invite_code'] = uinfo.invite_code
                data['user_info']['invite_url'] = '%sregister/?invite_code=%s' % \
                    (settings.SITE_URL, uinfo.invite_code)
            except:
                pass
            try:
                ubalance = UserBalance.objects.get(user=u)
                data['user_info']['cash'] = float(ubalance.cash)
                data['user_info']['invite_benifit'] = float(ubalance.invite_benifit)
                data['user_info']['total_amount'] = float(ubalance.total)
            except:
                pass
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/user/detail.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def oplog(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')
        optype = int(request.GET.get('optype', -1))

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
                'username': o.user.username,
                'optype': UserOplog.OPTYPE[o.optype],
                'content': o.content,
                'optime': optime,
                'ip': o.ip
            }
            data['oplog_list']['data'].append(d)
        return render(request, 'backend/user/oplog.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
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
@login_required(login_url='/backend/login/')
@staff_required()
def payment(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')
        pay_type = request.GET.get('pay_type', 'ALL')
        status = int(request.GET.get('status', -2))

        q = UserPayment.objects
        if pay_type != 'ALL':
            q = q.filter(pay_type=pay_type)
        if status != -2:
            q = q.filter(status=status)
        if username:
            try:
                u = Auth_user.objects.get(username=username)
                q = q.filter(user_id=u.id)
            except:
                pass

        form_initial = {'pay_type': pay_type,
                        'username': username,
                        'status': status}
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
                create_time = utils.dt_field_to_local(p.create_at) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                create_time = ''
            d = {
                'id': p.id,
                'user_id': p.user.id,
                'order_id': p.order_id,
                'partner_order_id': p.partner_order_id,
                'username': p.user.username,
                'payout': float(p.amount),
                'point': int(p.point),
                'pay_type': p.pay_type,
                'create_time': create_time,
                'ip': p.ip,
                'status': int(p.status),
                'status_name': UserPayment.STATUS[p.status]
            }
            data['payment_list']['data'].append(d)
        return render(request, 'backend/user/payment.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def payment_success(request):
    try:
        order_id = request.POST.get('order_id', '')
        if not order_id:
            return utils.ErrResp(errors.ArgMiss)
        try:
            upayment = UserPayment.objects.get(order_id=order_id)
        except:
            return utils.ErrResp(errors.DataNotExists)
        if upayment.status != 1:
            upayment.status = request.POST.get('status', upayment.status)
            upayment.save()
            try:
                ubalance = UserBalance.objects.get(user_id=upayment.user_id)
            except:
                ubalance = UserBalance(
                    user_id=upayment.user_id,
                    point=0,
                    cash=0
                )
            if upayment.point:
                ubalance.point = ubalance.point + upayment.point
            else:
                if upayment.currency == 1:
                    ubalance.cash = int(upayment.amount)/ settings.CURRENCY_RATIO
                else:
                    ubalance.cash = int(upayment.amount)
            ubalance.save()

            if upayment.callback:
                requests.get(upayment.callback, verify=False)

    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)
    return utils.NormalResp()


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
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


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def mailbox(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        from_user = request.GET.get('from_user', '')
        to_user = request.GET.get('to_user', '')
        ctype = request.GET.get('ctype', 'member')

        q = UserMessage.objects
        if from_user:
            try:
                u = Auth_user.objects.get(username=from_user)
                q = q.filter(from_user_id=u.id)
            except:
                pass
        if to_user:
            try:
                u = Auth_user.objects.get(username=to_user)
                q = q.filter(to_user_id=u.id)
            except:
                pass
        if ctype:
            q = q.filter(ctype=ctype)

        form_initial = {'from_user': from_user,
                        'to_user': to_user,
                        'ctype': ctype}
        form = MailboxSearchForm(initial=form_initial)

        data = {
            'index': 'user',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'mail_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        mails = q.all().order_by('-id')[(p - 1) * n:p * n]
        for m in mails:
            try:
                send_time = utils.dt_field_to_local(m.create_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                send_time = ''
            try:
                read_time = utils.dt_field_to_local(m.read_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                read_time = ''
            d = {
                'id': m.id,
                'from_user': m.from_user.username,
                'to_user': m.to_user.username,
                'title': m.title,
                'ctype': m.ctype,
                'send_time': send_time,
                'read_time': read_time,
                'status_name': UserMessage.STATUS[m.status],
                'status': m.status
            }
            data['mail_list']['data'].append(d)
        return render(request, 'backend/user/mailbox.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def mailinfo(request, mail_id):
    try:
        data = {
            'mail_info': {}
        }
        data['mail_info'] = UserMessage.objects.get(id=int(mail_id))
    except:
        pass
    finally:
        return render(request, 'backend/user/mailinfo.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def mailreply(request, mail_id):
    try:
        data = {
            'mail_info': {}
        }
        data['mail_info'] = UserMessage.objects.get(id=int(mail_id))
        if request.method == 'POST':
            if data['mail_info'].status != 2:
                m = UserMessage(
                    from_user_id=1,
                    to_user_id=data['mail_info'].from_user_id,
                    title='回复：'+data['mail_info'].title.encode('UTF-8'),
                    content=request.POST.get('content'),
                    ctype='member',
                    create_time=timezone.now(),
                    status=0
                )
                m.save()

                data['mail_info'].status = 2
                data['mail_info'].save()

            return HttpResponseRedirect('/backend/user/mailbox/?ctype=company')
    except:
        traceback.print_exc()
    finally:
        return render(request, 'backend/user/mailreply.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def maildrop(request, mail_id):
    try:
        mail_info = UserMessage.objects.get(id=int(mail_id))
        mail_info.delete()
    except:
        pass
    finally:
        return HttpResponseRedirect('/backend/user/mailbox/')


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def feedback(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')

        q = UserFeedback.objects
        if username:
            try:
                u = Auth_user.objects.get(username=username)
                q = q.filter(user=u)
            except:
                pass

        form_initial = {'username': username}
        form = FeedbackSearchForm(initial=form_initial)

        data = {
            'index': 'user',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'feedback_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        feedbacks = q.all().order_by('-id')[(p - 1) * n:p * n]
        for f in feedbacks:
            try:
                create_time = utils.dt_field_to_local(f.create_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                create_time = ''
            d = {
                'id': f.id,
                'username': f.user.username,
                'title': f.title,
                'create_time': create_time,
                'status': UserFeedback.STATUS[f.status]
            }
            data['feedback_list']['data'].append(d)
        return render(request, 'backend/user/feedback.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def feedback_info(request, f_id):
    try:
        data = {
            'feedback_info': {}
        }
        data['feedback_info'] = UserFeedback.objects.get(id=int(f_id))
    except:
        pass
    finally:
        return render(request, 'backend/user/feedback_info.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def feedback_drop(request, f_id):
    try:
        feedback_info = UserFeedback.objects.get(id=int(f_id))
        feedback_info.delete()
    except:
        pass
    finally:
        return HttpResponseRedirect('/backend/user/feedback/')


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def withdraw(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')

        q = UserWithDraw.objects
        if username:
            try:
                u = Auth_user.objects.get(username=username)
                q = q.filter(user=u)
            except:
                pass

        form_initial = {'username': username}
        form = WithDrawSearchForm(initial=form_initial)

        data = {
            'index': 'user',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'withdraw_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        withdraws = q.all().order_by('-id')[(p - 1) * n:p * n]
        for w in withdraws:
            try:
                create_time = utils.dt_field_to_local(w.create_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                create_time = ''
            try:
                update_time = utils.dt_field_to_local(w.update_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                update_time = ''
            d = {
                'id': w.id,
                'username': w.user.username,
                'amount': float(w.amount),
                'pay_type': UserWithDraw.PAY_TYPE[w.pay_type],
                'pay_account': w.pay_account,
                'order_id': w.order_id,
                'create_time': create_time,
                'update_time': update_time,
                'status': UserWithDraw.STATUS[w.status]
            }
            data['withdraw_list']['data'].append(d)
        return render(request, 'backend/user/withdraw.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def withdraw_pass(request, f_id):
    try:
        next_url = request.GET.get('next_url')
        UserWithDraw.objects.filter(id=f_id).update(status=1)
    except:
        next_url = '/backend/user/withdraw/'
    finally:
        return HttpResponseRedirect(next_url)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def withdraw_reject(request, f_id):
    try:
        next_url = request.GET.get('next_url')
        withdraw = UserWithDraw.objects.get(id=f_id)
        withdraw.status = 2
        withdraw.save()

        # ubalance = UserBalance.objects.get(user_id=withdraw.user_id)
        # ubalance.cash = float(ubalance.cash) + float(withdraw.amount)
        # ubalance.save()
    except:
        next_url = '/backend/user/withdraw/'
    finally:
        return HttpResponseRedirect(next_url)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def visa_apply(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')
        status = int(request.GET.get('status', -1))

        q = UserVisaApply.objects
        if username:
            try:
                u = Auth_user.objects.get(username=username)
                q = q.filter(user_id=u.id)
            except:
                pass
        if status != -1:
            q = q.filter(status=status)

        form_initial = {'username': username, 'status': status}
        form = VisaSearchForm(initial=form_initial)

        data = {
            'index': 'user',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'list': {
                'p': p,
                'n': n,
                'data': q.all().order_by('-id')[(p - 1) * n:p * n],
            }
        }
        return render(request, 'backend/user/visa_apply.html', data)
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def visa_detail(request, apply_id):
    try:
        data = {
            'info': {}
        }
        data['info'] = UserVisaApply.objects.get(id=int(apply_id))
    except:
        pass
    finally:
        return render(request, 'backend/user/visa_detail.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def visa_update(request, f_id):
    try:
        vapply = UserVisaApply.objects.get(id=f_id)
        vapply.status = request.POST.get('status', vapply.status)
        vapply.save()
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)
    return utils.NormalResp()
