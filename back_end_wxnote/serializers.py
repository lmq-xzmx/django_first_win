# coding:utf-8
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from back_end_wxnote.models import note_header
from back_end_wxnote.models import note_list


class note_headerSerializerNew(serializers.ModelSerializer):
    class Meta:
        # 指定序列化器需要作用的模型
        model = note_header
        # 指定序列化器的模型字段
        '''
        fields = (
            'id',
            'custom_topic',
            'mail_title',
            'date',
            'created',
        )
        '''
        fields = '__all__'

class note_listSerializerNew(serializers.ModelSerializer):
    
    e_note_list_id=serializers.IntegerField()
      
    class Meta:
        # 指定序列化器需要作用的模型
        model = note_list
        # 指定序列化器的模型字段
        '''
        fields = (
            'id',
            'create_time',
            'chater',
            'chat_content',
            'e_note_list_id',
        )
        '''
        fields = '__all__'
        depth = 1
