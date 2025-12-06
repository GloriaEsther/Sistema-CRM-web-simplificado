from django.urls import path
from . import views

app_name = 'cliente'
urlpatterns = [
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('listar/', views.listar_clientes, name='listar_clientes'),
    path('editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    # Vistas AJAX (Las que usa el JS para obtener datos)
    path('ajax/consultar/<int:pk>/', views.ajax_consultar_cliente, name='ajax_consultar_cliente'),
]
