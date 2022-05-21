from rest_framework.routers import DefaultRouter
from .views import WithdrawalViewSet

router = DefaultRouter()
router.register('withdrawal', WithdrawalViewSet, basename='withdrawal')

