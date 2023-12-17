from django.contrib import admin
from .models import *
	
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Habitacion)
admin.site.register(Reserva)
admin.site.register(Estancia)
admin.site.register(Servicio)
admin.site.register(ReservaServicio)
admin.site.register(Empleado)
admin.site.register(CheckIn)
admin.site.register(CheckOut)
admin.site.register(Comentario)
admin.site.register(Comodidad)
admin.site.register(HabitacionComodidad)
admin.site.register(Evento)
admin.site.register(ReservaEvento)
admin.site.register(Puntuacion)
admin.site.register(CuentaBancaria)
admin.site.register(Promocion)
