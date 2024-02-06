from rest_framework import serializers
from .models import *
from .forms import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class HabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = '__all__'
        
class ClienteSerializerMejorado(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True, many=True)

    class Meta:
        model = Cliente
        fields = ('usuario', 'nombre', 'correo_electronico', 'telefono', 'direccion')
        
class HabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = '__all__'
        
class HabitacionSerializerMejorado(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ('numero_hab', 'tipo', 'precio_noche')
        
class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
        
class ReservaSerializerMejorado(serializers.ModelSerializer):
    cliente = ClienteSerializerMejorado()
    habitacion = HabitacionSerializerMejorado()
    fecha_entrada = serializers.DateTimeField(format=('%d-%m-%Y %H:%M:%S'))
    fecha_salida = serializers.DateTimeField(format=('%d-%m-%Y %H:%M:%S'))

    class Meta:
        fields = ('cliente','habitacion','fecha_entrada','fecha_salida')
        model = Reserva
    
    def validate_fecha_entrada(self,fecha_entrada):
        fechaHoy = date.today()
        if fechaHoy >= fecha_entrada:
            raise serializers.ValidationError('La fecha de entrada debe ser mayor a Hoy')
            return fecha_entrada
        
    def validate_fecha_salida(self,fecha_salida):
        fechaHoy = date.today()
        if fechaHoy >= fecha_salida:
            raise serializers.ValidationError('La fecha de salida debe ser mayor a Hoy')
            return fecha_salida
        
    def validate_cliente(self,cliente):
        if len(cliente) < 1:
            raise serializers.ValidationError('Debe seleccionar al menos un cliente')
        return cliente
    
    def validate_habitacion(self,habitacion):
        if len(habitacion) < 1:
            raise serializers.ValidationError('Debe seleccionar al menos una habitacion')
        return habitacion