from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from djangoProjectDAY2.consumers import SSHConsumer

# 如果是 WebSocket 连接 (ws://或 wss://), 则连接会交给 AuthMiddlewareStack验证去请求对象，然后连接将被给到 URLRouter
application = ProtocolTypeRouter({
    # 'http': # 普通的HTTP请求不需要我们手动在这里添加，框架会自动加载
    # 用于WebSocket认证
    'websocket': AuthMiddlewareStack(
        # 用于WebSocket认证
        URLRouter([
            # URL路由匹配,访问asset/terminal的时候，交给SSHConsumer处理
            re_path(r'^asset/terminal/', SSHConsumer),
        ])
    ),
})
