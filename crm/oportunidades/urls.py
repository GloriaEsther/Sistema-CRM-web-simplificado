from django.urls import path
from . import views

app_name = 'oportunidades'
urlpatterns = [
    path('kanban/', views.kanban, name='kanban'),
    path('crear/', views.crear_oportunidad, name='crear'),
    path('mover/<int:pk>/', views.mover_oportunidad, name='mover'),  # AJAX
    path('listar/', views.listar_oportunidades, name='listar'),
    path('editar/<int:pk>/',views.editar_oportunidad,name='editar'),
    path('eliminar/<int:pk>/',views.eliminar_oportunidad,name='eliminar'),
    #ajax helpers
    path('ajax/consultar/<int:pk>/', views.ajax_consultar_oportunidad, name='ajax_consultar'),
    path('ajax/buscar_cliente/', views.ajax_buscar_cliente, name='ajax_buscar_cliente'),
    path('ajax/buscar_vendedor/', views.ajax_buscar_vendedor, name='ajax_buscar_vendedor'),
]
