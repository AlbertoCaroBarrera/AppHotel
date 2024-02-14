from rest_framework import serializers
from .models import *
from .forms import *
from django.utils import timezone

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
        
class ReservaSerializerCreate(serializers.ModelSerializer):
    fecha_entrada = serializers.DateTimeField(format=('%d-%m-%Y %H:%M:%S'))
    fecha_salida = serializers.DateTimeField(format=('%d-%m-%Y %H:%M:%S'))

    class Meta:
        model = Reserva
        fields = ('cliente','habitacion','fecha_entrada','fecha_salida')
    
    def validate_fecha_entrada(self, fecha_entrada):
        fecha_actual = timezone.now()
        if fecha_actual >= fecha_entrada:
            raise serializers.ValidationError('La fecha de entrada debe ser mayor a Hoy')
        return fecha_entrada
        
    def validate_fecha_salida(self, fecha_salida):
        fecha_actual = timezone.now()
        if fecha_actual >= fecha_salida:
            raise serializers.ValidationError('La fecha de salida debe ser mayor a Hoy')
        return fecha_salida
        
    def validate_cliente(self,cliente):
        if not cliente:
            raise serializers.ValidationError('Debe seleccionar al menos un cliente')
        return cliente
    
    def validate_habitacion(self,habitacion):
        if not habitacion:
            raise serializers.ValidationError('Debe seleccionar al menos una habitacion')
        return habitacion
    
class ReservaSerializerActualizarFecha(serializers.ModelSerializer):
 
    class Meta:
        model = Reserva
        fields = ['fecha_entrada']
    
    def validate_fecha(self,fecha_entrada):
        reservaFecha = Reserva.objects.filter(fecha_entrada=fecha_entrada).first()
        if(not reservaFecha is None and reservaFecha.id != self.instance.id):
            raise serializers.ValidationError('Ya existe una reserva con ese tipo')
        return fecha_entrada
    
    
class ClienteSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('nombre', 'correo_electronico', 'telefono', 'direccion')
        
    def validate_nombre(self, nombre):
        if not nombre:
            raise serializers.ValidationError('Debe proporcionar un nombre')
        return nombre
    
    def validate_correo_electronico(self, correo_electronico):
        if not correo_electronico:
            raise serializers.ValidationError('Debe proporcionar un correo electrónico')
        return correo_electronico



class HabitacionSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ('numero_hab', 'tipo', 'precio_noche')
        
    def validate_numero_habitacion(self, numero_hab):
        if numero_hab>100 or numero_hab<0 or not numero_hab:
            raise serializers.ValidationError('La habitacion no existe')
        return numero_hab
    
class ClienteSerializerActualizarNombre(serializers.ModelSerializer):
 
    class Meta:
        model = Cliente
        fields = ['nombre']
    
    def validate_nombre(self,nombre):
        clientenombre = Cliente.objects.filter(nombre=nombre).first()
        if(not clientenombre is None and clientenombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe un cliente con ese nombre')
        return nombre
    


class HabitacionSerializerActualizarNombre(serializers.ModelSerializer):
 
    class Meta:
        model = Habitacion
        fields = ['tipo']
    
    def validate_nombre(self,tipo):
        habitacionTipo = Habitacion.objects.filter(tipo=tipo).first()
        if(not habitacionTipo is None and habitacionTipo.id != self.instance.id):
            raise serializers.ValidationError('Ya existe una habitacion con ese tipo')
        return tipo
    


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file', 'uploaded_on',)
        

class UsuarioSerializerRegistro(serializers.Serializer):
 
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    
    def validate_username(self,username):
        usuario = Usuario.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username