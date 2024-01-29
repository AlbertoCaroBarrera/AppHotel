from rest_framework import serializers
from .models import *
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'ROL')
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class ClienteSerializerMejorado(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True, many=True)

    class Meta:
        model = Cliente
        fields = ('usuario', 'nombre', 'correo_electronico', 'telefono', 'direccion')
        
class HabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ['numero_hab','precio_noche']
        
class HabitacionSerializerMejorado(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ('numero_hab', 'tipo', 'precio_noche')
        
class ReservaSerializerMejorado(serializers.ModelSerializer):
    cliente = ClienteSerializerMejorado()
    habitacion = HabitacionSerializerMejorado()
    fecha_entrada = serializers.DateTimeField(format=('%d-%m-%Y %H:%M:%S'))
    fecha_salida = serializers.DateTimeField(format=('%d-%m-%Y %H:%M:%S'))

    class Meta:
        fields = ('cliente','habitacion','fecha_entrada','fecha_salida')
        model = Reserva