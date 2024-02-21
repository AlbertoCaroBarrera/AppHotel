from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication

from .serializers import FileUploadSerializer
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
    serializer = ReservaSerializer(reservas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reserva_list_mejorado(request):
    reserva= Reserva.objects.all()
    serializer = ReservaSerializer(reserva,many=True)
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
    reservaCreateSerializer = ReservaSerializerCreate(data=request.data)
    if reservaCreateSerializer.is_valid():
        try:
            reservaCreateSerializer.save()
            return Response("Reserva CREADA")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(reservaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET']) 
def reserva_obtener(request,reserva_id):
    reserva = Reserva.objects.select_related("cliente").select_related("habitacion")
    reserva = reserva.get(id=reserva_id)
    serializer =  ReservaSerializer(reserva)
    return Response(serializer.data)

@api_view(['PUT'])
def reserva_editar(request,reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    reservaCreateSerializer = ReservaSerializerCreate(data=request.data,instance=reserva)
    if reservaCreateSerializer.is_valid():
        try:
            reservaCreateSerializer.save()
            return Response("reserva EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(reservaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def reserva_actualizar_fecha(request,reserva_id):
    serializers = ReservaSerializerCreate(data=request.data)
    reserva = Reserva.objects.get(id=reserva_id)
    serializers = ReservaSerializerActualizarFecha(data=request.data,instance=reserva)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Reserva EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def reserva_eliminar(request,reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    try:
        reserva.delete()
        return Response("reserva ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def cliente_create(request):
    print(request.data)
    clienteCreateSerializer = ClienteSerializerCreate(data=request.data)
    if clienteCreateSerializer.is_valid():
        try:
            clienteCreateSerializer.save()
            return Response("Cliente CREADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(clienteCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET']) 
def cliente_obtener(request,cliente_id):
    cliente = Cliente.objects
    cliente = cliente.get(id=cliente_id)
    serializer =  ClienteSerializer(cliente)
    return Response(serializer.data)

@api_view(['PUT'])
def cliente_editar(request,cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    clienteCreateSerializer = ClienteSerializerCreate(data=request.data,instance=cliente)
    if clienteCreateSerializer.is_valid():
        try:
            clienteCreateSerializer.save()
            return Response("cliente EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(clienteCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def cliente_actualizar_nombre(request,cliente_id):
    serializers = ClienteSerializerCreate(data=request.data)
    cliente = Cliente.objects.get(id=cliente_id)
    serializers = ClienteSerializerActualizarNombre(data=request.data,instance=cliente)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("cliente EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



    
@api_view(['DELETE'])
def cliente_eliminar(request,cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    try:
        cliente.delete()
        return Response("cliente ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

@api_view(['POST'])
def habitacion_create(request):
    if(request.user.has_perm("hotel.add_habitacion")):
        print(request.data)
        habitacionCreateSerializer = HabitacionSerializerCreate(data=request.data)
        if habitacionCreateSerializer.is_valid():
            try:
                habitacionCreateSerializer.save()
                return Response("Cliente CREADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(habitacionCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene permisos",status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET']) 
def habitacion_obtener(request,habitacion_id):
    habitacion = Habitacion.objects
    habitacion = habitacion.get(id=habitacion_id)
    serializer =  HabitacionSerializer(habitacion)
    return Response(serializer.data)

@api_view(['PUT'])
def habitacion_editar(request,habitacion_id):
    habitacion = Habitacion.objects.get(id=habitacion_id)
    habitacionCreateSerializer = HabitacionSerializerCreate(data=request.data,instance=habitacion)
    if habitacionCreateSerializer.is_valid():
        try:
            habitacionCreateSerializer.save()
            return Response("habitacion EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(habitacionCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def habitacion_actualizar_nombre(request,habitacion_id):
    serializers = HabitacionSerializerCreate(data=request.data)
    habitacion = Habitacion.objects.get(id=habitacion_id)
    serializers = HabitacionSerializerActualizarNombre(data=request.data,instance=habitacion)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Habitacion EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def habitacion_eliminar(request,habitacion_id):
    habitacion = Habitacion.objects.get(id=habitacion_id)
    try:
        habitacion.delete()
        return Response("habitacion ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # you can access the file like this from serializer
            # uploaded_file = serializer.validated_data["file"]
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
# views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny

class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = int(request.data.get('rol'))
                user = Usuario.objects.create_user(
                        username = serializers.data.get("username"), 
                        email = serializers.data.get("email"), 
                        password = serializers.data.get("password1"),
                        ROL = rol,
                        )
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
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


from oauth2_provider.models import AccessToken     
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)