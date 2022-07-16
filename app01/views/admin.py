from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import AdminModelForm, AdminModelEditForm, AdminModelResetForm
from django.core.paginator import Paginator
from django.contrib.messages.views import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def admin_list(request):
    form = AdminModelForm()
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["username__contains"] = value
    order_by = request.GET.get("orderby")
    if order_by is None:
        order_by = "-id"

    queryset = models.Admin.objects.filter(**data_dict).order_by(order_by)
    total = models.Admin.objects.count()
    paginator = Paginator(queryset, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/admin_list.html',
                  {'form': form, 'queryset': queryset, 'value': value, 'page_obj': page_obj, 'total': total})


# def admin_add(request):
#     button_value = "Add New Admin"
#     if request.method == "GET":
#         form = AdminModelForm()
#         return render(request, 'home/change_template.html', {"button_value": button_value, 'form': form})
#     form = AdminModelForm(data=request.POST)
#     if form.is_valid():
#         form.save()
#         messages.success(request, "<< %s >> has been Added" % request.POST.get('username'))
#         return redirect('/admin/list/')
#     return render(request, 'home/change_template.html', {"button_value": button_value, "form": form})
@csrf_exempt
def admin_add(request):
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def admin_edit(request, nid):
    """"""
    value = "编辑管理员"
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'old/error.html', {"msg": "ID错误"})

    if request.method == "GET":
        form = AdminModelEditForm(instance=row_object)
        return render(request, 'home/change_template.html',
                      {"form": form, "value": value})
    form = AdminModelEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'home/change_template.html', {"form": form, "value": value})


def admin_delete(request, nid):
    row_object = models.Admin.objects.filter(id=nid).exists()
    if not row_object:
        return render(request, 'old/error.html', {'msg': "ID错误"})
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    """"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'old/error.html', {"msg": "ID错误"})
    value = "重置{}密码".format(row_object.username)
    if request.method == "GET":
        form = AdminModelResetForm()
        return render(request, 'old/change.html', {"value": value, "form": form})
    form = AdminModelResetForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'old/change.html', {"value": value, "form": form})
