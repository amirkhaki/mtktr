from rest_framework.serializers import (
        ModelSerializer, ValidationError)
from .models import TelegramAccount, TelegramTask

class TelegramAccountSerializer(ModelSerializer):

    def create(self, validated_data):
        tasks = validated_data.pop('tasks', [])
        account = TelegramAccount.objects.create(owner=self.context['request'].user,
                **validated_data)
        account.tasks.set(tasks)
        return account
    class Meta:
        model = TelegramAccount
        fields = '__all__'
        read_only_fields = ['owner', 'verified', 'tid']


class TelegramTaskSerializer(ModelSerializer):

    def validate_cpp(self, value):
        if value < 0 :
            raise ValidationError("cpp could not be negative")
        return value

    class Meta:
        model = TelegramTask
        fields = '__all__'
