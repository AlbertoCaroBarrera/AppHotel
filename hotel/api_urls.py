from django.urls import path
from .api_views import *

urlpatterns = [
    path('usuarios', usuario_list),
    path('clientes', cliente_list),
    path('clientes/mejorado', cliente_list_mejorado),
    path('habitaciones', habitacion_list),
    path('habitaciones/mejorado', habitacion_list_mejorado),
    path('reservas', reserva_list),
]