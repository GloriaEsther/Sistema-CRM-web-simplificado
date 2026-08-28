from django.urls import path
from . import views

app_name = 'cobros'
urlpatterns = [
    path('', views.listar_cobros, name='listar'),
    path('crear/<int:pk>', views.crear_cobro, name='crear_cobro'),
    path('consultar/<int:pk>',views.consultar_cobro, name='consultar_cobro')
]
