from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01.utils.form import AccountModelForm
from django.contrib.auth import authenticate, login
from app01 import models


def logins(request):
    if request.method == "GET":
        form = AccountModelForm()
        return render(request, 'accounts/login.html', {"form": form})
    form = AccountModelForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # form.add_error("password", "Username or Password is Invalid")
            # return render(request, 'accounts/login.html', {'form': form})
            # request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
            login(request, user)
            return redirect('/index/')
        form.add_error("password", "用户名或密码错误")
        return render(request, 'accounts/login.html', {"form": form})
    else:
        return render(request, 'accounts/login.html', {"form": form})


def logout(request):
    request.session.clear()
    return redirect('/login/')


def index(request):
    server_total = models.AssetsInfo.objects.count()
    app_total = models.Application.objects.count()
    password_total = models.PasswordManagement.objects.count()

    return render(request, 'home/index.html',
                  {"server_total": server_total, "app_total": app_total, "password_total": password_total})


def error_404(request, exception):
    return render(request, 'home/page-404.html')


# 构造钉钉登录url
def ding_url(request):
    appid = 'dingyxlaspxbccsj4ppu'  # 替换成自己的appid
    redirect_uri = 'http://127.0.0.1:8000/dingding_back/'  # 替换成自己的回调路由

    return redirect(
        'https://oapi.dingtalk.com/connect/qrconnect?appid=' + appid + '&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=' + redirect_uri)

