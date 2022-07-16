from django.shortcuts import render, redirect
from django.contrib.messages.views import messages
from django.core.paginator import Paginator
from app01 import models
from app01.utils.form import AssetsModelForm
from app01.utils.collection_assets.tasks import process
from notifications.signals import notify


def assets_list(request):
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["ipv4__contains"] = value
    order_by = request.GET.get("orderby")
    if order_by is None:
        order_by = "-id"

    queryset = models.AssetsInfo.objects.filter(**data_dict).order_by(order_by)
    total = models.AssetsInfo.objects.count()
    paginator = Paginator(queryset, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/assets_list.html',
                  {'queryset': queryset, 'value': value, 'page_obj': page_obj, 'total': total})


def assets_add(request):
    button_value = "Add New Assets"
    if request.method == "GET":
        form = AssetsModelForm()
        return render(request, 'home/change_template.html', {"button_value": button_value, "form": form})
    form = AssetsModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/assets/list/')

    return render(request, 'home/change_template.html', {"button_value": button_value, "form": form})


def assets_edit(request, nid):
    button_value = "edit"
    row_object = models.AssetsInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AssetsModelForm(instance=row_object)
        return render(request, 'home/change_template.html', {'form': form, "button_value": button_value})
    form = AssetsModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/assets/list/')
    return render(request, 'home/change_template.html', {"form": form, "button_value": button_value})


def assets_delete(request, nid):
    models.AssetsInfo.objects.filter(id=nid).delete()
    return redirect('/assets/list/')


def assets_manual_update(request):
    task_id = process.delay().task_id
    notify.send(request.user, recipient=request.user, verb='taskid %s 开始' % task_id)
    messages.success(request, "资产更新请求已发往后台，根据机器数量，可能需要几分钟，请留意站内信,任务编号：%s" % task_id)
    return redirect('/assets/list/')
