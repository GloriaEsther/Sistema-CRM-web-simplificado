from django import forms
from .models import Venta,VentaDetalle
from oportunidades.models import Oportunidad
from servicios.models import Servicio
from inventario.models import Inventario
from cliente.models import Cliente
from django.forms import inlineformset_factory, BaseInlineFormSet

class VentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        self.owner = kwargs.pop("owner", None)

        super().__init__(*args, **kwargs)
        self.fields["oportunidad_venta"].required = False

        if self.owner:
            oportunidades_usadas = Venta.objects.filter(
                oportunidad_venta__isnull=False
            ).values_list('oportunidad_venta', flat=True)

            self.fields["oportunidad_venta"].queryset = (
                Oportunidad.activos
                .filter(negocio_oportunidad=self.owner,
                etapa_ventas__nombre_etapa="Cierre-Ganado")
                .exclude(etapa_ventas__nombre_etapa = "Cierre-Perdido")# Excluimos cualquier oportunidad cuyo ID esté en la lista de "usadas"
                .exclude(pk__in=oportunidades_usadas)
            )
            self.fields["oportunidad_venta"].empty_label = "Seleccione una oportunidad (Opcional)..."
            self.fields["cliente"].queryset = Cliente.todos.filter(
                owner=self.owner, 
                activo=True 
            )
            self.fields["cliente"].empty_label = "Seleccione un cliente..."#esto es para quitar el ---- del selector vacio 
        else:
            self.fields["oportunidad_venta"].queryset = Oportunidad.objects.none()
            self.fields["cliente"].queryset = Cliente.todos.none()
            
    class Meta:
        model = Venta
        fields = [
            "nombreventa",
            "oportunidad_venta",
            "estatus_cobro",
            "preciototal",
            "cfdi",
            "comentarios",
            "cliente"
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
    class Meta:
        model = VentaDetalle
        fields = ['servicio', 'inventario', 'cantidad', 'precio_unitario', 'subtotal']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-select form-select-sm select-servicio'}),
            'inventario': forms.Select(attrs={'class': 'form-select form-select-sm select-inventario'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control form-control-sm cantidad-input', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control form-control-sm precio-input', 'min': 0}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control form-control-sm subtotal-input', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        # Recibimos el owner que nos manda la clase BaseVentaDetalleFormSet
        self.owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)

        if self.owner:
            self.fields['servicio'].queryset = Servicio.todos.filter(activo=True, owner=self.owner)
            self.fields['inventario'].queryset = Inventario.todos.filter(activo=True, owner=self.owner)
        else:
            self.fields['servicio'].queryset = Servicio.todos.none()
            self.fields['inventario'].queryset = Inventario.todos.none()

    # Esta clase inyecta el 'owner' a cada renglón nuevo que Django o el usuario cree
class BaseVentaDetalleFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['owner'] = self.owner
        return super()._construct_form(i, **kwargs)

VentaDetalleFormSet = inlineformset_factory(
    Venta,             
    VentaDetalle,      
    form=VentaDetalleForm,
    formset=BaseVentaDetalleFormSet, # Usamos nuestra base personalizada
    extra=1,           # Cuántos formularios vacíos mostrar por defecto
    can_delete=True    # Permite al usuario eliminar líneas de artículos
)