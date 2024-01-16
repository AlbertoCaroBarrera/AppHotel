from django.urls import path
from .api_views import *

urlpatterns = [
    path('clientes',cliente_list)
]