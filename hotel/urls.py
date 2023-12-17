from django.urls import path,re_path
from .import views
urlpatterns = [
    path('',views.index,name='index'),

    path('habitacion/<int:id_habitacion>',views.habitacion_info,name='habitacion_info'),
    path('eventos/<int:anio>/<int:mes>/<int:dia>',views.eventos_info,name='eventos_info'),
    path('empleados/<int:anio>',views.empleados_checkin_anio,name='empleados_checkin_anio'),
    path('comentarios/<str:texto>',views.comentarios_texto,name='comentarios_texto'),
    path('cliente/ultimo',views.ultimo_cliente,name='ultimo_cliente'),
    path('habitacion/sincomodidad',views.habitacion_sincomodidad,name='habitacion_sincomodidad'),
    path('Reservas/cliente/<int:id_cliente>',views.reservas_cliente,name='reservas_cliente'),
    path('Servicios/<int:precio1>/<int:precio2>',views.servicioconreserva,name="servicioconreserva"),
    path('Comodidades/<str:texto>',views.comodidades_texto,name="comodidades_texto"),
    path('puntuacion/ultima/<int:id_evento>',views.ultimapuntuacion,name="ultimapuntuacion"),
    path('eventos/puntuacion3/<int:id_cliente>',views.eventospuntuacion3,name="eventospuntuacion3"),
    path('clientes/sinvotos',views.clientessinvotos,name="clientessinvotos"),
    path('cuentas/nombre/<str:texto>',views.cuentas_nombre,name="cuentas_nombre"),
    path('eventos/media',views.eventosconmediamayor,name="eventosconmediamayor"),
    
   
    path('lista/habitaciones',views.lista_habitaciones,name="lista_habitaciones"),
    path('habitacion/formulario',views.habitacion_create,name="habitacion_create"),
    path('habitacion/buscar',views.habitacion_buscar,name="habitacion_buscar"),
    path('habitacion/busquedaAvanzada',views.habitacion_busqueda_avanzada,name="habitacion_busqueda_avanzada"),
    path('habitacion/editar/<int:habitacion_id>',views.habitacion_editar,name='habitacion_editar'),
    path('habitacion/eleminar/<int:habitacion_id>',views.habitacion_eliminar,name='habitacion_eliminar'),
    
    path('lista/clientes',views.listar_clientes,name='listar_clientes'),
    path('clientes/formulario',views.cliente_create,name="cliente_create"),
    path('cliente/busqueda',views.cliente_busqueda_avanzada,name="cliente_busqueda_avanzada"),
    path('cliente/editar/<int:cliente_id>',views.cliente_editar,name='cliente_editar'),
    path('cliente/eliminar/<int:cliente_id>',views.cliente_eliminar,name='cliente_eliminar'),
    
    path('lista/promociones', views.lista_promociones, name='lista_promociones'),
    path('promocion/formulario',views.promocion_create,name="promocion_create"),
    path('promocion/busqueda',views.promocion_busqueda_avanzada,name="promocion_busqueda_avanzada"),
    path('promocion/editar/<int:promocion_id>',views.promocion_editar,name='promocion_editar'),
    path('promocion/eliminar/<int:promocion_id>',views.promocion_eliminar,name='promocion_eliminar'),
    
    path('listar/reservas', views.listar_reservas, name='listar_reservas'),
    path('reserva/formulario',views.reserva_create,name="reserva_create"),
    path('reserva/busqueda',views.buscar_reservas,name="buscar_reservas"),
    path('reserva/editar/<int:reserva_id>',views.editar_reserva,name='editar_reserva'),
    path('reserva/eliminar/<int:reserva_id>',views.reserva_eliminar,name='reserva_eliminar'),
    
    path('listar/servicios',views.listar_servicios,name="listar_servicios"),
    path('servicio/formulario',views.crear_servicio,name="crear_servicio"),
    path('servicio/busqueda',views.buscar_servicios,name="buscar_servicios"),
    path('servicio/editar/<int:servicio_id>',views.editar_servicio,name='editar_servicio'),
    path('servicio/eliminar/<int:servicio_id>',views.servicio_eliminar,name='servicio_eliminar'),
    
    path('listar/empleados',views.listar_empleados,name="listar_empleados"),
    path('empleado/formulario',views.crear_empleado,name="crear_empleado"),
    path('empleado/busqueda',views.buscar_empleados,name="buscar_empleados"),
    path('empleado/editar/<int:empleado_id>',views.editar_empleado,name='editar_empleado'),
    path('empleado/eliminar/<int:empleado_id>',views.eliminar_empleado,name='eliminar_empleado'),
    
    path('listar/comentarios',views.listar_comentarios,name="listar_comentarios"),
    path('comentario/formulario',views.crear_comentario,name="crear_comentario"),
    path('comentario/busqueda',views.buscar_comentarios,name="buscar_comentarios"),
    path('comentario/editar/<int:comentario_id>',views.editar_comentario,name='editar_comentario'),
    path('comentario/eliminar/<int:comentario_id>',views.eliminar_comentario,name='eliminar_comentario'),
    
    path('registrar',views.registrar_usuario,name="registrar_usuario"),

    
]

