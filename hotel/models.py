from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    correo_electronico = models.EmailField()
    telefono = models.IntegerField()
    direccion =  models.TextField()
    
class Habitacion(models.Model):
    numero_hab = models.IntegerField()
    tipo = models.CharField(max_length=200)
    precio_noche = models.FloatField()

class Reserva(models.Model):
    Cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    Habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(default=timezone.now)
    
class Estancia(models.Model):
    Reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    fecha_llegada = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(default=timezone.now)
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.FloatField()
    
class ReservaServicio(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
class Empleado(models.Model):
    nombre = models.CharField(max_length=200)
    trabajo = [("Bo","Botones"),("Re","Recepcionista"),("Se","Servicio de habitaciones"),("At","Atencion al cliente"),("Gp","Gestion y protocolo")]
    cargo = models.CharField(
        max_length=2,
        choices=trabajo,
        default="Bo"
    )
    
class CheckIn(models.Model):
    estancia = models.OneToOneField(Estancia, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_hora_check_in = models.DateTimeField(default=timezone.now)
    
class CheckOut(models.Model):
    estancia = models.OneToOneField(Estancia, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_hora_check_out = models.DateTimeField(default=timezone.now)

class Comentario(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    
class Comodidad(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    
class HabitacionComodidad(models.Model):
    habitacion = models.ForeignKey(Habitacion,on_delete=models.CASCADE)
    comodidad = models.ForeignKey(Comodidad,on_delete=models.CASCADE)
    
class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    hora_inicio = models.DateTimeField(default=timezone.now)
    hora_final = models.DateTimeField(default=timezone.now)
    ubicacion = models.CharField(max_length=200)

class ReservaEvento(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)