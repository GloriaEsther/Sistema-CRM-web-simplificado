from django.shortcuts import render, redirect, get_object_or_404
from .forms import OportunidadForm
from .models import Oportunidad,Cliente,Usuario
from usuario.models import RolUsuario
from ventas.models import Venta, EtapaVentas
from django.views.decorators.http import require_POST
from django.contrib import messages
from crm.utils import queryset_usuarios_segun_rol,obtener_owner,clientes_para_oportunidad
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Q

def kanban(request):
    usuario_id = request.session.get('idusuario') 

    if not usuario_id:
        return redirect('usuario:iniciar_sesion') 
    
    usuario=Usuario.activos.get(idusuario=usuario_id)
    #negocio = usuario.owner_id if usuario.owner_id else usuario
    owner=obtener_owner(request,usuario)

    if not owner:
        # superusuario sin supervisar → no ve nada
        etapas = EtapaVentas.objects.all()
        data = {e.nombre_etapa: Oportunidad.activos.none() for e in etapas}
        return render(request, 'oportunidades/kanban.html', {
            'etapas': etapas,
            'data': data,
            'form_crear': OportunidadForm()
        })


    etapas = EtapaVentas.objects.all()
    data = {}

    rol = usuario.rol.nombre_rol
    es_supervisando = request.session.get("modo_superusuario", False)
    es_dueno = (
            rol in ["Dueño", "Administrador"] or
            (rol == "Superusuario" and es_supervisando)
    ) 
    for e in etapas:
        
        if es_dueno:
            # Dueño/admin ve las oportunidades del negocio
            qs = Oportunidad.activos.filter(
                negocio_oportunidad = owner,
                etapa_ventas=e
            )
        elif rol == "Vendedor":
            # Vendedor solo ve lo que él atiende
            qs = Oportunidad.activos.filter(
                usuario_responsable=usuario,
                etapa_ventas=e
            )
        elif rol == "Consultor":
           qs = Oportunidad.activos.filter(
                etapa_ventas=e
            ) 
        else:
            qs = Oportunidad.activos.none()

        data[e.nombre_etapa] = qs.order_by('-fecha_registro')
    return render(request, 'oportunidades/kanban.html', {
        'etapas': etapas, 
        'data': data,
        'form_crear': OportunidadForm()  
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

    owner = obtener_owner(request,usuario)
    if not owner:
        messages.error(request, "No hay negocio seleccionado.")
        return redirect("superusuario:listar_negocios")

    if request.method == 'POST':
        form = OportunidadForm(request.POST)
        if form.is_valid():
            try:
                op = form.save(commit=False)
                vendedor = op.usuario_responsable
                rol_real = usuario.rol.nombre_rol
                rol = (
                    "Dueño"
                    if rol_real == "Superusuario" and request.session.get("modo_superusuario")
                    else rol_real
                )

                # Regla: solo vendedores tienen restricciones fuertes
                if rol == "Vendedor":
                    if vendedor.rol.id_rol in roles_no_responsables:
                        messages.error(
                            request,
                            "No puedes asignar oportunidades a administradores o dueños."
                        )
                        return redirect("oportunidades:crear")

                    if vendedor.idusuario != usuario.idusuario:
                        messages.error(
                            request,
                            "Como vendedor, solo puedes asignarte oportunidades a ti mismo."
                        )
                        return redirect("oportunidades:kanban")

                
                op.creado_por = usuario
                op.negocio_oportunidad = owner
                op.save()
                messages.success(request, "Oportunidad creada correctamente.")
                return redirect('oportunidades:kanban')
            except IntegrityError:
                messages.error(request, "Error al crear la oportunidad. ¿Ya existe una con mismo nombre?")
            except Exception as e:
                messages.error(request, f"Error interno: No se pudo guardar la oportunidad. {e}")
        
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    field_name = field.replace('_', ' ').capitalize()
                    messages.error(request, f"Error en '{field_name}': {err}")
    return redirect('oportunidades:kanban')
    
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
    usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
    owner = obtener_owner(request, usuario)

    if not owner:
        oportunidades = Oportunidad.activos.none()
    else:
        rol = usuario.rol.nombre_rol

        if rol in ["Dueño", "Administrador"] or (
            rol == "Superusuario" and request.session.get("modo_superusuario")
        ):
            oportunidades = Oportunidad.activos.filter(
                negocio_oportunidad=owner
            )

        elif rol == "Vendedor":
            oportunidades = Oportunidad.activos.filter(
                usuario_responsable=usuario
            )

        elif rol == "Consultor":
            oportunidades = Oportunidad.activos.filter(
                negocio_oportunidad=owner
            )

        else:
            oportunidades = Oportunidad.activos.none()

    return render(request, "oportunidades/listar.html", {
        "oportunidades": oportunidades
    })

def editar_oportunidad(request, pk):
    usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
    owner = obtener_owner(request, usuario)

    oportunidad = get_object_or_404(
        Oportunidad.activos,
        pk=pk,
        negocio_oportunidad=owner
    )

    clientes = Cliente.activos.filter(owner=owner)
    etapas = EtapaVentas.objects.all()
    usuarios = queryset_usuarios_segun_rol(usuario, owner)

    if request.method == "POST":
        oportunidad.nombreoportunidad = request.POST.get("nombreoportunidad")
        oportunidad.valor_estimado = request.POST.get("valor_estimado")
        oportunidad.fecha_cierre_estimada = request.POST.get("fecha_cierre_estimada")
        oportunidad.comentarios = request.POST.get("comentarios")
        oportunidad.etapa_ventas_id = request.POST.get("etapa_ventas")

        cliente_id = request.POST.get("cliente_oportunidad")
        usuario_id = request.POST.get("usuario_responsable")

        if cliente_id and cliente_id.isdigit():
            oportunidad.cliente_oportunidad = get_object_or_404(
                Cliente.activos,
                pk=cliente_id,
                owner=owner
            )

        if usuario_id and usuario_id.isdigit():
            oportunidad.usuario_responsable = get_object_or_404(
                Usuario.activos,
                pk=usuario_id
            )

        oportunidad.save()
        messages.success(request, "Oportunidad actualizada.")
        return redirect("oportunidades:kanban")

    if request.headers.get("HX-Request") == "true":
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
#solo se cargan los cambios al reiniciar pagina....
def eliminar_oportunidad(request, pk):
    usuario_id = request.session.get("idusuario")
    usuario_logueado = get_object_or_404(Usuario, idusuario=usuario_id)
    owner = obtener_owner(request, usuario_logueado)

    oportunidad = get_object_or_404(
        Oportunidad.activos,
        pk=pk,
        negocio_oportunidad=owner
    )
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
    usuario_id = request.session.get("idusuario")
    usuario = Usuario.activos.filter(idusuario=usuario_id).first()
    owner = obtener_owner(request, usuario)
    clientes = clientes_para_oportunidad(usuario,owner)#queryset_clientes_por_rol(usuario,owner)#

    if q:
        clientes = clientes.filter(
            Q(nombre__icontains=q) |
            Q(apellidopaterno__icontains=q) |
            Q(apellidomaterno__icontains=q)
        )

    clientes = clientes[:15]

    res = [{
        'id': c.idcliente,
        'display': f"{c.nombre} {c.apellidopaterno or ''} {c.apellidomaterno or ''}".strip()
    } for c in clientes]

    return JsonResponse(res, safe=False)

def ajax_buscar_vendedor(request):
    q = request.GET.get('q', '').strip()
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    owner = obtener_owner(request, usuario)
    usuarios = queryset_usuarios_segun_rol(usuario,owner)

    if q:
        usuarios = usuarios.filter(nombre__icontains=q)

    usuarios = usuarios.order_by("nombre")[:15]
    res = [{
        'id': u.idusuario, 
        'display': f"{u.nombre} {u.apellidopaterno} {u.apellidomaterno}"
    } for u in usuarios[:15]
    ]
    
    return JsonResponse(res, safe=False)