from django.shortcuts import render, redirect, get_object_or_404
from .forms import OportunidadForm
from .models import Oportunidad,Cliente,Usuario
from usuario.models import RolUsuario
from ventas.models import Venta, EtapaVentas
from django.views.decorators.http import require_POST
from django.contrib import messages
from crm.utils import require_roles,queryset_usuarios_segun_rol#permisos y filtros de busqueda (varia segun el rol)
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError
from django.core import serializers
from django.db.models import Q

def kanban(request):
    etapas = EtapaVentas.objects.all()
    data = {}
    for e in etapas:
        data[e.nombre_etapa] = Oportunidad.activos.filter(etapa_ventas=e).order_by('-fecha_registro')
    form_crear = OportunidadForm()
    return render(request, 'oportunidades/kanban.html', {
        'etapas': etapas, 
        'data': data,
        'form_crear': form_crear,
        'preferencias': request.context.get('preferencias', None) 
        if hasattr(request, 'context') else None
    })

def crear_oportunidad(request): 
    usuario_id = request.session.get('idusuario')
    usuario_creador =Usuario.activos.filter(idusuario=usuario_id).first()
    
    #Se obtienen los roles del sistema 
    rol_vendedor = RolUsuario.objects.filter(nombre_rol__iexact="Vendedor").first()
    rol_admin = RolUsuario.objects.filter(nombre_rol__in=["Administrador", "Dueño"])
   
    if usuario_creador.rol.nombre_rol in ["Administrador", "Dueño"]:
        vendedores = Usuario.activos.all()

    elif usuario_creador.rol.nombre_rol == "Vendedor":
        vendedores = Usuario.activos.filter(rol=rol_vendedor)

    else:
     vendedores = Usuario.activos.none()

    if request.method == 'POST':
        form = OportunidadForm(request.POST)
        if form.is_valid():
            try:
                op = form.save(commit=False)
                vendedor = op.usuario_responsable
                if vendedor.rol.id_rol in rol_admin:
                    messages.error(request, " No puedes asignar oportunidades a administradores o dueños.")
                    return redirect("oportunidades:crear")
                op.usuario_registro = usuario_creador
                op.save()
                messages.success(request, "Oportunidad creada correctamente.")
                return redirect('oportunidades:kanban')
            except IntegrityError as e:
                messages.error(request, "Error al crear la oportunidad. ¿Ya existe una con mismo nombre?")
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    else:
        form = OportunidadForm()
    redirect('oportunidades:kanban')
    
@require_POST
def mover_oportunidad(request, pk):
    nueva_etapa_id = request.POST.get('etapa_id')
    if not nueva_etapa_id:
        return JsonResponse({'ok': False, 'error': 'No se recibió etapa.'})
    op = get_object_or_404(Oportunidad, pk=pk)
    etapa = get_object_or_404(EtapaVentas, pk=nueva_etapa_id)
    op.etapa_ventas = etapa
    op.save()
    return JsonResponse({'ok': True, 'nueva_etapa': etapa.nombre_etapa})

def listar_oportunidades(request):
    oportunidades = Oportunidad.activos.all()
    return render(request, "oportunidades/listar.html", {
        "oportunidades": oportunidades
    })

def editar_oportunidad(request, pk):
    oportunidad = get_object_or_404(Oportunidad.activos, pk=pk)
    clientes = Cliente.activos.all()
    etapas = EtapaVentas.objects.all()
    usuarios = Usuario.activos.all()

    
    if request.method == "POST":
        oportunidad.nombreoportunidad = request.POST.get("nombreoportunidad")
        oportunidad.valor_estimado = request.POST.get("valor_estimado")
        oportunidad.fecha_cierre_estimada = request.POST.get("fecha_cierre_estimada")
        oportunidad.comentarios = request.POST.get("comentarios")

        #oportunidad.cliente_oportunidad_id = request.POST.get("cliente_oportunidad")
        oportunidad.etapa_ventas_id = request.POST.get("etapa_ventas")
        #oportunidad.usuario_responsable_id = request.POST.get("usuario_responsable")

        # Obtener los IDs del POST
        cliente_id = request.POST.get("cliente_oportunidad")
        usuario_id = request.POST.get("usuario_responsable")

        # Asignar Cliente
        if cliente_id and cliente_id.isdigit():
            # Buscamos el objeto Cliente antes de asignarlo
            oportunidad.cliente_oportunidad = get_object_or_404(Cliente, pk=cliente_id)
        # Asignar Usuario Responsable 
        if usuario_id and usuario_id.isdigit():
            # Buscamos el objeto Usuario antes de asignarlo
            oportunidad.usuario_responsable = get_object_or_404(Usuario, pk=usuario_id)

        try:
            oportunidad.save()
            messages.success(request, "Oportunidad actualizada.")
            return redirect("oportunidades:kanban")
        except Exception as e:
            messages.error(request, f"Error al guardar la oportunidad: {e}")
    
    if (
        request.headers.get("HX-Request") == "true" or
        request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        return render(request, "oportunidades/_editar.html", {
            "oportunidad": oportunidad,
            "clientes": clientes,
            "etapas": etapas,
            "usuarios": usuarios,
        })

    
    return render(request, "oportunidades/editar.html", {
        "oportunidad": oportunidad,
        "clientes": clientes,
        "etapas": etapas,
        "usuarios": usuarios,
    })


def eliminar_oportunidad(request, pk):
    usuario_id = request.session.get("idusuario")
    usuario_logueado = get_object_or_404(Usuario, idusuario=usuario_id)

   
    oportunidad = get_object_or_404(Oportunidad.activos, pk=pk)

    if request.method == "POST":

        
        if usuario_logueado.rol.nombre_rol == "Vendedor":

            if oportunidad.usuario_registro != usuario_logueado:
                messages.error(request, "No puedes eliminar oportunidades que no registraste.")
                return redirect("oportunidades:kanban")
            
        
        oportunidad.eliminar_logico()
        messages.success(request, "Oportunidad eliminada.")
        return redirect("oportunidades:kanban")

  
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "oportunidades/_eliminar_confirmar.html", {
            "oportunidad": oportunidad
        })

   
    return redirect("oportunidades:kanban")


def buscar_clientes(request):
    texto = request.GET.get("q", "").strip()

    clientes = Cliente.activos.filter(
        nombre__icontains=texto
    ) | Cliente.activos.filter(
        apellidopaterno__icontains=texto
    ) | Cliente.activos.filter(
        apellidomaterno__icontains=texto
    )

    return JsonResponse([
        {
            "id": c.idcliente,
            "nombre": f"{c.nombre} {c.apellidopaterno} {c.apellidomaterno}"
        }
        for c in clientes
    ], safe=False)

def buscar_vendedores(request):
    texto = request.GET.get("q", "").strip()

    #agarra la sesion del usuario 
    usuario_id = request.session.get("idusuario")
    usuario = Usuario.activos.filter(idusuario=usuario_id).first()
    
    usuarios = queryset_usuarios_segun_rol(usuario)
   
    vendedores = usuarios.filter(
        nombre__icontains=texto
    ) | usuarios.filter(
        apellidopaterno__icontains=texto
    )

    return JsonResponse([
        {
            "id": v.idusuario,
            "nombre": f"{v.nombre} {v.apellidopaterno} {v.apellidomaterno}"
        }
        for v in vendedores
    ], safe=False)

#vistas ajax
def ajax_consultar_oportunidad(request, pk):
    o = Oportunidad.activos.get(pk=pk)
    return JsonResponse({
        'id': o.idoportunidad,
        'nombre': o.nombreoportunidad,
        'valor': float(o.valor_estimado),
        'comentarios': o.comentarios,
        'cliente': str(o.cliente_oportunidad),
        'cliente_id': o.cliente_oportunidad.idcliente,
        'usuario': str(o.usuario_responsable),
        'usuario_id': o.usuario_responsable.idusuario,
        'user_display': f"{o.usuario_responsable.nombre} {o.usuario_responsable.apellidopaterno or ''}",
        'etapa': o.etapa_ventas.nombre_etapa,
        'etapa_id': o.etapa_ventas.idetapa_ventas,
        'fecha': o.fecha_cierre_estimada.strftime('%d/%m/%Y'),
        'fecha_iso': o.fecha_cierre_estimada.strftime('%Y-%m-%d'),
    })

def ajax_buscar_cliente(request):
    q = request.GET.get('q', '').strip()
    qs = Cliente.activos.filter(nombre__icontains=q)[:15] if q else Cliente.activos.all()[:15]
    res = [{'id': c.idcliente, 'display': f"{c.nombre} {c.apellidopaterno}"} for c in qs]
    return JsonResponse(res, safe=False)

def ajax_buscar_vendedor(request):
    q = request.GET.get('q', '').strip()
    
    usuario_id = request.session.get("idusuario")
    usuario = Usuario.activos.filter(idusuario=usuario_id).first()

    usuarios = queryset_usuarios_segun_rol(usuario)

    if q:
        usuarios = usuarios.filter(nombre__icontains=q)

    res = [{'id': u.idusuario, 'display': f"{u.nombre} {u.apellidopaterno}"} for u in usuarios[:15]]
    
    return JsonResponse(res, safe=False)