# AppHotel

Este será mi projecto de gestión de reserva de hoteles.



Examen 

He añadido nuevo modelo Promocion

He añadido el formulario de PromocionForm y BusquedaAvanzadaPromocionForm. 

He añadido las vistas lista_promociones, promocion_create, crear_Promocion_modelo y promocion_busqueda_avanzada, promocion_editar y promocion_eliminar

La carpeta de los nuevos templates es templates/promocion/


Ejercicios de CRUDS realizado a los siguientes modelos:

Habitacion
Cliente
Reserva
Servicio
Empleado
Comentario

HabitacionForm:
numero_hab: Debe ser único y estar entre 1 y 100.
tipo: Longitud máxima de 100 caracteres.
precio_noche: Debe estar entre 50 y 200.

BusquedaHabitacionForm:
textoBusqueda: Debe tener menos de 100 caracteres.

BusquedaAvanzadaHabitacionForm:
textoBusqueda: Debe tener menos de 100 caracteres.
numero_hab: Debe ser un valor entero entre 1 y 100.
precio_noche: Debe ser un valor entre 50 y 200.

ClienteForm:
nombre: Debe tener al menos 4 caracteres.
correo_electronico: Debe tener al menos 10 caracteres.
telefono: Debe tener exactamente 9 dígitos.
direccion: Debe tener al menos 1 caracter.

BusquedaAvanzadaClienteForm:
textoBusqueda: Debe tener al menos 3 caracteres si se proporciona.
telefono: Debe tener exactamente 9 dígitos si se proporciona.

ReservaForm:
fecha_entrada: Debe ser anterior a fecha_salida.

BusquedaAvanzadaReservaForm:
texto_busqueda: Debe tener menos de 100 caracteres si se proporciona.
fecha_entrada_desde y fecha_entrada_hasta: La fecha hasta no puede ser menor que la fecha desde.

ServicioForm:
nombre: Debe ser único.
descripcion: Debe tener al menos 100 caracteres.
precio: Debe ser un valor numérico.

BusquedaAvanzadaServicioForm:
texto_busqueda: Debe tener menos de 100 caracteres si se proporciona.
precio_minimo y precio_maximo: El precio máximo no puede ser menor que el precio mínimo.

EmpleadoForm:
nombre: No puede estar vacío.

BusquedaAvanzadaEmpleadoForm:
texto_busqueda: Debe tener al menos 1 caracter si se proporciona.

ComentarioForm:
puntuacion: Debe estar entre 0 y 5.
comentario: No puede estar vacío.

BusquedaAvanzadaComentarioForm:
texto_busqueda: Debe tener al menos 1 caracter si se proporciona.
puntuacion_minima y puntuacion_maxima: La puntuación máxima no puede ser menor que la puntuación mínima.