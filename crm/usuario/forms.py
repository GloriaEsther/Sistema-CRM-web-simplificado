from django import forms
from .models import Usuario,RolUsuario
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password

class UsuarioForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = [
            'nombre', 'apellidopaterno', 'apellidomaterno',
            'numerotel', 'correo', 'contrasena', 'rfc', 'local_Fijo','nombre_negocio'
        ]
        widgets = {
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    #Validacion de contrasena
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
       
        # Validar duplicados
        if correo and Usuario.todos.filter(correo=correo).exists():#activos
            self.add_error('correo', "Ya existe un usuario con ese correo.")
        if rfc and Usuario.todos.filter(rfc=rfc).exists():
            self.add_error('rfc', "Ya existe un usuario con ese RFC.")
        return data
    
    def save(self, commit=True):
        usr = super().save(commit=False)
        # hash de contraseña
        if usr.contrasena and not usr.contrasena.startswith('pbkdf2_'):
            usr.contrasena = make_password(usr.contrasena)
        if commit:
            usr.save()
        return usr
    
class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))