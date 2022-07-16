#!/usr/bin/env python
# -*- coding:utf-8 -*-
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite_day2',
        'USER': 'root',
        'PASSWORD': 'Welcome1234!@#$',
        'HOST': '192.168.31.100',
        'PORT': '3306',

    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PLUGIN_CLASS_DICT = {
    'memory': 'lib.plugins.memory.MemoryPlugin',
    'network': 'lib.plugins.network.NetworkPlugin',
    'basic': 'lib.plugins.basic.BasicPlugin',
}

# celery
# Broker配置，使用Redis作为消息中间件
BROKER_URL = 'redis://192.168.31.100:6379/0'

# BACKEND配置，这里使用redis
CELERY_RESULT_BACKEND = 'redis://192.168.31.100:6379/0'

# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'

# 任务结果过期时间，秒
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24

# 时区配置
CELERY_TIMEZONE = 'Asia/Shanghai'

# 指定导入的任务模块，可以指定多个
# CELERY_IMPORTS = (
#    'other_dir.tasks',
# )

# 通知设置

DJANGO_NOTIFICATIONS_CONFIG = {'SOFT_DELETE': True}

# 添加ASGI用于支持channels
ASGI_APPLICATION = 'djangoProjectDAY2.routing.application'
