# coding: utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from lib import utils
from lib.pagination import Pagination
from lib.permissions import staff_required
from config import errors
from dbmodel.ziben.models import InviteCode
from forms import SearchForm, QuickJumpForm



@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def home(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        code = request.GET.get('code', '')
        status = int(request.GET.get('status', -1))

        q = InviteCode.objects
        if status != -1:
            q = q.filter(status=status)
        if code:
            q = q.filter(code=code)

        form = SearchForm(initial={'status': status, 'code': code})
        quick_jump_form = QuickJumpForm(initial={'status': status, 'code': code, 'p': p, 'n': n})
        data = {
            'index': 'admin',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'quick_jump_form': quick_jump_form,
            'code_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        codes = q.all().order_by('-id')[(p - 1) * n:p * n]
        for c in codes:
            try:
                update_time = utils.dt_field_to_local(c.update_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                update_time = ''
            data['code_list']['data'].append({
                'id': c.id,
                'code': c.code,
                'status': c.status,
                'status_name': InviteCode.STATUS[c.status],
                'update_time': update_time
            })
        return render(request, 'backend/invite_code.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@staff_required()
def test(request):
    code = InviteCode.objects.pop()
    d = {'code': code}
    return utils.NormalResp(d)
