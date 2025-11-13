from django.urls import path
from . import views

app_name = 'reportes'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/ventas-mensuales/', views.ventas_mensuales_json, name='ventas_mensuales_json'),
    path('api/clientes-frecuentes/', views.clientes_frecuentes_json, name='clientes_frecuentes_json'),
]
