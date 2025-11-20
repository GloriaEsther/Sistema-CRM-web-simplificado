from django.shortcuts import render, redirect, get_object_or_404
from .forms import OportunidadForm
from .models import Oportunidad,Cliente,Usuario
from ventas.models import Venta, EtapaVentas
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from crm.utils import require_roles
from django.utils import timezone

def kanban(request):
    etapas = EtapaVentas.objects.all()
    data = {}
    for etapa in etapas:
        qs = Oportunidad.objects.filter(etapa_ventas=etapa, activo=True).order_by('-fecha_registro')
        data[etapa.nombre_etapa] = qs
    return render(request, 'oportunidades/kanban.html', {'data': data, 'etapas': etapas})


def crear_oportunidad(request):#si funciona :D
    clientes = Cliente.activos.all()#Cliente.objects.all()
    etapas = EtapaVentas.objects.all()
    usuarios = Usuario.activos.all()

    if request.method == 'POST':
        form = OportunidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Oportunidad creada.")
            return redirect('oportunidades:kanban')
    else:
        form = OportunidadForm()

    return render(request, 'oportunidades/crear.html', {
        'form': form,
        'clientes': clientes,
        'etapas': etapas,
        'usuarios': usuarios,
    })

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

def listar_oportunidades(request):#prueba
    oportunidades = Oportunidad.activos.all()# oportunidades = Oportunidad.activos.all
    return render(request, "oportunidades/listar.html", {
        "oportunidades": oportunidades
    })

def editar_oportunidad(request, pk):
    oportunidad = Oportunidad.activos.get(pk=pk)
    clientes = Cliente.activos.all()
    etapas = EtapaVentas.objects.all()
    usuarios = Usuario.activos.all()

    if request.method == "POST":
        '''
        oportunidad.titulo = request.POST.get("titulo")
        oportunidad.descripcion = request.POST.get("descripcion")
        oportunidad.cliente = Cliente.activos.get(pk=request.POST.get("cliente"))
        oportunidad.etapa = request.POST.get("etapa")
        '''
        oportunidad.nombreoportunidad = request.POST.get("nombreoportunidad")
        oportunidad.valor_estimado = request.POST.get("valor_estimado")
        oportunidad.fecha_cierre_estimada = request.POST.get("fecha_cierre_estimada")
        oportunidad.comentarios = request.POST.get("comentarios")

        oportunidad.cliente_oportunidad_id = request.POST.get("cliente_oportunidad")
        oportunidad.etapa_ventas_id = request.POST.get("etapa_ventas")
        oportunidad.usuario_responsable_id = request.POST.get("usuario_responsable")

        oportunidad.save()

        return redirect("oportunidades:listar")

    return render(request, "oportunidades/editar.html", {
        "oportunidad": oportunidad,
        "clientes": clientes,
        "etapas": etapas,
        "usuarios": usuarios,
    })

def eliminar_oportunidad(request, pk):
    oportunidad = Oportunidad.activos.get(pk=pk)

    if request.method == "POST":
        oportunidad.eliminar_logico()
        return redirect("oportunidades:listar")

    return render(request, "oportunidades/eliminar.html", {
        "oportunidad": oportunidad
    })





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

