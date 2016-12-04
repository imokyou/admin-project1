# coding: utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from lib import utils
from lib.pagination import Pagination
from lib.permissions import staff_required
from config import errors
from dbmodel.ziben.models import Projects
from forms import SearchForm, CreateForm, EditForm


@csrf_exempt
def test(request):
    return utils.NormalResp()


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def home(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        name = request.GET.get('name', '')
        status = int(request.GET.get('status', -1))

        q = Projects.objects
        if status != -1:
            q = q.filter(status=status)
        if name:
            q = q.filter(name__icontains=name)

        form = SearchForm(initial={'status': status, 'name': name})
        data = {
            'index': 'admin',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'project_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        projects = q.all().order_by('-id')[(p - 1) * n:p * n]
        for p in projects:
            try:
                create_time = utils.dt_field_to_local(p.create_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                create_time = ''
            data['project_list']['data'].append({
                'id': p.id,
                'name': p.name,
                'total': p.total,
                'price': float(p.price),
                'status': p.status,
                'status_name': Projects.STATUS[p.status],
                'create_time': create_time
            })
        return render(request, 'backend/project/list.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def create(request):
    try:
        data = {
            'msg': '',
            'index': 'project',
            'form': CreateForm(request.POST)
        }
        if request.method == 'POST':
            name = request.POST.get('name', '')
            description = request.POST.get('description', '')
            try:
                price = float(request.POST.get('price', 0))
            except:
                price = 0
            try:
                total = int(request.POST.get('total', 0))
            except:
                total = 0
            if not name:
                data['msg'] = '项目名称不能为空'
            else:
                project = Projects(
                    name=name,
                    price=price,
                    total=total,
                    description=description,
                    status=1
                )
                project.save()
                data['msg'] = '项目创建成功'
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/project/create.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def edit(request):
    try:
        project_id = request.GET.get('id', '')
        form = EditForm()
        if project_id:
            try:
                u = Projects.objects.get(id=project_id)
                form_initial = {
                    'name': u.name,
                    'status': u.status,
                    'description': u.description,
                    'price': u.price,
                    'total': u.total
                }
                form = EditForm(initial=form_initial)
            except:
                pass
        data = {
            'msg': '',
            'index': 'project',
            'form': form,
            'project_id': project_id
        }
        if request.method == 'POST':
            name = request.POST.get('name', '')
            description = request.POST.get('description', '')
            try:
                status = int(request.POST.get('status', 1))
            except:
                status = 1
            try:
                total = int(request.POST.get('total', 0))
            except:
                total = 0
            try:
                price = float(request.POST.get('price', 0))
            except:
                price = 0

            if not name:
                data['msg'] = '项目名称不能为空'
            else:
                u_exists = Projects.objects.filter(name=name).exists()
                if not u_exists:
                    data['msg'] = '项目不存在'
                else:
                    u = Projects.objects.get(name=name)
                    u.status = status
                    u.price = price
                    u.total = total
                    u.description = description
                    u.save()
                    data['msg'] = '修改成功'
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/project/edit.html', data)
