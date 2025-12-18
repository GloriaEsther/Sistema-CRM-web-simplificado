from django.urls import path
from . import views

app_name = "proveedor"

urlpatterns = [
    path("", views.proveedor_list, name="listar"),
    path("crear/", views.proveedor_crear, name="crear"),
    path("<int:pk>/editar/", views.proveedor_editar, name="editar"),
    path("<int:pk>/eliminar/", views.proveedor_eliminar, name="eliminar"),
    path("<int:pk>/", views.proveedor_detalle, name="detalle"),
]
