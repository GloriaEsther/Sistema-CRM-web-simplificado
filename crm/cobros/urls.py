from django.urls import path
from . import views

app_name = 'cobros'
urlpatterns = [
    path('', views.listar_cobros, name='listar'),
    path('crear/<int:venta_id>', views.crear_cobro, name='crear_cobro'),
    #path('editar/<int:pk>/', views.editar_cobro, name='editar_cobro'),
    #path('eliminar/<int:pk>/', views.eliminar_cobro, name='eliminar_cobro'),
    #path('consultar/<int:pk>',views.consultar_cobro, name='consultar_cobro')
]
