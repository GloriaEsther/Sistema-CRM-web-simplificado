from django.shortcuts import render, redirect, get_object_or_404
from ventas.forms import VentaForm,VentaDetalleFormSet,VentaDetalleForm
from django.db import transaction
from ventas.models import Venta,Cobros
from usuario.models import Usuario
from servicios.models import Servicio
from inventario.models import Inventario
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count
from crm.utils import queryset_ventas_por_rol,obtener_owner
from time import time
from django.contrib import messages
import json
from django.http import HttpResponse

def listar_ventas(request):
    fecha_inicio = request.GET.get('desde')
    fecha_fin = request.GET.get('hasta')
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    owner = obtener_owner(request, usuario)

    if not owner:
        qs = Venta.activos.none()
    else:
        qs = queryset_ventas_por_rol(usuario, owner)

    if fecha_inicio and fecha_fin:
        qs = qs.filter(fecha_registro__date__range=[fecha_inicio, fecha_fin])
    return render(request, 'ventas/listar_ventas.html', {'ventas': qs})

def crear_venta_manual(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    if not usuario:
        return redirect("usuario:iniciar_sesion")
    
    owner = obtener_owner(request, usuario)

    if not owner:
        messages.error(request, "No hay negocio seleccionado.")
        return redirect("superusuario:listar_negocios")

    if usuario.rol.nombre_rol == "Consultor":
        messages.error(
            request,
            "No tienes permisos para registrar ventas."
        )
        return redirect("ventas:listar")
    
    if request.method == "POST":
        form = VentaForm(
            request.POST,
            usuario=usuario, 
            owner=owner
        )
        formset = VentaDetalleFormSet (request.POST, owner=owner)
        if form.is_valid() and formset.is_valid():
            try:
                # Usamos una transacción para que si algo falla en los detalles, se cancele la venta completa
                with transaction.atomic():
                    venta = form.save(commit=False)
                    venta.owner = owner
                    venta.usuario_registro = usuario 
                    venta.save() 

                    #Obtener los siguientes datos:
                    forma_pago = form.cleaned_data.get('forma_cobro')
                    monto_inicial = form.cleaned_data.get('monto_pago_inicial') or 0
                    estatus = form.cleaned_data.get('estatus_cobro')
                    estatus_nombre=str(estatus)
    
                    if estatus_nombre in ['Cobro parcial', 'Cobrado']:
                        
                        monto_a_registrar = venta.preciototal if estatus == '3' else monto_inicial
                        restante = float(venta.preciototal) - float(monto_a_registrar)
                        
                        if estatus == 'Cobrado':
                            restante = 0
                        
                        Cobros.objects.create(
                            monto_recibido=monto_a_registrar,
                            fecha_cobro=timezone.now(),
                            monto_restante=restante,
                            activo =True,
                            forma_cobro=forma_pago,
                            ventas_registro=venta,
                            usuario_registro=usuario,
                            owner=owner
                        )
                        
                    formset.instance = venta
                    formset.save()
                messages.success(request, "Venta y sus detalles creados correctamente.")
                return redirect("ventas:listar")     
            except Exception as e:
                messages.error(request, f"Ocurrió un error al guardar los detalles: {e}")
    else:
        form = VentaForm(usuario=usuario, owner=owner)
        formset = VentaDetalleFormSet(owner=owner)

    servicios_qs = Servicio.todos.filter(activo=True, owner=owner)
    inventario_qs = Inventario.todos.filter(activo=True, owner=owner)

    diccionario_precios = {
        'servicios': {str(s.idservicio): float(s.precio) for s in servicios_qs},
        'inventario': {str(i.idinventario): float(i.precio) for i in inventario_qs}
    }

    return render(request, "ventas/crear_ventas.html", {
        "form": form,
        "formset": formset, 
        "diccionario_precios": diccionario_precios
    })

def consultar_venta(request, venta_id):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    owner = obtener_owner(request, usuario)

    #Venta y relaciones de productos/servicios
    venta = get_object_or_404(
        Venta.objects.select_related('cliente').prefetch_related('detalles__servicio', 'detalles__inventario'),
        pk=venta_id,
        owner=owner  
    )
    #Recuperamos todos los cobros activos asociados a esta venta
    historial_cobros = Cobros.objects.filter(ventas_registro=venta, activo=True).order_by('-fecha_cobro')
    
    #Sumamos el monto total recibido de los cobros realizados
    # aggregate devuelve un diccionario, ej: {'total': 150.00}
    resultado_pagado = historial_cobros.aggregate(total=Sum('monto_recibido'))
    total_pagado = resultado_pagado['total'] or 0
    
    #Esto se hace para tener una "Unica fuente de verdad"
    #Calculamos el saldo restante actual
    saldo_restante = float(venta.preciototal) - float(total_pagado)
    
    #Aseguramos que el saldo no sea negativo por cuestiones de redondeo de flotantes
    if saldo_restante < 0:
        saldo_restante = 0

    return render(request, "ventas/consultar_venta.html", {
        "venta": venta,
        "historial_cobros": historial_cobros,
        "total_pagado": total_pagado,
        "saldo_restante": saldo_restante
    })

def corte_caja(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    if not usuario:
        return redirect("usuario:login")
    owner = obtener_owner(request, usuario)

    if not owner:
        messages.error(request, "No hay negocio seleccionado.")
        return redirect("superusuario:listar_negocios")
    
    if usuario.rol.nombre_rol == "Consultor":
        messages.error(
            request,
            "No tienes permiso para ver corte de caja."
        )
        return redirect("ventas:listar")
    hoy = timezone.now().date()

    fecha_inicio = request.GET.get("desde")
    fecha_fin = request.GET.get("hasta")

    qs = Venta.objects.filter(activo=True,owner=owner,estatus_cobro__nombre_estatus_cobro="COBRADO")

    if fecha_inicio and fecha_fin:
        qs = qs.filter(
            fecha_registro__date__range=[fecha_inicio, fecha_fin]
        )
    else:
        qs = qs.filter(fecha_registro__date=hoy)

    total_ventas = qs.aggregate(
        total=Sum("preciototal")
    )["total"] or 0

    total_operaciones = qs.count()

    # Por estatus de cobro
    por_estatus = (
        qs.values("estatus_cobro__nombre_estatus_cobro")
        .annotate(
            total=Sum("preciototal"),
            cantidad=Count("idventa")
        )
    )

    ventas_canceladas = Venta.objects.filter(
        activo=False,
        owner=owner,
        fecha_eliminacion__date=hoy
    ).aggregate(
        total=Sum("preciototal")
    )["total"] or 0

    return render(request, "ventas/corte_caja.html", {
        "total_ventas": total_ventas,
        "total_operaciones": total_operaciones,
        "por_estatus": por_estatus,
        "ventas_canceladas": ventas_canceladas,
        "fecha": hoy
    })

def ventas_hoy(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    if not usuario:
        return redirect("usuario:login")
    owner = obtener_owner(request, usuario)

    if not owner:
        messages.error(request, "No hay negocio seleccionado.")
        return redirect("superusuario:listar_negocios")
    
    hoy = timezone.now().date()

    ventas = Venta.objects.filter(
        activo=True,
        owner=owner,
        fecha_registro__date=hoy,
        estatus_cobro__nombre_estatus_cobro="COBRADO"
    ).order_by("-fecha_registro")


    total_hoy = ventas.aggregate(
       total=Sum("preciototal")
    )["total"] or 0

    return render(request, "ventas/ventas_hoy.html", {
        "ventas": ventas,
        "total_hoy": total_hoy,
        "fecha": hoy
    })

def venta_editar(request, pk):#vista y template por corregir 
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    if not usuario:
        return redirect("usuario:login")
    owner = obtener_owner(request, usuario)
    qs = queryset_ventas_por_rol(usuario,owner)
    venta = get_object_or_404(qs, idventa=pk)

    if venta.estatus_cobro.idestatus_cobros == 3:#cobrado
       messages.error(request, "No se puede editar una venta cobrada.")
       return redirect("ventas:listar")
    
    if usuario.rol.nombre_rol == "Consultor":
        messages.error(
            request,
            "No tienes permisos para editar ventas."
        )
        return redirect("ventas:listar")
    
    if usuario.rol.nombre_rol == "Vendedor":
        if venta.usuario_registro != usuario:
            messages.error(
                request,
                "No tienes permiso para editar esta venta."
            )
            return redirect("ventas:listar")
        
    if request.method == "POST":
        # Pasamos instance=venta para que sepa qué registro actualizar
        form = VentaForm(request.POST, instance=venta, usuario=usuario,owner=owner)
        # El formset también recibe el POST y la instancia de la venta madre
        formset = VentaDetalleFormSet(request.POST, instance=venta)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guarda los cambios del formulario principal (ej. nombre o precio total)
                    venta = form.save()
                    
                    # Guarda los cambios de los detalles (crea, edita o elimina automáticamente)
                    formset.save()
                    
                messages.success(request, "Venta actualizada correctamente.")
                return redirect("ventas:listar")
            except Exception as e:
                messages.error(request, f"Ocurrió un error al actualizar los detalles: {e}")
    else:
        # En la petición GET, cargamos los datos actuales de la BD pasando instance=venta
        form = VentaForm(instance=venta, usuario=usuario, owner=owner)
        formset = VentaDetalleFormSet(instance=venta)

    return render(request, "ventas/editar_ventas.html", {
        "form": form,
        "formset": formset,
        "venta": venta
    })

def venta_eliminar(request, pk):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    if not usuario:
        return redirect("usuario:login")
    
    owner = obtener_owner(request, usuario)

    qs = queryset_ventas_por_rol(usuario,owner)
    venta = get_object_or_404(qs, idventa=pk)
    rol=usuario.rol.nombre_rol

    if rol in ["Dueño", "Administrador", "Superusuario"]:
        if venta.estatus_cobro.idestatus_cobros == 3:
          messages.error(request, "No se puede eliminar una venta cobrada.")
          return redirect("ventas:listar")
        venta.eliminar_logico()
        messages.success(request, "Venta eliminada correctamente.")
        return redirect("ventas:listar")
    
    if usuario.rol.nombre_rol == "Consultor":
        messages.error(
            request,
            "No tienes permisos para eliminar ventas."
        )
        return redirect("ventas:listar")
    
    if rol == "Vendedor":
        if venta.usuario_registro != usuario.idusuario:
            messages.error(
                request,
                "No tienes permiso para eliminar este cliente."
            )
            return redirect("ventas:listar")
        if venta.estatus_cobro.idestatus_cobros == 3:
          messages.error(request, "No se puede eliminar una venta cobrada.")
          return redirect("ventas:listar")
        
        venta.eliminar_logico()
        messages.success(request, "Venta eliminada correctamente.")
        return redirect("ventas:listar")