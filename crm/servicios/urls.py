from django.urls import path
from . import views

app_name = "servicio"

urlpatterns = [
    path("", views.servicios_list, name="listar"),
    path("crear/", views.servicio_crear, name="crear"),
    path("<int:pk>/editar/", views.servicio_editar, name="editar"),
    path("<int:pk>/eliminar/", views.servicio_eliminar, name="eliminar"),
    path("<int:pk>/", views.servicio_detalle, name="detalle"),
]
