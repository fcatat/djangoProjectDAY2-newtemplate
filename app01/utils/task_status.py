from celery import Task
from notifications.signals import notify


class TaskHook(Task):

    def on_success(self, retval, task_id, args, kwargs):
        print('task id:%s ,successful !' % task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('task id:%s ,failure !' % task_id)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('task id:%s ,retry !' % task_id)
