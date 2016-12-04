# coding=utf8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from dbmodel.ziben.models import News, NewsCategory
from config import errors
from lib import utils
from lib.pagination import Pagination
from lib.permissions import staff_required
from forms import CateCreateForm, CateSearchForm, CateEditForm, SearchForm, CreateForm, EditForm


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
        title = request.GET.get('title', '')

        try:
            category = int(request.GET.get('category', -1))
        except:
            category = -1
        try:
            status = int(request.GET.get('status', -1))
        except:
            status = -1
        q = News.objects
        if status != -1:
            q = q.filter(status=status)
        if category != -1:
            q = q.filter(category=category)
        if title:
            q = q.filter(title__icontains=title)

        form_initial = {'status': status,
                        'category': category,
                        'title': title}
        form = SearchForm(initial=form_initial)
        data = {
            'index': 'news',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'news_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        newslist = q.all().order_by('-id')[(p - 1) * n:p * n]
        for p in newslist:
            try:
                create_time = utils.dt_field_to_local(p.create_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                create_time = ''
            data['news_list']['data'].append({
                'id': p.id,
                'title': p.title,
                'category_id': p.category.id,
                'category_name': p.category.name,
                'status': p.status,
                'status_name': News.STATUS[p.status],
                'create_time': create_time
            })
        return render(request, 'backend/news/list.html', data)
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
            'index': 'news',
            'form': CreateForm(request.POST)
        }
        if request.method == 'POST':
            title = request.POST.get('title', '')
            content = request.POST.get('content', '')
            try:
                category = int(request.POST.get('category', 0))
            except:
                category = 0

            if not title:
                data['msg'] = '标题不能为空'
            elif not category:
                data['msg'] = '分类不能为空'
            else:
                cate = News(
                    title=title,
                    content=content,
                    category_id=category
                )
                cate.save()
                data['msg'] = '创建成功'
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/news/create.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def edit(request):
    try:
        data = {
            'msg': '',
            'index': 'news',
            'form': '',
            'news_id': ''
        }
        if request.method == 'POST':
            news_id = request.POST.get('id', '')
            title = request.POST.get('title', '')
            content = request.POST.get('content', '')
            try:
                status = int(request.POST.get('status', 1))
            except:
                status = 1
            try:
                category = int(request.POST.get('category', 1))
            except:
                category = 1
            if not title:
                data['msg'] = '标题不能为空'
            else:
                u_exists = News.objects.filter(id=news_id).exists()
                if not u_exists:
                    data['msg'] = '资讯不存在'
                else:
                    u = News.objects.get(id=news_id)
                    u.title = title
                    u.content = content
                    u.category_id = category
                    u.status = status
                    u.save()
                    data['msg'] = '修改成功'
        news_id = request.GET.get('id', '')
        if news_id:
            form = EditForm()
            try:
                u = News.objects.get(id=news_id)
                form_initial = {
                    'id': u.id,
                    'title': u.title,
                    'category': u.category_id,
                    'content': u.content,
                    'status': u.status,
                }
                form = EditForm(initial=form_initial)
            except:
                pass
            data['form'] = form
            data['news_id'] = news_id

    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/news/edit.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def category_home(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 25))
        name = request.GET.get('name', '')
        status = int(request.GET.get('status', -1))

        q = NewsCategory.objects
        if status != -1:
            q = q.filter(status=status)
        if name:
            q = q.filter(name__icontains=name)

        form = CateSearchForm(initial={'status': status, 'name': name})
        data = {
            'index': 'news',
            'paging': Pagination(request, q.count()),
            'forms': form,
            'cate_list': {
                'p': p,
                'n': n,
                'data': [],
            }
        }

        cates = q.all().order_by('-id')[(p - 1) * n:p * n]
        for p in cates:
            try:
                create_time = utils.dt_field_to_local(p.create_time) \
                    .strftime('%Y-%m-%d %H:%M:%S')
            except:
                create_time = ''
            data['cate_list']['data'].append({
                'id': p.id,
                'name': p.name,
                'status': p.status,
                'status_name': NewsCategory.STATUS[p.status],
                'create_time': create_time
            })
        return render(request, 'backend/news/category_list.html', data)
    except:
        import traceback
        traceback.print_exc()
        return utils.ErrResp(errors.FuncFailed)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def category_create(request):
    try:
        data = {
            'msg': '',
            'index': 'news',
            'form': CateCreateForm(request.POST)
        }
        if request.method == 'POST':
            name = request.POST.get('name', '')
            if not name:
                data['msg'] = '名称不能为空'
            else:
                cate = NewsCategory(
                    name=name
                )
                cate.save()
                data['msg'] = '创建成功'
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/news/category_create.html', data)


@csrf_exempt
@login_required(login_url='/backend/login/')
@staff_required()
def category_edit(request):
    try:
        data = {
            'msg': '',
            'index': 'news',
            'form': '',
            'cate_id': ''
        }
        if request.method == 'POST':
            cate_id = int(request.POST.get('id', ''))
            name = request.POST.get('name', '')
            try:
                status = int(request.POST.get('status', 1))
            except:
                status = 1
            if not name:
                data['msg'] = '名称不能为空'
            else:
                u_exists = NewsCategory.objects.filter(id=cate_id).exists()
                if not u_exists:
                    data['msg'] = '分类不存在'
                else:
                    u = NewsCategory.objects.get(id=cate_id)
                    u.name = name
                    u.status = status
                    u.save()
                    data['msg'] = '修改成功'

        cate_id = request.GET.get('id', '')
        form = CateEditForm()
        if cate_id:
            try:
                u = NewsCategory.objects.get(id=cate_id)
                form_initial = {
                    'id': u.id,
                    'name': u.name,
                    'status': u.status,
                }
                form = CateEditForm(initial=form_initial)
            except:
                pass
        data['form'] = form
        data['cate_id'] = cate_id
    except:
        utils.debug()
        return utils.ErrResp(errors.FuncFailed)
    return render(request, 'backend/news/category_edit.html', data)
