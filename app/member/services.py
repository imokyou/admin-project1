# coding=utf8
import traceback
import bisect
import random
from django.utils import timezone
from django.db.models import Sum
from dbmodel.ziben.models import UserInfo, UserBalance, UserConnection, UserRevenue, Statics, SiteSetting, CBCDInit
from lib import utils


def get_statics(user_id):
    result = {
        'recommend_users': 0,
        'balance': 0,
        'point': 0,
        'member': 0,
        'online': 0,
        'total_paid': 0
    }
    result['recommend_users'] = UserConnection.objects \
        .filter(parent_id=user_id).count()
    ubalance = UserBalance.objects.filter(user_id=user_id).first()
    if ubalance:
        result['balance'] = float(ubalance.total)
        result['point'] = ubalance.point

    stat = Statics.objects.order_by('-id').first()
    result['member'] = stat.members
    result['online'] = stat.online
    result['total_paid'] = float(stat.total_paid)
    return result


def get_recommends(user):
    try:
        result = UserInfo.objects \
            .filter(recommend_user=user.username).count()
    except:
        result = 0
    finally:
        return result


def get_invite_benifit(user):
    try:
        q = UserRevenue.objects \
            .filter(parent_user_id=user.id)
        result = q.aggregate(revenue_promote=Sum('revenue_promote'))
        revenue_promote = float(result.get('revenue_promote', 0))
    except:
        revenue_promote = 0
    finally:
        return revenue_promote


def get_balance(user):
    result = {
        'cash': 0,
        'invite_benifit': 0,
        'total_investment': 0,
        'update_time': timezone.now()
    }
    try:
        ubalance = UserBalance.objects.get(user=user)
        result['cash'] = float(ubalance.cash)
        result['invite_benifit'] = float(ubalance.invite_benifit)
        result['total_investment'] = float(ubalance.total_investment)
        result['update_time'] = utils.dt_field_to_local(ubalance.create_time)
    except:
        traceback.print_exc()
        pass
    finally:
        return result


def pay_cash(user, should_pay):
    result = False
    try:
        try:
            ubalance = get_balance(user)
            ucash = float(ubalance['cash'])
        except:
            ucash = 0
        rcash = ucash - should_pay
        if rcash >= 0:
            UserBalance.objects \
                .filter(user_id=user.id) \
                .update(cash=rcash)
            result = True
    except Exception, e:
        traceback.print_exc()
        raise e
    finally:
        return result


def get_price():
    return 0.3


# 扣除资本兑
def cbcd_reduce(point):
    cinit = CBCDInit.objects.filter(status=1).order_by('id').first()
    if int(cinit.unsell) < int(point):
        cinit.status = 0
        cinit.save()
        return False
    else:
        cinit.unsell = int(cinit.unsell) - int(point)
        cinit.save()
        return True


def weighted_random(items):
    total = sum(w for _, w in items)
    n = random.uniform(0, total)
    for x, w in items:
        if n < w:
            break
        n -= w
    return x
