# coding=utf8
import traceback
import bisect
import random
import hashlib
from django.utils import timezone
from django.db.models import Sum, Count
from django.contrib.auth.models import User as Auth_user
from dbmodel.ziben.models import UserInfo, UserBalance, UserConnection, UserRevenue, Statics, SiteSetting, CBCDInit, CBCDPriceLog,UserOrderSell, News
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
        result['balance'] = float(ubalance.cash)
        result['point'] = float(ubalance.invite_benifit)

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
        'point': 0,
        'update_time': timezone.now()
    }
    try:
        ubalance = UserBalance.objects.get(user=user)
        result['cash'] = float(ubalance.cash)
        result['invite_benifit'] = float(ubalance.invite_benifit)
        result['total_investment'] = float(ubalance.total_investment)
        result['point'] = int(ubalance.point)
        result['update_time'] = utils.dt_field_to_local(ubalance.update_time)
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
    if not cinit:
        return False
    if int(cinit.unsell) < int(point):
        cinit.status = 0
        cinit.save()
        return False
    else:
        cinit.unsell = int(cinit.unsell) - int(point)
        cinit.save()
        return True


def get_closing_price():
    pass


def get_opening_price():
    init_price = 0
    try:
         pricelog = CBCDPriceLog.objects.order_by('-id').first()
         init_price = float(pricelog.price)
    except:
        cbcdinit = CBCDInit.objects.filter(status=1).order_by('-id').first()
        if cbcdinit:
            init_price = float(cbcdinit.price)
    finally:
        return init_price


def get_init_price():
    init_price = 0
    try:
        cinit = CBCDInit.objects.filter(status=1).order_by('id').first()
        init_price = float(cinit.price)
    except:
        pass
    finally:
        return float(cinit.price)


def get_current_order():
    result = {
        'user_id': 0,
        'price': 0,
        'num': 0
    }
    try:
        order = UserOrderSell.objects \
            .filter(status=0).order_by('id').first()
        result['user_id'] = order.seller_user_id
        result['price'] = float(order.price)
        result['num'] = int(order.num_unsell)
    except:
        utils.debug()
    finally:
        return result


def is_hall_open():
    return True
    result = False
    utc_hour = timezone.now().hour
    if utc_hour <= 3 or utc_hour >= 15:
        result = True
    return result


def weighted_random(items):
    total = sum(w for _, w in items)
    n = random.uniform(0, total)
    for x, w in items:
        if n < w:
            break
        n -= w
    return x


def sorted_sict(adict): 
    keys = adict.keys() 
    keys.sort() 
    return [adict[key]  for key  in keys]


def get_sign(data, sign_key):
    try:
        result = ''
        sign_list = []
        keys = data.keys() 
        keys.sort()
        for k in keys:
            sign_list.append('%s=%s' % (k, data[k]))

        m1 = hashlib.md5()
        m1.update(sign_key)
        md5_sign_key = m1.hexdigest().upper()

        m2 = hashlib.md5()
        m2.update('&'.join(sign_list)+'&'+md5_sign_key)
        result = m2.hexdigest().upper()
    except:
        pass
    finally:
        return result

def get_news(request):
    q = News.objects
    if request.session['lang'] == 'cn':
        q = q.filter(category=1)
    else:
        q = q.filter(category=2)
    return q.order_by('-id')[0:10]

def get_sub_member_nums(user_id):
    ret = {
        'username': Auth_user.objects.filter(id=user_id).first().username,
        'user_id': user_id,
        'lnums': 0,
        'rnums': 0
    }
    q = UserConnection.objects.filter(parent_id=user_id)
    ret['lnums'] = q.filter(member_area='left').count()
    ret['rnums'] = q.filter(member_area='right').count()
    return ret

def get_most_sub_member(user_id, area='left'):
    uconnet = UserConnection.objects.filter(parent_id=user_id).first()
    if not uconnet:
        return None
    q = UserConnection.objects.filter(parent_id=user_id).filter(member_area=area).all()
    uids = [x.user_id for x in q]

    info = UserConnection.objects.filter(parent_id__in=uids).annotate(nums=Count('id')).values('parent_id').order_by('-nums').first()
    if info:
        ret = {
            'user_id': info['user_id'],
            'nums': info['nums'] if 'nums' in info else 0
        }
    else:
        info = UserConnection.objects.filter(parent_id=user_id).filter(member_area=area).first()
        if info:
            ret = {
                'user_id': info.user_id,
                'nums': 0
            }
        else:
            return None
    return ret


