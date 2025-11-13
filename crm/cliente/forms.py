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
        widgets = {'fecha_nacimiento': forms.DateInput(attrs={'type':'date'})}

    def clean(self):
        data = super().clean()
        correo = data.get('correo')
        rfc = data.get('rfc')
        # validar duplicados entre activos
        if correo and Cliente.activos.filter(correo=correo).exists():
            raise forms.ValidationError("Ya existe un cliente activo con ese correo.")
        if rfc and Cliente.activos.filter(rfc=rfc).exists():
            raise forms.ValidationError("Ya existe un cliente activo con ese RFC.")
        return data
