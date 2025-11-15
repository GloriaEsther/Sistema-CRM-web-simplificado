from django.shortcuts import render, redirect, get_object_or_404
from .forms import OportunidadForm
from .models import Oportunidad
from ventas.models import Venta, EtapaVentas
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from crm.utils import require_roles

def kanban(request):
    etapas = EtapaVentas.objects.all()
    data = {}
    for etapa in etapas:
        qs = Oportunidad.objects.filter(etapa_ventas=etapa, activo=True).order_by('-fecha_registro')
        data[etapa.nombre_etapa] = qs
    return render(request, 'oportunidades/kanban.html', {'data': data, 'etapas': etapas})

def crear_oportunidad(request):
    if request.method == 'POST':
        form = OportunidadForm(request.POST)
        if form.is_valid():
            op = form.save(commit=False)
            op.save()
            messages.success(request, "Oportunidad creada.")
            return redirect('oportunidades:kanban')
    else:
        form = OportunidadForm()
    return render(request, 'oportunidades/crear.html', {'form': form})

@require_POST
def mover_oportunidad(request, pk):
    # endpoint AJAX que recibe nueva etapa id
    nueva_etapa_id = request.POST.get('etapa_id')
    if not nueva_etapa_id:
        return JsonResponse({'ok': False, 'error': 'No se recibió etapa.'})
    op = get_object_or_404(Oportunidad, pk=pk)
    etapa = get_object_or_404(EtapaVentas, pk=nueva_etapa_id)
    op.etapa_ventas = etapa
    op.save()
    return JsonResponse({'ok': True, 'nueva_etapa': etapa.nombre_etapa})

'''
def oportunidades_cierre_ganado(request):#esto devolvera un json para que lo use e frontend
    oportunidades = Oportunidad.objects.filter(
        etapa_ventas__nombre_etapa="Cierre-Ganado",
        activo=True
    )

    return JsonResponse([
        {
            "id": o.idoportunidad,
            "nombre": o.nombreoportunidad,
            "valor": float(o.valor_estimado),
            "cliente": str(o.cliente_oportunidad),
            "usuario": str(o.usuario_responsable)
        }
        for o in oportunidades
    ], safe=False)
'''

