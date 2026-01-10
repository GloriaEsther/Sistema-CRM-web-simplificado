from django.urls import path
from . import views

app_name = 'ventas'
urlpatterns = [
    path('', views.listar_ventas, name='listar'),
    path('crear/', views.crear_venta_manual, name='crear_venta_manual'),
   # path('generar_desde_oportunidad/<int:oportunidad_id>/', views.generar_venta_desde_oportunidad, name='generar_venta_desde_oportunidad'),
    path('corte_caja/', views.corte_caja, name='corte_caja'),
    path('ventas_del_dia/', views.ventas_hoy, name='ventas_hoy'),
    path('editar/<int:pk>/', views.venta_editar, name='venta_editar'),
    path('eliminar/<int:pk>/', views.venta_eliminar, name='venta_eliminar'),
]
