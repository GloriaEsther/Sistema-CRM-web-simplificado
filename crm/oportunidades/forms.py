from django import forms
from .models import Oportunidad,Usuario
from ventas.models import Venta, EtapaVentas

class OportunidadForm(forms.ModelForm):
    class Meta:
        model = Oportunidad
        fields = ['nombreoportunidad','valor_estimado','fecha_cierre_estimada','comentarios','cliente_oportunidad','etapa_ventas','usuario_responsable']
        widgets = {'fecha_cierre_estimada': forms.DateInput(attrs={'type':'date'})}

'''
def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar por apellido paterno
        self.fields['usuario_responsable'].queryset = Usuario.activos.all().order_by(
            'apellidopaterno', 'apellidomaterno','nombre'
        )
           

'''
    