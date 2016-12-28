# coding=utf8
import traceback
import bisect
import random
from django.utils import timezone
from django.db.models import Sum
from dbmodel.ziben.models import UserInfo, UserBalance, UserConnection, UserRevenue, Statics, SiteSetting
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


def weighted_random(items):  
    total = sum(w for _,w in items)  
    n = random.uniform(0, total)#在饼图扔骰子  
    for x, w in items:#遍历找出骰子所在的区间  
        if n<w:  
            break  
        n -= w  
    return x 


class WeightRandom:  
    def __init__(self, items):  
        weights = [w for _,w in items]  
        self.goods = [x for x,_ in items]  
        self.total = sum(weights)  
        self.acc = list(self.accumulate(weights))  
  
    #累和.如accumulate([10,40,50])->[10,50,100]
    def accumulate(self, weights):   
        cur = 0  
        for w in weights:  
            cur = cur+w  
            yield cur  
  
    def __call__(self):  
        return self.goods[bisect.bisect_right(self.acc , random.uniform(0, self.total))]