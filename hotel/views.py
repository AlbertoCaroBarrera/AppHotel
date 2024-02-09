from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group

from datetime import datetime
# Create your views here.
def index(request):
    
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return render(request, 'index.html')

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

def lista_habitaciones(request):
    habitacion = Habitacion.objects.all()
    return render(request, 'habitacion/lista_habitacion.html', {'habitaciones': habitacion})
    

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

def habitacion_busqueda_avanzada(request):

    if (len(request.GET)>0):
        formulario = BusquedaAvanzadaHabitacionForm(request.GET)
        if formulario.is_valid():
            mensaje="Se ha buscado por:\n"
            
            QShabitacion = Habitacion.objects
            
            textoBusqueda=formulario.cleaned_data.get('textoBusqueda')
            numero_hab=formulario.cleaned_data.get('numero_hab')
            precio_noche=formulario.cleaned_data.get('precio_noche')
            
            if textoBusqueda is not None:
                QShabitacion = QShabitacion.filter(tipo__contains=textoBusqueda)
                mensaje+=" Contiene: "+ textoBusqueda+"\n"
            
            if numero_hab is not None:
                QShabitacion = QShabitacion.filter(numero_hab=numero_hab)
                mensaje+= str(numero_hab)+"\n"
            
            if precio_noche is not None:
                QShabitacion = QShabitacion.filter(precio_noche__lte=precio_noche)
                mensaje+= str(numero_hab)+"\n"
            
            habitacion = QShabitacion.all()
            
            return render(request,'habitacion/lista_habitacion.html',{"habitaciones":habitacion})
    else:
        formulario = BusquedaAvanzadaHabitacionForm(None)
    return render(request,'habitacion/habitacion_busqueda.html',{"formulario":formulario})




def habitacion_editar(request,habitacion_id):
    habitacion = Habitacion.objects.get(id=habitacion_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = HabitacionForm(datosFormulario,instance = habitacion)
    
    if request.method == "POST":
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                return redirect("lista_habitaciones")
            except Exception as e:
                pass
    return render(request,"habitacion/actualizar.html",{"formulario":formulario,"habitacion":habitacion})


def habitacion_eliminar(request,habitacion_id):
    habitacion = Habitacion.objects.get(id=habitacion_id)
    try:
        habitacion.delete()
        messages.success(request, "Se ha elimnado el habitacion "+habitacion.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_habitaciones')



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
             return redirect("listar_clientes")
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
                return redirect('listar_clientes')  
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
    return redirect('listar_clientes')

def listar_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'reserva/listar_reservas.html', {'reservas': reservas})

def reserva_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = ReservaForm(datosFormulario)
    
    
    if (request.method == "POST"):
        reserva_creado = crear_Reserva_modelo(formulario)
        if(reserva_creado):
            messages.success(request, 'Se ha creado la reserva'+formulario.cleaned_data.get('nombre')+" correctamente")
            return redirect("listar_reservas")
    return render(request,"reserva/create.html", {"formulario_reserva":formulario})



def crear_Reserva_modelo(formulario):
    promocion_creado = False

    if formulario.is_valid():
        try:
            formulario.save()
            promocion_creado = True
        except:
            pass
    return promocion_creado


def buscar_reservas(request):

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaReservaForm(request.GET)
        
        if formulario.is_valid():
            mensaje = "Se ha buscado por:\n"
            
            qs_reservas = Reserva.objects.all()

            texto_busqueda = formulario.cleaned_data.get('texto_busqueda')
            fecha_entrada_desde = formulario.cleaned_data.get('fecha_entrada_desde')
            fecha_entrada_hasta = formulario.cleaned_data.get('fecha_entrada_hasta')

            if texto_busqueda:
                qs_reservas = qs_reservas.filter(
                    Q(cliente__nombre__icontains=texto_busqueda) |
                    Q(habitacion__tipo__icontains=texto_busqueda)
                )
                mensaje += f" Contiene: {texto_busqueda}\n"

            if fecha_entrada_desde:
                qs_reservas = qs_reservas.filter(fecha_entrada=fecha_entrada_desde)
                mensaje += f" Fecha de entrada desde: {fecha_entrada_desde}\n"

            if fecha_entrada_hasta:
                qs_reservas = qs_reservas.filter(fecha_entrada=fecha_entrada_hasta)
                mensaje += f" Fecha de entrada hasta: {fecha_entrada_hasta}\n"

            reservas = qs_reservas.all()
            
            return render(request, 'reserva/listar_reservas.html', {"reservas": reservas, "texto": mensaje})

    else:
        formulario = BusquedaAvanzadaReservaForm(None)

    return render(request, 'reserva/buscar_reservas.html', {"formulario": formulario})


def editar_reserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    
    datos_formulario = None
    
    if request.method == "POST":
        datos_formulario = request.POST
    
    formulario = ReservaForm(datos_formulario, instance=reserva)
    
    if request.method == "POST":
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, f'Se ha editado la reserva {formulario.cleaned_data.get("cliente")} correctamente')
                return redirect('listar_reservas')  
            except Exception as error:
                print(error)
    
    return render(request, 'reserva/actualizar.html', {"formulario": formulario, "reserva": reserva})



def reserva_eliminar(request,reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    try:
        reserva.delete()
        messages.success(request, "Se ha elimnado la reserva "+reserva+" correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_reservas')


def listar_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicio/listar_servicios.html', {'servicios': servicios})

def crear_servicio(request):
    datos_formulario = None

    if request.method == "POST":
        datos_formulario = request.POST

    formulario = ServicioForm(datos_formulario)

    if request.method == "POST":
        servicio_creado = crear_servicio_modelo(formulario)
        if servicio_creado:
            messages.success(request, f'Se ha creado el servicio {formulario.cleaned_data.get("nombre")} correctamente')
            return redirect("listar_servicios")

    return render(request, "servicio/create.html", {"formulario_servicio": formulario})

def crear_servicio_modelo(formulario):
    servicio_creado = False

    if formulario.is_valid():
        try:
            formulario.save()
            servicio_creado = True
        except Exception as error:
            print(error)

    return servicio_creado


def buscar_servicios(request):

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaServicioForm(request.GET)
        
        if formulario.is_valid():
            mensaje = "Se ha buscado por:\n"
            
            qs_servicios = Servicio.objects.all()

            texto_busqueda = formulario.cleaned_data.get('texto_busqueda')
            precio_minimo = formulario.cleaned_data.get('precio_minimo')
            precio_maximo = formulario.cleaned_data.get('precio_maximo')

            if texto_busqueda:
                qs_servicios = qs_servicios.filter(
                    Q(nombre__icontains=texto_busqueda) |
                    Q(descripcion__icontains=texto_busqueda)
                )
                mensaje += f" Contiene: {texto_busqueda}\n"

            if precio_minimo is not None:
                qs_servicios = qs_servicios.filter(precio__gte=precio_minimo)
                mensaje += f" Precio mínimo: {precio_minimo}\n"

            if precio_maximo is not None:
                qs_servicios = qs_servicios.filter(precio__lte=precio_maximo)
                mensaje += f" Precio máximo: {precio_maximo}\n"

            servicios = qs_servicios.all()
            
            return render(request, 'servicio/listar_servicios.html', {"servicios": servicios, "texto": mensaje})

    else:
        formulario = BusquedaAvanzadaServicioForm(None)

    return render(request, 'servicio/buscar_servicios.html', {"formulario": formulario})

def editar_servicio(request, servicio_id):
    servicio = Servicio.objects.get(id=servicio_id)
    
    datos_formulario = None
    
    if request.method == "POST":
        datos_formulario = request.POST
    
    formulario = ServicioForm(datos_formulario, instance=servicio)
    
    if request.method == "POST":
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, f'Se ha editado el servicio {formulario.cleaned_data.get("nombre")} correctamente')
                return redirect('listar_servicios') 
            except Exception as error:
                print(error)
    
    return render(request, 'servicio/actualizar.html', {"formulario": formulario, "servicio": servicio})

def servicio_eliminar(request,servicio_id):
    servicio = Servicio.objects.get(id=servicio_id)
    try:
        servicio.delete()
        messages.success(request, "Se ha elimnado la servicio "+servicio+" correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_servicios')


def listar_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleado/listar_empleados.html', {'empleados': empleados})


def crear_empleado(request):
    datos_formulario = None

    if request.method == "POST":
        datos_formulario = request.POST

    formulario = EmpleadoForm(datos_formulario)

    if request.method == "POST":
        empleado_creado = crear_empleado_modelo(formulario)
        if empleado_creado:
            messages.success(request, f'Se ha creado el empleado {formulario.cleaned_data.get("nombre")} correctamente')
            return redirect("listar_empleados")

    return render(request, "empleado/create.html", {"formulario_empleado": formulario})

def crear_empleado_modelo(formulario):
    empleado_creado = False

    if formulario.is_valid():
        try:
            formulario.save()
            empleado_creado = True
        except Exception as error:
            print(error)

    return empleado_creado

def buscar_empleados(request):

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaEmpleadoForm(request.GET)
        
        if formulario.is_valid():
            mensaje = "Se ha buscado por:\n"
            
            qs_empleados = Empleado.objects.all()

            texto_busqueda = formulario.cleaned_data.get('texto_busqueda')
            cargo = formulario.cleaned_data.get('cargo')

            if texto_busqueda:
                qs_empleados = qs_empleados.filter(
                    Q(nombre__icontains=texto_busqueda) |
                    Q(cargo__icontains=texto_busqueda)
                )
                mensaje += f" Contiene: {texto_busqueda}\n"

            if cargo:
                qs_empleados = qs_empleados.filter(cargo=cargo)
                mensaje += f" Cargo: {cargo}\n"

            empleados = qs_empleados.all()
            
            return render(request, 'empleado/listar_empleados.html', {"empleados": empleados, "texto": mensaje})

    else:
        formulario = BusquedaAvanzadaEmpleadoForm(None)

    return render(request, 'empleado/buscar_empleados.html', {"formulario": formulario})

def editar_empleado(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    
    datos_formulario = None
    
    if request.method == "POST":
        datos_formulario = request.POST
    
    formulario = EmpleadoForm(datos_formulario, instance=empleado)
    
    if request.method == "POST":
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, f'Se ha editado el empleado {formulario.cleaned_data.get("nombre")} correctamente')
                return redirect('listar_empleados')
            except Exception as error:
                print(error)
    
    return render(request, 'empleado/actualizar.html', {"formulario": formulario, "empleado": empleado})

def eliminar_empleado(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    try:
        empleado.delete()
        messages.success(request, f"Se ha eliminado el empleado {empleado.nombre} correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_empleados')


def listar_comentarios(request):
    comentarios = Comentario.objects.all()
    return render(request, 'comentario/listar_comentarios.html', {'comentarios': comentarios})

def crear_comentario(request):
    datos_formulario = None

    if request.method == "POST":
        datos_formulario = request.POST

    formulario = ComentarioForm(datos_formulario)

    if request.method == "POST":
        comentario_creado = crear_comentario_modelo(formulario)
        if comentario_creado:
            messages.success(request, f'Se ha creado el comentario correctamente')
            return redirect("listar_comentarios")

    return render(request, "comentario/create.html", {"formulario_comentario": formulario})

def crear_comentario_modelo(formulario):
    comentario_creado = False

    if formulario.is_valid():
        try:
            formulario.save()
            comentario_creado = True
        except Exception as error:
            print(error)

    return comentario_creado

def buscar_comentarios(request):

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaComentarioForm(request.GET)
        
        if formulario.is_valid():
            mensaje = "Se ha buscado por:\n"
            
            qs_comentarios = Comentario.objects.all()

            texto_busqueda = formulario.cleaned_data.get('texto_busqueda')
            puntuacion_minima = formulario.cleaned_data.get('puntuacion_minima')
            puntuacion_maxima = formulario.cleaned_data.get('puntuacion_maxima')

            if texto_busqueda:
                qs_comentarios = qs_comentarios.filter(
                    Q(cliente__nombre__icontains=texto_busqueda) |
                    Q(habitacion__tipo__icontains=texto_busqueda) |
                    Q(comentario__icontains=texto_busqueda)
                )
                mensaje += f" Contiene: {texto_busqueda}\n"

            if puntuacion_minima is not None:
                qs_comentarios = qs_comentarios.filter(puntuacion__gte=puntuacion_minima)
                mensaje += f" Puntuación mínima: {puntuacion_minima}\n"

            if puntuacion_maxima is not None:
                qs_comentarios = qs_comentarios.filter(puntuacion__lte=puntuacion_maxima)
                mensaje += f" Puntuación máxima: {puntuacion_maxima}\n"

            comentarios = qs_comentarios.all()
            
            return render(request, 'comentario/listar_comentarios.html', {"comentarios": comentarios, "texto": mensaje})

    else:
        formulario = BusquedaAvanzadaComentarioForm(None)

    return render(request, 'comentario/buscar_comentarios.html', {"formulario": formulario})

def editar_comentario(request, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    
    datos_formulario = None
    
    if request.method == "POST":
        datos_formulario = request.POST
    
    formulario = ComentarioForm(datos_formulario, instance=comentario)
    
    if request.method == "POST":
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, f'Se ha editado el comentario correctamente')
                return redirect('listar_comentarios')
            except Exception as error:
                print(error)
    
    return render(request, 'comentario/actualizar.html', {"formulario": formulario, "comentario": comentario})

def eliminar_comentario(request, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    try:
        comentario.delete()
        messages.success(request, f"Se ha eliminado el comentario correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_comentarios')




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
    return render(request,"promocion/reserva_busqueda.html", {"formulario_promocion":formulario})



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







def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if(rol == Usuario.CLIENTE):
                grupo = Group.objects.get(name='Clientes') 
                grupo.user_set.add(user)
                cliente = Cliente.objects.create( usuario = user)
                cliente.save()
            elif(rol == Usuario.EMPLEADO):
                grupo = Group.objects.get(name='Empleados') 
                grupo.user_set.add(user)
                empleado = Empleado.objects.create(usuario = user)
                empleado.save()
            
            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})