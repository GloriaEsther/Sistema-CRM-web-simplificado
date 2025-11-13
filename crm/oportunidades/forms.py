from django import forms
from .models import Oportunidad
from ventas.models import Venta, EtapaVentas

class OportunidadForm(forms.ModelForm):
    class Meta:
        model = Oportunidad
        fields = ['nombreoportunidad','valor_estimado','fecha_cierre_estimada','comentarios','cliente_oportunidad','etapa_ventas','usuario_responsable']
        widgets = {'fecha_cierre_estimada': forms.DateInput(attrs={'type':'date'})}
