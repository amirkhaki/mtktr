from rest_framework.routers import DefaultRouter
from . import views

account_router = DefaultRouter()
account_router.register('telegram', views.TelegramAccountViewSet)
account_router.register('discord', views.DiscordAccountViewSet)
task_router = DefaultRouter()
task_router.register('telegram', views.TelegramTaskViewSet, basename='task')
task_router.register('discord', views.DiscordTaskViewSet, basename='task')
