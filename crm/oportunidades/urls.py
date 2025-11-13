from django.urls import path
from . import views

app_name = 'oportunidades'
urlpatterns = [
    path('kanban/', views.kanban, name='kanban'),
    path('crear/', views.crear_oportunidad, name='crear_oportunidad'),
    path('mover/<int:pk>/', views.mover_oportunidad, name='mover_oportunidad'),  # AJAX
]
