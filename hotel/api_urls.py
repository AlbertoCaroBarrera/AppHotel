from django.urls import path
from .api_views import *

urlpatterns = [
    path('usuarios', usuario_list),
    path('clientes', cliente_list),
    path('clientes/mejorado', cliente_list_mejorado),
    path('habitaciones', habitacion_list),
    path('habitaciones/mejorado', habitacion_list_mejorado),
    path('reservas', reserva_list),
    path('cliente_busqueda_avanzada',cliente_busqueda_avanzada),
    path('habitacion_busqueda_avanzada',habitacion_busqueda_avanzada),
    path('reserva_busqueda_avanzada',reserva_busqueda_avanzada),
    
]