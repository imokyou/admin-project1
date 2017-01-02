# coding=utf8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from lib import utils
from lib.permissions import staff_required
from django.contrib.auth.models import User as Auth_user
from dbmodel.ziben.models import SiteSetting, CBCDInit, UserOrderSell
from config import errors
from forms import InitForm, BonusForm, UserOrderSellSearchForm
from lib.pagination import Pagination


def test(request):
    return utils.NormalResp()


@login_required(login_url='/backend/login/')
@staff_required()
def home(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        q = CBCDInit.objects
        data = {
            'index': 'cbcd',
            'paging': Pagination(request, q.count()),
            'form': InitForm(),
            'inits': {
                'p': p,
                'n': n,
                'data': q.all().order_by('-id')[(p - 1) * n:p * n],
            }
        }
        if request.method == 'POST':
            data['form'] = InitForm(request.POST)
            if data['form'].is_valid():
                try:
                    CBCDInit.objects.all().update(status=0)
                except:
                    pass
                cinit = CBCDInit(
                    total=int(request.POST.get('total')),
                    unsell=int(request.POST.get('total')),
                    price=float(request.POST.get('price')),
                    status=1
                )
                cinit.save()
                return HttpResponseRedirect('/backend/cbcd/')
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/cbcd/index.html', data)


@login_required(login_url='/backend/login/')
@staff_required()
def bonus(request):
    try:
        Sseting = SiteSetting.objects.order_by('-id').first()
        data = {
            'form': BonusForm(instance=Sseting)
        }
        if request.method == 'POST':
            data['form'] = BonusForm(request.POST)
            if data['form'].is_valid():
                Sseting.bonus_switch = request.POST.get('bonus_switch')
                Sseting.bonus_50 = request.POST.get('bonus_50')
                Sseting.bonus_100 = request.POST.get('bonus_100')
                Sseting.bonus_200 = request.POST.get('bonus_200')
                Sseting.bonus_400 = request.POST.get('bonus_400')
                Sseting.bonus_600 = request.POST.get('bonus_600')
                Sseting.bonus_800 = request.POST.get('bonus_800')
                Sseting.bonus_1000 = request.POST.get('bonus_1000')
                Sseting.bonus_2000 = request.POST.get('bonus_2000')
                Sseting.save()
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/cbcd/bonus.html', data)


@login_required(login_url='/backend/login/')
@staff_required()
def order(request):
    try:
        q = UserOrderSell.objects

        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        username = request.GET.get('username', '')
        status = int(request.GET.get('status', -1))
        if username:
            try:
                u = Auth_user.objects.get(username=username)
                q = q.filter(user=u)
            except:
                pass
        if status != -1:
            q = q.filter(status=status)

        data = {
            'index': 'cbcd',
            'paging': Pagination(request, q.count()),
            'form': UserOrderSellSearchForm(),
            'orders': {
                'p': p,
                'n': n,
                'data': [],
            }
        }
        results = q.all().order_by('-id')[(p - 1) * n:p * n]
        for r in results:
            data['orders']['data'].append({
                'id': r.id,
                'order_id': r.order_id,
                'seller': r.seller_user.username,
                'price': float(r.price),
                'num': int(r.num),
                'num_unsell': int(r.num_unsell),
                'create_at': r.create_at,
                'status': r.status
            })
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/cbcd/order.html', data)
