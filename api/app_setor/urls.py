from rest_framework.routers import DefaultRouter
from .views import SetorViewSet

router = DefaultRouter()
router.register(r'setores', SetorViewSet, basename='setor')
urlpatterns = router.urls