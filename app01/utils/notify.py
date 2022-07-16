from notifications.signals import notify


def send_notifications(actor, verb, recipient, target=None, description=None, **kwargs):
    """
        这里原本放的是上文各个参数的说明
    """
    notify.send(sender=actor,
                recipient=recipient,
                verb=verb,
                target=target,
                description=description,
                **kwargs
                )


