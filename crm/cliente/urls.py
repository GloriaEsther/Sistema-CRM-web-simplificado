from django.urls import path
from . import views

app_name = 'cliente'
urlpatterns = [
    
    path("", views.clientes_list, name="listar"),
    path("crear/", views.cliente_crear, name="crear"),
    path("editar/<int:pk>/", views.cliente_editar, name="editar"),
    path("eliminar/<int:pk>/", views.cliente_eliminar, name="eliminar"),
    path("detalle/<int:pk>/", views.cliente_detalle, name="detalle"),
    path("importar/", views.importar_clientes, name="importar"),
]