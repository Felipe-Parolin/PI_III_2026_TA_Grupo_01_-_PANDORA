from rest_framework.routers import DefaultRouter
from .views import PermissaoViewSet

router = DefaultRouter()
router.register(r'permissoes', PermissaoViewSet)
urlpatterns = router.urls