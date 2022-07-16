from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info == '/login/':
            return None
        if 'api/assets' in request.path_info:
            return None
        if 'low_value_consumable' in request.path_info:
            return None
        if 'dingding' in request.path_info:
            return None
        is_auth = request.user.is_authenticated
        if is_auth:
            return None

        return redirect('/login/')

