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