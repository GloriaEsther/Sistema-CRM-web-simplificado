from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError

class UsuarioForm(forms.ModelForm):#02-04/11/2025
    class Meta:
        model = Usuario
        fields = [
            'nombre', 'apellidopaterno', 'apellidomaterno',
            'numerotel', 'correo', 'contrasena', 'rfc', 'direccion',
            'curp', 'rol', 'local_Fijo', 'nss'
        ]
        widgets = {
            'contrasena': forms.PasswordInput(),
           # 'rol': forms.Select(attrs={'class': 'form-select'}),
           #'local_Fijo': forms.Select(attrs={'class': 'form-select'}),
        }

    #Validaciones
    def clean_correo(self):
            correo = self.cleaned_data.get('correo')
            if Usuario.activos.filter(correo=correo).exists():#comprueba si ya esta registrado(solo los activos y no los eliminados logicamente, esto se senala en el modelo). Usuario.objects.filter(correo=correo).exists():
                raise ValidationError("Este correo ya está registrado.")
            return correo

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if len(contrasena) < 10:
          raise ValidationError("La contraseña debe tener al menos 10 caracteres.")
        return contrasena
    
    #para que no ande pidiendo claveusuario porque se genera solo :b
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'claveusuario' in self.fields:
            self.fields['claveusuario'].required = False
    
#05/11/2025
class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))