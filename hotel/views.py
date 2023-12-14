from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .models import *
from .forms import *
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')

#1 vamos a hacer una view para listar todos los clientes con sus datos

def listar_clientes(request):
    cliente = Cliente.objects.prefetch_related(
                                Prefetch("cliente_reserva"),
                                Prefetch("cliente_comentario")
    ).all()
    
    return render(request,"cliente/cliente_list.html",{"clientes":cliente})

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
        return render(request,'habitacion/lista_habitacion.html',{"habitacion_mostrar":habitacion,"texto_busqueda":texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")

def habitacion_editar(request,habitacion_id):
    habitacion = Habitacion.objects.get(id=habitacion_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = HabitacionForm(datosFormulario,istance = habitacion)
    
    if request.method == "POST":
        if formulario.is_valir():
            formulario.save()
            try:
                formulario.save()
                return redirect("habitacion_lista")
            except Exception as e:
                pass
    return render(request,"habitacion/actualizar.html",{"formulario":formulario,"habitacion":habitacion})


def cliente_create(request):
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = ClienteForm(datosFormulario)

    
    if (request.method == "POST"):
        cliente_creado = crear_Cliente_modelo(formulario)
        if(cliente_creado):
             messages.success(request, 'Se ha creado el cliente'+formulario.cleaned_data.get('nombre')+" correctamente")
             return redirect("lista_clientes")
    return render(request,"cliente/create.html", {"formulario_cliente":formulario})



def crear_Cliente_modelo(formulario):
    cliente_creado = False

    if formulario.is_valid():
        try:
 
            formulario.save()
            cliente_creado = True
        except:
            pass
    return cliente_creado


def cliente_busqueda_avanzada(request):

    if (len(request.GET)>0):
        formulario = BusquedaAvanzadaClienteForm(request.GET)
        if formulario.is_valid():
            mensaje="Se ha buscado por:\n"
            
            QScliente = Cliente.objects
            
            textoBusqueda=formulario.cleaned_data.get('textoBusqueda')
            telefono=formulario.cleaned_data.get('telefono')

            if textoBusqueda is not None:
                QScliente = QScliente.filter(Q(nombre__contains=textoBusqueda) | Q(correo_electronico__contains=textoBusqueda) | Q(direccion__contains=textoBusqueda))
                mensaje+=" Contiene: "+ textoBusqueda+"\n"
            
            if telefono is not None:
                QScliente = QScliente.filter(telefono__startswith=telefono)
                mensaje+= str(telefono)+"\n"
            
            cliente = QScliente.all()
            
            return render(request,'cliente/cliente_list.html',{"clientes":cliente, "texto":mensaje})
    else:
        formulario = BusquedaAvanzadaClienteForm(None)
    return render(request,'cliente/cliente_busqueda.html',{"formulario":formulario})

def cliente_editar(request,cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = ClienteForm(datosFormulario,instance = cliente)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el cliente'+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('lista_clientes')  
            except Exception as error:
                print(error)
    return render(request, 'cliente/actualizar.html',{"formulario":formulario,"cliente":cliente})

def cliente_eliminar(request,cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    try:
        cliente.delete()
        messages.success(request, "Se ha elimnado el cliente "+cliente.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_clientes')

#Examen formularios

def lista_promociones(request):
    promociones = Promocion.objects.all()
    return render(request, 'promocion/lista_promociones.html', {'promociones': promociones})



def promocion_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = PromocionForm(datosFormulario)

    
    if (request.method == "POST"):
        promocion_creado = crear_Promocion_modelo(formulario)
        if(promocion_creado):
            messages.success(request, 'Se ha creado la promocion'+formulario.cleaned_data.get('nombre')+" correctamente")
            return redirect("lista_promociones")
    return render(request,"promocion/create.html", {"formulario_promocion":formulario})



def crear_Promocion_modelo(formulario):
    promocion_creado = False

    if formulario.is_valid():
        try:
            formulario.save()
            promocion_creado = True
        except:
            pass
    return promocion_creado



def promocion_busqueda_avanzada(request):

    if (len(request.GET)>0):
        formulario = BusquedaAvanzadaPromocionForm(request.GET)
        if formulario.is_valid():
            mensaje="Se ha buscado por:\n"
            
            QSpromocion = Promocion.objects
            
            textoBusqueda=formulario.cleaned_data.get('textoBusqueda')
            fecha_fin_desde=formulario.cleaned_data.get('fecha_fin_desde')
            fecha_fin_hasta=formulario.cleaned_data.get('fecha_fin_hasta')
            descuento_minimo=formulario.cleaned_data.get('descuento_minimo')
            usuarios=formulario.cleaned_data.get('usuarios')
            


            if textoBusqueda is not None:
                QSpromocion = QSpromocion.filter(Q(nombre__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
                mensaje+=" Contiene: "+ textoBusqueda+"\n"
            
            if fecha_fin_desde:
                promociones = promociones.filter(fecha_fin__gte=fecha_fin_desde)

            if fecha_fin_hasta:
                promociones = promociones.filter(fecha_fin__lte=fecha_fin_hasta)

            if descuento_minimo is not None:
                promociones = promociones.filter(descuento__gte=descuento_minimo)

            if usuarios:
                promociones = promociones.filter(usuario__in=usuarios)
            
            promocion = QSpromocion.all()
            
            return render(request,'promocion/lista_promociones.html',{"promociones":promocion, "texto":mensaje})
    else:
        formulario = BusquedaAvanzadaPromocionForm(None)
    return render(request,'promocion/promocion_busqueda.html',{"formulario":formulario})


def promocion_editar(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = PromocionForm(datosFormulario,instance = promocion)
    
    if (request.method == "POST"):

        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado la promocion'+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('lista_promociones')
            except Exception as error:
                print(error)
    return render(request, 'promocion/actualizar.html',{"formulario":formulario,"promocion":promocion})


def promocion_eliminar(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, "Se ha elimnado el promocion "+promocion.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_promociones')