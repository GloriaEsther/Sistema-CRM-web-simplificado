from django import forms
from .models import Usuario,RolUsuario
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password

class UsuarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      if self.instance.pk:
            self.fields['contrasena'].required = False
    class Meta:
        model = Usuario
        fields = [
            'nombre', 'apellidopaterno', 'apellidomaterno','numerotel','correo', 'contrasena', 
            'rfc', 'local_Fijo','nombre_negocio'
        ]
        widgets = {
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    #Validacion de contrasena
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        # Si está editando y no escribió contraseña, no validar
        if self.instance.pk and not contrasena:
            return self.instance.contrasena

        if len(contrasena) < 10:
            raise ValidationError("La contraseña debe tener al menos 10 caracteres.")
        if not re.search(r'[A-Z]', contrasena):
            raise ValidationError("Debe contener al menos una letra mayúscula.")
        if not re.search(r'\d', contrasena):
            raise ValidationError("Debe contener al menos un número.")

        return contrasena
    
    def clean(self):
        data = super().clean()
        correo = data.get('correo')
        rfc = data.get('rfc')
        if correo:
            qs = Usuario.todos.filter(correo=correo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('correo', "Ya existe un usuario con ese correo.")

        if rfc:
            qs = Usuario.todos.filter(rfc=rfc)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('rfc', "Ya existe un usuario con ese RFC.")

        return data
    
    def clean_local_fijo(self):
        local_fijo = self.cleaned_data.get('local_Fijo')
        if not local_fijo:
            raise forms.ValidationError("Por favor, mencione si cuenta con un local fijo o no.")#Error
        return local_fijo
    
class EmpleadoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      if self.instance.pk:
            self.fields['contrasena'].required = False

    rol = forms.ModelChoiceField(
        queryset=RolUsuario.objects.filter(nombre_rol__in=['Vendedor', 'Administrador']),
        label="Rol del empleado",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Usuario
        fields = [
            'nombre', 
            'apellidopaterno', 
            'apellidomaterno',
            'numerotel', 
            'correo', 
            'contrasena',
            'rol',
        ]#
        widgets = {
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    # Validación de la contraseña
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
         # Si es edición y no cambió contraseña → no validar
        if self.instance.pk and not contrasena:
            return self.instance.contrasena

        if not contrasena:
            raise ValidationError("La contraseña es obligatoria.")

        if len(contrasena) < 10:
            raise ValidationError("La contraseña debe tener al menos 10 caracteres.")
        if not re.search(r'[A-Z]', contrasena):
            raise ValidationError("Debe contener al menos una letra mayúscula.")
        if not re.search(r'\d', contrasena):
            raise ValidationError("Debe contener al menos un número.")

        return contrasena

    def clean(self):
        data = super().clean()
        correo = data.get('correo')

        if correo:
         qs = Usuario.todos.filter(correo=correo)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            self.add_error("correo", "Ya existe un usuario con ese correo.")
        return data
    
    def clean_rol(self):
        rol = self.cleaned_data.get('rol')
        if not rol:
            raise forms.ValidationError("Debes seleccionar un rol.")
        return rol

class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))