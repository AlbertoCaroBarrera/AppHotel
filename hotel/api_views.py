from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch

@api_view(['GET'])
def cliente_list(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reserva_list(request):
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