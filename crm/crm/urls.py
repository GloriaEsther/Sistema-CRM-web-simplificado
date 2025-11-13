"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from usuario import views

urlpatterns = [
    path('admin/', admin.site.urls),#admin de django :b
    path('', views.registrar_usuario, name='registrar_usuario'),#apunta a la vista principal
    path('usuario/', include('usuario.urls',namespace='usuario')),
    path('clientes/', include('cliente.urls',namespace='cliente')),
    path('oportunidades/', include('oportunidades.urls', namespace='oportunidades')),
    path('ventas/', include('ventas.urls', namespace='ventas')),
    path('reportes/', include('reportes.urls', namespace='reportes')),
]
