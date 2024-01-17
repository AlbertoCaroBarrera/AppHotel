from rest_framework import serializers
from .models import *

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class HabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ['numero_hab','precio_noche']
        
class ReservaSerializerMejorado(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    habitacion = HabitacionSerializer()
    fecha_entrada = serializers.DateField(format=('%d-%m-%Y'))
    fecha_salida = serializers.DateField(format=('%d-%m-%Y'))
    
    class Meta:
        fields = ('cliente','habitacion','fecha_entrada','fecha_salida')
        model = Reserva