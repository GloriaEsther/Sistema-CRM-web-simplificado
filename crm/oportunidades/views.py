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
    usuario_id = request.session.get('idusuario') 

    if not usuario_id:
        return redirect('usuario:iniciar_sesion') 
    
    usuario=Usuario.activos.get(idusuario=usuario_id)

    etapas = EtapaVentas.objects.all()
    data = {}

    # Regla por rol
    es_dueno = usuario.rol.nombre_rol in ["Dueño", "Administrador"]
    es_vendedor = usuario.rol.nombre_rol == "Vendedor"
    es_consultor =usuario.rol.nombre_rol =="Consultor" 
    for e in etapas:
        
        if es_dueno:
            # Dueño/admin ve las oportunidades del negocio
            qs = Oportunidad.activos.filter(
                negocio_oportunidad=usuario,
                etapa_ventas=e
            )
        elif es_vendedor:
            # Vendedor solo ve lo que él atiende
            qs = Oportunidad.activos.filter(
                usuario_responsable=usuario,
                etapa_ventas=e
            )
        elif es_consultor:
           qs = Oportunidad.activos.filter(
                etapa_ventas=e
            ) 
        else:
            qs = Oportunidad.activos.none()

        data[e.nombre_etapa] = qs.order_by('-fecha_registro')
    form_crear = OportunidadForm()
    return render(request, 'oportunidades/kanban.html', {
        'etapas': etapas, 
        'data': data,
        'form_crear': form_crear
    })

def crear_oportunidad(request): 
    usuario_id = request.session.get('idusuario')
    usuario =Usuario.activos.filter(idusuario=usuario_id).first()

    if not usuario:
        return redirect('usuario:iniciar_sesion')

    # roles que no pueden ser responsables de la oportunidad registrada por vendedor
    roles_no_responsables = RolUsuario.objects.filter(
        nombre_rol__in=["Administrador", "Dueño"]
    ).values_list("id_rol", flat=True)

    # determinar dueño real del negocio
    negocio = usuario.owner_id if usuario.owner_id else usuario #pruebas

    if request.method == 'POST':
        form = OportunidadForm(request.POST)
        if form.is_valid():
            try:
                op = form.save(commit=False)
                vendedor = op.usuario_responsable
                if vendedor.rol.id_rol in roles_no_responsables:
                    messages.error(request, " No puedes asignar oportunidades a administradores o dueños.")
                    return redirect("oportunidades:crear")
                op.creado_por = usuario
                op.negocio_oportunidad = negocio 
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

    return render(request, "oportunidades/kanban.html", {"form": form})#redirect('oportunidades:kanban')
    
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

        oportunidad.etapa_ventas_id = request.POST.get("etapa_ventas")
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

            if oportunidad.creado_por != usuario_logueado:
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
    res = [{'id': c.idcliente, 'display': f"{c.nombre} {c.apellidopaterno} {c.apellidomaterno}"} for c in qs]
    return JsonResponse(res, safe=False)

def ajax_buscar_vendedor(request):
    q = request.GET.get('q', '').strip()
    
    usuario_id = request.session.get("idusuario")
    usuario = Usuario.activos.filter(idusuario=usuario_id).first()

    usuarios = queryset_usuarios_segun_rol(usuario)#filtros de mostrar vendedores segun el rol

    if q:
        usuarios = usuarios.filter(nombre__icontains=q)

    res = [{'id': u.idusuario, 'display': f"{u.nombre} {u.apellidopaterno} {u.apellidomaterno}"} for u in usuarios[:15]]
    
    return JsonResponse(res, safe=False)