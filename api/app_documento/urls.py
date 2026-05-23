from rest_framework.routers import DefaultRouter
from .views import DocumentoEquipamentoViewSet

router = DefaultRouter()
router.register(r'documentos-equipamento', DocumentoEquipamentoViewSet, basename='documento-equipamento')
urlpatterns = router.urls