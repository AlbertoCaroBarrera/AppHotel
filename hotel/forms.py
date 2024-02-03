from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm

class BusquedaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    

class HabitacionForm(ModelForm):
    class Meta:
        model = Habitacion
        fields = [ 'numero_hab', 'tipo', 'precio_noche' ]
        labels = {
            "numero_hab":("Numero de la habitacion"),
            "tipo":("Tipo de habitacion"),
            "precio_noche":("Precio de la habitacion por noche")
        }
        help_texts = {
            "numero_hab":("Valor entre el 1 y 100"),
            "tipo":("100 caracteres como maximo"),
            "precio_noche":("Precio entre 50 y 200")
        }

    def clean(self):
        super().clean()
        numero_hab = self.cleaned_data.get('numero_hab')
        tipo = self.cleaned_data.get('tipo')
        precio_noche = self.cleaned_data.get('precio_noche')
        # comprobamos que no exista una habitacion con ese mismo numero_hab
        habitacionNumero = Habitacion.objects.filter(numero_hab=numero_hab).first()
        if (not habitacionNumero is None):
            self.add_error('numero_hab','Ya existe una habitacion con ese numero')
        
        if not(1<=int(numero_hab)<=100):
            self.add_error('numero_hab','La habitacion tiene que tener un valor entre 1 y 100')
        if not(50<=int(precio_noche)<=200):
            self.add_error('precio_noche','El precio de la habitacion tiene que tener un valor entre 50 y 200€')
        

        return self.cleaned_data


class BusquedaHabitacionForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)

class BusquedaAvanzadaHabitacionForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    numero_hab = forms.IntegerField(required=False)
    
    precio_noche = forms.FloatField(required=False)
    
    def clean(self):
        super().clean()
        
        #Obtenemos los campos 
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        numero_hab = self.cleaned_data.get('numero_hab')
        precio_noche = self.cleaned_data.get('precio_noche')
            
        #Controlamos los campos
        #Ningún campo es obligatorio, pero al menos debe introducir un valor en alguno para buscar
        if(textoBusqueda == "" 
           and numero_hab is None
           and precio_noche is None
           ):
            self.add_error('textoBusqueda','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('numero_hab','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('precio_noche','Debe introducir al menos un valor en un campo del formulario')
        else:

            if len(textoBusqueda) > 100:
                self.add_error("textoBusqueda","La descripción debe tener menos de 100 caracteres.")
            if not numero_hab is None:
                if not 1 <= numero_hab <= 100:
                    self.add_error("numero_hab","El numero_hab debe ser un valor entero entre 1 y 100.")
            if not precio_noche is None:
                if not 50 <= precio_noche <= 200:
                    self.add_error("precio_noche","El precio_noche debe ser un valor entero entre 50 y 200€.")
        return self.cleaned_data
            

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['usuario','nombre', 'correo_electronico', 'telefono', 'direccion']
        labels = {
            "usuario":("usuario"),
            "nombre": ("Nombre"),
            "correo_electronico": ("correo electronico"),
            "telefono": ("Introduzca el teléfono"),
            "direccion": ("direccion")
        }
        
        help_texts = {
            "nombre": ("50 caracteres como máximo"),
            "telefono": ("9 caracteres"),
        }

    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get("nombre")
        correo_electronico = self.cleaned_data.get("correo_electronico")
        telefono = self.cleaned_data.get("telefono")
        direccion = self.cleaned_data.get("direccion")

    
        if len(nombre) < 4:
            self.add_error("nombre", "Debe tener al menos 4 caracteres")
            
        if len(correo_electronico) < 10:
            self.add_error("correo_electronico", "Debe tener al menos 10 caracteres")
            
        
        if len(str(telefono)) < 9 or len(str(telefono)) > 9:
            self.add_error("telefono", "Debe contener 9 caracteres")

        if len(direccion) < 1:
            self.add_error("direccion", "Debe contener una direccion mas larga")

        return self.cleaned_data
    
    
class BusquedaAvanzadaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    telefono = forms.IntegerField(required=False)
    usuarios = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(),  
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Usuarios'
    )

    def clean(self):
        super().clean()
        textoBusqueda=self.cleaned_data.get('textoBusqueda')
        telefono=self.cleaned_data.get('telefono')

        if(textoBusqueda == ""
           and telefono is None):
            
            self.add_error('textoBusqueda','Debes introducir algún valor')
            self.add_error('telefono','Debes introducir algún valor')
            
        else:
            if (textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda','Debe introducir al menos 3 caracteres')

            if (not telefono is None and len(str(telefono)) != 9):
                self.add_error('telefono','Debe tener 9 digitos')

        return self.cleaned_data


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'fecha_entrada', 'fecha_salida']
        labels = {
            'cliente': 'Cliente',
            'habitacion': 'Habitación',
            'fecha_entrada': 'Fecha de Entrada',
            'fecha_salida': 'Fecha de Salida',
        }

    def clean(self):
        super().clean()
        fecha_entrada = self.cleaned_data.get('fecha_entrada')
        fecha_salida = self.cleaned_data.get('fecha_salida')

        if fecha_entrada and fecha_salida and fecha_entrada >= fecha_salida:
            self.add_error('fecha_salida', 'La fecha de salida debe ser posterior a la fecha de entrada.')

        return self.cleaned_data

class BusquedaAvanzadaReservaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label='Buscar en cliente y habitación')
    fecha_desde = forms.DateField(required=False, label='Fecha de entrada desde')
    fecha_hasta = forms.DateField(required=False, label='Fecha de entrada hasta')

    def clean(self):
        super().clean()
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')

        if not textoBusqueda and not fecha_desde and not fecha_hasta:
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario')


        if fecha_desde and fecha_hasta and fecha_hasta < fecha_desde:
            self.add_error('fecha_entrada_desde', 'La fecha hasta no puede ser menor que la fecha desde')
            self.add_error('fecha_hasta', 'La fecha hasta no puede ser menor que la fecha desde')

        return self.cleaned_data



class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'reserva']
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripción",
            "precio": "Precio",
            "reserva": "Reserva",
        }

        help_texts = {
            "nombre": "El nombre tiene que ser único.",
            "descripcion": "Debe tener al menos 100 caracteres.",
            "precio": "El precio debe ser un valor numérico.",
            "reserva": "Seleccione las reservas asociadas al servicio.",
        }

    def clean(self):
        super().clean()

        descripcion = self.cleaned_data.get("descripcion")
        precio = self.cleaned_data.get("precio")

        if len(descripcion) < 100:
            self.add_error("descripcion", "La descripción debe tener al menos 100 caracteres.")

        if not isinstance(precio, (int, float)):
            self.add_error("precio", "El precio debe ser un valor numérico.")

        return self.cleaned_data

class BusquedaAvanzadaServicioForm(forms.Form):
    texto_busqueda = forms.CharField(required=False, label='Buscar en nombre y descripción')
    precio_minimo = forms.FloatField(required=False, label='Precio mínimo')
    precio_maximo = forms.FloatField(required=False, label='Precio máximo')
    reservas = forms.ModelMultipleChoiceField(
        queryset=Reserva.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Reservas'
    )

    def clean(self):
        super().clean()
        texto_busqueda = self.cleaned_data.get('texto_busqueda')
        precio_minimo = self.cleaned_data.get('precio_minimo')
        precio_maximo = self.cleaned_data.get('precio_maximo')

        if not texto_busqueda and not precio_minimo and not precio_maximo:
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario')

        if texto_busqueda == "":
            if not precio_minimo and not precio_maximo:
                self.add_error('texto_busqueda', 'Debes introducir algún valor')


        if precio_minimo is not None and precio_maximo is not None and precio_maximo < precio_minimo:
            self.add_error('precio_minimo', 'El precio máximo no puede ser menor que el precio mínimo')
            self.add_error('precio_maximo', 'El precio máximo no puede ser menor que el precio mínimo')

        return self.cleaned_data


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['usuario', 'nombre', 'cargo']
        labels = {
            "usuario": "Usuario",
            "nombre": "Nombre",
            "cargo": "Cargo",
        }

        help_texts = {
            "usuario": "Seleccione el usuario asociado al empleado.",
            "nombre": "Ingrese el nombre del empleado.",
            "cargo": "Seleccione el cargo del empleado.",
        }

    def clean(self):
        super().clean()

        nombre = self.cleaned_data.get("nombre")

        if len(nombre) < 1:
            self.add_error("nombre", "El nombre del empleado no puede estar vacío.")

        return self.cleaned_data

class BusquedaAvanzadaEmpleadoForm(forms.Form):
    texto_busqueda = forms.CharField(required=False, label='Buscar por nombre y cargo')
    cargo = forms.ChoiceField(
        choices=Empleado.trabajo,
        required=False,
        label='Cargo'
    )

    def clean(self):
        super().clean()
        texto_busqueda = self.cleaned_data.get('texto_busqueda')
        cargo = self.cleaned_data.get('cargo')

        if not texto_busqueda and not cargo:
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario')

        return self.cleaned_data



class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['cliente', 'habitacion', 'puntuacion', 'comentario','fecha']
        labels = {
            "cliente": "Cliente",
            "habitacion": "Habitación",
            "puntuacion": "Puntuación",
            "comentario": "Comentario",
            "fecha":"fecha",
        }

        help_texts = {
            "cliente": "Seleccione el cliente asociado al comentario.",
            "habitacion": "Seleccione la habitación asociada al comentario.",
            "puntuacion": "Ingrese la puntuación del comentario.",
            "comentario": "Escriba el comentario.",
            "fecha":"Escriba la fecha",
        }

    def clean(self):
        super().clean()

        puntuacion = self.cleaned_data.get("puntuacion")
        comentario = self.cleaned_data.get("comentario")
        

        if not 0 <= puntuacion <= 5:
            self.add_error("puntuacion", "La puntuación debe estar entre 0 y 5.")

        if len(comentario) < 1:
            self.add_error("comentario", "El comentario no puede estar vacío.")

        return self.cleaned_data

class BusquedaAvanzadaComentarioForm(forms.Form):
    texto_busqueda = forms.CharField(required=False, label='Buscar por cliente y habitación')
    puntuacion_minima = forms.IntegerField(required=False, label='Puntuación mínima')
    puntuacion_maxima = forms.IntegerField(required=False, label='Puntuación máxima')

    def clean(self):
        super().clean()
        texto_busqueda = self.cleaned_data.get('texto_busqueda')
        puntuacion_minima = self.cleaned_data.get('puntuacion_minima')
        puntuacion_maxima = self.cleaned_data.get('puntuacion_maxima')

        if not texto_busqueda and not puntuacion_minima and not puntuacion_maxima:
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario')

        if puntuacion_minima is not None and puntuacion_maxima is not None and puntuacion_maxima < puntuacion_minima:
            self.add_error('puntuacion_minima', 'La puntuación máxima no puede ser menor que la puntuación mínima')
            self.add_error('puntuacion_maxima', 'La puntuación máxima no puede ser menor que la puntuación mínima')

        return self.cleaned_data
# Formularios del examen


class PromocionForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre', 'descripcion', 'usuario', 'descuento','fecha_fin']
        labels = {
            "nombre": ("Nombre"),
            "descripcion": ("Descripcion"),
            "usuario": ("Introduzca el usuario"),
            "descuento": ("descuento"),
            "fecha_fin":'fecha_fin'
        }
        
        help_texts = {
            "nombre": ("el nombre tiene que ser único."),
            "descripcion": ("Debe tener al menos 100 caracteres"),
            "usuario": ("Un usuario no puede usar la misma promoción dos veces"),
            "descuento": ("Tiene que ser un valor entero entre 0 y 100"),
            "fecha_fin":('Esta fecha no puede inferior a la fecha actual')
        }

    def clean(self):
        super().clean()

        descripcion = self.cleaned_data.get("descripcion")
        usuario = self.cleaned_data.get("usuario")
        descuento = self.cleaned_data.get("descuento")
        fecha_fin = self.cleaned_data.get("fecha_fin")

        existing_promocion = Promocion.objects.filter(usuario=usuario).first()
        if existing_promocion:
            self.add_error("usuario","Este usuario ya tiene una promoción asociada.")

        if len(descripcion) < 100:
            self.add_error("descripcion","La descripción debe tener al menos 100 caracteres.")

        if fecha_fin < timezone.now().date():
            self.add_error("fecha_fin","La fecha fin no puede ser inferior a la fecha actual.")

        if not 0 <= descuento <= 100:
            self.add_error("descuento","El descuento debe ser un valor entero entre 0 y 100.")

        return self.cleaned_data
    

class BusquedaAvanzadaPromocionForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label='Buscar en nombre y descripción')
    fecha_fin_desde = forms.DateField(required=False, label='Fecha fin desde')
    fecha_fin_hasta = forms.DateField(required=False, label='Fecha fin hasta')
    descuento_minimo = forms.IntegerField(required=False, label='Descuento mínimo')
    usuarios = forms.ModelMultipleChoiceField(
        queryset=Cliente.objects.all(),  
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Usuarios'
    )
    

    def clean(self):
        super().clean()
        textoBusqueda=self.cleaned_data.get('textoBusqueda')
        fecha_fin_desde=self.cleaned_data.get('fecha_fin_desde')
        fecha_fin_hasta=self.cleaned_data.get('fecha_fin_hasta')
        descuento_minimo=self.cleaned_data.get('descuento_minimo')

        if(textoBusqueda == "" 
           and fecha_fin_desde is None
           and fecha_fin_hasta is None
           ):
            self.add_error('textoBusqueda','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_fin_desde','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_fin_hasta','Debe introducir al menos un valor en un campo del formulario')
        else:
            if(textoBusqueda == ""):
                self.add_error('textoBusqueda','Debes introducir algún valor')
            else:
                if len(textoBusqueda) < 100:
                    self.add_error("textoBusqueda","La descripción debe tener al menos 100 caracteres.")

            if(not fecha_fin_desde is None  and not fecha_fin_hasta is None and fecha_fin_hasta < fecha_fin_desde):
                self.add_error('fecha_fin_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_fin_hasta','La fecha hasta no puede ser menor que la fecha desde')

            if not 0 <= descuento_minimo <= 100:
                self.add_error("descuento_minimo","El descuento debe ser un valor entero entre 0 y 100.")

        return self.cleaned_data


class RegistroForm(UserCreationForm): 
    roles = (
                                (Usuario.CLIENTE, 'cliente'),
                                (Usuario.EMPLEADO, 'empleado'),
            )   
    rol = forms.ChoiceField(choices=roles)  
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2','rol')