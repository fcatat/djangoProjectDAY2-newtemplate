from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.form import *
from django.forms.models import model_to_dict
from django.db.models import Q


def password_management_list(request):
    form = PasswordManagementModelForm
    value = request.GET.get('q', "")

    order_by = request.GET.get("orderby")
    if order_by is None:
        order_by = "-id"

    queryset = models.PasswordManagement.objects.filter(
        Q(url__icontains=value) | Q(username__icontains=value) | Q(remark__icontains=value)).order_by(order_by)
    total = models.PasswordManagement.objects.count()
    paginator = Paginator(queryset, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/password_management_list.html',
                  {'form': form, 'queryset': queryset, 'value': value, 'page_obj': page_obj, 'total': total})


def password_management_details(request):
    nid = request.GET.get("nid")
    row_dict = models.PasswordManagement.objects.filter(id=nid).values("url", "username", "password", "remark",
                                                                       "update_user",
                                                                       "create_time", "update_time").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def password_management_add(request):
    form = PasswordManagementModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        '''审计功能'''
        url = request.POST.get("url")
        user = request.user
        msg = "由 %s 用户创建" % user
        models.PasswordManagementRecord.objects.create(url=url, msg=msg)
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})


@csrf_exempt
def password_management_edit(request):
    nid = request.GET.get("nid")
    row_object = models.PasswordManagement.objects.filter(id=nid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在"})
    original_data = models.PasswordManagement.objects.filter(id=nid).first()
    form = PasswordManagementEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        """审计功能"""
        url = models.PasswordManagement.objects.filter(id=nid).values("url")
        new_data = models.PasswordManagement.objects.filter(id=nid).first()
        diff = model_to_dict(new_data).items() - model_to_dict(original_data).items()
        user = request.user
        msg = "用户 %s 将源数据 %s 变更了 %s" % (user, model_to_dict(original_data), diff)
        models.PasswordManagementRecord.objects.create(url=url, msg=msg)
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


@csrf_exempt
def password_management_delete(request):
    nid = request.GET.get("nid")
    exists = models.PasswordManagement.objects.filter(id=nid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "数据不存在"})
    """审计功能"""
    url = models.PasswordManagement.objects.filter(id=nid).values("url")
    content = models.PasswordManagement.objects.filter(id=nid).first()
    content_dict = model_to_dict(content)
    user = request.user
    msg = "用户 %s 删除了 %s" % (user, content_dict)
    models.PasswordManagementRecord.objects.create(url=url, msg=msg)
    """删除记录"""
    models.PasswordManagement.objects.filter(id=nid).delete()
    return JsonResponse({"status": True})


def password_management_record(request):
    form = PasswordManagementRecordModelForm
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["url__contains"] = value
    order_by = request.GET.get("orderby")
    if order_by is None:
        order_by = "-id"

    queryset = models.PasswordManagementRecord.objects.filter(**data_dict).order_by(order_by)
    total = models.PasswordManagementRecord.objects.count()
    paginator = Paginator(queryset, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/password_management_record.html',
                  {'form': form, 'queryset': queryset, 'value': value, 'page_obj': page_obj, 'total': total})
