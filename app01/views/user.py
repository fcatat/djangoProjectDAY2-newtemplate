from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import UserModelForm
from django.core.paginator import Paginator


def user_list(request):
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["username__contains"] = value
    order_by = request.GET.get("orderby")
    if order_by is None:
        order_by = "-id"

    queryset = models.UserInfo.objects.filter(**data_dict).order_by(order_by)
    total = models.UserInfo.objects.count()
    paginator = Paginator(queryset, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/user_list.html',
                  {'queryset': queryset, 'value': value, 'page_obj': page_obj, 'total': total})


def user_add(request):
    button_value = "Add New User"
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'home/change_template.html', {"button_value": button_value, "form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request, 'home/change_template.html', {"button_value": button_value, "form": form})


def user_edit(request, nid):
    button_value = "edit"
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, 'home/change_template.html', {'form': form, "button_value": button_value})
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'home/change_template.html', {"form": form, "button_value": button_value})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
