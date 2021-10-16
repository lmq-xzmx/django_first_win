#from django.shortcuts import render

# Create your views here.


from rest_framework.decorators import api_view

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from back_end_wxnote.models import note_header
from back_end_wxnote.serializers import note_headerSerializerNew
from back_end_wxnote.models import note_list
from back_end_wxnote.serializers import note_listSerializerNew
# https://q1mi.github.io/Django-REST-framework-documentation/api-guide/serializers_zh/#_20
# objects.all()、objects.get()与objects.filter()
# 话题列表资源
@api_view(['GET','POST'])
def note_topic_list(request):
    if request.method == 'GET':
        # 查询所有电影信息
        note_headers = note_header.objects.all()
        # 实例化一个序列化器，指示为多条数据的序列化
        note_headers_serializer = note_headerSerializerNew(note_headers,many=True)
        # 返回序列化的json数据
        return Response(note_headers_serializer.data)

    elif request.method == 'POST':
        # 解析http请求的数据
        #note_header_data = JSONParser().parse(request)
        # 实例化一个序列化器
        note_headers_serializer = note_headerSerializerNew(data=request.data)
        # 如果序列化数据有效
        if note_headers_serializer.is_valid():
            note_headers_serializer.save()
            return Response(note_headers_serializer.data,status=status.HTTP_201_CREATED)
        return Response(note_headers_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# 话题列表内容清单
@api_view(['GET','POST'])
def note_list_list(request):
    if request.method == 'GET':
        # 查询所有电影信息
        note_lists = note_list.objects.all()
        # 实例化一个序列化器，指示为多条数据的序列化
        note_lists_serializer = note_listSerializerNew(note_lists,many=True)
        # 返回序列化的json数据
        return Response(note_lists_serializer.data)

    elif request.method == 'POST':
        # 解析http请求的数据
        #note_list_data = JSONParser().parse(request)
        # 实例化一个序列化器
        note_lists_serializer = note_listSerializerNew(data=request.data)
        # 如果序列化数据有效
        if note_lists_serializer.is_valid():
            note_lists_serializer.save()
            return Response(note_lists_serializer.data,status=status.HTTP_201_CREATED)
        return Response(note_lists_serializer.errors,status=status.HTTP_400_BAD_REQUEST)