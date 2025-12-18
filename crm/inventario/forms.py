from django import forms
from .models import Inventario
from .models import Proveedor

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = [
            'nombrearticulo',
            'descripcion',
            'precio',
            'cantidad_disponible',
            'tipo',
            'unidad',
            'proveedor',
            'comentarios',
        ]

        widgets = {
            'nombrearticulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Café americano'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción breve'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'cantidad_disponible': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'unidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'proveedor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'comentarios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Comentarios adicionales'
            }),
        }
