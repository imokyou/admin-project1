# coding=utf8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, logout as auth_logout
from django.contrib.auth.models import User as Auth_user
from django.db.models import Count
from dbmodel.ziben.models import UserOplog, News, UserMessage, UserPromoteRank, UserInfo, UserBalance, UserConnection, UserSellingMall, UserConnectionBuying, UserChangeRecommend, UserWithDraw, SiteSetting
from lib import utils
from lib.pagination import Pagination
from forms import ChatForm, ChangeRecommendForm, ChangePwdForm, ChangeUserInfoForm, WithDrawForm
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


@login_required(login_url='/login/')
def promotion(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {
            'uconnect': []
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

    return render(request, 'frontend/member/promotion.html', data)


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
        user_id = request.POST.get('user_id')
        mall = UserSellingMall(
            user_id=user_id,
            parent_user=request.user
        )
        mall.save()

        UserConnection.objects \
            .filter(user_id=user_id).update(is_selling=1)
        return HttpResponseRedirect('/member/selling/')

    return render(request, 'frontend/member/selling.html', data)


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
        if services.pay_cash(request.user, int(ssetings.user_buy_price)):
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
            data['errmsg'] = '余额不足，请充值'

    return render(request, 'frontend/member/buying.html', data)


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
            recommend_username = request.POST.get('username')
            unifo = UserInfo.objects.get(user=request.user)
            if recommend_username == request.user.username:
                data['errmsg'] = '不能把自己设置为转介人'
            elif recommend_username == unifo.recommend_user:
                data['errmsg'] = '%s已经是你的当前推荐人' % recommend_username
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

    return render(request, 'frontend/member/change_recommend_user.html', data)


@login_required(login_url='/login/')
def setting(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'changePwdForm': ChangePwdForm(),
        'changeInfoForm': ChangeUserInfoForm(),
        'data': {
            'userinfo': {}
        },
        'errmsg': ''
    }
    if request.method == 'POST':
        if request.POST.get('ctype') == 'changepwd':
            data['changePwdForm'] = ChangePwdForm(request.POST)
            if data['changePwdForm'].is_valid():
                user = authenticate(username=request.user.username,
                                    password=request.POST['password'])
                if not user:
                    data['errmsg'] = '原密码输入有误'
                else:
                    u = Auth_user.objects.get(username=request.user.username)
                    u.set_password(request.POST['new_password'])
                    u.save()
                    auth_logout(request)
                    return HttpResponseRedirect('/login/')
        elif request.POST.get('ctype') == 'changinfo':
            data['changeInfoForm'] = ChangeUserInfoForm(request.POST)
            if data['changeInfoForm'].is_valid():
                pass

    return render(request, 'frontend/member/settings.html', data)


@login_required(login_url='/login/')
def dashboard(request):
    weekday2name = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {}
    }
    curr_weekday = timezone.now().weekday()
    data['data']['curr_weekday'] = weekday2name[curr_weekday]
    data['data']['invite_users'] = UserConnection.objects \
        .filter(parent=request.user).count()
    data['data']['buy_users'] = UserConnectionBuying.objects \
        .filter(parent=request.user).count()
    data['data']['total_users'] = data['data']['invite_users'] + data['data']['buy_users']
    data['data']['balance'] = services.get_balance(request.user)
    return render(request, 'frontend/member/dashboard.html', data)


@login_required(login_url='/login/')
def us_bank_account(request):
    data = {
        'index': 'member',
        'sub_index': 'deposite',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'data': {}
    }
    return render(request, 'frontend/member/us_bank_account.html', data)


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
    data['form'] = WithDrawForm(initial={'cash': ubalance['cash']})

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
                        amount=float(request.POST.get('amount'))
                    )
                    udraw.save()

                    return HttpResponseRedirect('/member/withdraw/')
                else:
                    data['errmsg'] = '余额不足'
            else:
                data['errmsg'] = '密码不正确'

    return render(request, 'frontend/member/withdraw.html', data)
