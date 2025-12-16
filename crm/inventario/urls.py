from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.inventario_list, name="listar"),
    path("crear/", views.inventario_crear, name="crear"),
    path("<int:pk>/editar/", views.inventario_editar, name="editar"),
    path("<int:pk>/eliminar/", views.inventario_eliminar, name="eliminar"),
    path("<int:pk>/", views.inventario_detalle, name="detalle"),
]
