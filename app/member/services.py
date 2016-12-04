# coding=utf8
from dbmodel.ziben.models import UserBalance, UserConnection, Statics


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
