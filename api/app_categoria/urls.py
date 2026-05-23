from rest_framework.routers import DefaultRouter
from .views import CategoriaDocumentoViewSet

router = DefaultRouter()
router.register(r'categorias-documento', CategoriaDocumentoViewSet, basename='categoria-documento')
urlpatterns = router.urls