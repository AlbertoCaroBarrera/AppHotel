from django.urls import path
from .api_views import *

urlpatterns = [
    path('usuarios', usuario_list),
    path('clientes', cliente_list),
    path('clientes/mejorado', cliente_list_mejorado),
    path('clientes/crear',cliente_create),
    path('cliente/<int:cliente_id>',cliente_obtener),
    path('cliente/editar/<int:cliente_id>',cliente_editar),
    path('cliente/actualizar/nombre/<int:cliente_id>',cliente_actualizar_nombre),
    path('cliente/eliminar/<int:cliente_id>',cliente_eliminar),
    
    
    
    path('habitaciones', habitacion_list),
    path('habitaciones/mejorado', habitacion_list_mejorado),
    path('habitacion/crear',habitacion_create),
    path('habitacion/<int:habitacion_id>',habitacion_obtener),
    path('habitacion/editar/<int:habitacion_id>',habitacion_editar),
    path('habitacion/actualizar/nombre/<int:habitacion_id>',habitacion_actualizar_nombre),
    path('habitacion/eliminar/<int:habitacion_id>',habitacion_eliminar),
    
    
    path('reservas', reserva_list),
    path('cliente_busqueda_avanzada',cliente_busqueda_avanzada),
    path('habitacion_busqueda_avanzada',habitacion_busqueda_avanzada),
    path('reserva_busqueda_avanzada',reserva_busqueda_avanzada),
    path('reservas/crear',reserva_create),
    path('reserva/<int:reserva_id>',reserva_obtener),
    path('reserva/editar/<int:reserva_id>',reserva_editar),
    path('reserva/actualizar/fecha/<int:reserva_id>',reserva_actualizar_fecha),
    path('reserva/eliminar/<int:reserva_id>',reserva_eliminar),
    
    path('upload-file/', FileUploadAPIView.as_view(), name='upload-file'),
    
]