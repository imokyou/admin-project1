# coding=utf8
from ipware.ip import get_ip
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, logout as auth_logout
from django.contrib.auth.models import User as Auth_user
from django.db.models import Count, Sum
from dbmodel.ziben.models import UserOplog, News, UserMessage, UserPromoteRank, UserInfo, UserBalance, UserConnection, UserSellingMall, UserConnectionBuying, UserChangeRecommend, UserWithDraw, SiteSetting, UserBonus, CBDCPriceLog, UserOrder, CBCDInit
from lib import utils
from lib.pagination import Pagination
from forms import ChatForm, ChangeRecommendForm, ChangePwdForm, ChangeUserInfoForm, WithDrawForm
import services
from config import errors


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
        'index': 'member_seller',
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


@csrf_exempt
@login_required(login_url='/login/')
def bonus(request):
    data = {
        'index': 'member',
        'sub_index': 'bonus',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }

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
            ubonus = UserBonus.objects \
                .filter(user=request.user).first()
            if ubonus:
                if ubonus.status == 1:
                    return utils.ErrResp(errors.BonusExists)
                point = ubonus.point
                level = b2c['bonus_%s' % point]
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
                'money': int(point*services.get_price())
            }
            return utils.NormalResp(resp)

    return render(request, 'frontend/member/bonus.html', data)


@login_required(login_url='/login/')
def cbcd_price(request):
    data = {
        'index': 'member',
        'sub_index': 'home',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10]
    }

    n = 20
    p = request.GET.get('p', 1)
    q = CBDCPriceLog.objects
    data['pricelist'] = {
        'tot': q.count(),
        'paging': Pagination(request, q.count()),
        'data': q.all().order_by('-id')[(p - 1) * n:p * n]
    }

    return render(request, 'frontend/member/CBCD_price_log.html', data)


@csrf_exempt
@login_required(login_url='/login/')
def cbcd_sell(request):
    if request.method == 'POST':
        num = int(request.POST.get('num'))
        price = float(request.POST.get('price'))
        try:
            ubalance = UserBalance.objects.get(user=request.user)
        except:
            return utils.ErrResp(errors.CBCDLimit)
        if not ubalance.point or int(ubalance.point) < num:
            return utils.ErrResp(errors.CBCDLimit)
        ubalance.point = ubalance.point - num
        ubalance.save()
        uorder = UserOrder(
            seller_user=request.user,
            buyer_user_id=0,
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
        num = int(request.POST.get('num', 0))
        price = float(request.POST.get('price', 0))

        if not num or not price:
            return utils.ErrResp(errors.ArgMiss)

        result = UserOrder.objects.filter(status=0) \
            .aggregate(total=Sum('num_unsell'))

        if num > int(result.get('total', 0)):
            return utils.ErrResp(errors.CBCDLimit)

        # 付款
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

        # 更新订单状态和收钱
        uorders = UserOrder.objects.filter(status=0).order_by('id')
        unpaid_num = num
        for order in uorders:
            seller = UserBalance.objects.get(user_id=order.seller_user_id)
            if order.num_unsell <= unpaid_num:
                unpaid_num = unpaid_num - order.num_unsell
                order.status = 1
                order.num_unsell = 0
                order.save()

                seller.cash = float(seller.cash) + float(order.num*order.price)
                seller.save()
            else:
                order.num_unsell = order.num_unsell - unpaid_num
                order.save()

                seller.cash = float(seller.cash) + float(unpaid_num*order.price)
                seller.save()
                break
            
        return utils.NormalResp()

@login_required(login_url='/login/')
def trading_hall(request, ctype):
    data = {
        'index': 'member',
        'sub_index': 'deposite',
        'statics': services.get_statics(request.user.id),
        'news': News.objects.all().order_by('-id')[0:10],
        'errmsg': '',
        'ctype': ctype,
        'data': {}
    }

    result = UserOrder.objects.filter(status=0) \
        .aggregate(total=Sum('num_unsell'))
    try:
        
        data['data']['total'] = int(result.get('total', 0))
    except:
        data['data']['total'] = 0
    
    cinit = CBCDInit.objects.filter(status=1).order_by('id').first()
    data['data']['price_init'] = float(cinit.price)
    data['data']['price'] = float(cinit.price)
    if ctype == 'sell':
        ubalance = services.get_balance(request.user)
        data['data']['point'] = ubalance['point']
    else:
        data['data']['point'] = 0

    return render(request, 'frontend/member/trading_hall.html', data)
