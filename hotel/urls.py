from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('lista/clientes',views.listar_clientes,name='lista_clientes'),
    path('habitacion/<int:id_habitacion>',views.habitacion_info,name='habitacion_info'),
    path('eventos/<int:anio>/<int:mes>/<int:dia>',views.eventos_info,name='eventos_info'),
    path('empleados/<int:anio>',views.empleados_checkin_anio,name='empleados_checkin_anio'),
    path('comentarios/<str:texto>',views.comentarios_texto,name='comentarios_texto'),
    path('cliente/ultimo',views.ultimo_cliente,name='ultimo_cliente'),
    path('habitacion/sincomodidad',views.habitacion_sincomodidad,name='habitacion_sincomodidad'),
    path('Reservas/cliente/<int:id_cliente>',views.reservas_cliente,name='reservas_cliente'),
    path('Servicios/<int:precio1>/<int:precio2>',views.servicioconreserva,name="servicioconreserva"),
    path('Comodidades/<str:texto>',views.comodidades_texto,name="comodidades_texto"),
]

