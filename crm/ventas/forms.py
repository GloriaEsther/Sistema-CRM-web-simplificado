from django import forms
from .models import Venta
from oportunidades.models import Oportunidad

class VentaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        self.owner = kwargs.pop("owner", None)

        super().__init__(*args, **kwargs)
        self.fields["oportunidad_venta"].required = False
        
        if self.owner:
            self.fields["oportunidad_venta"].queryset = (
                Oportunidad.activos
                .filter(negocio_oportunidad=self.owner)
                .exclude(etapa_ventas = 6)#etapa_ventas="Cierre-Perdido"
            )
        else:
            self.fields["oportunidad_venta"].queryset = Oportunidad.objects.none()
            
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
    
    def clean_preciototal(self):
        precio = self.cleaned_data.get("preciototal")

        if precio <= 0:
            raise forms.ValidationError(
                "El precio total debe ser mayor a 0."
            )

        return precio
