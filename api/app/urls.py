from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('api/', include('app_core.urls')),
    path('api/', include('app_empresa.urls')),
    path('api/', include('app_setor.urls')),
    path('api/', include('app_permissao.urls')),
    path('api/', include('app_grupo.urls')),
    path('api/', include('app_usuario.urls')),
    path('api/', include('app_equipamento.urls')),
    path('api/', include('app_categoria.urls')),
    path('api/', include('app_documento.urls')),
    path('api/', include('app_os.urls')),
    path('api/', include('app_anexo.urls')),
    path('api/', include('app_historico.urls')),
    path('api/', include('app_analise.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)