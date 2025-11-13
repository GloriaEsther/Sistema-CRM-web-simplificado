from django.urls import path
from . import views

app_name = 'cliente'#haber si funciona
urlpatterns = [
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('listar/', views.listar_clientes, name='listar_clientes'),
    path('eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
]
