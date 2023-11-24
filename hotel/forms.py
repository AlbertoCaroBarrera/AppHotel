from django.forms import ModelForm
from hotel.models import *
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