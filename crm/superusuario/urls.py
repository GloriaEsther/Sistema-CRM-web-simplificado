from django.urls import path
from . import views

app_name = "superusuario"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("negocios/",views.buscar_negocios,name="listar_negocios"),
    path("consultar_negocios/<int:dueno_id>/",views.detalles_del_negocio,name="consultar_negocios"),
    path("ver_negocio/<int:id_dueno>/",views.ver_negocio,name="ver_negocio"),
    path("salir_negocio/",views.salir_negocio,name="salir_negocio"),
]
