from django import forms
from .models import Venta,VentaDetalle
from oportunidades.models import Oportunidad
from servicios.models import Servicio
from inventario.models import Inventario
from django.forms import inlineformset_factory
class VentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        self.owner = kwargs.pop("owner", None)

        super().__init__(*args, **kwargs)
        self.fields["oportunidad_venta"].required = False
        
        if self.owner:
            self.fields["oportunidad_venta"].queryset = (
                Oportunidad.activos
                .filter(negocio_oportunidad=self.owner,
                etapa_ventas__nombre_etapa="Cierre-Ganado")
                .exclude(etapa_ventas__nombre_etapa = "Cierre-Perdido")
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

class VentaDetalleForm(forms.ModelForm):
    '''
    
    def __init__(self, *args, **kwargs):
       # self.usuario = kwargs.pop("usuario", None)
        self.owner = kwargs.pop("owner", None)
        super().__init__(*args, **kwargs)
        self.fields["servicio"].required = False
        self.fields["inventario"].required = False

        if self.owner:
            self.fields["servicio"].queryset = (
                Servicio.activos.filter(owner=self.owner)
            )
            self.fields["inventario"].queryset = (
                Inventario.activos.filter(owner=self.owner)
            )
        else:
            self.fields["servicio"].queryset = Servicio.todos.none()
            self.fields["inventario"].queryset = Inventario.todos.none()
    '''
    
    class Meta:
        model = VentaDetalle
        fields = ['servicio', 'inventario', 'cantidad', 'precio_unitario', 'subtotal']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'inventario': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), 
        }

VentaDetalleFormSet = inlineformset_factory(
    Venta,             
    VentaDetalle,      
    form=VentaDetalleForm,
    extra=1,           # Cuántos formularios vacíos mostrar por defecto
    can_delete=True    # Permite al usuario eliminar líneas de artículos
)