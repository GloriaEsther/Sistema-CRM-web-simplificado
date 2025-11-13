from django import forms
from .models import Venta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['claveventa','nombreventa','estatus_cobro','preciototal','cfdi','comentarios','oportunidad_venta']
        #widgets = {'fecha_venta': forms.DateTimeInput(attrs={'type':'datetime-local'})}
