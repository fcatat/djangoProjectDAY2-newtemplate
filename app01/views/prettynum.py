from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import PrettyNumForm, PrettyNumEditForm
from django.core.paginator import Paginator


def prettynum_list(request):
    # for i in range(300):
    #     models.PrettyNumber.objects.create(mobile='18818181818', price=10, level=2, status=1)

    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["mobile__contains"] = value

    queryset = models.PrettyNumber.objects.filter(**data_dict).order_by("-level")
    paginator = Paginator(queryset, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'old/prettynum_list.html', {'queryset': queryset, 'value': value, 'page_obj': page_obj})


def prettynum_add(request):
    if request.method == "GET":
        form = PrettyNumForm()
        return render(request, 'old/prettynum_add.html', {'form': form})
    form = PrettyNumForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    return render(request, 'old/prettynum_add.html', {'form': form})


def prettynum_edit(request, nid):
    row_object = models.PrettyNumber.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyNumEditForm(instance=row_object)
        return render(request, 'old/prettynum_add.html', {'form': form})
    form = PrettyNumEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    return render(request, 'old/prettynum_add.html', {"form": form})


def prettynum_delete(request, nid):
    models.PrettyNumber.objects.filter(id=nid).delete()
    return redirect('/prettynum/list/')