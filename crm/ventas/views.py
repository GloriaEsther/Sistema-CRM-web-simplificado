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

'''
def generar_venta_desde_oportunidad(request, oportunidad_id):#en esta version mvp del crm no se va a incluir.....
    # acción: crear venta solo si oportunidad está en Cierre-Ganado y no tiene venta
    
    op = get_object_or_404(Oportunidad, pk=oportunidad_id)
    if op.venta_oportunidad:
        messages.warning(request, "La oportunidad ya tiene venta asociada.")
        return redirect('oportunidades:kanban')

    # verificar etapa (asume 'Cierre-Ganado' en tabla de etapas)
    if op.etapa_ventas.nombre_etapa != 'Cierre-Ganado':
        messages.error(request, "Solo se puede generar venta desde oportunidades en Cierre-Ganado.")
        return redirect('oportunidades:kanban')

    # generar clave simple
   # prefijo = "VTA"#No funciono en el backend, a lo mejor ya con el frontend si lo haga (auida)
    #contador = Venta.objects.filter(claveventa__startswith=prefijo).count() + 1
   # clave = f"{prefijo}{contador:05d}"
    venta = Venta.objects.create(
        claveventa=Venta.claveventa,#mejor la llama desde el modelo
        nombreventa=op.nombreoportunidad,
        estatus_cobro=1,  # ajustar id por defecto; o buscar EstatusCobros.objects.get(nombre='Pendiente')
        preciototal=op.valor_estimado,
        fecha_venta=timezone.now(),
        oportunidad_venta=op
    )
    op.venta_oportunidad = venta
    op.save()
    messages.success(request, "Venta generada desde oportunidad.")
    return redirect('ventas:listar')
'''

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

    qs = Venta.objects.filter(activo=True,owner=owner)

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
        fecha_registro__date=hoy
    ).order_by("-fecha_registro")

    total_hoy = ventas.aggregate(
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

    venta.eliminar_logico()
    messages.success(request, "Venta eliminada correctamente.")
    return redirect("ventas:listar")
