from django.urls import path
from . import views

app_name = "cotizacion"

urlpatterns = [
    path("", views.cotizaciones_list, name="listar"),
    path("crear/", views.cotizacion_crear, name="crear"),
    path("<int:pk>/", views.cotizacion_detalle, name="detalle"),
]
