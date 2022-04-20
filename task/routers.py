from rest_framework.routers import DefaultRouter
from . import views

account_router = DefaultRouter()
account_router.register('telegram', views.TelegramAccountViewSet)
task_router = DefaultRouter()
task_router.register('telegram', views.TelegramTaskViewSet)
