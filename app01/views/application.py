from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import AppModelForm, AppEditModelForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q


def app_list(request):
    # for i in range(300):
    #     models.PrettyNumber.objects.create(mobile='18818181818', price=10, level=2, status=1)

    form = AppModelForm()
    # data_dict = {}
    value = request.GET.get('q', "")

    # queryset = models.Application.objects.filter(Q(app_name__contains=value) | Q(app_type__contains=value))
    order_by = request.GET.get("orderby")
    if order_by is None:
        order_by = "-id"

    queryset = models.Application.objects.filter(
        Q(app_name__icontains=value) | Q(app_type__icontains=value)).order_by(order_by)

    total = models.Application.objects.count()
    paginator = Paginator(queryset, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/app_list.html',
                  {'form': form, 'queryset': queryset, 'value': value, 'page_obj': page_obj, 'total': total})


@csrf_exempt
def app_add(request):
    form = AppModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def app_edit(request, nid):
    row_object = models.Application.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AppEditModelForm(instance=row_object)
        return render(request, 'home/change_template.html', {'form': form})
    form = AppEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/app/list/')
    return render(request, 'home/change_template.html', {"form": form})


def app_delete(request, nid):
    models.Application.objects.filter(id=nid).delete()
    return redirect('/app/list/')
