from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from usuario import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),  # pantalla bienvenida
    path('usuario/', include('usuario.urls', namespace='usuario')),
    path('clientes/', include('cliente.urls',namespace='cliente')),
    path('oportunidades/', include('oportunidades.urls',namespace='oportunidades')),
    path('ventas/', include('ventas.urls')),
    path("servicios/", include("servicios.urls",namespace="servicio")),#en el include debe coincidir el nomrbe d ela app con el nombre de la carpeta(literal)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
