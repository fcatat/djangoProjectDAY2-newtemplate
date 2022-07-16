import json

from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from app01 import models


# class BaseResponse(object):
#     def __init__(self, status=True, data=None, error=None):
#         self.status = status
#         self.data = data
#         self.error = error
#
#     @property
#     def dict(self):
#         return self.__dict__
#
#
# def test(request):
#     result = BaseResponse()
#     nid = request.GET.get('id')
#     if nid == 10:
#         result.data = '数据正确，已收到'
#     else:
#         result.error = '错误'
#         result.status = False
#     return JsonResponse(result.dict)

class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetsInfo
        fields = '__all__'


class AssetsView(APIView):
    def get(self, request, *args, **kwargs):
        nid = request.GET.get('nid')
        app = request.GET.get('app')

        if not nid and not app:
            result = models.AssetsInfo.objects.all()
            ser = AssetsSerializer(instance=result, many=True)
            return Response(ser.data)
        if app:
            result = models.AssetsInfo.objects.all().filter(app=app)
            ser = AssetsSerializer(instance=result, many=True)
            return Response(ser.data)
        else:
            result = models.AssetsInfo.objects.all().filter(id=nid).first()
            ser = AssetsSerializer(instance=result, many=False)
            return Response(ser.data)

    # def post(self, request, *args, **kwargs):
    #     ser = AssetsSerializer(data=request.data)
    #     if ser.is_valid():
    #         ser.save()
    #         return Response(ser.data)
    #     return Response(ser.errors)

    """牛鼻，试了一天总算开窍了"""

    def post(self, request, *args, **kwargs):
        ipv4 = request.data.get('ipv4')
        sn = request.data.get('sn')
        status = request.data.get('status')
        if sn:
            core_num = request.data.get('core_num')
            mem = request.data.get('mem')
            disk = request.data.get('disk')
            sn_obj = models.AssetsInfo.objects.filter(sn=sn).exists()
            if sn_obj:
                models.AssetsInfo.objects.filter(sn=sn).update(ipv4=ipv4, core_num=core_num, mem=mem, disk=disk,
                                                               status=status)
                return Response("数据一致，无需更新")
            ser = AssetsSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data)
        if not sn:
            ipv4_obj = models.AssetsInfo.objects.filter(ipv4=ipv4).exists()
            if ipv4_obj:
                models.AssetsInfo.objects.filter(ipv4=ipv4).update(status=status)
                return Response("此台机器离线")
            return Response("首次录入且错误，未完成")

    def delete(self, request, *args, **kwargs):
        nid = kwargs.get('nid')
        models.AssetsInfo.objects.filter(id=nid).delete()
        return Response("删除%s号记录成功" % nid)

    def put(self, request, nid):
        """全量更新，需要把所有字段都输入"""
        obj = models.AssetsInfo.objects.filter(id=nid).first()
        if not obj:
            return Response("数据不存在，无法更新")

        ser = AssetsSerializer(instance=obj, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("修改成功")
        else:
            return Response("验证失败")


"""全自动写法,自动完成增删改查"""

# class AssetsView(ModelViewSet):
#     queryset = models.AssetsInfo.objects
#     serializer_class = AssetsSerializer
