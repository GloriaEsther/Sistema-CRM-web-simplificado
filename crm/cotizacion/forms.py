from django import forms
from .models import Cotizacion, CotizacionDetalle,Cliente,Servicio

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class CotizacionDetalleForm(forms.ModelForm):
    class Meta:
        model = CotizacionDetalle
        fields = ['servicio', 'cantidad']
        widgets = {
            'servicio': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
        }
