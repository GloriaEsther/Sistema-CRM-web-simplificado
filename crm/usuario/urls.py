from django.urls import path
from . import views

app_name='usuario'

urlpatterns = [
    #Dueño
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('inicio/', views.inicio, name='inicio'),
    path('subir-logo/', views.subir_logo, name='subir_logo'),
    path('editar/<int:pk>/', views.editar_perfil, name='editar_usuario'),
    
    #Relacionado a Empleado
    path('agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('listar_empleados/', views.empleados_lista, name='empleados_lista'),
    path('editar_empleado/<int:pk>/', views.editar_empleado, name='editar_empleado'),
    path('consultar_empleado/<int:pk>/',views.consultar_empleado,name="consultar_empleado"),
    
    #Eliminar
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    
]
