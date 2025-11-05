from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'claveusuario', 'nombre', 'apellidopaterno', 'apellidomaterno',
            'numerotel', 'correo', 'contrasena', 'rfc', 'direccion',
            'curp', 'rol', 'local_Fijo', 'nss'
        ]
        widgets = {
            'contrasena': forms.PasswordInput(),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'local_Fijo': forms.Select(attrs={'class': 'form-select'}),
        }

    #Validaciones
    def clean_correo(self):
            correo = self.cleaned_data.get('correo')
            if Usuario.objects.filter(correo=correo).exists():
                raise ValidationError("Este correo ya está registrado.")
            return correo

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if len(contrasena) < 10:
          raise ValidationError("La contraseña debe tener al menos 10 caracteres.")
        return contrasena