# coding=utf8
import traceback
import requests
import json
from ipware.ip import get_ip
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, logout as auth_logout
from django.contrib.auth.models import User as Auth_user
from django.db.models import Count, Sum
from dbmodel.ziben.models import UserOplog, News, UserMessage, UserPromoteRank, UserInfo, UserBalance, UserConnection, UserSellingMall, UserConnectionBuying, UserChangeRecommend, UserWithDraw, SiteSetting, UserBonus, CBCDPriceLog, UserOrderSell, CBCDInit, UserOrderBuy, UserPayment, UserVisaApply, UserResetPwd
from lib import utils
from lib.pagination import Pagination
from forms import ChatForm, ChangeRecommendForm, ChangePwdForm, ChangeUserInfoForm, WithDrawForm, EnChangePwdForm,EnChatForm
import services
from config import errors


def test(request):
    # return HttpResponse('ok')
    return utils.NormalResp()


@login_required(login_url='/login/')
def home(request):
    data = {
        'index': 'member',
        'sub_index': 'home'
    }

    data['statics'] = services.get_statics(request.user.id)
    return utils.crender(request, 'frontend/member/index.html', data)


@login_required(login_url='/login/')
def log(request, logtype):
    data = {
        'index': 'member',
        'sub_index': 'log',
        'statics': services.get_statics(request.user.id),
        'news': services.get_news(request)
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

    return utils.crender(request, 'frontend/member/log_%s.html' % logtype, data)


@login_required(login_url='/login/')
def log_payment(request):
    data = {
        'index': 'member',
        'sub_index': 'log',
        'statics': services.get_statics(request.user.id),
        'news': services.get_news(request)
    }

    n = 20
    p = request.GET.get('p', 1)
    q = UserPayment.objects \
        .filter(user_id=request.user.id) \
        .filter(status=1)

    data['loglist'] = {
        'paging': Pagination(request, q.count()),
        'data': q.all().order_by('-id')[(p - 1) * n:p * n]
    }

    return utils.crender(request, 'frontend/member/log_payment.html', data)


@login_required(login_url='/login/')
def log_withdraw(request):
    data = {
        'index': 'member',
        'sub_index': 'log',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }

    n = 20
    p = request.GET.get('p', 1)
    q = UserWithDraw.objects \
        .filter(user_id=request.user.id)

    data['loglist'] = {
        'paging': Pagination(request, q.count()),
        'data': q.all().order_by('-id')[(p - 1) * n:p * n]
    }

    return utils.crender(request, 'frontend/member/log_withdraw.html', data)

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
    if request.session['lang'] == 'en':
        q = q.filter(category=2)

    data['news'] = {
        'paging': Pagination(request, q.count()),
        'data': q.all().order_by('-id')[(p - 1) * n:p * n]
    }

    return utils.crender(request, 'frontend/member/news.html', data)


@login_required(login_url='/login/')
def chat(request):
    data = {
        'index': 'member_chat',
        'sub_index': 'log',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'form': ChatForm()
    }
    if request.session['lang'] == 'cn':
        data['form'] = ChatForm()
    else:
        data['form'] = EnChatForm()
    if request.method == 'POST':
        if request.session['lang'] == 'cn':
            data['form'] = ChatForm(request.POST)
        else:
            data['form'] = EnChatForm(request.POST)
        if data['form'].is_valid():
            username = request.POST.get('username')
            if username == 'company':
                m = UserMessage(
                    to_user_id=1,
                    from_user_id=request.user.id,
                    title=request.POST.get('title'),
                    content=request.POST.get('message'),
                    ctype='company',
                    create_time=timezone.now(),
                    status=0
                )
            else:
                to_user = Auth_user.objects \
                    .get(username=username)
                m = UserMessage(
                    to_user_id=to_user.id,
                    from_user_id=request.user.id,
                    title=request.POST.get('title'),
                    content=request.POST.get('message'),
                    ctype='member',
                    create_time=timezone.now(),
                    status=0
                )
            m.save()
            return HttpResponseRedirect('/member/chat/')

    return utils.crender(request, 'frontend/member/chat.html', data)



@login_required(login_url='/login/')
def shop(request):
    data = {
        'index': 'member_shop',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }

    return utils.crender(request, 'frontend/member/shop.html', data)


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
    q = UserMessage.objects.filter(ctype='member')
    if ctype == 'sended':
        q = q.filter(from_user_id=request.user.id)
    elif ctype == 'received':
        q = q.filter(to_user_id=request.user.id)

    data['maillist'] = {
        'tot': q.count(),
        'paging': Pagination(request, q.count()),
        'data': q.all().order_by('-id')[(p - 1) * n:p * n]
    }

    return utils.crender(request, 'frontend/member/mailbox.html', data)


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

    return utils.crender(request, 'frontend/member/rank.html', data)


@login_required(login_url='/login/')
def seller(request):
    data = {
        'index': 'member_seller',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }

    return utils.crender(request, 'frontend/member/seller.html', data)


@login_required(login_url='/login/')
def promotion(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {
            'uconnect': [],
            'ucount': 0
        }
    }
    invite_code = UserInfo.objects.get(user=request.user).invite_code
    uconnections = UserConnection.objects.filter(parent=request.user)

    data['data']['invite_url'] = '%sregister?invite_code=%s' % \
        (settings.SITE_URL, invite_code)
    data['data']['ubalance'] = services.get_balance(request.user)
    for uconnect in uconnections:
        recommends = services.get_recommends(uconnect.user)
        invite_benifit = services.get_invite_benifit(uconnect.user)
        try:
            last_login = utils.dt_field_to_local(uconnect.user.last_login)
        except:
            last_login = ''
        data['data']['uconnect'].append({
            'username': uconnect.user.username,
            'reg_time': utils.dt_field_to_local(uconnect.user.date_joined),
            'recommends': recommends,
            'last_login': last_login,
            'invite_benifit': invite_benifit
        })
    data['data']['ucount'] = len(data['data']['uconnect'])

    return utils.crender(request, 'frontend/member/promotion.html', data)


@login_required(login_url='/login/')
def selling(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {
            'uconnect': []
        }
    }
    uconnections = UserConnection.objects \
        .filter(parent=request.user).filter(is_selling=0)
    for uconnect in uconnections:
        ubalance = services.get_balance(uconnect.user)
        data['data']['uconnect'].append({
            'user_id': uconnect.user.id,
            'username': uconnect.user.username,
            'total_investment': ubalance['total_investment']
        })
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        if user_id:
            mall = UserSellingMall(
                user_id=user_id,
                parent_user=request.user
            )
            mall.save()

            UserConnection.objects \
                .filter(user_id=user_id).update(is_selling=1)
            return HttpResponseRedirect('/member/selling/')

    return utils.crender(request, 'frontend/member/selling.html', data)


@login_required(login_url='/login/')
def buying(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'errmsg': '',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {
            'members': []
        }
    }
    sellings = UserSellingMall.objects \
        .exclude(parent_user=request.user) \
        .exclude(user=request.user) \
        .order_by('-id')
    for s in sellings:
        data['data']['members'].append({
            'user_id': s.user.id,
            'username': s.user.username,
            'reg_time': utils.dt_field_to_local(s.user.date_joined)
        })
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        # todo: 扣钱
        ssetings = SiteSetting.objects.first()
        if services.pay_cash(request.user, int(ssetings.user_buy_price)*settings.CURRENCY_RATIO):
            ucb = UserConnectionBuying(
                user_id=user_id,
                parent=request.user,
                ratio=100
            )
            ucb.save()

            UserSellingMall.objects \
                .filter(user_id=user_id).delete()
            return HttpResponseRedirect('/member/buying/')
        else:
            should_pay = int(ssetings.user_buy_price)*settings.CURRENCY_RATIO
            ubalance = services.get_balance(request.user)
            need_pay = should_pay - float(ubalance['cash'])
            data['errmsg'] = '余额不足，请充值: %s元' % need_pay

    return utils.crender(request, 'frontend/member/buying.html', data)


@login_required(login_url='/login/')
def subm(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'form': ChangeRecommendForm(),
        'data': {
            'changelist': []
        },
        'errmsg': ''
    }
    # 首层
    nets = {'name': request.user.username, 'user_id': request.user.id, 'lnums': 0, 'rnums': 0}
    result = services.get_sub_member_nums(request.user.id)
    nets['lnums'], nets['rnums'] = result['lnums'], result['rnums']

    # 第二层
    # 左
    left2user = services.get_most_sub_member(request.user.id, 'left')
    if left2user:
        result = services.get_sub_member_nums(left2user['user_id'])
        nets['left2'] = {'name': result['username'], 'user_id': result['user_id'], 'lnums': result['lnums'], 'rnums': result['rnums']}
    # 右
    right2user = services.get_most_sub_member(request.user.id, 'right')
    if right2user:
        result = services.get_sub_member_nums(right2user['user_id'])
        nets['right2'] = {'name': result['username'], 'user_id': result['user_id'], 'lnums': result['lnums'], 'rnums': result['rnums']}

    # 第三层
    if 'left2' in nets:
        left2l3user = services.get_most_sub_member(nets['left2']['user_id'], 'left')
        if left2l3user:
            result = services.get_sub_member_nums(left2l3user['user_id'])
            nets['left2']['left3'] = {'name': result['username'], 'user_id': result['user_id'], 'lnums': result['lnums'], 'rnums': result['rnums']}

        left2r3user = services.get_most_sub_member(nets['left2']['user_id'], 'right')
        if left2r3user:
            result = services.get_sub_member_nums(left2r3user['user_id'])
            nets['left2']['right3'] = {'name': result['username'], 'user_id': result['user_id'], 'lnums': result['lnums'], 'rnums': result['rnums']}

    if 'right2' in nets:
        right2l3user = services.get_most_sub_member(nets['right2']['user_id'], 'left')
        if right2l3user:
            result = services.get_sub_member_nums(right2l3user['user_id'])
            nets['right2']['left3'] = {'name': result['username'], 'user_id': result['user_id'], 'lnums': result['lnums'], 'rnums': result['rnums']}

        right2r3user = services.get_most_sub_member(nets['right2']['user_id'], 'right')
        if right2r3user:
            result = services.get_sub_member_nums(right2r3user['user_id'])
            nets['right2']['right3'] = {'name': result['username'], 'user_id': result['user_id'], 'lnums': result['lnums'], 'rnums': result['rnums']}


        # 第四层,左
        if 'left3' in nets['left2']:
            left3l4user = services.get_most_sub_member(nets['left2']['left3']['user_id'], 'left')
            if left3l4user:
                result = services.get_sub_member_nums(left3l4user['user_id'])
                nets['left2']['left3']['left4'] = {'name': result['username'], 'user_id': result['user_id'], 'lnums': result['lnums'], 'rnums': result['rnums']}

            left3r4user = services.get_most_sub_member(nets['left2']['left3']['user_id'], 'right')
            if left3r4user:
                result = services.get_sub_member_nums(left3r4user['user_id'])
                nets['left2']['left3']['right4'] = {'name': result['username'], 'user_id': result['user_id'], 'lnums': result['lnums'], 'rnums': result['rnums']}

        if 'right3' in nets['left2']:
            right3l4user = services.get_most_sub_member(nets['left2']['right3']['user_id'], 'left')
            if right3l4user:
                result = services.get_sub_member_nums(right3l4user['user_id'])
                nets['left2']['right3']['left4'] = {'name': result['username'], 'user_id': result['user_id'], 'lnums': result['lnums'], 'rnums': result['rnums']}

            right3r4user = services.get_most_sub_member(right3l4user['user_id'], 'right')
            if right3r4user:
                result = services.get_sub_member_nums(right3r4user['user_id'])
                nets['left2']['right3']['rihgt4'] = {'name': result['username'], 'user_id': result['user_id'],  'lnums': result['lnums'], 'rnums': result['rnums']}

        # 第四层,右
        if 'left3' in nets['right2']:
            ret = services.get_most_sub_member(nets['right2']['left3']['user_id'], 'left')
            if ret:
                result = services.get_sub_member_nums(ret['user_id'])
                nets['right2']['left3']['left4'] = {'name': result['username'], 'user_id': result['user_id'],  'lnums': result['lnums'], 'rnums': result['rnums']}
            ret = services.get_most_sub_member(nets['right2']['left3']['user_id'], 'right')
            if ret:
                result = services.get_sub_member_nums(ret['user_id'])
                nets['right2']['left3']['right4'] = {'name': result['username'], 'user_id': result['user_id'],  'lnums': result['lnums'], 'rnums': result['rnums']}

        if 'right3' in nets['right2']:
            ret = services.get_most_sub_member(nets['right2']['right3']['user_id'], 'left')
            if ret:
                result = services.get_sub_member_nums(ret['user_id'])
                nets['right2']['right3']['left4'] = {'name': result['username'], 'user_id': result['user_id'],  'lnums': result['lnums'], 'rnums': result['rnums']}
            ret = services.get_most_sub_member(nets['right2']['right3']['user_id'], 'right')
            if ret:
                result = services.get_sub_member_nums(ret['user_id'])
                nets['right2']['right3']['right4'] = {'name': result['username'], 'user_id': result['user_id'],  'lnums': result['lnums'], 'rnums': result['rnums']}

    data['nets'] = nets
    return utils.crender(request, 'frontend/member/subm.html', data)


@login_required(login_url='/login/')
def change_recommend_user(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'form': ChangeRecommendForm(),
        'data': {
            'changelist': []
        },
        'errmsg': ''
    }
    changelist = UserChangeRecommend.objects \
        .filter(user_id=request.user.id) \
        .values('user_id') \
        .annotate(times=Count('id')) \
        .order_by('-times')
    for c in changelist:
        uinfo = UserInfo.objects.get(user_id=c.get('user_id'))
        ubalance = services.get_balance(uinfo.user)
        data['data']['changelist'].append({
            'username': uinfo.user.username,
            'recommend_user': uinfo.recommend_user,
            'investment': ubalance['total_investment'],
            'reg_time': utils.dt_field_to_local(uinfo.user.date_joined),
            'times': c.get('times', 1)
        })
    if request.method == 'POST':
        data['form'] = ChangeRecommendForm(request.POST)
        if data['form'].is_valid():
            change_times = UserChangeRecommend.objects \
                .filter(user=request.user).count()
            recommend_username = request.POST.get('username', '')
            unifo = UserInfo.objects.get(user=request.user)
            if recommend_username == request.user.username:
                data['errmsg'] = '不能把自己设置为转介人'
            elif recommend_username == unifo.recommend_user:
                data['errmsg'] = '%s已经是你的当前推荐人' % recommend_username.encode('UTF-8')
            else:
                if change_times < 3:
                    ruinfo = UserInfo.objects \
                        .get(user__username=recommend_username)
                    ucr = UserChangeRecommend(
                        user_id=request.user.id,
                        recommend_user_id=ruinfo.user_id
                    )
                    ucr.save()

                    UserInfo.objects \
                        .filter(user=request.user) \
                        .update(recommend_user=request.POST.get('username'))

                    UserConnection.objects \
                        .filter(user_id=request.user.id) \
                        .update(parent_id=ruinfo.user_id)

                    return HttpResponseRedirect('/member/change-recommend-user/')
                else:
                    data['errmsg'] = '你的转介次数已满3次，不能再次转介'

    return utils.crender(request, 'frontend/member/change_recommend_user.html', data)


@csrf_exempt
@login_required(login_url='/login/')
def setting(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'changePwdForm': ChangePwdForm(),
        'changeInfoForm': ChangeUserInfoForm(),
        'userinfo': {},
        'errmsg': ''
    }
    if request.session['lang'] == 'cn':
        data['changePwdForm'] = ChangePwdForm()
    else:
        data['changePwdForm'] = EnChangePwdForm()
    uinfo = UserInfo.objects.get(user=request.user)
    data['userinfo'] = uinfo

    if request.method == 'POST':
        if request.POST.get('ctype') == 'changepwd':
            if request.session['lang'] == 'cn':
                data['changePwdForm'] = ChangePwdForm(request.POST)
            else:
                data['changePwdForm'] = EnChangePwdForm(request.POST)
            if data['changePwdForm'].is_valid():
                user = authenticate(username=request.user.username,
                                    password=request.POST['password'])
                if not user:
                    if request.session['lang'] == 'cn':
                        data['errmsg'] = '原密码输入有误'
                    else:
                        data['errmsg'] = 'old password invalid'
                else:
                    u = Auth_user.objects.get(username=request.user.username)
                    u.set_password(request.POST['new_password'])
                    u.save()

                    uinfo = UserInfo.objects.get(user=request.user)
                    uinfo.pwd = request.POST['new_password']
                    uinfo.save()

                    auth_logout(request)
                    return HttpResponseRedirect('/login/')
        elif request.POST.get('ctype', '') == 'changeinfo':
            try:
                uinfo = UserInfo.objects.get(user=request.user)
                uinfo.city = request.POST.get('city', uinfo.city)
                uinfo.provincy = request.POST.get('provincy', uinfo.provincy)
                uinfo.country = request.POST.get('country', uinfo.country)
                uinfo.phone_number = request.POST.get('phone', uinfo.phone_number)
                uinfo.bank_code = request.POST.get('bank_code', uinfo.bank_code)
                uinfo.bank_card = request.POST.get('bank_card', uinfo.bank_card)
                uinfo.save()
                return utils.NormalResp()
            except:
                traceback.print_exc()
                return utils.ErrResp(errors.FuncFailed)
    return utils.crender(request, 'frontend/member/settings.html', data)


@login_required(login_url='/login/')
def dashboard(request):
    weekday2name = {
        'cn': ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天'],
        'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
    data = {
        'index': 'member',
        'sub_index': 'balance',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {
            'curr_weekday': {
                'cn': '',
                'en': ''
            }
        },

    }
    curr_weekday = timezone.now().weekday()
    data['data']['curr_weekday']['cn'] = weekday2name['cn'][curr_weekday]
    data['data']['curr_weekday']['en'] = weekday2name['en'][curr_weekday]
    data['data']['invite_users'] = UserConnection.objects \
        .filter(parent=request.user).count()
    data['data']['buy_users'] = UserConnectionBuying.objects \
        .filter(parent=request.user).count()
    data['data']['total_users'] = data['data']['invite_users'] + data['data']['buy_users']
    data['data']['balance'] = services.get_balance(request.user)
    return utils.crender(request, 'frontend/member/dashboard.html', data)


@login_required(login_url='/login/')
def us_bank_account(request):
    data = {
        'index': 'member',
        'sub_index': 'deposite',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {}
    }
    return utils.crender(request, 'frontend/member/us_bank_account.html', data)


@login_required(login_url='/login/')
def withdraw(request):
    data = {
        'index': 'member',
        'sub_index': 'deposite',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'errmsg': '',
        'data': {'withdraws': []}
    }
    ubalance = services.get_balance(request.user)
    uinfo = UserInfo.objects.get(user=request.user)
    initial = {
        'cash': ubalance['cash'],
        'pay_type': uinfo.bank_code,
        'pay_account': uinfo.bank_card,
    }
    data['form'] = WithDrawForm(initial=initial)

    withdraws = UserWithDraw.objects.filter(user=request.user).order_by('-id')
    for w in withdraws:
        data['data']['withdraws'].append({
            'order_id': w.order_id,
            'create_time': w.create_time,
            'amount': float(w.amount),
            'status': UserWithDraw.STATUS[w.status]
        })
    if request.method == 'POST':
        data['form'] = WithDrawForm(request.POST)
        if data['form'].is_valid():
            uauth = authenticate(username=request.user.username,
                                 password=request.POST['password'])
            if uauth:
                pay_amount = float(request.POST.get('amount'))
                if services.pay_cash(request.user, pay_amount):
                    udraw = UserWithDraw(
                        user=request.user,
                        pay_type=request.POST.get('pay_type'),
                        pay_account=request.POST.get('pay_account'),
                        bank_code=request.POST.get('bank_code', ''),
                        amount=float(request.POST.get('amount'))
                    )
                    udraw.save()

                    return HttpResponseRedirect('/member/withdraw/')
                else:
                    data['errmsg'] = '余额不足'
            else:
                data['errmsg'] = '密码不正确'

    return utils.crender(request, 'frontend/member/withdraw.html', data)


@csrf_exempt
@login_required(login_url='/login/')
def bonus(request):
    data = {
        'index': 'member',
        'sub_index': 'bonus',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }
    # 查抽奖列表
    data['bonuslist'] = UserBonus.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        b2c = {
            'bonus_50': 0,
            'bonus_100': 7,
            'bonus_200': 6,
            'bonus_400': 5,
            'bonus_600': 4,
            'bonus_800': 3,
            'bonus_1000': 2,
            'bonus_2000': 1
        }
        result = SiteSetting.objects.all().order_by('-id').first()
        if not result.bonus_switch:
            return utils.ErrResp(errors.BonusSwitchOff)
        else:
            # 写日志
            firstday, lastday = utils.getMonthFirstDayAndLastDay()
            ubonus = UserBonus.objects \
                .filter(create_time__gte=firstday) \
                .filter(create_time__lte=lastday) \
                .filter(user=request.user)  
            if ubonus:
                return utils.ErrResp(errors.BonusExists)
            else:
                bonuss = []
                for b in b2c:
                    bonuss.append((b, getattr(result, b)))
                wr = services.weighted_random(bonuss)
                point = int(wr.split('bonus_')[1])
                level = b2c[wr]

                # 扣除资本兑总量
                if not services.cbcd_reduce(point):
                    return utils.ErrResp(errors.BonusSwitchOff)

                ubonus = UserBonus(
                    user=request.user,
                    point=point,
                    status=0
                )
                ubonus.save()

                log = UserOplog(
                    user_id=request.user.id,
                    optype=9,
                    content='会员认购中抽中资本兑: %s' % point,
                    ip=get_ip(request),
                )
                log.save()

            resp = {
                'level': level,
                'point': point,
                'money': int(point*services.get_price()),
                'bonus_id': ubonus.id
            }
            return utils.NormalResp(resp)

    return utils.crender(request, 'frontend/member/bonus.html', data)


@login_required(login_url='/login/')
def bonus_update(request):
    bonus_id = int(request.GET.get('id', 0))
    if bonus_id:
        ubonus = UserBonus.objects.get(id=bonus_id)
        ubonus.status = 1
        ubonus.save()
    return utils.NormalResp()

@login_required(login_url='/login/')
def cbcd_price(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {}
    }

    data['data']['ordersell'] = UserOrderSell.objects \
        .filter(seller_user=request.user) \
        .all().order_by('id')[0:15]
    data['data']['orderbuy'] = UserOrderBuy.objects \
        .filter(buyer_user=request.user) \
        .all().order_by('-id')[0:15]

    return utils.crender(request, 'frontend/member/cbcd_price.html', data)


@login_required(login_url='/login/')
def cbcd_order(request):
    data = {
        'index': 'member',
        'sub_index': 'hall',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {}
    }

    data['data']['ordersell'] = UserOrderSell.objects \
        .filter(status=0) \
        .all().order_by('id')[0:15]
    data['data']['orderbuy'] = UserOrderBuy.objects \
        .all().order_by('-id')[0:15]

    return utils.crender(request, 'frontend/member/CBCD_order.html', data)


@csrf_exempt
@login_required(login_url='/login/')
def cbcd_sell(request):
    if request.method == 'POST':
        # if not services.is_hall_open():
        #     return utils.ErrResp(errors.HallNotOpened)

        num = int(request.POST.get('num'))
        price = float(request.POST.get('price'))

        current_order = services.get_current_order()
        if int(price*1000) >= int(current_order['price'] * 1000 * 1.1):
            return utils.ErrResp(errors.PriceTooHigh)
        if int(price*1000) <= int(current_order['price'] * 1000 * 0.9):
            return utils.ErrResp(errors.PriceTooLow)
        try:
            ubalance = UserBalance.objects.get(user=request.user)
        except:
            return utils.ErrResp(errors.CBCDLimit)

        if not ubalance.point or int(ubalance.point*0.05) < num:
            return utils.ErrResp(errors.CBCDLimit)
        ubalance.point = ubalance.point - num
        ubalance.save()
        uorder = UserOrderSell(
            seller_user=request.user,
            num=num,
            num_unsell=num,
            price=price,
            status=0
        )
        uorder.save()
        return utils.NormalResp()


@csrf_exempt
@login_required(login_url='/login/')
def cbcd_buy(request):
    if request.method == 'POST':
        if not services.is_hall_open():
            return utils.ErrResp(errors.HallNotOpened)

        num = int(request.POST.get('num', 0))
        price = float(request.POST.get('price', 0))

        if not num or not price:
            return utils.ErrResp(errors.ArgMiss)

        current_order = UserOrderSell.objects.filter(status=0).order_by('id').first()

        if num > int(current_order.num_unsell):
            return utils.ErrResp(errors.CBCDLimit)
        price = float(current_order.price)

        # 买家付款
        try:
            buyer = UserBalance.objects.get(user_id=request.user.id)
        except:
            utils.debug()
            return utils.ErrResp(errors.MoneyLimit)
        # 美元
        money = float(num * price)

        if not buyer.cash or float(buyer.cash) < money:
            return utils.ErrResp(errors.MoneyLimit)
        buyer.point = buyer.point + num
        buyer.cash = float(buyer.cash) - money
        buyer.save()

        # 更新订单状态
        current_order.num_unsell = current_order.num_unsell - num
        if int(current_order.num_unsell) == 0:
            current_order.status = 1
        current_order.save()

        # 卖家收钱
        seller = UserBalance.objects.get(user=current_order.seller_user)
        seller.cash = float(seller.cash) + float(num * price)
        seller.save()

        # 写买入记录
        buyorder = UserOrderBuy(
            seller_order_id=current_order.order_id,
            buyer_user=request.user,
            price=price,
            num=num
        )
        buyorder.save()
        return utils.NormalResp()


@login_required(login_url='/login/')
def trading_hall(request, ctype):
    data = {
        'index': 'member',
        'sub_index': 'hall',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'errmsg': '',
        'ctype': ctype,
        'data': {}
    }

    result = UserOrderSell.objects.filter(status=0) \
        .aggregate(total=Sum('num_unsell'))
    try:
        data['data']['total'] = int(result.get('total', 0))
    except:
        data['data']['total'] = 0
    data['data']['price_init'] = services.get_init_price()
    current_order = services.get_current_order()
    data['data']['price_current'] = current_order['price']
    if ctype == 'sell':
        ubalance = services.get_balance(request.user)
        data['data']['point'] = ubalance['point']
    else:
        data['data']['point'] = current_order['num']
    data['data']['price_open'] = services.get_opening_price()
    data['data']['price_up'] = data['data']['price_current'] - data['data']['price_open']
    data['data']['ratio'] = (data['data']['price_current'] - data['data']['price_init'])*100 / data['data']['price_init']

    return utils.crender(request, 'frontend/member/trading_hall.html', data)


@login_required(login_url='/login/')
def trading_hall_home(request):
    data = {
        'index': 'member',
        'sub_index': 'hall',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'errmsg': '',
        'data': {}
    }
    current_order = services.get_current_order()
    data['data']['price_buy'] = current_order['price']
    data['data']['price_sell'] = current_order['price']

    # 7天价格走势
    data['data']['pricelog'] = {
        'date': [],
        'price': []
    }
    pricelogs = CBCDPriceLog.objects.all().order_by('id')[0:7]
    for log in pricelogs:
        data['data']['pricelog']['date'].append(
            utils.dt_field_to_local(log.closing_date).strftime('%m-%d')
        )
        data['data']['pricelog']['price'].append(
            float(log.price)
        )

    # 交易状态
    data['data']['ordersell'] = UserOrderSell.objects \
        .filter(status=0) \
        .all().order_by('id')[0:5]
    data['data']['orderbuy'] = UserOrderBuy.objects \
        .all().order_by('-id')[0:5]
    return utils.crender(request, 'frontend/member/trading_hall_home.html', data)


@login_required(login_url='/login/')
def cbcd_current(request):
    data = {
        'index': 'member',
        'sub_index': 'my-cbcd',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'errmsg': '',
        'data': {}
    }
    try:
        result = UserOrderSell.objects \
            .filter(status=0).filter(seller_user=request.user) \
            .aggregate(num=Sum('num_unsell'))[0]
        sell_num = int(result.get('num'))
    except:
        sell_num = 0
    
    ubalance = services.get_balance(request.user)
    data['data']['num'] = sell_num + int(ubalance['point'])

    current_order = services.get_current_order()
    data['data']['price_buy'] = current_order['price']
    data['data']['price_sell'] = current_order['price']

    return utils.crender(request, 'frontend/member/cbcd_current.html', data)


@login_required(login_url='/login/')
def payment(request):
    if not request.GET.get('point', 0):
        return utils.ErrResp(errors.ArgMiss)
    if not request.GET.get('amount', 0):
        return utils.ErrResp(errors.MonenyNotZero)
    bonus_id = request.GET.get('bonus_id', 0)
    # 生成订单写入数据库
    upayment = UserPayment(
        user=request.user,
        amount=float(request.GET.get('amount', 0)) * settings.CURRENCY_RATIO,
        point=int(request.GET.get('point', 0)),
        currency=1,
        pay_type='CSPAY',
        ip=get_ip(request),
        request_url=settings.PAYMENT_API,
        callback=settings.SITE_URL+'member/bonus/update/?id='+bonus_id
    )
    upayment.save()

    # 组织参数及签名
    data = {
        'Amount': int(upayment.amount),
        'BillNo': upayment.order_id,
        'MerNo': settings.PAYMENT_MERNO,
        'ReturnURL': settings.PAYMENT_RETURNURL
    }
    sign = services.get_sign(data, settings.PAYMENT_KEY)
    data['MD5info'] = sign
    data['PayType'] = upayment.pay_type
    data['NotifyURL'] = settings.PAYMENT_NOTIFYURL
    data['api'] = settings.PAYMENT_API

    return utils.crender(request, 'frontend/member/payment.html', data)


@login_required(login_url='/login/')
def payment_center(request):
    if not request.GET.get('amount', 0):
        return utils.ErrResp(errors.MonenyNotZero)
    bonus_id = request.GET.get('bonus_id', 0)
    pay_type = request.GET.get('pay_type', '')
    if not pay_type:
        ubonus = UserBonus.objects.filter(user=request.user).filter(id=bonus_id).first()
        if not ubonus:
            return utils.ErrResp(errors.ArgMiss)
        if ubonus.status == 1:
            return utils.ErrResp(errors.ArgMiss)

    # 生成订单写入数据库
    upayment = UserPayment(
        user=request.user,
        amount=float(request.GET.get('amount', 0)) * settings.CURRENCY_RATIO,
        point=int(request.GET.get('point', 0)),
        currency=1,
        pay_type='CSPAY',
        ip=get_ip(request),
        request_url=settings.PAYMENT_API,
        callback=settings.SITE_URL+'member/bonus/update/?id=%s' % bonus_id
    )
    if pay_type:
        upayment.pay_type=pay_type
        upayment.callback = ''
    upayment.save()

    # 组织参数及签名
    data = {
        'Amount': int(upayment.amount),
        'BillNo': upayment.order_id,
        'MerNo': settings.PAYMENT_MERNO,
        'ReturnURL': settings.PAYMENT_RETURNURL
    }
    sign = services.get_sign(data, settings.PAYMENT_KEY)
    data['MD5info'] = sign
    data['PayType'] = upayment.pay_type
    data['NotifyURL'] = settings.PAYMENT_NOTIFYURL
    data['api'] = settings.PAYMENT_API
    data['point'] = upayment.point
    return utils.crender(request, 'frontend/member/payment_center.html', data)


@csrf_exempt
@login_required(login_url='/login/')
def payment_update(request):
    order_id = request.POST.get('order_id', '')
    if not order_id:
        return utils.ErrResp(errors.ArgMiss)
    try:
        upayment = UserPayment.objects.get(order_id=order_id)
    except:
        return utils.ErrResp(errors.DataNotExists)
    upayment.pay_type = request.POST.get('pay_type', upayment.pay_type)
    upayment.save()

    return utils.NormalResp()


@csrf_exempt
def payment_callback(request):
    MD5info = str(request.POST.get('MD5info'))
    Result = unicode(request.POST.get('Result'))
    MerRemark = str(request.POST.get('MerRemark'))
    Orderno = str(request.POST.get('Orderno'))

    params = {
        'Amount': request.POST.get('Amount'),
        'BillNo': request.POST.get('BillNo'),
        'MerNo': request.POST.get('MerNo'),
        'Succeed': request.POST.get('Succeed')
    }
    sign = services.get_sign(params, settings.PAYMENT_KEY)

    # 订单是否存在
    upayment = UserPayment.objects.filter(order_id=params['BillNo']).first()
    if upayment:
        upayment.partner_order_id = Orderno
        upayment.resp_code = '%s:%s' % (params['Succeed'], Result)
        upayment.update_at = timezone.now()
        upayment.remark = MerRemark
        upayment.save()
        # 验证签名
        if MD5info == sign:
            # 订单已成功的则不作处理
            if upayment.status != 1:
                # 验证返回信息，如成功则status=1
                if int(params['Succeed']) == 88:
                    upayment.status = 1
                else:
                    upayment.status = -1
                upayment.save()

                # 加点加钱
                if upayment.status == 1:
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
                            ubalance.cash = ubalance.cash + int(upayment.amount)/ settings.CURRENCY_RATIO
                            ubalance.total = ubalance.total + int(upayment.amount)/ settings.CURRENCY_RATIO
                        else:
                            ubalance.cash = ubalance.cash + int(upayment.amount)
                            ubalance.total = ubalance.total + int(upayment.amount)
                    ubalance.save()

                    if upayment.callback:
                        requests.get(upayment.callback, verify=False)
    return HttpResponseRedirect('/member/cbcd/current/')


@csrf_exempt
def payment_notify(request):
    MD5info = str(request.POST.get('MD5info'))
    Result = unicode(request.POST.get('Result'))
    MerRemark = str(request.POST.get('MerRemark'))
    Orderno = str(request.POST.get('Orderno'))

    params = {
        'Amount': request.POST.get('Amount'),
        'BillNo': request.POST.get('BillNo'),
        'MerNo': request.POST.get('MerNo'),
        'Succeed': request.POST.get('Succeed')
    }
    sign = services.get_sign(params, settings.PAYMENT_KEY)

    upayment = UserPayment.objects.filter(order_id=params['BillNo'])
    if upayment:
        upayment.update_at = timezone.now()
        upayment.partner_order_id = Orderno
        upayment.resp_code = '%s:%s' % (params['Succeed'], Result)
        upayment.remark = MerRemark
        upayment.save()
    
        # 验证签名
        if MD5info == sign:
            # 订单是否存在、订单已成功的则不作处理
            if upayment.status != 1:
                # 验证返回信息，如成功则status=1
                if int(Succeed) == 88:
                    upayment.status = 1
                else:
                    upayment.status = -1
                upayment.save()

                # 加点加钱
                if upayment.status == 1:
                    try:
                        ubalance = UserBalance.objects.get(user_id=upayment.user_id)
                    except:
                        ubalance = UserBalance(
                            user_id=upayment.user_id,
                            point=0
                        )
                    if upayment.point:
                        ubalance.point = ubalance.point + upayment.point
                    else:
                        if upayment.currency == 1:
                            ubalance.cash = int(params['Amount'])/ settings.CURRENCY_RATIO
                        else:
                            ubalance.cash = int(params['Amount'])
                    ubalance.save()

                    if upayment.callback:
                        requests.get(upayment.callback, verify=False)
    return HttResponse('yes')


@csrf_exempt
@login_required(login_url='/login/')
def visa_apply(request):
    hashkey = CaptchaStore.generate_key()
    captcha_url = captcha_image_url(hashkey)

    data = {
        'index': 'member',
        'sub_index': 'visa',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'hashkey': hashkey,
        'captcha_url': captcha_url,
        'ages': range(18, 61),
        'data': {},
        'errmsg': ''
    }
    if request.method == 'POST':
        try:
            exists = UserVisaApply.objects.filter(user=request.user).exists()
            if exists:
                return utils.ErrResp(errors.VisaApplyExists)

            captcha_code = request.POST.get('captcha_code', '')
            captcha_code_key = request.POST.get('captcha_code_key', '')
            cs = CaptchaStore.objects.filter(hashkey=captcha_code_key)
            true_key = cs[0].response
            print true_key, captcha_code.lower()
            if captcha_code.lower() != true_key:
                return utils.ErrResp(errors.CaptchCodeInvalid)
            CaptchaStore.objects.filter(hashkey=captcha_code_key).delete()
            uapply = UserVisaApply(
                user=request.user,
                first_name=request.POST.get('first_name', ''),
                last_name= request.POST.get('last_name', ''),
                age=request.POST.get('age', 0),
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone', ''),
                id_card=request.POST.get('id_card', ''),
                address=request.POST.get('address', ''),
                city=request.POST.get('city', ''),
                provincy=request.POST.get('provincy', ''),
                country=request.POST.get('country', ''),
                zip_code=request.POST.get('zip_code', '')
            )
            uapply.save()
            return utils.NormalResp()
        except:
            traceback.print_exc()
            return utils.ErrResp(errors.FuncFailed)
    else:
        return utils.crender(request, 'frontend/member/visa_apply.html', data)


@csrf_exempt
def find_password(request):
    hashkey = CaptchaStore.generate_key()
    captcha_url = captcha_image_url(hashkey)

    data = {
        'index': 'member',
        'sub_index': 'visa',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'hashkey': hashkey,
        'captcha_url': captcha_url,
        'ages': range(18, 61),
        'data': {},
        'errmsg': ''
    }
    if request.method == 'POST':
        try:
            captcha_code = request.POST.get('captcha_code', '')
            captcha_code_key = request.POST.get('captcha_code_key', '')
            email = request.POST.get('email', '')
            if not utils.verify_captcha(captcha_code, captcha_code_key):
                return utils.ErrResp(errors.CaptchCodeInvalid)
            try:
                u = Auth_user.objects.get(email=email)
            except:
                return utils.ErrResp(errors.EmailNotExists)
                
            uresetpwd = UserResetPwd(
                username=u.username,
                email=email
            )
            uresetpwd.save()

            # 发邮件
            resetpwd_dt = dict({
                'title': '重置密码',
                'email': email,
                'username': u.username,
                'reset_url': '/member/reset-pwd?hashkey=%s' % uresetpwd.hashkey
            })

            import email_template
            subject = email_template.resetpwd_template['subject']
            subject = subject.format(**resetpwd_dt)

            html = email_template.resetpwd_template['password']
            html = html.format(**resetpwd_dt)
            utils.mailgun_send_email([email], subject, html)
            return utils.NormalResp()
        except:
            traceback.print_exc()
            return utils.ErrResp(errors.FuncFailed)
    else:
        return utils.crender(request, 'frontend/member/find_password.html', data)


@csrf_exempt
def reset_password(request):
    hashkey = CaptchaStore.generate_key()
    captcha_url = captcha_image_url(hashkey)

    pwd_hashkey = request.GET.get('hashkey', '')
    try:
        uhashkey = UserResetPwd.objects.get(hashkey=pwd_hashkey)
    except:
        return utils.ErrResp(errors.FuncFailed)
    data = {
        'index': 'member',
        'sub_index': 'visa',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'hashkey': hashkey,
        'captcha_url': captcha_url,
        'pwd_hashkey': pwd_hashkey,
        'data': {},
        'errmsg': ''
    }
    if request.method == 'POST':
        try:
            captcha_code = request.POST.get('captcha_code', '')
            captcha_code_key = request.POST.get('captcha_code_key', '')
            pwd_hashkey = request.POST.get('pwd_hashkey', '')
            password = request.POST.get('password', '')
            if not utils.verify_captcha(captcha_code, captcha_code_key):
                return utils.ErrResp(errors.CaptchCodeInvalid)
            try:
                uhashkey = UserResetPwd.objects.get(hashkey=pwd_hashkey)
                if uhashkey.status != 0 or uhashkey.expire_at < timezone.now():
                    return utils.ErrResp(errors.FuncFailed)
                u = Auth_user.objects.get(username=uhashkey.username)
                u.set_password(password)
                u.save()

                uhashkey.update_at = timezone.now()
                uhashkey.status = 1
                uhashkey.save()
            except Exception, e:
                raise e
            return utils.NormalResp()
        except:
            traceback.print_exc()
            return utils.ErrResp(errors.FuncFailed)
    else:
        return utils.crender(request, 'frontend/member/reset_password.html', data)


@csrf_exempt
def find_username(request):
    hashkey = CaptchaStore.generate_key()
    captcha_url = captcha_image_url(hashkey)

    data = {
        'index': 'member',
        'sub_index': 'visa',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'hashkey': hashkey,
        'captcha_url': captcha_url,
        'ages': range(18, 61),
        'data': {},
        'errmsg': ''
    }
    if request.method == 'POST':
        try:
            captcha_code = request.POST.get('captcha_code', '')
            captcha_code_key = request.POST.get('captcha_code_key', '')
            email = request.POST.get('email', '')
            if not utils.verify_captcha(captcha_code, captcha_code_key):
                return utils.ErrResp(errors.CaptchCodeInvalid)
            try:
                u = Auth_user.objects.get(email=email)
            except:
                return utils.ErrResp(errors.EmailNotExists)
                
            # 发邮件
            resetpwd_dt = dict({
                'title': '找回账号',
                'email': email,
                'username': u.username
            })

            import email_template
            subject = email_template.resetpwd_template['subject']
            subject = subject.format(**resetpwd_dt)

            html = email_template.resetpwd_template['account']
            html = html.format(**resetpwd_dt)
            utils.mailgun_send_email([email], subject, html)
            return utils.NormalResp()
        except:
            traceback.print_exc()
            return utils.ErrResp(errors.FuncFailed)
    else:
        return utils.crender(request, 'frontend/member/find_username.html', data)


@csrf_exempt
def refresh_captcha(request):
    to_json_response = dict()
    to_json_response['status'] = 1
    to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
    to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
    return HttpResponse(json.dumps(to_json_response), content_type='application/json')
