from rest_framework.viewsets import ModelViewSet
from .serializers import WithdrawalSerializer
from .models import Withdrawal
from .permissions import IsAdminOrOwner


class WithdrawalViewSet(ModelViewSet):
    permission_classes = [IsAdminOrOwner]
    serializer_class = WithdrawalSerializer

    def get_queryset(self):
        queryset = Withdrawal.objects.all()
        if self.action in ['update', 'partial_update','destroy']:
            queryset = queryset.exclude(status='a')
        return queryset
    
