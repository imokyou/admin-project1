# coding=utf8
from ipware.ip import get_ip
from django.contrib.auth.models import User as Auth_user
from django.utils import timezone
from dbmodel.ziben.models import UserInfo, UserConnection, UserBalance


def _get_reg_params(request):
    params = {}
    params['first_name'] = request.POST.get('first_name', '')
    params['last_name'] = request.POST.get('last_name', '')
    params['username'] = request.POST.get('username', '')
    params['password'] = request.POST.get('password', '')
    params['confirm_password'] = request.POST.get('confirm_password', '')
    params['email'] = request.POST.get('email', '')
    params['phone_number'] = request.POST.get('phone_number', '')
    params['address1'] = request.POST.get('address1', '')
    params['address2'] = request.POST.get('address2', '')
    params['city'] = request.POST.get('city', '')
    params['provincy'] = request.POST.get('provincy', '')
    params['country'] = request.POST.get('country', '')
    params['zip_code'] = request.POST.get('zip_code', '')
    params['sexal'] = request.POST.get('sexal', '')
    params['age'] = request.POST.get('age', '')
    params['recommend_user'] = request.POST.get('recommend_user', '')
    params['member_area'] = request.POST.get('member_area', 'left')

    return params


def reg(request):
    '''会员注册
    @param1:  form
    @return: boolean True/False
    '''
    data = request.POST
    u = Auth_user.objects.create_user(data['username'],
                                      data['email'],
                                      data['password'])
    u.first_name = data['first_name']
    u.last_name = data['last_name']
    u.save()

    unifo = UserInfo(
        user=u,
        pwd=data['password'],
        phone_number=data['phone'],
        address1=data['address1'],
        address2=data['address2'],
        city=data['city'],
        provincy=data['provincy'],
        country=data['country'],
        zip_code=data['zip_code'],
        recommend_user=data['recommend_user'],
        sexal=data['sexal'],
        age=data['age'],
        reg_time=timezone.now(),
        reg_ip=get_ip(request),
        reg_code='',
        member_area=data['member_area']
    )
    if data['recommend_user']:
        unifo.reg_type = 2
    unifo.save()

    if data['recommend_user']:
        try:
            u_parent = Auth_user.objects.get(username=data['recommend_user'])
            u_parent_grid = UserConnection.objects \
                .filter(user_id=u_parent.id).first()
            user_grid = UserConnection(
                parent_id=u_parent.id,
                user_id=u.id,
                depth=0,
                create_time=timezone.now(),
                ratio=100
            )
            if u_parent_grid:
                user_grid.depth = u_parent_grid.depth + 1
            user_grid.save()
        except:
            pass

    # 写余额表
    ubalance = UserBalance(
        user=u,
        cash=0,
        invite_benifit=0,
        total=0,
        point=0,
        revenue_promote=0,
        total_investment=0
    )
    ubalance.save()
    return True
