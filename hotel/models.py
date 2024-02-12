from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Creamos una tabla de los clientes del hotel
class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    EMPLEADO = 3
    ROLES = ((ADMINISTRADOR, 'administrador'),
            (CLIENTE,'cliente'),
            (EMPLEADO,'empleado'))
    
    ROL = models.PositiveSmallIntegerField(
        choices=ROLES,default=1
    )


class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario,on_delete=models.CASCADE, default=2)
    nombre = models.CharField(max_length=200)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=200)
    direccion =  models.TextField()
    def __str__(self):
        return self.nombre
    
# Creamos una tabla de las habitaciones del hotel
    
class Habitacion(models.Model):
    numero_hab = models.IntegerField()
    tipo = models.CharField(max_length=200)
    precio_noche = models.FloatField()
    def __str__(self):
        return self.tipo

# Creamos una tabla con las reservas de los clientes y las habitaciones que han reservado

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE,related_name='cliente_reserva')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE,related_name='habitacion_reserva')
    fecha_entrada = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(default=timezone.now)
    
# Creamos una tabla con la Estancia real de los clientes. Es decir un cliente realiza una reserva, y en caso de que llegue puede estar mas o menos tiempo
# por lo que la Estancia es lo que realmente si ha estado o no el cliente en el hotel y el tiempo real.
    
class Estancia(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE,related_name='reserva_estancia')
    fecha_llegada = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(default=timezone.now)
    
# Creamos una tabla de servicios que el cliente puede obtener del hotel. Por ejemplo servicio de desayuno, servicio de gimnasio en el hotel...
# Lo unimos con la tabla reserva pues un cliente puede pagar una reserva con un servicio por ejemplo de desayuno en el hotel y luego faltar al hotel,
# por lo que ese servicio ha sido pagado aunque el usuario no haya realizado una Estancia en el hotel.
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.FloatField()
    reserva = models.ManyToManyField(Reserva,through='ReservaServicio',related_name='reserva_servicio')
    def __str__(self):
        return self.nombre

# Tabla intermedia entre los servicios y las reservas. Un servicio puede tener muchas reservas y una reserva muchos servicios.
    
class ReservaServicio(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=True)

# Tabla con los empleados del hotel.

class Empleado(models.Model):
    usuario = models.OneToOneField(Usuario,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    trabajo = [("Bo","Botones"),("Re","Recepcionista"),("Se","Servicio de habitaciones"),("At","Atencion al cliente"),("Gp","Gestion y protocolo")]
    cargo = models.CharField(
        max_length=2,
        choices=trabajo,
        default="Bo"
    )
    def __str__(self):
        return self.nombre
    
# Tabla donde se recoje la estancia del cliente en el hotel, que empleado ha realizado dicho checkin y a que hora se realizo.
    
class CheckIn(models.Model):
    estancia = models.OneToOneField(Estancia, on_delete=models.CASCADE,related_name='estancia_checkin')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE,related_name='empleado_checkin')
    fecha_hora_check_in = models.DateTimeField(default=timezone.now)
    
# Tabla donde se recoje la estancia del cliente en el hotel, que empleado ha realizado dicho checkout y a que hora se realizo.
    
class CheckOut(models.Model):
    estancia = models.OneToOneField(Estancia, on_delete=models.CASCADE,related_name='estancia_checkout')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE,related_name='empleado_checkout')
    fecha_hora_check_out = models.DateTimeField(default=timezone.now)
    
# Tabla sobre los comentarios de los clientes a sus habitaciones. Con una puntuacion que da el usuario en un momento determinado.

class Comentario(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,related_name='cliente_comentario')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE,related_name='habitacion_comentario')
    puntuacion = models.IntegerField()
    comentario = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.comentario
    
    
# Las comodidades a diferencia de los servicios , son las comodidades que dispone cada habitacion.(Los servicios son del hotel en general) 
# Por ejemplo una habitacion puede tener una television ,varias camas dobles, un Minibar, Jacuzzi...
    
class Comodidad(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    habitacion = models.ManyToManyField(Habitacion,through='HabitacionComodidad',related_name='habitacion_comodidad')
    def __str__(self):
        return self.nombre
# Tabla de union entre las habitaciones y sus comodidades.
    
class HabitacionComodidad(models.Model):
    habitacion = models.ForeignKey(Habitacion,on_delete=models.CASCADE)
    comodidad = models.ForeignKey(Comodidad,on_delete=models.CASCADE)
    
# Tabla de eventos que se producen en el hotel. Por ejemplo una Boda. Es un evento durante un tiempo que se produce en algun sitio del hotel. 
# Para la realizacion de este evento es necesario que conste en la reserva del cliente.
    
class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    hora_inicio = models.DateTimeField(default=timezone.now)
    hora_final = models.DateTimeField(default=timezone.now)
    ubicacion = models.CharField(max_length=200)
    reserva = models.ManyToManyField(Reserva,through='ReservaEvento',related_name="reserva_evento")
    def __str__(self):
        return self.nombre
# Tabla de union de los eventos con sus reservas

class ReservaEvento(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    
# Incluimos la tabla puntuacion que los clientes pueden votar los eventos

class Puntuacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,related_name='cliente_puntuacion')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE,related_name='evento_puntuacion')
    puntuacion = models.IntegerField()
    comentario = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

# Incluimos la tabla de la cuentaBancaria del cliente ¡con numero de cuenta correspondiente.

class CuentaBancaria(models.Model):
    cliente = models.OneToOneField(Cliente,on_delete=models.CASCADE)
    BANCOS = [
            ("Ca","Caixa"), 
            ("BB","BBVA"), 
            ("Un", "UNICAJA"), 
            ("In","ING")
            ]
    tipo = models.CharField(max_length=2,choices=BANCOS,default="Ca")
    numero_cuenta = models.IntegerField()
    
# Modelo del examen de formulario

class Promocion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(validators=[MinLengthValidator(100)])
    usuario = models.ForeignKey(Cliente,related_name="promocion_usuario",on_delete=models.CASCADE)
    descuento = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha_fin = models.DateField()

# Modelo con archivos

class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.uploaded_on.date()