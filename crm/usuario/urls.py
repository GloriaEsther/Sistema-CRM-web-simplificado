from django.urls import path
from . import views

app_name='usuario'

urlpatterns = [
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('inicio/', views.inicio, name='inicio'),

    # CRUD usuarios
    path('listar/', views.listar_usuarios, name='listar_usuarios'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('subir-logo/', views.subir_logo, name='subir_logo'),
]
