"""djangoProjectDAY2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls import handler404, handler500
from app01.views import depart, user, prettynum, admin, account, order, api, assets, notification, password_management, application, IT
import notifications.urls

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/edit/<int:nid>', depart.depart_edit),
    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/edit/<int:nid>', user.user_edit),
    path('user/delete/<int:nid>', user.user_delete),
    # 靓号管理
    path('prettynum/list/', prettynum.prettynum_list),
    path('prettynum/add/', prettynum.prettynum_add),
    path('prettynum/edit/<int:nid>/', prettynum.prettynum_edit),
    path('prettynum/delete/<int:nid>/', prettynum.prettynum_delete),
    # 管理员
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/edit/<int:nid>', admin.admin_edit),
    path('admin/delete/<int:nid>', admin.admin_delete),
    path('admin/reset/<int:nid>', admin.admin_reset),
    # 登录注销
    path('login/', account.logins),
    path('logout/', account.logout),
    # 钉钉三方登录
    path('dingding_back/', IT.ding_back),
    path('dingding_url/', IT.ding_url),
    # 订单管理
    path('order/list/', order.order_list),
    # api管理
    # 全自动写法

    # path('api/assets/', api.AssetsView.as_view({'get': 'list', 'post': 'create'})),
    # path('api/assets/<pk>/',
    #      api.AssetsView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),

    # 传统写法
    path('api/assets/', api.AssetsView.as_view()),
    # path('api/assets/<int:nid>/', api.AssetsView.as_view()),

    # 资产管理
    path('assets/list/', assets.assets_list),
    path('assets/add/', assets.assets_add),
    path('assets/edit/<int:nid>', assets.assets_edit),
    path('assets/delete/<int:nid>', assets.assets_delete),
    path('assets/manual_update/', assets.assets_manual_update),
    # index
    path('index/', account.index),

    # 密码管理
    path('password_management/list/', password_management.password_management_list),
    path('password_management/details/', password_management.password_management_details),
    path('password_management/add/', password_management.password_management_add),
    path('password_management/edit/', password_management.password_management_edit),
    path('password_management/delete/', password_management.password_management_delete),
    # 密码审计
    path('password_management/record/', password_management.password_management_record),

    # 应用管理
    path('app/list/', application.app_list),
    path('app/add/', application.app_add),
    path('app/edit/<int:nid>/', application.app_edit),
    path('app/delete/<int:nid>/', application.app_delete),


    # 通知
    # path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('my_notifications/', notification.my_notifications),
    path('update_notifications/', notification.change_unread),
    path('already_read_notifications/', notification.already_read_notifications),
    path('delete_all_unread_notifications/', notification.delete_all_unread_notifications),

    # IT
    path('low_value_consumable_list/', IT.low_value_consumable_list),
    path('get_low_value_consumable/<int:nid>', IT.get_low_value_consumable),
    path('add_low_value_consumable/', IT.add_low_value_consumable),
    path('edit_low_value_consumable/<int:nid>', IT.edit_low_value_consumable),
    path('delete_low_value_consumable/<int:nid>', IT.delete_low_value_consumable),
    path('low_value_consumable_record/', IT.low_value_consumable_record),

]

handler404 = 'app01.views.account.error_404'

