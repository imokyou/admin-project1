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
        date_joined = utils.dt_field_to_local(uparent.parent.date_joined) \
            .strftime('%Y-%m-%d %H:%M:%S')
    except:
        date_joined = ''
    try:
        last_login = utils.dt_field_to_local(uparent.parent.last_login) \
            .strftime('%Y-%m-%d %H:%M:%S')
    except:
        last_login = ''
    parent_info = {
        'id': uparent.parent.id,
        'username': uparent.parent.username,
        'email': uparent.parent.email,
        'first_name': uparent.parent.first_name,
        'last_name': uparent.parent.last_name,
        'date_joined': date_joined,
        'last_login': last_login,
        'reg_ip': '',
        'cash': 0,
        'invite_benifit': 0,
        'total_amount': 0
    }
    try:
        uinfo = UserInfo.objects.get(user=uparent.parent)
        parent_info['reg_ip'] = uinfo.reg_ip
    except:
        pass
    try:
        ubalance = UserBalance.objects.get(user=uparent.parent)
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
            date_joined = utils.dt_field_to_local(u.user.date_joined) \
                .strftime('%Y-%m-%d %H:%M:%S')
        except:
            date_joined = ''
        try:
            last_login = utils.dt_field_to_local(u.user.last_login) \
                .strftime('%Y-%m-%d %H:%M:%S')
        except:
            last_login = ''
        d = {
            'id': u.user.id,
            'username': u.user.username,
            'email': u.user.email,
            'first_name': u.user.first_name,
            'last_name': u.user.last_name,
            'date_joined': date_joined,
            'last_login': last_login,
            'reg_ip': '',
            'cash': 0,
            'invite_benifit': 0,
            'total_amount': 0
        }
        try:
            uinfo = UserInfo.objects.get(user=u.user)
            d['reg_ip'] = uinfo.reg_ip
        except:
            pass
        try:
            ubalance = UserBalance.objects.get(user=u.user)
            d['cash'] = float(ubalance.ubalance)
            d['invite_benifit'] = float(ubalance.invite_benifit)
            d['total_amount'] = float(ubalance.total)
        except:
            pass
        childs.append(d)
    return childs
