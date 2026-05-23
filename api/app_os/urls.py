from rest_framework.routers import DefaultRouter
from .views import OrdemServicoViewSet

router = DefaultRouter()
router.register(r'ordens-servico', OrdemServicoViewSet, basename='ordem-servico')
urlpatterns = router.urls