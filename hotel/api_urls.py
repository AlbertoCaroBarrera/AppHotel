from django.urls import path
from .api_views import *

urlpatterns = [
    path('clientes',cliente_list),
    path('reservas',reserva_list),
    path('cliente_buscar',cliente_buscar),
]