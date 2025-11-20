from django.urls import path
from . import views

app_name = 'oportunidades'
urlpatterns = [
    path('kanban/', views.kanban, name='kanban'),
    path('crear/', views.crear_oportunidad, name='crear'),
    path('mover/<int:pk>/', views.mover_oportunidad, name='mover'),  # AJAX
    path('listar/', views.listar_oportunidades, name='listar'),
    path('editar/<int:pk>',views.editar_oportunidad,name='editar'),
    path('eliminar/<int:pk>',views.eliminar_oportunidad,name='eliminar'),
]
#te quedaste corrigiendo lo de oportunidad para consultar editar y eliinar
#descarga e instala apa 7 en word aun estas a tiempo (20/11/2025->03:25 am)