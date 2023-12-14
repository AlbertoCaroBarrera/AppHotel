from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime

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
        precio = self.cleaned_data.get('precio')
        # comprobamos que no exista una habitacion con ese mismo numero_hab
        habitacionNumero = Habitacion.objects.filter(numero_hab=numero_hab).first()

        if (not habitacionNumero is None):
            self.add_error('numero_hab','Ya existe una habitacion con ese numero')

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
            ):
            self.add_error('textoBusqueda','Debe introducir al menos un valor en un campo del formulario')
        else:
            #Si introduce un texto al menos que tenga  3 caracteres o más
            if(textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda','Debe introducir al menos 3 caracteres')
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo_electronico', 'telefono', 'direccion']
        labels = {
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
            if(textoBusqueda == "" is None):
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
