from django.urls import path
from . import views

app_name = 'ventas'
urlpatterns = [
    path('', views.listar_ventas, name='listar_ventas'),
    path('crear/', views.crear_venta_manual, name='crear_venta_manual'),
    path('generar_desde_oportunidad/<int:oportunidad_id>/', views.generar_venta_desde_oportunidad, name='generar_venta_desde_oportunidad'),
]
