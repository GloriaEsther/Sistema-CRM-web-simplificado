from django.contrib import admin
from django.urls import include,path


urlpatterns = [
    path('admin/', admin.site.urls),#admin de django :b
    path('', include('usuario.urls', namespace='usuario')),
    path('usuario/', include('usuario.urls',namespace='usuario')),
    path('clientes/', include('cliente.urls',namespace='cliente')),
    path('oportunidades/', include('oportunidades.urls', namespace='oportunidades')),
    path('ventas/', include('ventas.urls', namespace='ventas')),
    path('reportes/', include('reportes.urls', namespace='reportes')),
]
