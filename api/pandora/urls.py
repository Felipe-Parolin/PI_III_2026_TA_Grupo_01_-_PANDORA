from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet, SetorViewSet, PermissaoViewSet, GrupoViewSet,
    UsuarioViewSet, EquipamentoViewSet, OrdemServicoViewSet,
    CategoriaDocumentoViewSet, DocumentoEquipamentoViewSet,
    AnexoOSViewSet, AnaliseLLMViewSet, HistoricoOSViewSet
)

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'setores', SetorViewSet)
router.register(r'permissoes', PermissaoViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'equipamentos', EquipamentoViewSet)
router.register(r'ordens-servico', OrdemServicoViewSet)
router.register(r'categorias-documento', CategoriaDocumentoViewSet)
router.register(r'documentos-equipamento', DocumentoEquipamentoViewSet)
router.register(r'anexos-os', AnexoOSViewSet)
router.register(r'analises-llm', AnaliseLLMViewSet)
router.register(r'historicos-os', HistoricoOSViewSet)

urlpatterns = [
    path('', include(router.urls)),
]