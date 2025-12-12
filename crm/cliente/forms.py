from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre','apellidopaterno','apellidomaterno',
            'numerotelcli','correo','direccion','rfc',
            'fecha_nacimiento','fecha_ultimocontacto','comentarios',
            'frecuencia_compra','estado_cliente'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidopaterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidomaterno': forms.TextInput(attrs={'class': 'form-control'}),
            'numerotelcli': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_ultimocontacto': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'frecuencia_compra': forms.Select(attrs={'class': 'form-select'}),
            'estado_cliente': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        data = super().clean()
        rfc = data.get('rfc')
        if rfc and Cliente.todos.filter(rfc=rfc).exists():#if rfc and Cliente.activos.filter(rfc=rfc).exists():
            raise forms.ValidationError("Ya existe un cliente activo con ese RFC.")
        return data
