from django.shortcuts import redirect,render,get_object_or_404
from usuario.models import Usuario
from ventas.models import Venta
from cobros.models import Cobros
from decimal import Decimal
from crm.utils import obtener_owner,abonos_por_rol
from cobros.forms import CobrosForm
from django.db.models import Sum
from django.contrib import messages

def listar_cobros(request):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    owner = obtener_owner(request, usuario)

    if not owner:
        cobros = Cobros.activos.none()
    else:
        cobros = abonos_por_rol(usuario, owner)
        
    return render(request, "cobros/lista_cobros.html", {
        "cobros": cobros
    })

def crear_cobro(request, pk):#def crear_cobro(request, venta_id):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    owner = obtener_owner(request, usuario)

    #Venta relacionada con el nuevo cobro
    venta = get_object_or_404(
        Venta.objects.select_related('cliente').prefetch_related('detalles__servicio', 'detalles__inventario'),
        pk=pk,
        owner=owner  
    )
    historial_cobros = Cobros.objects.filter(ventas_registro=venta, activo=True).order_by('-fecha_cobro')
    resultado_pagado = historial_cobros.aggregate(total=Sum('monto_recibido'))
    total_pagado = resultado_pagado['total'] or 0
    
    saldo_restante = Decimal(str(venta.preciototal)) - Decimal(str(total_pagado))
    
    if saldo_restante < 0:
        saldo_restante = Decimal('0.00')


    if request.method == "POST":
        form =  CobrosForm(
            request.POST,
            usuario=usuario, 
            owner=owner,
            monto_restante=saldo_restante
        )
        
        if form.is_valid():
            cobro = form.save(commit=False)
            cobro.ventas_registro = venta
            cobro.owner = owner
            cobro.usuario_registro = usuario 
            cobro.monto_restante = saldo_restante - Decimal(str(cobro.monto_recibido))
            cobro.save()

            if cobro.monto_restante == Decimal('0.00'):
                venta.estatus_cobro_id= 3
                venta.save()

            messages.success(request, "Abono creado correctamente.")
            return redirect("cobros:listar") 
    else:
        form = CobrosForm(usuario=usuario, owner=owner, monto_restante=saldo_restante)
    
    return render(request, "cobros/crear_cobro.html", {
        "form": form,
        "saldo_restante": saldo_restante
    })