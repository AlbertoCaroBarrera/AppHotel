from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from django.db.models import Q
from rest_framework import status

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
    