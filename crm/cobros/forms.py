from django import forms
from cobros.models import Cobros,FormaCobro
from decimal import Decimal

class CobrosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        self.owner = kwargs.pop("owner", None)
        self.monto_restante = kwargs.pop("monto_restante", None)
        
        super().__init__(*args, **kwargs)
        self.fields["forma_cobro"].required = False

        if self.owner:
            self.fields["forma_cobro"].queryset = (
                FormaCobro.activos.filter(forma_cobro__nombre_forma_cobro="Cierre-Ganado")
            )
            self.fields["forma_cobro"].empty_label = "Seleccione una forma de cobro ..."
        else:
            self.fields["forma_cobro"].queryset = FormaCobro.objects.none()
            
    class Meta:
        model = Cobros
        fields = [
            "monto_recibido",
            "forma_cobro"
        ]
        
        widgets = {
            'forma_cobro': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }
    
    def clean_monto_recibido(self):
        monto_recibido = self.cleaned_data.get("monto_recibido")
        
        if self.monto_restante is not None and monto_recibido is not None:
            # Convertimos ambos valores a Decimal para una comparación exacta
            monto_rec_dec = Decimal(str(monto_recibido))
            monto_rest_dec = Decimal(str(self.monto_restante))
            
            if monto_rec_dec > monto_rest_dec:
                raise forms.ValidationError(
                    f"El abono no puede ser mayor al saldo pendiente (${monto_rest_dec})."
                )
        return monto_recibido