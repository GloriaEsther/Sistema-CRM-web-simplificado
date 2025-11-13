from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VentaForm
from .models import Venta
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from crm.utils import require_roles

def listar_ventas(request):
    # filtro por rango de fechas opcional
    fecha_inicio = request.GET.get('desde')
    fecha_fin = request.GET.get('hasta')
    qs = Venta.objects.filter(activo=True)
    if fecha_inicio and fecha_fin:
        qs = qs.filter(fecha_venta__range=[fecha_inicio, fecha_fin])
    return render(request, 'ventas/listar.html', {'ventas': qs})

def crear_venta_manual(request):
    # si quieres permitir crear ventas manualmente (aparte de generar desde oportunidad)
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Venta creada.")
            return redirect('ventas:listar_ventas')
    else:
        form = VentaForm()
    return render(request, 'ventas/crear.html', {'form': form})

def generar_venta_desde_oportunidad(request, oportunidad_id):
    # acción: crear venta solo si oportunidad está en Cierre-Ganado y no tiene venta
    from oportunidades.models import Oportunidad
    op = get_object_or_404(Oportunidad, pk=oportunidad_id)
    if op.venta_oportunidad:
        messages.warning(request, "La oportunidad ya tiene venta asociada.")
        return redirect('oportunidades:kanban')

    # verificar etapa (asume 'Cierre-Ganado' en tabla de etapas)
    if op.etapa_ventas.nombre_etapa != 'Cierre-Ganado':
        messages.error(request, "Solo se puede generar venta desde oportunidades en Cierre-Ganado.")
        return redirect('oportunidades:kanban')

    # generar clave simple
    prefijo = "VTA"
    contador = Venta.objects.filter(claveventa__startswith=prefijo).count() + 1
    clave = f"{prefijo}{contador:05d}"
    venta = Venta.objects.create(
        claveventa=clave,
        nombreventa=op.nombreoportunidad,
        estatus_cobro=1,  # ajustar id por defecto; o buscar EstatusCobros.objects.get(nombre='Pendiente')
        preciototal=op.valor_estimado,
        fecha_venta=timezone.now(),
        oportunidad_venta=op
    )
    op.venta_oportunidad = venta
    op.save()
    messages.success(request, "Venta generada desde oportunidad.")
    return redirect('ventas:listar_ventas')

