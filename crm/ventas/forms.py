from django import forms
from .models import Venta
from oportunidades.models import Oportunidad


class VentaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)

        if usuario:
            # Base queryset: oportunidades activas y ganadas
            qs = Oportunidad.activos.filter(
                etapa_ventas__nombre_etapa__iexact="Cierre-Ganado"
            )

            # Dueño
            if usuario.rol.nombre_rol == "Dueño":
                qs = qs.filter(negocio_oportunidad=usuario)

            # Empleado
            else:
                qs = qs.filter(negocio_oportunidad=usuario.owner_id)

            self.fields["oportunidad_venta"].queryset = qs

    class Meta:
        model = Venta
        fields = [
            "nombreventa",
            "oportunidad_venta",
            "estatus_cobro",
            "preciototal",
            "cfdi",
            "comentarios",
        ]
        widgets = {
            'comentarios': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Comentarios opcionales'
            }),
        }
    # Validación fuerte del precio
    def clean_preciototal(self):
        precio = self.cleaned_data.get("preciototal")

        if precio is None:
            raise forms.ValidationError("El precio total es obligatorio.")

        if precio <= 0:
            raise forms.ValidationError(
                "El precio total debe ser mayor a 0."
            )

        return precio
