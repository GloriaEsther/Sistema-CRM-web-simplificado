from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'nombre',
            'numero',
            'razon_social',
            'rfc_proveedor',
            'codigo_postal',
            'comentarios'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre comercial'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razón social'
            }),
            'rfc_proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RFC (13 caracteres)'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código Postal'
            }),
            'comentarios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Comentarios adicionales'
            }),
        }