from rest_framework.serializers import ModelSerializer
from .models import Withdrawal


class WithdrawalSerializer(ModelSerializer):

    def create(self, validated_data):
        w = Withdrawal.objects.create(user=self.context['request'].user, **validated_data)
        return w

    class Meta:
        model = Withdrawal
        fields = ['id', 'user', 'amount', 'address', 'status', 'message']
        read_only_fields = ['user', 'status', 'message']
