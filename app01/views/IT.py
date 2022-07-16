from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.messages.views import messages
from django.core.paginator import Paginator
from app01 import models
from app01.utils.form import LowValueConsumableModelForm, LowValueConsumableEditModelForm, \
    LowValueConsumableRecordModelForm
from django.db.models import F, Q
import time
import hmac
import base64
from hashlib import sha256
import urllib
import json
import requests


# 构造钉钉登录url
def ding_url(request):
    appid = 'dingyxlaspxbccsj4ppu'  # 替换成自己的appid
    redirect_uri = 'http://127.0.0.1:8000/dingding_back/'  # 替换成自己的回调路由

    return redirect(
        'https://oapi.dingtalk.com/connect/qrconnect?appid=' + appid + '&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=' + redirect_uri)


def ding_back(request):
    # 获取code
    code = request.GET.get("code")

    t = time.time()
    # 时间戳
    timestamp = str((int(round(t * 1000))))
    # 替换成自己的appSecret
    appSecret = '38dIeS7lD6bpMZFfpG3JvjvMb5hX7P8ziWzGw-W5ih4McDBrpez9u4nmv0W0R0L1'
    # 构造签名
    signature = base64.b64encode(
        hmac.new(appSecret.encode('utf-8'), timestamp.encode('utf-8'), digestmod=sha256).digest())
    # 请求接口，换取钉钉用户名
    payload = {'tmp_auth_code': code}
    headers = {'Content-Type': 'application/json'}
    res = requests.post('https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature=' + urllib.parse.quote(
        signature.decode("utf-8")) + "&timestamp=" + timestamp + "&accessKey=dingyxlaspxbccsj4ppu",
                        data=json.dumps(payload), headers=headers)  # accessKey替换成自己的appid

    res_dict = json.loads(res.text)
    # print(res_dict)
    try:
        dingtalk_user = res_dict["user_info"]["nick"]
        dingtalk_user_unicode = dingtalk_user.encode("unicode_escape").decode('utf-8')
        # print(dingtalk_user, dingtalk_user_unicode)
        # response = HttpResponse(res.text)
        # response.set_cookie('dingtalk_user', dingtalk_user)
        # return redirect('/low_value_consumable_list/')
        rep = redirect('/low_value_consumable_list/')
        rep.set_cookie('dingtalk_user', dingtalk_user_unicode)
        return rep
    except:
        return redirect('/dingding_url/')


def low_value_consumable_list(request):
    current_dingtalk_user = request.COOKIES.get('dingtalk_user')
    if current_dingtalk_user is None:
        return redirect('/dingding_back/')
    current_dingtalk_user = current_dingtalk_user.encode('utf-8').decode('unicode_escape')
    value = request.GET.get('q', "")
    order_by = request.GET.get("orderby")
    if order_by is None:
        order_by = "-id"
    queryset = models.LowValueConsumable.objects.filter(
        Q(name__icontains=value) | Q(brand__icontains=value) | Q(model__icontains=value)).order_by(order_by)
    total = models.LowValueConsumable.objects.count()
    paginator = Paginator(queryset, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/low_value_consumable_list.html',
                  {'queryset': queryset, 'value': value, 'page_obj': page_obj, 'total': total,
                   'current_dingtalk_user': current_dingtalk_user})


def get_low_value_consumable(request, nid):
    current_dingtalk_user = request.COOKIES.get('dingtalk_user')
    if current_dingtalk_user is None:
        return redirect('/dingding_back/')
    current_dingtalk_user = current_dingtalk_user.encode('utf-8').decode('unicode_escape')
    button_value = "edit"
    page_tag = "get_low_value_consumable"
    row_object = models.LowValueConsumable.objects.filter(id=nid).first()
    if request.method == "GET":
        form = LowValueConsumableModelForm(instance=row_object)
        return render(request, 'home/change_template_low_value_consumable.html',
                      {'form': form, "button_value": button_value})
    form = LowValueConsumableModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        '''库存减去1，限制用户每次仅能领用1个'''
        models.LowValueConsumable.objects.filter(id=nid).update(inventory_quantity=F('inventory_quantity') - 1)
        '''添加审计'''
        username = current_dingtalk_user
        model = request.POST.get('name') + ' ' + request.POST.get('brand') + ' ' + request.POST.get('model')
        models.LowValueConsumableRecord.objects.create(username=username, model=model)
        return redirect('/low_value_consumable_list/')
    return render(request, 'home/change_template_low_value_consumable.html',
                  {"form": form, "button_value": button_value, "page_tag": page_tag})


def add_low_value_consumable(request):
    button_value = "Add New Assets"
    if request.method == "GET":
        form = LowValueConsumableEditModelForm
        return render(request, 'home/change_template.html', {"button_value": button_value, "form": form})
    form = LowValueConsumableEditModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/low_value_consumable_list/')

    return render(request, 'home/change_template.html', {"button_value": button_value, "form": form})


def edit_low_value_consumable(request, nid):
    button_value = "edit"
    row_object = models.LowValueConsumable.objects.filter(id=nid).first()
    if request.method == "GET":
        form = LowValueConsumableEditModelForm(instance=row_object)
        return render(request, 'home/change_template.html', {'form': form, "button_value": button_value})
    form = LowValueConsumableEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/low_value_consumable_list/')
    return render(request, 'home/change_template.html', {"form": form, "button_value": button_value})


def delete_low_value_consumable(request, nid):
    models.LowValueConsumable.objects.filter(id=nid).delete()
    return redirect('/low_value_consumable_list/')


def low_value_consumable_record(request):
    form = LowValueConsumableRecordModelForm
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["username__contains"] = value
    order_by = request.GET.get("orderby")
    if order_by is None:
        order_by = "-id"

    queryset = models.LowValueConsumableRecord.objects.filter(**data_dict).order_by(order_by)
    total = models.LowValueConsumableRecord.objects.count()
    paginator = Paginator(queryset, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/low_value_consumable_record.html',
                  {'form': form, 'queryset': queryset, 'value': value, 'page_obj': page_obj, 'total': total})
