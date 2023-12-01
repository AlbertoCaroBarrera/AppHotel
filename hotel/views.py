from django.shortcuts import render,redirect
from datetime import datetime
from django.db.models import Q,Prefetch,Avg
from hotel.models import Cliente, Habitacion, Reserva, Estancia, Servicio, ReservaServicio, Empleado, CheckIn, CheckOut, Comentario, Comodidad, HabitacionComodidad, Evento, ReservaEvento,Puntuacion,CuentaBancaria
from hotel.forms import *
# Create your views here.
def index(request):
    return render(request,'index.html')

#1 vamos a hacer una view para listar todos los clientes con sus datos

def listar_clientes(request):
    cliente = Cliente.objects.prefetch_related(
                                Prefetch("cliente_reserva"),
                                Prefetch("cliente_comentario")
    ).all()
    
    return render(request,"lista/clientes.html",{"clientes":cliente})

#2 vista para ver informacion sobre una habitacion en concreto

def habitacion_info(request,id_habitacion):
    habitacion = Habitacion.objects.prefetch_related(
                                        Prefetch("habitacion_reserva"),
                                        Prefetch("habitacion_comentario"),
                                        Prefetch("habitacion_comodidad")
    )
    habitacion = habitacion.filter(id= id_habitacion).get()
    
    return render(request,"habitacion/habitacion.html",{"habitaciones":habitacion})

#3 vista para ver los eventos de una fecha de inicio concreta (hora de inicio es realmente el año, mes ,dia y hora del evento), buscaremos los eventos de un dia concreto.

def eventos_info(request,anio,mes,dia):
    # calculamos cual seria la hora inicio de ese dia y la hora fin de ese dia, para ver todos los eventos de esa fecha
    fecha_inicio = datetime(int(anio), int(mes), int(dia))
    fecha_fin = fecha_inicio.replace(hour=23, minute=59, second=59)
    
    evento = Evento.objects.prefetch_related('reserva')
    evento = evento.filter(hora_inicio__gte=fecha_inicio, hora_inicio__lte=fecha_fin).all()
    
    return render(request,"evento/evento.html",{"eventos":evento})

#4 vista para ver los empleados que son Recepcionistas e hicieron un checkin o checkout a algun cliente en un año concreto (2023)

def empleados_checkin_anio(request,anio):
    empleado = Empleado.objects.prefetch_related(
                                    Prefetch("empleado_checkin"),
                                    Prefetch("empleado_checkout")
    )
    empleado = empleado.filter(cargo='Re').filter(
        Q(empleado_checkin__fecha_hora_check_in__year=anio)|Q(empleado_checkout__fecha_hora_check_out__year=anio)
        ).distinct().all()    # el distinct es necesario porque sino se repiten. No entiendo muy bien porque se repiten.
    
    return render(request,"empleado/empleados_checkin.html",{"empleados":empleado})

#5 vista para ver los comentarios de los clientes, cuyo comentario contenga una palabra

def comentarios_texto(request,texto):
    comentario = Comentario.objects.select_related("cliente","habitacion")
    comentario = comentario.filter(comentario__contains=texto).all()

    return render(request,"comentario/comentarios_texto.html",{"comentarios":comentario})

#6 vista para ver el ultimo cliente cuya estancia ha terminado. (es decir filtrar por la fecha de salida mas reciente de la estancia del cliente)

def ultimo_cliente(request):
    estancia = Estancia.objects.select_related("reserva")
    estancia = estancia.order_by('-fecha_salida')[:1].get()
    
    #cliente = Cliente.objects.prefetch_related(Prefetch("cliente_reserva"))
    #cliente = cliente.order_by('-cliente_reserva__reserva_estancia__fecha_salida')[:1].get() porque esto no es tmb correcto?
    
    return render(request,"cliente/ultimo_cliente.html",{"estancias":estancia})

#7 vista para las habitaciones sin comodidades

def habitacion_sincomodidad(request):
    habitacion = Habitacion.objects.filter(habitacioncomodidad=None).all()
    return render(request,"habitacion/habitacionsincomodidad.html",{"habitaciones":habitacion})

#8 vista para ver las reservas asociadas a un cliente

def reservas_cliente(request,id_cliente):
    reserva = Reserva.objects.prefetch_related("cliente",
                                                "habitacion",
                                                Prefetch("reserva_estancia"),
                                                Prefetch("reserva_evento"))
    reserva = reserva.filter(cliente=id_cliente).all()
    return render(request,"reserva/reservacliente.html",{"reservas":reserva})

# 9 vista de los Servicios que no tengan una reserva y que el precio servicio esté entre dos valores 

def servicioconreserva(request,precio1,precio2):
    servicio = Servicio.objects.prefetch_related("reserva")
    servicio = servicio.filter(reservaservicio=None,precio__gte=precio1,precio__lte=precio2).all()
    
    return render(request,"servicio/servicioconreserva.html",{"servicios":servicio})

# 10 Vista de las comodidades del hotel que el nombre comienzan por una palabra

def comodidades_texto(request,texto):
    comodidad = Comodidad.objects.prefetch_related("habitacion")
    comodidad = comodidad.filter(nombre__startswith=texto).all()
    
    return render(request,"comodidad/comodidadcontexto.html",{"comodidades":comodidad})    

# 11 Crear una página de Error personalizada para cada uno de los 4 tipos de errores que pueden ocurrir en nuestra Web.

def mi_error_400(request,exception=None):
    return render(request,'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request,'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request,'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request,'errores/500.html',None,None,500)


# El último voto que se realizó en un modelo principal en concreto (para un evento concreto en mi caso), 
# y mostrar el comentario, la votación e información del usuario o cliente que lo realizó.

def ultimapuntuacion(request,id_evento):
    puntuacion = Puntuacion.objects.select_related("cliente","evento")
    puntuacion = puntuacion.filter(evento=id_evento).order_by('-fecha')[:1].get()
    return render(request,"puntuacion/ultimapuntuacion.html",{"puntuaciones":puntuacion})

# Todos los modelos principales(eventos) que tengan votos con una puntuación numérica igual a 3 y que realizó un usuario o cliente en concreto. 

def eventospuntuacion3(request,id_cliente):
    puntuacion = Puntuacion.objects.select_related("cliente","evento")
    puntuacion = puntuacion.filter(puntuacion=3,cliente=id_cliente).all()
    return render(request,"puntuacion/puntuacion3.html",{"puntuaciones":puntuacion})

# Todos los usuarios o clientes que no han votado nunca y mostrar información sobre estos usuarios y clientes al completo..

def clientessinvotos(request):
    usuario = Cliente.objects.prefetch_related(Prefetch("cliente_puntuacion"))
    usuario = usuario.filter(cliente_puntuacion=None).all()
    return render(request,"cliente/sinpuntuacion.html",{"usuarios":usuario})

# Obtener las cuentas bancarias que sean de la Caixa o de Unicaja y que el propietario tenga un nombre que contenga un texto en concreto, por ejemplo “Juan”.

def cuentas_nombre(request,texto):
    cuenta = CuentaBancaria.objects.select_related("cliente")
    cuenta = cuenta.filter(Q(tipo="Ca")|Q(tipo="Un"))
    cuenta = cuenta.filter(cliente__nombre__contains=texto).all()
    return render(request,"cuenta/cuentas_nombre.html",{"cuentas":cuenta})

# Obtener todos los modelos principales que tengan una media de votaciones mayor del 2,5.

def eventosconmediamayor(request):
    evento = Evento.objects.prefetch_related("reserva",Prefetch("evento_puntuacion"))
    evento = evento.annotate(
        media_puntuacion=Avg('evento_puntuacion__puntuacion')
    ).filter(media_puntuacion__gt=2.5)
    return render(request, 'evento/mediamayor.html', {'eventos': evento})

# formularios

def habitacion_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = HabitacionForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("index")
            except Exception as error:
                print(error)
    
    
    return render(request,"habitacion/create.html",{'formulario':formulario})

def habitacion_buscar(request):
    formulario = BusquedaHabitacionForm(request.GET)
    if formulario.is_valid():
        texto  = formulario.cleaned_data.get('textoBusqueda')
        habitacion = Habitacion.objects.filter(Q(numero_hab=texto)|Q(tipo__contains=texto)|Q(precio_noche=texto)).all()
        return render(request,'habitacion/lista_habitacion.html',{"habitacion_mostrar":habitacion},{"texto_busqueda":texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")