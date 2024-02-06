from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
def usuario_list(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cliente_list(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cliente_list_mejorado(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializerMejorado(clientes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def habitacion_list(request):
    habitaciones = Habitacion.objects.all()
    serializer = HabitacionSerializer(habitaciones, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def habitacion_list_mejorado(request):
    habitaciones = Habitacion.objects.all()
    serializer = HabitacionSerializerMejorado(habitaciones, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reserva_list(request):
    reservas = Reserva.objects.all()
    serializer = ReservaSerializerMejorado(reservas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reserva_list_mejorado(request):
    reserva= Reserva.objects.all()
    serializer = ReservaSerializerMejorado(reserva,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def cliente_buscar(request):
    
    formulario = BusquedaClienteForm(request.query_params)
    if(formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        clientes = Cliente.objects.select_related('usuario')
        clientes = clientes.filter(Q(nombre__contains=texto)|Q(direccion__contains=texto)).all()
        serializers = ClienteSerializer(clientes,many=True)
        return Response(serializers.data)
    else:
        return Response(formulario.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def cliente_busqueda_avanzada(request):
    

    if (len(request.query_params)>0):
        formulario = BusquedaAvanzadaClienteForm(request.query_params)
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
            
            serializer = ClienteSerializer(cliente,many=True)

            return Response(serializer.data)
            
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def habitacion_busqueda_avanzada(request):
    
    if (len(request.query_params)>0):
        formulario = BusquedaAvanzadaHabitacionForm(request.query_params)
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
                QShabitacion = QShabitacion.filter(numero_hab__startswith=numero_hab)
                mensaje+= str(numero_hab)+"\n"
                
            if precio_noche is not None:
                QShabitacion = QShabitacion.filter(precio_noche__startswith=precio_noche)
                mensaje+= str(precio_noche)+"\n"

            habitacion = QShabitacion.all()
            
            serializer = HabitacionSerializer(habitacion,many=True)

            return Response(serializer.data)
            
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def reserva_busqueda_avanzada(request):
    
    if (len(request.query_params)>0):
        formulario = BusquedaAvanzadaReservaForm(request.query_params)
        if formulario.is_valid():
            mensaje="Se ha buscado por:\n"
            
            QSreserva = Reserva.objects
            
            textoBusqueda=formulario.cleaned_data.get('textoBusqueda')
            fecha_desde=formulario.cleaned_data.get('fecha_desde')
            fecha_hasta=formulario.cleaned_data.get('fecha_hasta')
            
            if textoBusqueda is not None:
                QSreserva = QSreserva.filter(
                    Q(cliente__nombre__icontains=textoBusqueda) |
                    Q(habitacion__tipo__icontains=textoBusqueda)
                )
                
                mensaje+=" Contiene: "+ textoBusqueda+"\n"
            
            #Comprobamos fechas
            #Obtenemos los libros con fecha publicacion mayor a la fecha desde
            if(not fecha_desde is None):
                QSreserva = QSreserva.filter(fecha_desde__gte=fecha_desde)
            
             #Obtenemos los libros con fecha publicacion menor a la fecha desde
            if(not fecha_hasta is None):
                QSreserva = QSreserva.filter(fecha_hasta__lte=fecha_hasta)

            reserva = QSreserva.all()
            
            serializer = ReservaSerializer(reserva,many=True)

            return Response(serializer.data)
            
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def reserva_create(request):
    serializers = ReservaSerializerMejorado(data=request.data)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Reserva Creada")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    