from rest_framework.routers import DefaultRouter
from .views import AnexoOSViewSet

router = DefaultRouter()
router.register(r'anexos-os', AnexoOSViewSet, basename='anexo-os')
urlpatterns = router.urls