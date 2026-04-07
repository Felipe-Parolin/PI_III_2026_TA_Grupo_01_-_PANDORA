from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet,
    SetorViewSet,
    PerfilViewSet,
    UsuariosViewSet,
    ManualViewSet,
    EquipamentoViewSet,
    OrdemServicoViewSet,
    AnexoOSViewSet,
    AnaliseLLMViewSet,
    login_usuario,
)

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'setores', SetorViewSet)
router.register(r'perfis', PerfilViewSet)
router.register(r'usuarios', UsuariosViewSet)
router.register(r'manuais', ManualViewSet)
router.register(r'equipamentos', EquipamentoViewSet)
router.register(r'ordens-servico', OrdemServicoViewSet)
router.register(r'anexos-os', AnexoOSViewSet)
router.register(r'analises-llm', AnaliseLLMViewSet)

urlpatterns = router.urls + [
    path('login/', login_usuario, name='login_usuario'),
]