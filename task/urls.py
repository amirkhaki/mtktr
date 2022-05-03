from django.urls import path, include
from .routers import account_router, task_router

urlpatterns = [
        path('accounts/', include(account_router.urls)),
        path('', include(task_router.urls)),
        ]

