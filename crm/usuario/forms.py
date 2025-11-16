from django import forms
from .models import Usuario,RolUsuario
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password

class UsuarioForm(forms.ModelForm):
    #class UsuarioForm(forms.ModelForm):
    rol = forms.ModelChoiceField(
            queryset=RolUsuario.objects.all(),
            empty_label="Seleccione un rol",
            label="Rol",
            widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Usuario
        fields = [
            'nombre', 'apellidopaterno', 'apellidomaterno',
            'numerotel', 'correo', 'contrasena', 'rfc', 'direccion',
            'curp', 'rol', 'local_Fijo', 'nss','nombre_negocio'
        ]
        widgets = {
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    #Validaciones
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if len(contrasena) < 10:
          raise ValidationError("La contraseña debe tener al menos 10 caracteres.")
        if not re.search(r'[A-Z]', contrasena):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'\d', contrasena):
            raise ValidationError("La contraseña debe contener al menos un número.")
        return contrasena
    
    def clean(self):
        data = super().clean()
        correo = data.get('correo')
        rfc = data.get('rfc')
        curp = data.get('curp')

        # Validar campos obligatorios vacíos
        campos_obligatorios = ['nombre', 'apellidopaterno', 'apellidomaterno', 'correo', 'contrasena','rol']# 'rfc', 'curp''direccion'
        faltantes = [campo for campo in campos_obligatorios if not data.get(campo)]

        if faltantes:
            raise forms.ValidationError(f"Faltan campos obligatorios: {', '.join(faltantes)}")

        # Validar duplicados
        if correo and Usuario.activos.filter(correo=correo).exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo.")
        if rfc and Usuario.activos.filter(rfc=rfc).exists():
            raise forms.ValidationError("Ya existe un usuario con ese RFC.")
        if curp and Usuario.activos.filter(curp=curp).exists():
            raise forms.ValidationError("Ya existe un usuario con esa CURP.")
        return data
    
    def save(self, commit=True):
        usr = super().save(commit=False)
        # hash de contraseña
        if usr.contrasena and not usr.contrasena.startswith('pbkdf2_'):
            usr.contrasena = make_password(usr.contrasena)
        if commit:
            usr.save()
        return usr
    
#05/11/2025
class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))