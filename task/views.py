from rest_framework.viewsets import ModelViewSet
from .serializers import TelegramAccountSerializer, TelegramTaskSerializer
from .models import TelegramAccount, TelegramTask
from . import permissions

class TelegramAccountViewSet(ModelViewSet):
    queryset = TelegramAccount.objects.all()
    serializer_class = TelegramAccountSerializer
    permission_classes = [permissions.IsAdminOrOwner]


class TelegramTaskViewSet(ModelViewSet):
    queryset = TelegramTask.objects.all()
    serializer_class = TelegramTaskSerializer
