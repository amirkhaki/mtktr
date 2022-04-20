from rest_framework.serializers import ModelSerializer, ValidationError
from .models import TelegramAccount, TelegramTask

class TelegramAccountSerializer(ModelSerializer):

    class Meta:
        model = TelegramAccount
        fields = '__all__'


class TelegramTaskSerializer(ModelSerializer):

    def validate_cpp(self, value):
        if value < 0 :
            raise ValidationError("cpp could not be negative")
        return value

    class Meta:
        model = TelegramTask
        fields = '__all__'
