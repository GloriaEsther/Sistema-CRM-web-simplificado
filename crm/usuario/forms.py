from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
import re

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
        }

    #Validaciones
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if len(contrasena) < 10:
          raise ValidationError("La contraseña debe tener al menos 10 caracteres.")
        
        # Verificar que contenga al menos una mayúscula
        if not re.search(r'[A-Z]', contrasena):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")

        # Verificar que contenga al menos un número
        if not re.search(r'\d', contrasena):
            raise ValidationError("La contraseña debe contener al menos un número.")
        return contrasena
    
    #para que no ande pidiendo claveusuario porque se genera solo :b
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'claveusuario' in self.fields:
            self.fields['claveusuario'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        rfc = cleaned_data.get('rfc')
        curp = cleaned_data.get('curp')

        # Validar campos obligatorios vacíos
        campos_obligatorios = ['nombre', 'apellidopaterno', 'apellidomaterno', 'correo', 'rfc', 'curp', 'contrasena','rol','direccion']
        faltantes = [campo for campo in campos_obligatorios if not cleaned_data.get(campo)]

        if faltantes:
            raise forms.ValidationError(f"Faltan campos obligatorios: {', '.join(faltantes)}")

        # Validar duplicados
        if Usuario.todos.filter(correo=correo).exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo.")
        if Usuario.todos.filter(rfc=rfc).exists():
            raise forms.ValidationError("Ya existe un usuario con ese RFC.")
        if Usuario.todos.filter(curp=curp).exists():
            raise forms.ValidationError("Ya existe un usuario con esa CURP.")

        return cleaned_data


#05/11/2025
class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))