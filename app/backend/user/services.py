# coding=utf8
from dbmodel.ziben.models import UserInfo, UserBalance, UserConnection
from lib import utils


def _get_parent_info(user_id):
    parent_info = {}
    parent_exists = UserConnection.objects \
        .filter(user_id=user_id).filter(parent_id__gt=0) \
        .exists()
    if not parent_exists:
        return parent_info
    uparent = UserConnection.objects \
        .filter(user_id=user_id).filter(parent_id__gt=0) \
        .first()
    try:
        date_joined = utils.dt_field_to_local(uparent.date_joined) \
            .strftime('%Y-%m-%d %H:%M:%S')
    except:
        date_joined = ''
    try:
        last_login = utils.dt_field_to_local(uparent.last_login) \
            .strftime('%Y-%m-%d %H:%M:%S')
    except:
        last_login = ''
    parent_info = {
        'id': uparent.id,
        'username': uparent.username,
        'email': uparent.email,
        'first_name': uparent.first_name,
        'date_joined': date_joined,
        'last_login': last_login,
        'reg_ip': '',
        'cash': 0,
        'invite_benifit': 0,
        'total_amount': 0
    }
    try:
        uinfo = UserInfo.objects.get(user=uparent)
        parent_info['reg_ip'] = uinfo.reg_ip
    except:
        pass
    try:
        ubalance = UserBalance.objects.get(user=uparent)
        parent_info['cash'] = float(ubalance.ubalance)
        parent_info['invite_benifit'] = float(ubalance.invite_benifit)
        parent_info['total_amount'] = float(ubalance.total)
    except:
        pass
    return parent_info


def _get_childs(user_id):
    childs = []
    uchilds = UserConnection.objects.filter(parent_id=user_id)
    for u in uchilds:
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
            d['reg_ip'] = uinfo.reg_ip
        except:
            pass
        try:
            ubalance = UserBalance.objects.get(user=u)
            d['cash'] = float(ubalance.ubalance)
            d['invite_benifit'] = float(ubalance.invite_benifit)
            d['total_amount'] = float(ubalance.total)
        except:
            pass
        childs.append(d)
    return childs
