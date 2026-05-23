from rest_framework.routers import DefaultRouter
from .views import AnaliseLLMViewSet

router = DefaultRouter()
router.register(r'analises-llm', AnaliseLLMViewSet, basename='analise-llm')
urlpatterns = router.urls