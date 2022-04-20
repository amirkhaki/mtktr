from rest_framework.viewsets import ModelViewSet
from .serializers import TelegramAccountSerializer, TelegramTaskSerializer
from .models import TelegramAccount, TelegramTask

class TelegramAccountViewSet(ModelViewSet):
    queryset = TelegramAccount.objects.all()
    serializer_class = TelegramAccountSerializer


class TelegramTaskViewSet(ModelViewSet):
    queryset = TelegramTask.objects.all()
    serializer_class = TelegramTaskSerializer
