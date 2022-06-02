from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model as gum
from djoser.conf import settings
from djoser.compat import get_user_email, get_user_email_field_name
from .models import Withdrawal


class WithdrawalSerializer(ModelSerializer):

    def create(self, validated_data):
        w = Withdrawal.objects.create(user=self.context['request'].user, **validated_data)
        return w

    class Meta:
        model = Withdrawal
        fields = ['id', 'user', 'amount', 'address', 'status', 'message']
        read_only_fields = ['user', 'status', 'message']

User = gum()
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'credit',
        )
        read_only_fields = (settings.LOGIN_FIELD,'credit',)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)

