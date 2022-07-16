from django.shortcuts import render, redirect
from celery.result import AsyncResult


def my_notifications(request):
    unread_list = request.user.notifications.unread()
    task_dict = {}
    for notice in unread_list:
        task_id = str(notice.verb).split(" ")[1]
        task = AsyncResult(task_id)
        task_dict[task_id] = (notice.id, task.status)
    # return render(request, 'home/notify.html', {"unread_list": unread_list})
    print(task_dict)
    return render(request, 'home/notify.html', {"task_dict": task_dict})


def change_unread(request):
    notice_id = request.GET.get('notice_id')
    if notice_id:
        # 更新一条
        request.user.notifications.get(id=notice_id).mark_as_read()
        return redirect('/my_notifications/')
    else:
        # 更新全部
        request.user.notifications.mark_all_as_read()
        return redirect('/my_notifications/')


def already_read_notifications(request):
    read_list = request.user.notifications.read()
    # for i in read_list:
    #     print(i)
    return render(request, 'home/notify_already_read.html', {"read_list": read_list})


def delete_all_unread_notifications(request):
    request.user.notifications.read().mark_all_as_deleted()
    return render(request, 'home/notify_already_read.html')
