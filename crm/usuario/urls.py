from django.urls import path
from . import views

app_name='usuario'
urlpatterns = [
    # path('', views.inicio, name='inicio'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    #aun no.....
   # path('listar/', views.listar_usuarios, name='listar_usuarios'),
    #path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('inicio/', views.inicio, name='inicio'),
]
