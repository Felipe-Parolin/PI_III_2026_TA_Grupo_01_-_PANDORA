from rest_framework.routers import DefaultRouter
from .views import HistoricoOSViewSet

router = DefaultRouter()
router.register(r'historicos-os', HistoricoOSViewSet, basename='historico-os')
urlpatterns = router.urls