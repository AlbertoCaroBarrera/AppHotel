from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

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

