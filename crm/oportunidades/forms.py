from django import forms
from .models import Oportunidad,Usuario
from ventas.models import Venta, EtapaVentas

class OportunidadForm(forms.ModelForm):
    class Meta:
        model = Oportunidad
        fields = ['nombreoportunidad','valor_estimado','fecha_cierre_estimada','comentarios','cliente_oportunidad','etapa_ventas','usuario_responsable']
        widgets = {'fecha_cierre_estimada': forms.DateInput(attrs={'type':'date'})}

    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get('nombreoportunidad')
        cliente = cleaned.get('cliente_oportunidad')
        if nombre and cliente:
            if Oportunidad.todos.filter(nombreoportunidad__iexact=nombre, cliente_oportunidad=cliente).exists():
                raise forms.ValidationError("Ya existe una oportunidad con ese nombre para ese cliente.")
        return cleaned