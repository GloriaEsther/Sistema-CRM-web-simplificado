from django import forms
from .models import Venta
from oportunidades.models import Oportunidad

class VentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)

        if usuario:
            # Dueño ve solo oportunidades de su negocio
            if usuario.rol.nombre_rol == "Dueño":
                self.fields["oportunidad_venta"].queryset = (
                    Oportunidad.activos.filter(
                        negocio_oportunidad=usuario
                    )
                )
            else:
                # Empleado ve solo oportunidades del negocio del dueño
                self.fields["oportunidad_venta"].queryset = (
                    Oportunidad.activos.filter(
                        negocio_oportunidad=usuario.owner_id
                    )
                )
    class Meta:
        model = Venta
        fields = ['nombreventa','estatus_cobro','preciototal','cfdi','comentarios','oportunidad_venta']
        #widgets = {'fecha_venta': forms.DateTimeInput(attrs={'type':'datetime-local'})}
