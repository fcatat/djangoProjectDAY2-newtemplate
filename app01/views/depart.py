from django.shortcuts import render, redirect
from app01 import models


def depart_list(request):
    queryset = models.Department.objects.all()
    return render(request, 'old/depart_list.html', {'queryset': queryset})


def depart_add(request):
    if request.method == "GET":
        return render(request, 'old/depart_add.html')
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list/")


def depart_delete(request):
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    if request.method == "GET":
        row_name = models.Department.objects.filter(id=nid).first()
        return render(request, 'old/depart_edit.html', {"row_name": row_name})
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")
