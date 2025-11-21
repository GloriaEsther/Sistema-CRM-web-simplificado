from django.shortcuts import render, redirect, get_object_or_404
from .forms import OportunidadForm
from .models import Oportunidad,Cliente,Usuario
from usuario.models import RolUsuario
from ventas.models import Venta, EtapaVentas
from django.views.decorators.http import require_POST
from django.contrib import messages
from crm.utils import require_roles
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError
from django.core import serializers
from django.db.models import Q


def kanban(request):#si funciona :D
    etapas = EtapaVentas.objects.all()
    data = {}
    # data será dict { etapa.nombre: queryset }
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

def crear_oportunidad(request): #prueba
    #Obtener los datos de cliente y etapas de venta.....
    clientes = Cliente.activos.all()
    etapas = EtapaVentas.objects.all()#.order_by('idetapa_ventas')#tiene que ordenarlas por etapa
   
    usuario_id = request.session.get('idusuario')#se obtiene la sesion del usuario logueado
    usuario_creador =Usuario.activos.filter(idusuario=usuario_id).first()
    
    #Se obtienen los roles del sistema 
    rol_vendedor = RolUsuario.objects.filter(nombre_rol__iexact="Vendedor").first()
    rol_admin = RolUsuario.objects.filter(nombre_rol__in=["Administrador", "Dueño"])
    '''
   #Filtrar vendedores 
    if usuario_creador.rol in rol_admin:
        #Usuario.activos.filter(nombre_rol__in=["Administrador", "Dueño"])
        vendedores =Usuario.activos.all()#si el suario es dueno o administrador puede ver a todos los usuarios(para asignar oportunidad)

    elif usuario_creador.rol == rol_vendedor:
       # crea una lista de Vendedores permitidos al registrar una oportunidad excluyendo a los duenos o administradores
       vendedores = Usuario.activos.filter(rol=rol_vendedor)#Usuario.activos.exclude(rol__in=rol_admin)
    
    else:
        vendedores =Usuario.activos.none()

   '''
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
                vendedor = op.usuario_responsable#prueba
                if vendedor.rol.id_rol in rol_admin:#if vendedor.rol.id_rol in [r.id_rol for r in rol_admin]
                    messages.error(request, " No puedes asignar oportunidades a administradores o dueños.")
                    return redirect("oportunidades:crear")
                
                op.save()
                messages.success(request, "Oportunidad creada correctamente.")
                return redirect('oportunidades:kanban')
            except IntegrityError as e:
                messages.error(request, "Error al crear la oportunidad. ¿Ya existe una con mismo nombre?")
        else:
            # form invalid -> mostrar errores en el modal
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    else:
        form = OportunidadForm()
    return render(request, 'oportunidades/crear.html', {
        'form': form,
        'clientes': clientes,
        'vendedores': vendedores
    })


@require_POST#funciona :D
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

def listar_oportunidades(request):#si funciona 
    oportunidades = Oportunidad.activos.all()# oportunidades = Oportunidad.activos.all
    return render(request, "oportunidades/listar.html", {
        "oportunidades": oportunidades
    })

def editar_oportunidad(request, pk):#prueba
    oportunidad = Oportunidad.activos.get(pk=pk)
    clientes = Cliente.activos.all()
    etapas = EtapaVentas.objects.all()
    usuarios = Usuario.activos.all()

    # Si es POST -> guardar cambios
    if request.method == "POST":
        oportunidad.nombreoportunidad = request.POST.get("nombreoportunidad")
        oportunidad.valor_estimado = request.POST.get("valor_estimado")
        oportunidad.fecha_cierre_estimada = request.POST.get("fecha_cierre_estimada")
        oportunidad.comentarios = request.POST.get("comentarios")

        oportunidad.cliente_oportunidad_id = request.POST.get("cliente_oportunidad")
        oportunidad.etapa_ventas_id = request.POST.get("etapa_ventas")
        oportunidad.usuario_responsable_id = request.POST.get("usuario_responsable")

        oportunidad.save()

        messages.success(request, "Oportunidad actualizada.")
        return redirect("oportunidades:listar")

    # AJAX/HTMX -> solo devolver el modal
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

    # Vista normal
    return render(request, "oportunidades/editar.html", {
        "oportunidad": oportunidad,
        "clientes": clientes,
        "etapas": etapas,
        "usuarios": usuarios,
    })


def eliminar_oportunidad(request, pk):#prueba
    # Obtener la oportunidad (solo activas)
    oportunidad = Oportunidad.activos.get(pk=pk)

    # Si es POST, elimina y redirige
    if request.method == "POST":
        oportunidad.eliminar_logico()
        return redirect("oportunidades:listar")

    # Si es AJAX -> devolver sólo el cuerpo del modal
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "oportunidades/_eliminar_confirmar.html", {
            "oportunidad": oportunidad
        })

    # Vista normal (sin AJAX)
    return render(request, "oportunidades/eliminar.html", {
        "oportunidad": oportunidad
    })


def buscar_clientes(request):#prueba
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

def buscar_vendedores(request):#prueba
    texto = request.GET.get("q", "").strip()

    vendedores = Usuario.activos.filter(
        rol__nombre_rol__iexact="Vendedor"
    ).filter(
        nombre__icontains=texto
    ) | Usuario.activos.filter(
        nombre__icontains=texto
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
    # filtra por rol vendedor: asumiendo RolUsuario existe y Usuario tiene FK
    from usuario.models import RolUsuario, Usuario
    rol_v = RolUsuario.objects.filter(nombre_rol__iexact='Vendedor').first()
    if rol_v:
        qs = Usuario.activos.filter(rol=rol_v, nombre__icontains=q)[:15] if q else Usuario.activos.filter(rol=rol_v)[:15]
    else:
        qs = Usuario.activos.filter(nombre__icontains=q)[:15] if q else Usuario.activos.all()[:15]
    res = [{'id': u.idusuario, 'display': f"{u.nombre} {u.apellidopaterno}"} for u in qs]
    return JsonResponse(res, safe=False)

















'''
prueba dos 
def crear_oportunidad(request): #prueba
    # Requerir login/permiso si corresponde
    if request.method == 'POST':
        form = OportunidadForm(request.POST)
        if form.is_valid():
            try:
                op = form.save(commit=False)
                # Si quieres: establecer usuario_responsable por defecto desde sesión
                # op.usuario_responsable = Usuario.activos.get(idusuario=request.session['idusuario'])
                op.save()
                messages.success(request, "Oportunidad creada correctamente.")
                return redirect('oportunidades:kanban')
            except IntegrityError as e:
                messages.error(request, "Error al crear la oportunidad. ¿Ya existe una con mismo nombre?")
        else:
            # form invalid -> mostrar errores en el modal
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    else:
        form = OportunidadForm()
    # Para mostrar clientes y vendedores en el form (usando selects)
    clientes = Cliente.activos.all()
    # Vendedores (filtrados por rol)
    rol_vendedor = RolUsuario.objects.filter(nombre_rol__iexact='Vendedor').first()
    vendedores = Usuario.activos.filter(rol=rol_vendedor) if rol_vendedor else Usuario.activos.all()
    return render(request, 'oportunidades/crear.html', {
        'form': form,
        'clientes': clientes,
        'vendedores': vendedores
    })

def consultar_oportunidad(request, pk):
    oportunidad = get_object_or_404(Oportunidad, pk=pk)
    # Si llamada AJAX (fetch), devolvemos partial HTML:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'oportunidades/_consultar.html', {'oportunidad': oportunidad})
    return render(request, 'oportunidades/consultar.html', {'oportunidad': oportunidad})

def editar_oportunidad(request, pk):
    oportunidad = get_object_or_404(Oportunidad, pk=pk)
    if request.method == 'POST':
        form = OportunidadForm(request.POST, instance=oportunidad)
        if form.is_valid():
            form.save()
            messages.success(request, "Oportunidad actualizada.")
            return redirect('oportunidades:kanban')
    else:
        form = OportunidadForm(instance=oportunidad)
    # Si fetch: devolver partial con form
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'oportunidades/_editar.html', {'form_editar': form, 'oportunidad': oportunidad})
    return render(request, 'oportunidades/editar.html', {'form': form, 'oportunidad': oportunidad})

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

def eliminar_oportunidad(request, pk):
    # uso de POST para seguridad
    op = get_object_or_404(Oportunidad, pk=pk)
    if request.method == 'POST':
        # condición: no eliminar si en Cierre-Ganado o Cierre-Perdido
        if op.etapa_ventas.nombre_etapa in ['Cierre-Ganado', 'Cierre-Perdido']:
            messages.error(request, "No se puede eliminar en esa etapa.")
            return redirect('oportunidades:kanban')
        op.activo = False
        op.fecha_eliminacion = timezone.now()
        op.save()
        messages.success(request, "Oportunidad eliminada.")
        return redirect('oportunidades:kanban')
    return render(request, 'oportunidades/confirmar_eliminar.html', {'oportunidad': op})
'''

'''
def buscar_clientes(request):#prueba se va a usar dentro de un modal
    q = request.GET.get("q", "")
    resultados = Cliente.activos.filter(
        nombre__icontains=q
    ) | Cliente.activos.filter(
        apellidopaterno__icontains=q
    ) | Cliente.activos.filter(
        apellidomaterno__icontains=q
    )

    return render(request, "oportunidades/_lista_clientes.html", {
        "clientes": resultados
    })

'''
'''
ay no se 
@require_POST#prueba 
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

def buscar_clientes(request):
    q = request.GET.get('q','').strip()
    if not q:
        return JsonResponse([], safe=False)
    resultados = Cliente.activos.filter(
        Q(nombre__icontains=q) | Q(apellidopaterno__icontains=q) | Q(apellidomaterno__icontains=q)
    )[:20]
    data = [{
        'id': c.idcliente,
        'nombre': f"{c.nombre} {c.apellidopaterno} {c.apellidomaterno}"
    } for c in resultados]
    return JsonResponse(data, safe=False)

def buscar_vendedores(request):
    q = request.GET.get('q','').strip()
    rol_vendedor = RolUsuario.objects.filter(nombre_rol__iexact='Vendedor').first()
    queryset = Usuario.activos.filter(rol=rol_vendedor) if rol_vendedor else Usuario.activos.all()
    if q:
        queryset = queryset.filter(Q(nombre__icontains=q) | Q(apellidopaterno__icontains=q) | Q(apellidomaterno__icontains=q))
    queryset = queryset[:20]
    data = [{'id': u.idusuario, 'nombre': f"{u.nombre} {u.apellidopaterno} {u.apellidomaterno}"} for u in queryset]
    return JsonResponse(data, safe=False)


'''


#lo que esta abajo si funcionaba 
'''
def listar_oportunidades(request):#si funciona 
    oportunidades = Oportunidad.activos.all()# oportunidades = Oportunidad.activos.all
    return render(request, "oportunidades/listar.html", {
        "oportunidades": oportunidades
    })

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
def editar_oportunidad(request, pk):#si funciona
    oportunidad = Oportunidad.activos.get(pk=pk)
    clientes = Cliente.activos.all()
    etapas = EtapaVentas.objects.all()
    usuarios = Usuario.activos.all()

    if request.method == "POST":
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

def eliminar_oportunidad(request, pk):#si funciona 
    oportunidad = Oportunidad.activos.get(pk=pk)

    if request.method == "POST":
        oportunidad.eliminar_logico()
        return redirect("oportunidades:listar")

    return render(request, "oportunidades/eliminar.html", {
        "oportunidad": oportunidad
    })
'''