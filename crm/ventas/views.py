from django.shortcuts import render, redirect, get_object_or_404
from .forms import VentaForm
from .models import Venta
from usuario.models import Usuario
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count
from crm.utils import queryset_ventas_por_rol
from oportunidades.models import Oportunidad
from time import time
from django.contrib import messages


def listar_ventas(request):
    # filtro por rango de fechas opcional
    fecha_inicio = request.GET.get('desde')
    fecha_fin = request.GET.get('hasta')
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    qs = queryset_ventas_por_rol(usuario)

    if fecha_inicio and fecha_fin:
        qs = qs.filter(fecha_registro__date__range=[fecha_inicio, fecha_fin])
    return render(request, 'ventas/listar.html', {'ventas': qs})

def crear_venta_manual(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    if not usuario:
        return redirect("usuario:login")

    owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner_id
  
    if request.method == "POST":
        form = VentaForm(
            request.POST,
            usuario=usuario, 
            owner=owner
        )
        if form.is_valid():
            venta = form.save(commit=False)

            venta.owner = owner
            venta.usuario_registro = usuario 

            venta.save()

            messages.success(
                request,
                "Venta creada correctamente."
            )
            return redirect("ventas:listar")
    else:
        form = VentaForm(usuario=usuario,owner=owner)

    return render(request, "ventas/crear.html", {
        "form": form
    })

def corte_caja(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    if not usuario:
        return redirect("usuario:login")

    owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner_id

    hoy = timezone.now().date()

    fecha_inicio = request.GET.get("desde")
    fecha_fin = request.GET.get("hasta")

    qs = Venta.objects.filter(activo=True,owner=owner,estatus_cobro__nombre_estatus_cobro="COBRADO")#cobrado...

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

    owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner_id

    hoy = timezone.now().date()

    ventas = Venta.objects.filter(
        activo=True,
        owner=owner,
        fecha_registro__date=hoy,
        estatus_cobro__nombre_estatus_cobro="COBRADO"#prueba..
    ).order_by("-fecha_registro")


    total_hoy = ventas.aggregate(#te quedaste aqui
       total=Sum("preciototal")
    )["total"] or 0

    return render(request, "ventas/ventas_hoy.html", {
        "ventas": ventas,
        "total_hoy": total_hoy,
        "fecha": hoy
    })

def venta_editar(request, pk):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    if not usuario:
        return redirect("usuario:login")
    
    qs = queryset_ventas_por_rol(usuario)
    venta = get_object_or_404(qs, idventa=pk)
    owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner_id

    if venta.estatus_cobro.idestatus_cobros == 3:#"COBRADO":
       messages.error(request, "No se puede editar una venta cobrada.")
       return redirect("ventas:listar")

    if request.method == "POST":
        form = VentaForm(request.POST, instance=venta, usuario=usuario,owner=owner)
        if form.is_valid():
            form.save()
            messages.success(request, "Venta actualizada correctamente.")
            return redirect("ventas:listar")
    else:
        form = VentaForm(instance=venta, usuario=usuario,owner=owner)

    return render(request, "ventas/venta_editar.html", {
        "form": form,
        "venta": venta
    })


def venta_eliminar(request, pk):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    qs = queryset_ventas_por_rol(usuario)
    venta = get_object_or_404(qs, idventa=pk)

    if venta.estatus_cobro.idestatus_cobros == 3:#"COBRADO"
          messages.error(request, "No se puede eliminar una venta cobrada.")
          return redirect("ventas:listar")
    venta.eliminar_logico()
    messages.success(request, "Venta eliminada correctamente.")
    return redirect("ventas:listar")
