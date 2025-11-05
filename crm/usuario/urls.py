from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
]
