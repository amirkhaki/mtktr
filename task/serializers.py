from rest_framework.serializers import (
        ModelSerializer, ValidationError, SerializerMethodField)
from django.conf import settings
#import telegram
from .models import TelegramAccount, TelegramTask

class TelegramAccountSerializer(ModelSerializer):

    verification_url = SerializerMethodField()

    def get_verification_url(self, obj):
        return f'https://t.me/{settings.BOT_USERNAME}?start={obj.id}_{obj.token}'

    def create(self, validated_data):
        account = TelegramAccount.objects.create(owner=self.context['request'].user,
                **validated_data)
        return account
    class Meta:
        model = TelegramAccount
        fields = ['owner', 'verified', 'username', 'id', 'verification_url']
        read_only_fields = ['owner', 'verified']

class TelegramTaskSerializer(ModelSerializer):
    chat_url = SerializerMethodField()

    def get_chat_url(self, obj):
        return f'https://t.me/{obj.chat_id}'
    class Meta:
        model = TelegramTask
        fields = ['id', 'cpp', 'task_type', 'chat_url']
