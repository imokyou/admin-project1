# coding=utf8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lib import utils
from lib.permissions import staff_required
from dbmodel.ziben.models import Statics, SiteSetting
from config import errors
from forms import EditForm, SsetingEditForm


def test(request):
    return utils.NormalResp()


@login_required(login_url='/backend/login/')
@staff_required()
def home(request):
    try:
        stat = Statics.objects.order_by('-id').first()
        data = {
            'form': EditForm(instance=stat)
        }
        if request.method == 'POST':
            data['form'] = EditForm(request.POST)
            if data['form'].is_valid():
                stat.members = request.POST.get('members')
                stat.online = request.POST.get('online')
                stat.hits = request.POST.get('hits')
                stat.total_paid = request.POST.get('total_paid')
                stat.offers = request.POST.get('offers')
                stat.pts_value = request.POST.get('pts_value')
                stat.ptc_value = request.POST.get('ptc_value')
                stat.save()
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/statics/index.html', data)


@login_required(login_url='/backend/login/')
@staff_required()
def common_setting(request):
    try:
        Sseting = SiteSetting.objects.order_by('-id').first()
        data = {
            'form': SsetingEditForm(instance=Sseting)
        }
        if request.method == 'POST':
            data['form'] = SsetingEditForm(request.POST)
            if data['form'].is_valid():
                Sseting.user_buy_price = request.POST.get('user_buy_price')
                Sseting.save()
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/statics/site_setting.html', data)
